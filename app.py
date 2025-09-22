import streamlit as st
from langchain_core.messages import HumanMessage 
from langgraph_backend import chatbot
from personas import PERSONAS
 
CONFIG = {"configurable": {"thread_id": "demo-thread"}}  
  
if "history" not in st.session_state:
    st.session_state["history"] = []
if "persona" not in st.session_state:
    st.session_state["persona"] = "FloodRiskExpert"

# Persona selector
persona = st.selectbox("Select persona:", list(PERSONAS.keys()), index=0)
st.session_state["persona"] = persona

# Display history
for msg in st.session_state["history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if q := st.chat_input("Ask me something..."):
    st.session_state["history"].append({"role": "user", "content": q})
    with st.chat_message("user"): st.write(q)

    result = chatbot.invoke(
        {"messages": [HumanMessage(content=q)], "persona": persona},
        config=CONFIG,
    )
    ai_text = result["messages"][-1].content
    st.session_state["history"].append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant"): st.write(ai_text)






