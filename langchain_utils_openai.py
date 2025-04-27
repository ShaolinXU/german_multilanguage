from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0.1, max_tokens=None, timeout=None, max_retries=2
)

prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a helpful assistant that translates {input_language} to {output_language}, provides IPA pronunciation, gives example sentences in both languages, and explains word usage in {output_language}.",
        ),
        ("human", "{input}"),
    ]
)


def work_on_the_word(word: str):
    """Translate a word, provide IPA, example sentences, and explanations using the given LLM."""
    chain = prompt | llm
    result = chain.invoke(
        {
            "input_language": "English",
            "output_language": "German",
            "input": f"{word}",
        }
    )
    return result


work_on_the_word("heute")
