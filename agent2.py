import json
import os
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from calendar_tools import (
    list_events,
    create_event,
    check_availability,
    get_current_date,
    delete_event_by_datetime,
)
from IPython.display import Image, display
from system_prompt import main_agent_system_prompt
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


tools = [list_events, create_event, check_availability, get_current_date, delete_event_by_datetime]

g = StateGraph(AgentState)
# llm = init_chat_model(model='orieg/gemma3-tools:1b',model_provider='ollama')
llm = init_chat_model(model="google_genai:gemini-2.0-flash")
tool_node = ToolNode(tools=tools)
llm_bind_tools = llm.bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    system_prompt = SystemMessage(main_agent_system_prompt)
    resp = llm_bind_tools.invoke([system_prompt]+state["messages"])
    return {"messages": [resp]}


g.add_node("agent", agent_node)
g.add_node("tools", tool_node)
g.add_edge(START, "agent")
g.add_conditional_edges(
    "agent",
    lambda s: (
        "tools"
        if isinstance(s["messages"][-1], AIMessage)
        and getattr(s["messages"][-1], "tool_calls", None)
        else END
    ),
    {
        "tools": "tools",
        END: END,
    },
)
g.add_edge("tools", "agent")
g.add_edge("agent", END)
agent_graph = g.compile()
