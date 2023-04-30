import openai

response = openai.Moderation.create(
    input="I want to kill them."
)

# output = response["results"][0]
# print(output)

# for result in response["results"]:
#     print(result)

print(response)