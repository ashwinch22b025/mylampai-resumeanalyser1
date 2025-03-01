import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
from langchain.schema import HumanMessage, AIMessage, SystemMessage
API_KEY = os.getenv("GOOGLE_API_KEY")
# from openai import AzureOpenAI

# API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
# AZURE_OPENAI_ENDPOINT=os.getenv('AZURE_OPENAI_ENDPOINT')
# API_KEY= "fae28ecf334e48b5aed8bb60ee94d351"
# AZURE_OPENAI_ENDPOINT="https://cvmaker1.openai.azure.com/"
# class Agent:
#     def __init__(self, system=""):
#         self.system = system
#         self.api_key = API_KEY
#         self.endpoint = AZURE_OPENAI_ENDPOINT
#         self.messages = []
#         if self.system:
#             self.messages.append(SystemMessage(content=system))
    
#     def __call__(self,message):
#         self.messages.append(HumanMessage(content=message))
#         result = self.execute()
#         self.messages.append(AIMessage(content=result))
#         return result

#     def execute(self):
#         client = AzureOpenAI(
#             api_key=self.api_key,
#             api_version="2024-02-01",
#             azure_endpoint=self.endpoint,
            
#         )
#         messages = []
#         for msg in self.messages:
#             if isinstance(msg, SystemMessage):
#                 messages.append({"role": "system", "content": msg.content})
#             elif isinstance(msg, HumanMessage):
#                 messages.append({"role": "user", "content": msg.content})
#             elif isinstance(msg, AIMessage):
#                 messages.append({"role": "assistant", "content": msg.content})
        
#         deployment_name = "gptcvmaker"
#         response = client.chat.completions.create(
#             model=deployment_name,
#             messages=messages
#         )
#         return response.choices[0].message.content
    

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append(SystemMessage(content=system))
    
    def __call__(self,message): 
        self.messages.append(HumanMessage(content=message))
        result = self.execute()
        self.messages.append(AIMessage(content=result))
        return result

    def execute(self):
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro",api_key=API_KEY,max_output_tokens=2048)
        
        
        messages = []
        for msg in self.messages:
            if isinstance(msg, SystemMessage):
                messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})
        
        ai_message = model.invoke(messages)
        return ai_message.content
