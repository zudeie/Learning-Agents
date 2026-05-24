from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
import os 
from dotenv import  load_dotenv

load_dotenv()
HF_TOKEN= os.getenv("HF_TOKEN")
@tool
def Search_web(query: str) -> str:
    
    """This tool allows to search the web for information. 
        Args:
        query (str): The search query for what to search about in the web examples."""
    try: 
        search=DuckDuckGoSearchTool()
        result=search.run(query)
        return result
    except Exception as e:
        return f"An error occurred while searching the web for {query}. Exception: {str(e)}"
    
def get_current_time(Country:str) -> str:
    """This tool allows to get the current time. 
        Args:
        Country (str): The country for which to get the current time. Examples: 'United States', 'India', 'Japan' etc.
        Returns:
        str: The current time in the format 'YYYY-MM-DD HH:MM:SS'."""
    try:
        timezone = pytz.country_timezones[Country][0]
        tz = pytz.timezone(timezone)
        current_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        return current_time
    except Exception as e:
        return f"An error occurred while getting the current time for {Country}. Exception: {str(e)}"


FinalAnswer=FinalAnswerTool()


model=InferenceClientModel(
    max_tokens=2096,
    temperature=0.5,
    model_id='Qwen/Qwen2.5-Coder-13B-Instruct',
    custom_role_conversion=None,
    token=HF_TOKEN
    )


with open('prompts.yaml', 'r') as f:
    prompt_templates = yaml.safe_load(f)

agent = CodeAgent(
    model=model,
    tools=[Search_web, get_current_time, FinalAnswer],
    max_steps=6,
    verbosity_level=1,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)

prompt = input("Enter your question: ")
response = agent.run(prompt)
print("Agent's response:", response)

