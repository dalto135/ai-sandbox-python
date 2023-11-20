# from utils import get_api_key
import os
import google.generativeai as palm
from google.api_core import client_options as client_options_lib, retry

def get_api_key():
    return ""

palm.configure(
    api_key=get_api_key(),
    transport="rest",
    client_options=client_options_lib.ClientOptions(
        api_endpoint=os.getenv("GOOGLE_API_BASE"),
    )
)

models = [
    m for m in palm.list_models()
    if 'generateText' 
    in m.supported_generation_methods
]

# for m in palm.list_models():
#     print(f"name: {m.name}")
#     print(f"description: {m.description}")
#     print(f"generation methods:{m.supported_generation_methods}\n")

model_bison = models[0]

prompt_template = """
{priming}

{question}

{decorator}

Your solution:
"""

# priming_text = "You are an expert at writing clear, concise Python code."
# question = "Create a very large list of random numbers in Python, and then write code to sort that list."
# decorator = "Insert comments for each line of code."

priming_text = "Can you please create test cases in code for this Python code?"
question = """
class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None


class SLinkedList:
    def __init__(self):
        self.headval = None


def create_linked_list(data_list):
    # Create a linked list node for each element in the data list.
    for data in data_list:
        new_node = Node(data)
        # Insert the new node at the head of the linked list.
        new_node.nextval = self.headval
        self.headval = new_node


def print_linked_list(headval):
    # Create a temporary node pointer to traverse the linked list.
    temp = headval
    # Print the data value of each node in the linked list.
    while temp is not None:
        print(temp.dataval)
        # Move the temporary node pointer to the next node in the linked list.
        temp = temp.nextval


if __name__ == "__main__":
    # Create a linked list with the data values "Mon", "Tue", and "Wed".
    data_list = ["Mon", "Tue", "Wed"]
    list1 = SLinkedList()
    create_linked_list(data_list)

    # Print the data values in the linked list.
    print_linked_list(list1.headval)

"""
decorator = "Explain in detail what these test cases are designed to achieve."

prompt = prompt_template.format(
    priming=priming_text,
    question=question,
    decorator=decorator
)

print(prompt)
print("---------------------------------------------")

@retry.Retry()
def generate_text(prompt=prompt, model=model_bison, temperature=0.0):
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)

completion = generate_text()

print(completion.result)
