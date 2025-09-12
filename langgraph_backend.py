from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage

from personas import build_system_prompt, PERSONAS
from tools.web_search import web_search

# ----- State -----
class ChatState(TypedDict):
    messages: Annotated[List, add_messages]
    persona: str

# ----- LLM -----
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0.2,
)

TOOLS = [web_search]
llm_tools = llm.bind_tools(TOOLS)
tool_node = ToolNode(TOOLS)

def agent_node(state: ChatState):
    persona = state.get("persona", "FloodRiskExpert")
    sys_prompt = SystemMessage(content=build_system_prompt(persona))
    msgs = [sys_prompt] + state["messages"]
    ai = llm_tools.invoke(msgs)
    return {"messages": [ai]}

# ----- Graph -----
builder = StateGraph(ChatState)
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# builder.add_edge(START, "agent")
# builder.add_conditional_edges("agent", tools_condition, {"tool": "tools", "__end__": END})
# builder.add_edge("tools", "agent")

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",   # when LLM calls web_search
        "__end__": END      # when conversation is done
    }
)

builder.add_edge("tools", "agent")

chatbot = builder.compile(checkpointer=InMemorySaver())
