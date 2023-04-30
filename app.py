# import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(prompt),
            # prompt=prompt.capitalize(),
            # n=2,
            # max_tokens=100,
            temperature=0.6,
        )
        def getText(response):
            return response["text"]

        text_map = map(getText, response["choices"])
        text_result = list(text_map)
        # text_result = response["choices"][0]
        print("RESULT")
        print(text_result)
        return redirect(url_for("index", result=text_result))
        # return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", len=1, result=result)

def generate_prompt(prompt):
    return """
        Suggest three names for an animal that is a superhero.
        Animal: Cat
        Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
        Animal: Dog
        Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
        Animal: {}
        Names:
    """.format(
            prompt.capitalize()
        )
