INIT_MESSAGE_TEMPLATE = """\
Your task is to generate a question that would test the reader's understanding of the \
excerpts below, with the special twist that a single question should require knowledge of \
BOTH excerpts, not just one.

First provide your question, then provide the answer. Remember, your question must somehow \
combine the information from both excerpts. Information from just one of them should not be \
sufficient to answer the question.

Your question and answer must AVOID calling the excerpts "excerpt" or "content" etc. They \
are part of a much larger document, plucked out for your convenience.

{context}\
"""
Q_A_PLACEHOLDER = "=563@;£'!÷41$kfgds.p"

EVAL_MESSAGE_TEMPLATE = f"""\
{{context}}

Determine which of the above excerpts is necessary to know for the following question and \
answer:

{Q_A_PLACEHOLDER}

Please respond with one of the following strings:
EXCERPT_1
EXCERPT_2
EXCERPT_1_AND_A_BIT_OF_2
EXCERPT_2_AND_A_BIT_OF_1
BOTH_EXCERPTS_ROUGHLY_EQUALLY
NEITHER_OR_INVALID
"""

IMPROVE_MESSAGE = """\
How would you modify the question and answer to change your evaluation to \
BOTH_EXCERPTS_ROUGHLY_EQUALLY? Your response should consist solely of the \
improved question and answer with no additional comments. The modified question \
should require knowledge of specific, concrete details from both excerpts. \

Also, the question and answer must AVOID calling the excerpts "excerpt" or "content" etc. They \
are part of a much larger document, plucked out for your convenience.
"""