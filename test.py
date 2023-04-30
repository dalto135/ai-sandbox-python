response = [
    {
        "text": "hello"
    },
    {
        "text": "goodbye"
    }
]

def getText(response):
    return response["text"]

results = map(getText, response)

for result in list(results):
    print(result)