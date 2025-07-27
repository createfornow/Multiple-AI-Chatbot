import streamlit as st
import requests

st.set_page_config(page_title="LangGrapg Agent UI", layout="centered")
st.title("AI Chatbot Agent")
st.write("Create and interact with AI Agents")

system_prompt=st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

MODEL_NAME_GROQ=["llama-3.3-70b-versatile","llama3-70b-8192","mixtral-8x7b-32768"]
MODEL_NAME_OPENAI=["gpt-4o-mini"]

provider=st.radio("Select Provider:",["Groq", "OpenAI"],
                  captions=[
                        "CEO - Jonathan Ross ",
                        "CEO - Sam Altman"
                    ]
                )

if provider=="Groq":
    selected_model=st.selectbox("Select Groq model:", MODEL_NAME_GROQ)
elif provider=="OpenAI":
    selected_model=st.selectbox("Select Groq model:", MODEL_NAME_OPENAI)
else:
    raise ValueError("Unsupposted model provider")

allow_web_search=st.checkbox("Allow Web search")

user_query=st.text_area("Enter you query:", height=150, placeholder="Ask anything...")

API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask Agent"):
    if user_query.strip():

        payload={
            "model_name": selected_model,
            "model_provider":provider,
            "system_prompt":system_prompt,
            "messages":[user_query],
            "allow_search":allow_web_search
        }

        response=requests.post(API_URL, json=payload)
        if response.status_code==200:
            response_data=response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"-- Final Response: -- {response_data}")

