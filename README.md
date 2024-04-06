# LLM Bootcamp

The LLM Bootcamp is a tool that, given a text, generates questions about it that are hard for an LLM to answer.

## Installation

Follow these steps to set up the LLM Bootcamp:

**1. Create a Virtual Environment:**

```bash
python3 -m venv .venv
```

Activate the environment. On Windows:

```bash
.venv\Scripts\activate
```

On macOS and Linux:

```bash
source .venv/bin/activate
```

**2. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**3. Set Up Environment Variables:**

Copy the `.env.example` file, rename it to `.env`, and fill in your values. You can just fill in the `OPENAI_API_KEY` variable for now and leave the rest as they are.

**4. Run the Tool:**

Start generating hard questions by running:

```bash
python src/bootcamp/main.py
```

## Requirements

- Python 3.11 or later.
- An OpenAI API key.

## Contributing

Interested in contributing? Fork the repository and submit a pull request.

## License

The project is available under the MIT License.
