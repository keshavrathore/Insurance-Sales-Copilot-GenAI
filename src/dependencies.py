from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import requests, uuid
from flask_cors import CORS
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
import json
import time
import openai
import tiktoken
import random
import os
import copy
import re
import pickle
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
import faiss
from faiss import read_index
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import HumanMessagePromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.vectorstores import FAISS
from langchain.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQA
from src.recommend_filter import *
from langchain.llms import AzureOpenAI
from config.config import *
from config.prompts import *
openai.api_key = OPENAI_API_KEY
openai.api_type = API_TYPE
openai.api_base = API_BASE
openai.api_version = API_VERSION

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_API_TYPE"]= API_TYPE
os.environ["OPENAI_API_BASE"]= API_BASE
os.environ["OPENAI_API_VERSION"]= API_VERSION
model_name = 'gpt-3.5-turbo'

model = OpenAI(model_name=model_name,engine="Absligpt35-SC",n=1,temperature=0.9,verbose=True,api_version="2023-03-15-preview",api_base="https://openaiabsli-sc.openai.azure.com/",api_key="e743d453bbfd4470bfeee7e695350b44",api_type="Azure")


messages=[SystemMessage(content='''You are a chatbot, virtual assistant for an insurance company, answer general insurance questions.
You can answer some general questions only based on finance (specifically inusurance, mutual funds, stock market etc).
If the query is of external topic (for example sports, movies etc) you would remind the user that you are a sales assistant and can't provide information on the external topics.''')]

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
# Create a BlobServiceClient object using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

deployment_id = None
result = openai.Deployment.list()

for deployment in result.data:
    if deployment["status"] != "succeeded":
        continue
    if deployment['model'] == "gpt-35-turbo":
        deployment_id = deployment['id']
        break

if not deployment_id:
    print('No deployment with status: succeeded found.')
    model_name = "gpt-35-turbo"

    # Now let's create the deployment
    print(f'Creating a new deployment with model: {model_name}')
    result = openai.Deployment.create(model=model_name, scale_settings={"scale_type":"standard"})
    deployment_id = result["id"]
    print(f'Successfully created {model_name} with deployment_id {deployment_id}')
else:
    print(f'Found a succeeded deployment with id: {deployment_id}.')