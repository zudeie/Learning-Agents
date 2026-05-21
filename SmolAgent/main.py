from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
import os 
from dotenv import  load_dotenv

load_dotenv()
HF_TOKEN= os.getenv("HF_TOKEN")