import random

import openai
from colorama import Fore
from icecream import ic
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.env_vars import INPUT_FILE_PATH, MODEL_NAME, TEMPERATURE
from utils.prompts import INIT_MESSAGE_TEMPLATE, IMPROVE_MESSAGE, Q_A_PLACEHOLDER, EVAL_MESSAGE_TEMPLATE

client = openai.OpenAI()

MAX_ATTEMPTS = 7
NUM_CONTENT_PARTS = 2
EVAL_OPTIONS = [
    "EXCERPT_1",
    "EXCERPT_2",
    "EXCERPT_1_AND_A_BIT_OF_2",
    "EXCERPT_2_AND_A_BIT_OF_1",
    "BOTH_EXCERPTS_ROUGHLY_EQUALLY",
    "NEITHER_OR_INVALID",
]
SHORT_SEPARATOR = "-" * 20 + "\n"
LONG_SEPARATOR = "\n" + "-" * 80 + "\n"

chat_history = []


def format_excerpts(excerpts):
    context_parts = []
    for i, excerpt in enumerate(excerpts, start=1):
        context_parts.append(f"Excerpt {i}:\n{excerpt}\n")
    return SHORT_SEPARATOR.join(context_parts)


def find_one_of_substrings(string, substrings):
    # Sort substrings by length in descending order
    substrings = sorted(substrings, key=len, reverse=True)
    ans = None
    for substring in substrings:
        if substring in string:
            if ans:
                # If there are multiple substrings in the string, return None
                return None
            ans = substring
            string = string.replace(substring, "")
    return ans


def get_last_message(chat_history):
    return chat_history[-1]["content"]


def generate(chat_history: list):
    assistant_response_content = ""

    # Yield chunks from the streaming response
    with client.chat.completions.create(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        messages=chat_history,
        stream=True,
    ) as stream:
        for chunk in stream:
            if chunk.choices[0].delta and chunk.choices[0].delta.content:
                # Accumulate the content only if it's not None
                assistant_response_content += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
            if chunk.choices[0].finish_reason == "stop":
                break  # Stop if the finish reason is 'stop'

    # Once the loop is done, append the full message to chat_history
    chat_history.append({"role": "assistant", "content": assistant_response_content})


def main():
    # Read the input file
    with open(INPUT_FILE_PATH, "r") as file:
        content = file.read()

    # Split the content into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )
    chunk_docs = text_splitter.create_documents([content])
    excerpts = [doc.page_content for doc in chunk_docs]

    ic(len(excerpts))
    ic(len(content) / len(excerpts))

    # Get NUM_CONTENT_PARTS random excerpts
    random_excerpts = random.sample(excerpts, NUM_CONTENT_PARTS)
    context=format_excerpts(random_excerpts)
                            
    init_message = INIT_MESSAGE_TEMPLATE.format(context=context)
    eval_message = EVAL_MESSAGE_TEMPLATE.format(context=context)
    improve_message = IMPROVE_MESSAGE
    system_message = "You are a helpful assistant."

    for i in range(MAX_ATTEMPTS):
        if i == 0:
            chat_history = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": init_message},
            ]
            print(Fore.GREEN + f"Initial prompt:\n{init_message}" + Fore.RESET)
            print(LONG_SEPARATOR)
        else:
            # Improve the question and answer
            chat_history.append({"role": "user", "content": improve_message})
            print(Fore.GREEN + f"Improvement prompt:\n{improve_message}" + Fore.RESET)
            print(LONG_SEPARATOR)

        for msg_part in generate(chat_history):
            print(msg_part, end="")

        print(LONG_SEPARATOR)        
        print("NEW CONVERSATION" + LONG_SEPARATOR)

        # Evaluate the question and answer
        init_message = eval_message.replace(
            Q_A_PLACEHOLDER, get_last_message(chat_history)
        )

        print(Fore.GREEN + f"Initial prompt:\n{init_message}" + Fore.RESET)
        print(LONG_SEPARATOR)

        while True:
            chat_history = [
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": init_message,
                },
            ]

            for msg_part in generate(chat_history):
                print(msg_part, end="")

            print(LONG_SEPARATOR)

            evaluation = find_one_of_substrings(
                get_last_message(chat_history), EVAL_OPTIONS
            )
            print(Fore.CYAN + f"Evaluation: {evaluation}\n" + Fore.RESET)

            if evaluation in EVAL_OPTIONS:
                break

            print("Invalid evaluation. Trying again...\n")

        if evaluation == "BOTH_EXCERPTS_ROUGHLY_EQUALLY":
            print("Question and answer are good!")
            break


if __name__ == "__main__":
    main()
