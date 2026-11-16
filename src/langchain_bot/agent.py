
# from dotenv import load_dotenv
# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI

# from langchain_bot.rag_tool import search_policies

# load_dotenv()



# def create_support_agent():

#     # Initialize the LLM
#     model = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0.2
#     )

#     # Tools available to the agent
#     tools = [
#         search_policies
#     ]

#     # Agent instructions
#     system_prompt = """
#     You are ShopEase, an AI-powered e-commerce customer support assistant.

#     Your responsibilities include helping customers with:

#     1. Returns
#     2. Refunds
#     3. Shipping
#     4. Order cancellation policies
#     5. General customer support questions

#     TOOL USAGE:

#     - Use search_policies for questions about returns,
#       shipping, refunds, and cancellation policies.

#     - Do not use search_policies for individual customer
#       orders, account details, or order tracking.

#     - Do not use tools for simple greetings or casual conversation.

#     RESPONSE RULES:

#     - Answer policy questions using retrieved policy information.
#     - Do not invent policy details.
#     - If relevant information is unavailable, tell the customer.
#     - Be friendly, professional, and concise.

#     IMPORTANT RETURN POLICY:

#     - Never automatically approve or reject a return.
#     - Return requests must remain pending until human admin review.
#     - Explain the next steps clearly to customers.
#     """

#     # Create LangChain 1.x agent
#     agent = create_agent(
#         model=model,
#         tools=tools,
#         system_prompt=system_prompt
#     )

#     return agent




# _agent = None


# def get_agent():

#     global _agent

#     if _agent is None:

#         print("Creating ShopEase support agent...")

#         _agent = create_support_agent()

#         print("ShopEase support agent ready.")

#     return _agent


import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_bot.rag_tool import search_policies
from langchain_bot.middleware import get_logging_middleware


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Singleton instances
_agent = None
_checkpointer = None
_checkpoint_connection = None


# --------------------------------------------------
# 2. Initialize SQLite checkpointer
# --------------------------------------------------

def get_checkpointer():

    global _checkpointer
    global _checkpoint_connection

    if _checkpointer is not None:
        return _checkpointer

    # Get checkpoint database path
    checkpoint_path = os.getenv(
        "CHECKPOINTS_DB_PATH",
        str(PROJECT_ROOT / "checkpoints.sqlite")
    )

    checkpoint_path = Path(checkpoint_path)

    if not checkpoint_path.is_absolute():
        checkpoint_path = PROJECT_ROOT / checkpoint_path

    checkpoint_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # SQLite connection
    _checkpoint_connection = sqlite3.connect(
        str(checkpoint_path),
        check_same_thread=False
    )

    # Create LangGraph checkpointer
    _checkpointer = SqliteSaver(
        conn=_checkpoint_connection
    )

    # Initialize checkpoint tables
    _checkpointer.setup()

    print(f"Checkpoint database ready: {checkpoint_path}")

    return _checkpointer


# --------------------------------------------------
# 3. Thread configuration
# --------------------------------------------------

def get_thread_config(user_email, conversation_id):

    return {
        "configurable": {
            "thread_id": f"{user_email}:{conversation_id}"
        },
        "recursion_limit": 20
    }


# --------------------------------------------------
# 4. Create support agent
# --------------------------------------------------

def create_support_agent():

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )

    tools = [
        search_policies
    ]

    system_prompt = """
    You are ShopEase, an AI-powered e-commerce
    customer support assistant.

    Help customers with:

    1. Returns
    2. Refunds
    3. Shipping
    4. Order cancellation policies
    5. General customer support

    TOOL USAGE:

    - Use search_policies for questions about returns,
      shipping, refunds, and cancellation policies.
    - Do not use search_policies for individual customer
      orders, account details, or order tracking.
    - Do not use tools for simple greetings.

    RESPONSE RULES:

    - Answer policy questions using retrieved documents.
    - Never invent policy details.
    - If information is unavailable, explain that clearly.
    - Be friendly, professional, and concise.

    RETURN POLICY:

    - Never automatically approve or reject returns.
    - New return requests must remain pending.
    - Return decisions require human admin review.

    CONVERSATION MEMORY:

    - Use the conversation history provided to you.
    - Remember relevant details shared earlier in this thread.
    - Do not assume information from another conversation.
    """

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=get_checkpointer()
        
    )

    return agent


# --------------------------------------------------
# 5. Singleton agent
# --------------------------------------------------

def get_agent():

    global _agent

    if _agent is None:

        print("Creating ShopEase support agent...")

        _agent = create_support_agent()

        print("ShopEase support agent ready.")

    return _agent


# --------------------------------------------------
# 6. Public exports
# --------------------------------------------------

__all__ = [
    "create_support_agent",
    "get_agent",
    "get_checkpointer",
    "get_thread_config"
]



# import os
# import sqlite3
# import asyncio
# from pathlib import Path

# from dotenv import load_dotenv

# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.sqlite import SqliteSaver

# from langchain.mcp import MCPAdapter
# from langchain_core.tools import StructuredTool

# from langchain_bot.rag_tool import search_policies
# from langchain_bot.sql_tools import get_sql_tools
# from langchain_bot.middleware import get_logging_middleware


# # --------------------------------------------------
# # 1. Load environment variables
# # --------------------------------------------------

# load_dotenv()

# PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# _agent = None
# _checkpointer = None
# _checkpoint_connection = None


# # --------------------------------------------------
# # 2. Gmail MCP configuration
# # --------------------------------------------------

# # GMAIL_MCP_CONFIG = {
# #     "mcpServers": {
# #         "gmail": {
# #             "command": "npx",
# #             "args": [
# #                 "-y",
# #                 "@gongrzhe/server-gmail-autoauth-mcp"
# #             ],
# #         },
# #     }
# # }
# # 

# # GMAIL_MCP_CONFIG = {
# #     "mcpServers": {
# #         "gmail": {
# #             "command": "npx",
# #             "args": ["-y", "@gongrzhe/server-gmail-autoauth-mcp"],
# #         },
# #     }
# # }



# # --------------------------------------------------
# # 3. Load Gmail MCP tools
# # --------------------------------------------------

# # async def load_gmail_tools():

# #     async with MCPAdapter(GMAIL_MCP_CONFIG) as adapter:

# #         tools = await adapter.list_tools()

# #         return 

# def _sync_mcp_tool(tool):
#     """MCPAdapter tools are async-only. agent.invoke needs a sync func."""
#     if getattr(tool, "func", None) is not None:
#         return tool

#     def _call(**kwargs):
#         return asyncio.run(tool.ainvoke(kwargs))

#     return StructuredTool(
#         name=tool.name,
#         description=tool.description,
#         args_schema=tool.args_schema,
#         func=_call,
#         response_format=getattr(tool, "response_format", "content_and_artifact"),
#     )



# # async def load_gmail_tools():
# #     async with MCPAdapter(GMAIL_MCP_CONFIG) as adapter:
# #         tools = await adapter.list_tools()

# #         print("Gmail MCP tools:")
# #         for tool in tools:
# #             print(tool.name)

# #         return tools



# import subprocess

# command = [
#     r"C:\Windows\System32\cmd.exe",
#     "/d",
#     "/s",
#     "/c",
#     '"C:\\Program Files\\nodejs\\npx.cmd" -y @gongrzhe/server-gmail-autoauth-mcp'
# ]

# try:
#     result = subprocess.run(
#         command,
#         cwd=r"C:\Training.gmail-mcp",
#         capture_output=True,
#         text=True,
#         timeout=15
#     )

#     print("RETURN CODE:", result.returncode)
#     print("STDOUT:", result.stdout)
#     print("STDERR:", result.stderr)

# except subprocess.TimeoutExpired as e:
#     print("PROCESS IS STILL RUNNING AFTER 15 SECONDS")
#     print("STDOUT:", e.stdout)
#     print("STDERR:", e.stderr)



# # --------------------------------------------------
# # 4. Convert async MCP tools to sync tools
# # --------------------------------------------------

# def _sync_mcp_tool(tool):
#     """
#     MCPAdapter tools are async-only.
#     agent.invoke() requires synchronous tool functions.
#     """

#     if getattr(tool, "func", None) is not None:
#         return tool

#     def _call(**kwargs):

#         return asyncio.run(
#             tool.ainvoke(kwargs)
#         )

#     return StructuredTool(
#         name=tool.name,
#         description=tool.description,
#         args_schema=tool.args_schema,
#         func=_call,
#         response_format=getattr(
#             tool,
#             "response_format",
#             "content_and_artifact"
#         ),
#     )


# # --------------------------------------------------
# # 5. Initialize SQLite checkpointer
# # --------------------------------------------------

# def get_checkpointer():

#     global _checkpointer
#     global _checkpoint_connection

#     if _checkpointer is not None:
#         return _checkpointer

#     checkpoint_path = os.getenv(
#         "CHECKPOINTS_DB_PATH",
#         str(PROJECT_ROOT / "checkpoints.sqlite")
#     )

#     checkpoint_path = Path(checkpoint_path)

#     if not checkpoint_path.is_absolute():
#         checkpoint_path = PROJECT_ROOT / checkpoint_path

#     checkpoint_path.parent.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     _checkpoint_connection = sqlite3.connect(
#         str(checkpoint_path),
#         check_same_thread=False
#     )

#     _checkpointer = SqliteSaver(
#         conn=_checkpoint_connection
#     )

#     _checkpointer.setup()

#     print(f"Checkpoint database ready: {checkpoint_path}")

#     return _checkpointer


# # --------------------------------------------------
# # 6. Thread configuration
# # --------------------------------------------------

# def get_thread_config(user_email, conversation_id):

#     return {
#         "configurable": {
#             "thread_id": f"{user_email}:{conversation_id}"
#         },
#         "recursion_limit": 20
#     }


# # --------------------------------------------------
# # 7. Create support agent
# # --------------------------------------------------

# def create_support_agent():

#     model = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0.2
#     )

#     # ----------------------------------------------
#     # Load Gmail MCP tools
#     # ----------------------------------------------

#     print("Connecting to Gmail MCP...")

#     raw_gmail_tools = asyncio.run(
#         load_gmail_tools()
#     )

#     gmail_tools = [
#         _sync_mcp_tool(tool)
#         for tool in raw_gmail_tools
#     ]

#     print(
#         "Gmail MCP tools:",
#         [tool.name for tool in gmail_tools]
#     )

#     # ----------------------------------------------
#     # Verify send_email
#     # ----------------------------------------------

#     send_tool = next(
#         (
#             tool for tool in gmail_tools
#             if tool.name == "send_email"
#         ),
#         None
#     )

#     if send_tool is None:
#         raise RuntimeError(
#             "Gmail MCP send_email tool not found"
#         )

#     if send_tool.func is None:
#         raise RuntimeError(
#             "Gmail send_email is not synchronous"
#         )

#     print(
#         "send_email sync function:",
#         send_tool.func is not None
#     )

#     # ----------------------------------------------
#     # Load SQL toolkit
#     # ----------------------------------------------

#     sql_tools = get_sql_tools()

#     print(
#         "SQL tools:",
#         [tool.name for tool in sql_tools]
#     )

#     # ----------------------------------------------
#     # Combine all tools
#     # ----------------------------------------------

#     tools = (
#         [search_policies]
#         + sql_tools
#         + gmail_tools
#     )

#     print(
#         "Total agent tools:",
#         [tool.name for tool in tools]
#     )

#     # ----------------------------------------------
#     # System prompt
#     # ----------------------------------------------

#     system_prompt = """
#     You are ShopEase, an AI-powered e-commerce
#     customer support assistant.

#     Help customers with:

#     1. Returns
#     2. Refunds
#     3. Shipping
#     4. Order cancellation policies
#     5. General customer support

#     ================================================
#     TOOL USAGE
#     ================================================

#     - Use search_policies for return, shipping,
#       refund and cancellation policy questions.

#     - Use SQL tools for customer information,
#       orders, order status, cancellation requests,
#       return requests and email logging.

#     - Use Gmail MCP for customer email communication.

#     - Do not use tools for simple greetings.

#     ================================================
#     GMAIL EMAIL RULES
#     ================================================

#     - Use send_email ONLY for sending emails.
#     - The to argument must always be a list.
#     - The list must contain ONLY the authenticated,
#       logged-in customer's email address.
#     - Never send emails to administrators or other
#       recipients.
#     - Never guess or invent a customer email address.
#     - Never use delete_email.
#     - Never use batch_delete_emails.
#     - Never use Gmail label or filter tools.

#     For cancellation and return requests:

#     1. Verify the customer and relevant order using SQL.
#     2. Submit the request according to the existing
#        application workflow.
#     3. Keep the request pending administrator review.
#     4. Send a short request-received email to the
#        logged-in customer using send_email.
#     5. Clearly mention that the request is pending
#        administrator review.

#     After an administrator makes a decision:

#     1. Retrieve the actual decision from SQL.
#     2. Send another email to the customer.
#     3. Explain what changed and the decision.
#     4. Never invent an administrator decision.

#     Email subject and body must clearly describe
#     the request and its current status.

#     ================================================
#     EMAIL DATABASE LOGGING
#     ================================================

#     After every successful send_email call:

#     - Use SQL tools to INSERT a row into email_logs.
#     - Get the customer's user_id using the authenticated
#       customer's email and users table.
#     - Store the following fields:

#       user_id
#       email
#       subject
#       body_preview
#       email_type
#       sent_at

#     - Use the actual email content for the preview.
#     - Use the current timestamp for sent_at.
#     - Use an appropriate email_type such as
#       RETURN_REQUEST, RETURN_DECISION,
#       CANCELLATION_REQUEST or CANCELLATION_DECISION.

#     - Do not insert an email log when sending fails.
#     - Do not claim the email was sent if send_email fails.
#     - Do not claim the log was saved unless the SQL
#       INSERT succeeds.

#     ================================================
#     RESPONSE RULES
#     ================================================

#     - Answer policy questions using retrieved documents.
#     - Never invent policy details.
#     - If information is unavailable, explain clearly.
#     - Be friendly, professional and concise.

#     ================================================
#     RETURN AND CANCELLATION POLICY
#     ================================================

#     - Never automatically approve or reject returns.
#     - Never automatically approve or reject cancellations.
#     - New requests must remain pending administrator review.
#     - Only an actual administrator decision can change
#       the request status.

#     ================================================
#     CONVERSATION MEMORY
#     ================================================

#     - Use the conversation history provided to you.
#     - Remember relevant details within this thread.
#     - Never assume information from another conversation.
#     """

#     # ----------------------------------------------
#     # Create agent
#     # ----------------------------------------------

#     agent = create_agent(
#         model=model,
#         tools=tools,
#         system_prompt=system_prompt,
#         middleware=get_logging_middleware(),
#         checkpointer=get_checkpointer()
#     )

#     return agent


# # --------------------------------------------------
# # 8. Singleton agent
# # --------------------------------------------------

# def get_agent():

#     global _agent

#     if _agent is None:

#         print("Creating ShopEase support agent...")

#         _agent = create_support_agent()

#         print("ShopEase support agent ready.")

#     return _agent


# # --------------------------------------------------
# # 9. Public exports
# # --------------------------------------------------

# __all__ = [
#     "create_support_agent",
#     "get_agent",
#     "get_checkpointer",
#     "get_thread_config"
# ]

