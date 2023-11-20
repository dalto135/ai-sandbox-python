from openai import OpenAI
client = OpenAI()

prompts = []
images = []

prompt = "a butterfly"
i = 0

while True:
    print("PROMPT")
    print(prompt)
    print()

    dall_e_response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image = dall_e_response.data[0].url
    images.append(image)

    print("IMAGE")
    print(image)
    print()

    vision_response = client.chat.completions.create(
        model = "gpt-4-vision-preview",
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": image,
                    },
                ],
            }
        ],
        max_tokens = 300,
    )

    prompt = vision_response.choices[0].message.content
    prompts.append(prompt)

    i += 1

    if i > 2:
        break

print("PROMPT")
print(prompt)
print()

print("PROMPT LIST")
print(prompts)
print()

print("IMAGE LIST")
print(images)