from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
import autogen
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"temperature": 0.7, "config_list": config_list, "seed": 42}

import openai
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(prompt),
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
        # return redirect(url_for("index", result=text_result))
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", len=1, result=result)

def generate_prompt(prompt):
    return f"""
        The following prompt delimited by triple backticks is meant to be used to generate an image using Generative AI.
        Take this prompt and generate a list of 10 new prompts that are more descriptive and can be used to produce more impressive outputs.
        Once this list is created, take turns suggesting changes for each prompt in the list and explain your reasoning for making these changes.
        This should be done in an iterative process where different prompt ideas are exchanged until consensus is reached on a list of the best 10 prompts.
        Each prompt should be improved upon a couple times, and after displaying the final list of 10 prompts, the task is done.

        ```{prompt}```

        Take a deep breath and work on this problem step-by-step.
    """

# coder = autogen.AssistantAgent(
#     name="Coder",
#     llm_config=llm_config
# )

# critic = autogen.AssistantAgent(
#     name="Critic",
#     # Missing text for bugs
#     system_message="""
#         Critic. You are a helpful assistant highly skilled in evaluating the quality of a given visualization code by providing a score from 0 to 10, 0 being the worst quality and 10 being the best.
#         - bugs (bugs): are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed?
#         - Data tranformation (transformations): Is the data transformed appropriately for the visualization type? E.g., is the dataset appropriated filtered, aggregated etc.
#         - Goal compliance (compliance): How well does the code meets the specified visualiaztion goals?
#         - Visualization type (type): CONSIDERING BEST PRACTICES, is the visualization type appropriate for the data and intent? Is there a visualization type that would be better?
#         - Data encoding (encoding): Is the data encoded appropriately for the visualization type?
#         - Aesthetics (aesthetics): Are the aesthetics of the visualization appropriate for the visualization type and the data?

#         YOU MUST PROVIDE A SCORE for each of the above dimensions.
#         {bugs: 0, tranformation: 0, compliance: 0, type: 0, encoding: 0, aesthetics: 0}
#         Do not suggest code.
#         Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
#     """,
#     llm_config=llm_config
# )

# scribe = autogen.AssistantAgent(
#     name="Scribe",
#     system_message="Your job is to create documentation for the code that is created by the Coder. You should give instructions on how to run the code and install all of the necessary dependencies.",
#     llm_config=llm_config
# )

agent1 = autogen.AssistantAgent(
    name="Agent1",
    system_message="You are Agent1. Your job is to collaborate with Agent2 to follow instructions given by the user.",
    llm_config=llm_config
)

agent2 = autogen.AssistantAgent(
    name="Agent2",
    system_message="You are Agent2. Your job is to collaborate with Agent1 to follow instructions given by the user.",
    llm_config=llm_config
)

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding"}
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, agent1, agent2], messages=[], max_round=40
)

groupchat2 = autogen.GroupChat(
    agents=[user_proxy, agent1, agent2], messages=[
        {
            'role':'system', 
            'content':"""You are a helpful assistant and world-class problem solver who is known for their ability to think creatively and find novel solutions.
            Your job is to help the user brainstorm different ideas based on their prompt through a use of iterative steps where you create a list of options and explore each option more deeply.
            """
        },    
        {
            'role':'user', 
            'content':"""Help me """
        }, 
        {
            'role':'assistant', 
            'content':"""write me a very short poem\
            about a happy carrot"""
        }, 
    ], max_round=40
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

prompt = "A butterfly"

user_proxy.initiate_chat(
    manager,
    message=f"""

        ```{prompt}```

        You are a world-class problem solver who is known for their ability to think creatively and find novel solutions.
        Take the above prompt delimited by triple backticks and brainstorm 5 potential responses you could give.
        These responses may entail generating new ideas or expanding upon existing ones or both, depending on the prompt.
        Consider a variety of factors when generating your responses.

        For each of the 5 proposed responses, evaluate their potential.
        Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges and expected outcomes.
        Assign a probability of success and a confidence level to each option based on these factors.

        Then, for each evaluation, deepen the thought process.
        Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome.
        Also, consider any potential unexpected outcomes and how they might be handled.

        Based on the evaluations and scenarios, rank the solutions in order of promise.
        Provide a justification for each ranking and offer any final thoughts or considerations for each solution.

        Take a deep breath and work on this problem step-by-step.
    """
)


# Use original prompts
user_proxy.initiate_chat(
    manager,
    message=f"""

        ```{prompt}```

        You are a world-class problem solver who is known for their ability to think creatively and find novel solutions.
        Take the above prompt delimited by triple backticks and brainstorm 5 potential responses you could give.
        These responses may entail generating new ideas or expanding upon existing ones or both, depending on the prompt.
        Consider a variety of factors when generating your responses.

        For each of the 5 proposed responses, evaluate their potential.
        Consider their pros and cons, initial effort needed, implementation difficulty, potential challenges and expected outcomes.
        Assign a probability of success and a confidence level to each option based on these factors.

        Then, for each evaluation, deepen the thought process.
        Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome.
        Also, consider any potential unexpected outcomes and how they might be handled.

        Based on the evaluations and scenarios, rank the solutions in order of promise.
        Provide a justification for each ranking and offer any final thoughts or considerations for each solution.

        Take a deep breath and work on this problem step-by-step.
    """
)

user_proxy.initiate_chat(
    manager,
    message=f"""

        ```{prompt}```

        You are a world-class problem solver who is known for their ability to think creatively and find novel solutions.
        Take the above prompt delimited by triple backticks and find a novel approach that synthesizes the information contained within the options provided.
        You can lean more heavily on one idea over the rest, or create a solution that draws from the breath of available information if this is helpful.
        Consider a variety of factors when generating your responses.

        Now take this solution and evaluate its potential.
        Consider its pros and cons, initial effort needed, implementation difficulty, potential challenges and expected outcomes.

        Then, deepen the thought process.
        Generate potential scenarios, strategies for implementation, any necessary partnerships or resources, and how potential obstacles might be overcome.
        Also, consider any potential unexpected outcomes and how they might be handled.

        Assign a probability of success and a confidence level for this option based on these factors.
        Provide a justification for these rankings and offer any final thoughts or considerations for this solution.

        Take a deep breath and work on this problem step-by-step.
    """
)

# ------------------------------------------------------------------

user_proxy.initiate_chat(
    manager,
    message=f"""

        ```{prompt}```

        **Assign role
        **Create 5 responses
        **Consider a variety of factors when generating your responses.

        For each of the 5 proposed responses, evaluate their potential.
        **Consider their pros and cons, among other factors
        Assign a probability of success and a confidence level to each option based on these factors.

        Then, for each evaluation, deepen the thought process.
        **Consider a variety of factors when generating your responses.
        Also, consider any potential unexpected outcomes and how they might be handled.

        Based on the evaluations and scenarios, rank the solutions in order of promise.
        Provide a justification for each ranking and offer any final thoughts or considerations for each solution.

        Take a deep breath and work on this problem step-by-step.
    """
)

user_proxy.initiate_chat(
    manager,
    message=f"""

        ```{prompt}```

        **Assign role
        **Synthesize options, drawing on inspiration from one or multiple.
        **Consider a variety of factors when generating your responses.

        Now take this solution and evaluate its potential.
        **Consider its pros and cons, other factors.

        Then, deepen the thought process.
        **Consider a variety of factors when generating your responses.
        Also, consider any potential unexpected outcomes and how they might be handled.

        Assign a probability of success and a confidence level for this option based on these factors.
        Provide a justification for these rankings and offer any final thoughts or considerations for this solution.

        Take a deep breath and work on this problem step-by-step.
    """
)