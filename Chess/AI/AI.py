from openai import OpenAI;
from dotenv import load_dotenv;
import os

load_dotenv();

client = OpenAI(
    api_key= os.getenv("api_key"),
    base_url="https://api.groq.com/openai/v1",
);

userInp = input("What do you want to ask? ");

response = client.responses.create(
    input=userInp,
    model="openai/gpt-oss-20b",
);

print(response.output_text);