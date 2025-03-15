from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

load_dotenv()

from contracts.index import Person

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, streaming=True)

person_parser = PydanticOutputParser(pydantic_object=Person)

prompt_country = ChatPromptTemplate.from_template(
    "What is the capital of {country}?, make sure explain and give me list of popular places to visit in {country},Note should not be more than 20 words"
)

prompt_person = ChatPromptTemplate.from_messages(
    [
        ("system", "Generate information about a random person."),
        ("human", "{format_instructions}"),
    ]
)


def generate_response(input_text):
    human_format_prompt = prompt_country.format(country=input_text)
    response = llm.invoke(human_format_prompt)
    return response.content


def generate_response_stream(input_text):
    human_format_prompt = prompt_country.format(country=input_text)
    response = llm.stream(human_format_prompt)

    full_response = ""
    for chunk in response:
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    return full_response


def generate_random_person():
    format_instructions = person_parser.get_format_instructions()
    # print("My format instructions:", format_instructions)
    messages = prompt_person.format_messages(format_instructions=format_instructions)

    try:
        response = llm.invoke(messages)
        return person_parser.parse(response.content)
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.content}")
        return None


def main():
    print("Country Response:")
    print(generate_response("France"))

    print("\n-------generate_response_stream-------")
    generate_response_stream("France")

    print("\n-------generate_random_person-------")
    print(generate_random_person())


if __name__ == "__main__":
    main()
