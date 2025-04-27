import json

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
            You are a helpful assistant that translates {input_language} to {output_language}, provides IPA pronunciation, gives example sentences in both languages, and explains word usage in {output_language}. Put one short sentence as input to get audio by the end of your response.
            
            structure your response should be in json format like this:
                "input": <input>,
                "ipa": <ipa>,
                "translation": <translation>,
                "explanation": <explanation>,
                "example_sentence": 
                    "{input_language}": <example_sentence_in_input_language>,
                    "{output_language}": <example_sentence_in_output_language>
            """,
        ),
        ("human", "{input}"),
    ]
)


def parse_json_from_markdown(markdown_text: str) -> dict:
    """
    Parse JSON content from a markdown text block.

    Args:
        markdown_text (str): Markdown text containing JSON content

    Returns:
        dict: Parsed JSON content
    """
    # Find the JSON block within markdown
    json_start = markdown_text.find("```json")
    if json_start == -1:
        raise ValueError("No JSON block found in markdown text")

    # Find the end of the JSON block
    json_content_start = markdown_text.find("\n", json_start) + 1
    json_content_end = markdown_text.find("```", json_content_start)

    if json_content_end == -1:
        raise ValueError("JSON block not properly closed")

    # Extract and parse the JSON content
    json_str = markdown_text[json_content_start:json_content_end].strip()
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {str(e)}")


def work_on_the_word(word: str, deepseek: bool = True):
    """Translate a word, provide IPA, example sentences, and explanations using the given LLM."""
    if deepseek:
        llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        chain = prompt | llm
    else:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        chain = prompt | llm
    result = chain.invoke(
        {
            "input_language": "english",
            "output_language": "german",
            "input": f"{word}",
        }
    )

    # parse the result.content to json
    return parse_json_from_markdown(result.content)


work_on_the_word("heute")

# # example of running the script
# if __name__ == "__main__":
#     result = work_on_the_word("heute")
#     print(result)
