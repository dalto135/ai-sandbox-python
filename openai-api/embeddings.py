import openai

input = "hello world"

response = openai.Embedding.create(
    input=input,
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']

print(embeddings)
print()
print(input)
print(len(embeddings))

# def get_embedding(text, model="text-embedding-ada-002"):
#     text = text.replace("\n", " ")
#     return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

# df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
# df.to_csv('output/embedded_1k_reviews.csv', index=False)