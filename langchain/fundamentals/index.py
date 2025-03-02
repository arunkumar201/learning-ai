from dotenv import load_dotenv

load_dotenv()
import os

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")
  # Streaming response with a callback
def print_callback(chunk):
    print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    response = model.invoke("What is the capital of France?")
    # print(response)
    # Streaming response
    response = model.stream("What is the capital of Ruri lahar MP?")
    for chunk in response:
        print_callback(chunk)
