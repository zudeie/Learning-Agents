import os 
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client=InferenceClient(model="moonshotai/Kimi-K2.5",token=HF_TOKEN)


# output = client.chat.completions.create(
#     messages=[
#         {"role": "user", "content": "The Capital of Nepal is"},],
#         stream=False,
#         max_tokens=100,
#         extra_body={'thinking': {'type': 'disabled'}},


# )
#  we used chat method by giving the messages in the form of list of dictionaries where each dictionary has role and content as keys. 
# The role can be user, assistant or system. The content is the actual message that we want to send to the model. 
# We also set stream to False, max_tokens to 100 and extra_body to disable thinking. 

# print(output.choices[0].message.content)

# Finally, we print the output which is the response from the model.

## MAKING A SYSTEM PROMPT 

def get_time():
    return "The current time is 08:08"

def get_pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Name: {data['name']}")
        print(f"ID: {data['id']}")
        # print(f"Height: {data['height']}")
        print(f"Height: 1000000m")
        print(f"Type: {data['types'][0]['type']['name']}")
        for ability in data['abilities']:
            print(f"Ability: {ability['ability']['name']}")
    else:
        print(f"Error: {response.status_code}")


# get_pokemon_info("pikachu")
# get_pokemon_info("squirtle")

SYSTEM_PROMPT = """ You are a helpful assistant that provides accurate and concise information to the user.
You have acess to following tools: 

get_time(): This tool returns the current time when called. You can use this tool to answer any questions related to time.

get_pokemon_info(name): This tool takes the name of a pokemon as input and returns its information such as name, id, height, type and abilities.
When the user asks for information about a pokemon, you should use the get_pokemon_info tool to fetch the information and provide it to the user.

The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and an `action_input` key (with the input to the tool going here).

for example, if the user asks for the current time, you should respond with the following json:
{{
    "action": "get_time"
}}

For example, if the user asks for information about pikachu, you should respond with the following json:


{{
    "action": "get_pokemon_info",
    "action_input": {"Pokemon": "pikachu"}
}}

ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:

$JSON_BLOB (inside markdown cell)

Observation: the result of the action. This Observation is unique, complete, and the source of truth.
(this Thought/Action/Observation can repeat N times, you should take several steps when needed. 
The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer.
 """
# messages = [
#     {"role": "system", "content": SYSTEM_PROMPT},
#     {"role": "user", "content": "Tell me  about mew"},
# ]

# output = client.chat.completions.create(
#     messages=messages,
#     stream=False,
#     max_tokens=500,
#     extra_body={'thinking': {'type': 'disabled'}},
# )
# print(output.choices[0].message.content)  # here the model is hallucinating and giving info by itself instead of calling the tool. 


# here is the block for time quesion 
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": " Tell mewhat time is it now."},
]   

output = client.chat.completions.create(
    messages=messages,
    max_tokens=150,
    stop=["Observation:"], # Let's stop before any actual function is called
    extra_body={'thinking': {'type': 'disabled'}},
)

# print(output.choices[0].message.content)

messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Tell me what time is it now."},
    {"role": "assistant", "content": output.choices[0].message.content + "Observation:" + str(get_time())},
]

output = client.chat.completions.create(
    messages=messages,
    max_tokens=150,
    stop=["Final Answer:"], # Let's stop before the final answer is given, so we can see the thought process.
    extra_body={'thinking': {'type': 'disabled'}},      

)
print(output.choices[0].message.content)





# here is the block for pokemon question
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Tell me about Metapod"},
]

output = client.chat.completions.create(
    messages=messages,
    max_tokens=150,
    stop=["Observation:"], # Let's stop before any actual function is called
    extra_body={'thinking': {'type': 'disabled'}},
)

# print(output.choices[0].message.content)

messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Tell me about Metapod"},
    {"role": "assistant", "content": output.choices[0].message.content + "Observation:" + str(get_pokemon_info("Metapod"))}, #manual observation
]

output = client.chat.completions.create(
    messages=messages,
    max_tokens=150,
    stop=["Final Answer:"], # Let's stop before the final answer is given, so we can see the thought process.
    extra_body={'thinking': {'type': 'disabled'}},      

)
print(output.choices[0].message.content)





# i purposely added the observation as the output of the function call to show that the model can use the observation to come to a final answer.
# i purposely made the height of the pokemon wrong to check that the model can use the observation to come to a final answer.