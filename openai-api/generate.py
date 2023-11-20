# import os
import openai

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    model="text-davinci-003",
    # model="davinci:ft-personal:poop-2023-04-25-23-10-38",
    prompt="Give me a list of 10 cool places to check out in Columbus, Ohio",
    # prompt="Explain the chain rule in calculus",
    n=1,
    # temperature=0,
    max_tokens=2048,
    # suffix="3. COSI"
)

for choice in response.choices:
    print(choice.text)

# print(response)
