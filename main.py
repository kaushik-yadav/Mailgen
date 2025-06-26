import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

# credentials
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
TOGETHER_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.together.xyz/v1")
TOGETHER_API_KEY  = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("Please set the TOGETHER_API_KEY environment variable.")

# creating two llm instances one for classification and another for generation of email
llm_classification = ChatOpenAI(openai_api_key=TOGETHER_API_KEY,
                         openai_api_base=TOGETHER_API_BASE,
                         model_name=MODEL,
                         temperature=0.0)

llm_generative = ChatOpenAI(openai_api_key=TOGETHER_API_KEY,
                         openai_api_base=TOGETHER_API_BASE,
                         model_name=MODEL,
                         temperature=0.7)

# prompt template for Classification part & Runnable
classification_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are an email assistant classifier. "
     "Given a short, imperfect prompt, identify:\n"
     "1) Email type: one of [leave_request, follow_up, meeting_schedule, apology, complaint, other]\n"
     "2) Tone: one of [formal, informal, neutral]\n"
     "3) Key slots: Date, Recipient Name, Subject Matter (use placeholders if missing)\n"
     "Respond in JSON with keys: type, tone, slots."
    ),
    ("user", "{user_input}")
])

classification_runnable: Runnable = classification_template | llm_classification

# prompt template for email generation along with its runnable sequence
generation_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are an intelligent email writer for non-native English speakers.\n"
     "Use the provided classification JSON to generate a clear, concise, and professional email.\n"
     "- Include a Subject line.\n"
     "- Use greeting, body, and closing.\n"
     "- Fill in placeholders [Date], [Recipient Name]."
    ),
    ("user", "{classification_json}")
])

generation_runnable: Runnable = generation_template | llm_generative

if __name__ == "__main__":
    prompt_text = input("Enter your informal email prompt: ")

    # classification
    cls_resp = classification_runnable.invoke({"user_input": prompt_text})
    classification_json = cls_resp.content
    print("\nClassification JSON:", classification_json)

    # generation
    gen_resp = generation_runnable.invoke({"classification_json": classification_json})
    final_email = gen_resp.content

    print("\nGenerated Email:\n")
    print(final_email)
