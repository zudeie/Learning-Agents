import os 
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client=InferenceClient(model="moonshotai/Kimi-K2.5",token=HF_TOKEN)


output = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "The Capital of Nepal is"},],
        stream=False,
        max_tokens=100,
        extra_body={'thinking': {'type': 'disabled'}},


)
#  we used chat method by giving the messages in the form of list of dictionaries where each dictionary has role and content as keys. 
# The role can be user, assistant or system. The content is the actual message that we want to send to the model. 
# We also set stream to False, max_tokens to 100 and extra_body to disable thinking. 

print(output.choices[0].message.content)

# Finally, we print the output which is the response from the model.

