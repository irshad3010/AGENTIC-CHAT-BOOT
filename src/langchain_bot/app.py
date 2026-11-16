# # import streamlit as st

# # from dotenv import load_dotenv

# # from langchain_openai import ChatOpenAI

# # from dotenv import load_dotenv
# # load_dotenv()

# # print("ShopEase Customer Support Chatbot Started Successfully!")
# # from langchain_core.messages import (
# #     AIMessage,
# #     HumanMessage
# # )
# # load_dotenv()




# # import streamlit as st

# import streamlit as st

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import AIMessage, HumanMessage


# # 3.2 — Get LLM
# def get_llm():
#     return ChatOpenAI(
#         model="gpt-4.1-mini",
#         temperature=0.3
#     )


# # 3.3 — Initialize session
# def init_session():
#     if "messages" not in st.session_state:
#         st.session_state.messages = [
#             AIMessage(content="Hi! Ask me anything.")
#         ]


# # 3.4 — Render chat history
# def render_history():
#     for msg in st.session_state.messages:

#         if isinstance(msg, HumanMessage):
#             role = "user"
#         else:
#             role = "assistant"

#         with st.chat_message(role):
#             st.markdown(msg.content)


# # 3.5 — Handle one chat round
# def chat_round(llm, user_input):

#     # Append user message
#     st.session_state.messages.append(
#         HumanMessage(content=user_input)
#     )

#     # Get response from LLM
#     response = llm.invoke(
#         st.session_state.messages
#     )

#     # Append assistant response
#     st.session_state.messages.append(response)


# # 3.6 — Main application
# def main():

#     st.set_page_config(
#         page_title="LangChain Bot",
#         page_icon="🤖"
#     )

#     load_dotenv()

#     init_session()

#     st.title("LangChain Chatbot")
#     st.caption("Powered by LangChain and OpenAI")

#     render_history()

#     prompt = st.chat_input("Ask a question")

#     if prompt:

#         llm = get_llm()

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 chat_round(llm, prompt)

#         st.rerun()


# # 3.7 — Entry point
# if __name__ == "__main__":
#     main()



# import streamlit as st
# from uuid import uuid4

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import AIMessage, HumanMessage

# from langchain_bot.auth import authenticate_user

# from langchain_bot.agent import get_agent
# from langchain_bot.rag_tool import initialize_vector_store


# # 1. Get LLM
# def get_llm():
#     return ChatOpenAI(
#         model="gpt-4.1-mini",
#         temperature=0.3
#     )


# # 2. Initialize session
# def init_session():

#     st.session_state.setdefault("conversations", {})
#     st.session_state.setdefault("messages", [])
#     st.session_state.setdefault("user_email", None)
#     st.session_state.setdefault("user_role", None)
#     st.session_state.setdefault("conversation_id", None)
#       # Step 10: Knowledge base initialization flag
#     st.session_state.setdefault("vector_store_ready", False)


# # 3. Render chat history
# def render_history():

#     for msg in st.session_state.messages:

#         if isinstance(msg, HumanMessage):
#             role = "user"
#         else:
#             role = "assistant"

#         with st.chat_message(role):
#             st.markdown(msg.content)


# # 4. Start a new conversation
# def start_new_conversation():

#     conversation_id = str(uuid4())

#     st.session_state.conversation_id = conversation_id

#     st.session_state.messages = [
#         AIMessage(
#             content="Hi! Welcome to our customer support. How can I help you?"
#         )
#     ]

#     st.session_state.conversations[conversation_id] = (
#         st.session_state.messages.copy()
#     )


# # 5. Load an existing conversation
# def load_conversation(conv_id):

#     if conv_id in st.session_state.conversations:

#         st.session_state.conversation_id = conv_id

#         st.session_state.messages = (
#             st.session_state.conversations[conv_id].copy()
#         )


# # 6. Handle chat round
# def chat_round(llm, user_input):

#     st.session_state.messages.append(
#         HumanMessage(content=user_input)
#     )

#     response = llm.invoke(
#         st.session_state.messages
#     )

#     st.session_state.messages.append(response)

#     conversation_id = st.session_state.conversation_id

#     if conversation_id:
#         st.session_state.conversations[conversation_id] = (
#             st.session_state.messages.copy()
#         )


# # 7. Main application
# def main():

#     st.set_page_config(
#         page_title="LangChain Customer Support",
#         page_icon="🤖"
#     )

#     load_dotenv()

#     init_session()

#     st.title("E-commerce Customer Support")

#     # LOGIN SCREEN
#     if not st.session_state.user_email:

#         st.subheader("Customer / Admin Login")

#         with st.form("login_form"):

#             email = st.text_input("Email")

#             password = st.text_input(
#                 "Password",
#                 type="password"
#             )

#             role = st.selectbox(
#                 "Select Role",
#                 ["customer", "admin"]
#             )

#             submitted = st.form_submit_button("Login")

#             if submitted:

#                 user = authenticate_user(
#                     email,
#                     password,
#                     role
#                 )

#                 if user:

#                     st.session_state.user_email = user["email"]
#                     st.session_state.user_role = user["role"]

#                     start_new_conversation()

#                     st.success("Login successful!")

#                     st.rerun()

#                 else:
#                     st.error(
#                         "Invalid email, password, or role."
#                     )

#         return

#     # SIDEBAR
#     with st.sidebar:

#         st.header("Conversations")

#         if st.button("Start new conversation"):

#             start_new_conversation()

#             st.rerun()

#         conversation_ids = list(
#             st.session_state.conversations.keys()
#         )

#         if conversation_ids:

#             current_id = st.session_state.conversation_id

#             selected_index = (
#                 conversation_ids.index(current_id)
#                 if current_id in conversation_ids
#                 else 0
#             )

#             selected_id = st.selectbox(
#                 "Select conversation",
#                 conversation_ids,
#                 index=selected_index
#             )

#             if selected_id != current_id:

#                 load_conversation(selected_id)

#                 st.rerun()

#         if st.button("Logout"):

#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]

#             st.rerun()

#     # USER INFORMATION
#     st.info(
#         f"Logged in: {st.session_state.user_email} | "
#         f"Role: {st.session_state.user_role} | "
#         f"Conversation ID: {st.session_state.conversation_id or '—'}"
#     )

#     # CHAT HISTORY
#     render_history()

#     # CHAT INPUT
#     prompt = st.chat_input("Ask a question")

#     if prompt:

#         llm = get_llm()

#         with st.chat_message("assistant"):

#             with st.spinner("Thinking..."):

#                 try:
#                     chat_round(llm, prompt)
#                     st.markdown(
#                         st.session_state.messages[-1].content
#                     )

#                 except Exception as e:
#                     st.error(f"Something went wrong: {e}")

#                     # Remove the failed user message
#                     if (
#                         st.session_state.messages
#                         and isinstance(
#                             st.session_state.messages[-1],
#                             HumanMessage
#                         )
#                     ):
#                         st.session_state.messages.pop()

#         st.rerun()


# # 8. Entry point
# if __name__ == "__main__":
#     main()


import streamlit as st
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

from langchain_bot.auth import authenticate_user
from langchain_bot.agent import get_agent
from langchain_bot.rag_tool import initialize_vector_store



from langchain_bot.agent import (
    get_agent,
    get_thread_config
)

from langchain_bot.thread_store import (
    load_threads,
    add_thread
)


# --------------------------------------------------
# 1. Initialize session
# --------------------------------------------------

def init_session():

    # st.session_state.setdefault("conversations", {})
    # st.session_state.setdefault("messages", [])
    st.session_state.setdefault("user_email", None)
    st.session_state.setdefault("user_role", None)
    st.session_state.setdefault("conversation_id", None)
    st.session_state.setdefault("threads", [])
    # Step 10: Knowledge base initialization flag
    st.session_state.setdefault("vector_store_ready", False)


# --------------------------------------------------
# 2. Render chat history
# --------------------------------------------------

# def render_history():

#     for msg in st.session_state.messages:

#         if isinstance(msg, HumanMessage):
#             role = "user"
#         else:
#             role = "assistant"

#         with st.chat_message(role):
#             st.markdown(msg.content)



def render_history():

    user_email = st.session_state.user_email
    conversation_id = st.session_state.conversation_id

    if not user_email or not conversation_id:
        return

    config = get_thread_config(
        user_email,
        conversation_id
    )

    # Read conversation from LangChain checkpointer
    snapshot = get_agent().get_state(config)

    messages = snapshot.values.get(
        "messages",
        []
    )

    for msg in messages:

        if msg.type == "human":

            with st.chat_message("user"):
                st.markdown(msg.content)

        elif msg.type == "ai" and msg.content:

            with st.chat_message("assistant"):
                st.markdown(msg.content)



# --------------------------------------------------
# 3. Start a new conversation
# --------------------------------------------------

# def start_new_conversation():

#     conversation_id = str(uuid4())

#     st.session_state.conversation_id = conversation_id

#     st.session_state.messages = [
#         AIMessage(
#             content=(
#                 "Hi! Welcome to ShopEase customer support. "
#                 "How can I help you today?"
#             )
#         )
#     ]

#     st.session_state.conversations[conversation_id] = (
#         st.session_state.messages.copy()
#     )

# def start_new_conversation():

#     conversation_id = str(uuid4())

#     st.session_state.conversation_id = conversation_id

#     # Save only UUID and label
#     threads = add_thread(
#         st.session_state.user_email,
#         conversation_id
#     )

#     st.session_state.threads = threads


# # --------------------------------------------------
# # 4. Load an existing conversation
# # --------------------------------------------------

# def load_conversation(conv_id):

#     if conv_id in st.session_state.conversations:

#         st.session_state.conversation_id = conv_id

#         st.session_state.messages = (
#             st.session_state.conversations[conv_id].copy()
#         )


# # --------------------------------------------------
# # 5. Handle chat round using LangChain agent
# # --------------------------------------------------

# def chat_round(user_input):

#     # Append customer message
#     st.session_state.messages.append(
#         HumanMessage(content=user_input)
#     )

#     # Convert history into agent-compatible messages
#     messages = []

#     for msg in st.session_state.messages:

#         if isinstance(msg, HumanMessage):
#             role = "user"
#         else:
#             role = "assistant"

#         messages.append({
#             "role": role,
#             "content": msg.content
#         })

#     # Invoke the LangChain agent
#     agent = get_agent()

#     result = agent.invoke({
#         "messages": messages
#     })

#     # Extract assistant response
#     response_messages = result.get("messages", [])

#     response_text = ""

#     if response_messages:

#         last_message = response_messages[-1]

#         response_text = last_message.content

#         # Handle non-string message content
#         if not isinstance(response_text, str):
#             response_text = str(response_text)

#     if not response_text:
#         response_text = (
#             "Sorry, I couldn't generate a response. "
#             "Please try again."
#         )

#     # Append assistant response
#     assistant_message = AIMessage(
#         content=response_text
#     )

#     st.session_state.messages.append(
#         assistant_message
#     )

#     # Save conversation in Streamlit session state
#     conversation_id = st.session_state.conversation_id

#     if conversation_id:

#         st.session_state.conversations[conversation_id] = (
#             st.session_state.messages.copy()
#         )

#     return response_text


def chat_round(user_input):

    user_email = st.session_state.user_email
    conversation_id = st.session_state.conversation_id

    config = get_thread_config(
        user_email,
        conversation_id
    )

    # Send only the new message.
    # LangChain retrieves previous messages from the checkpointer.
    get_agent().invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )



# --------------------------------------------------
# 6. Login screen
# --------------------------------------------------

def render_login():

    st.title("ShopEase Customer Support")

    st.subheader("Customer / Admin Login")

    with st.form("login_form"):

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Select Role",
            ["customer", "admin"]
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            user = authenticate_user(
                email.strip(),
                password,
                role
            )

            if user:

             st.session_state.user_email = user["email"]
             st.session_state.user_role = user["role"]

            # Load this customer's existing threads
            threads = load_threads(user["email"])

            st.session_state.threads = threads

            if threads:

              # Resume the first existing conversation
              st.session_state.conversation_id = threads[0]["id"]

            else:

              # Create the first conversation
              start_new_conversation()

            st.success("Login successful!")

            st.rerun()


# --------------------------------------------------
# 7. Sidebar
# --------------------------------------------------

# def render_sidebar():

#     with st.sidebar:

#         st.title("ShopEase")

#         st.header("Conversations")

#         if st.button(
#             "＋ Start new conversation",
#             use_container_width=True
#         ):

#             start_new_conversation()

#             st.rerun()

#         conversation_ids = list(
#             st.session_state.conversations.keys()
#         )

#         if conversation_ids:

#             current_id = st.session_state.conversation_id

#             selected_index = (
#                 conversation_ids.index(current_id)
#                 if current_id in conversation_ids
#                 else 0
#             )

#             selected_id = st.selectbox(
#                 "Select conversation",
#                 conversation_ids,
#                 index=selected_index
#             )

#             if selected_id != current_id:

#                 load_conversation(selected_id)

#                 st.rerun()

#         st.divider()

#         st.write(
#             f"**Email:** {st.session_state.user_email}"
#         )

#         st.write(
#             f"**Role:** {st.session_state.user_role}"
#         )

#         if st.button(
#             "Logout",
#             use_container_width=True
#         ):

#             for key in list(st.session_state.keys()):
#                 del st.session_state[key]

#             st.rerun()

    
    def render_sidebar():

      with st.sidebar:

        st.title("ShopEase")

        st.header("Conversations")

        # Start new conversation
        if st.button(
            "＋ Start new conversation",
            use_container_width=True
        ):

            start_new_conversation()

            st.rerun()

        threads = st.session_state.threads

        if threads:

            thread_ids = [
                thread["id"]
                for thread in threads
            ]

            thread_labels = {
                thread["id"]: thread["label"]
                for thread in threads
            }

            current_id = st.session_state.conversation_id

            selected_index = (
                thread_ids.index(current_id)
                if current_id in thread_ids
                else 0
            )

            selected_id = st.selectbox(
                "Select conversation",
                thread_ids,
                index=selected_index,
                format_func=lambda x: thread_labels[x]
            )

            if selected_id != current_id:

                load_conversation(selected_id)

                st.rerun()

        st.divider()

        st.write(
            f"Email: {st.session_state.user_email}"
        )

        st.write(
            f"Role: {st.session_state.user_role}"
        )

        if st.button(
            "Logout",
            use_container_width=True
        ):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()


# --------------------------------------------------
# 8. Initialize ChromaDB
# --------------------------------------------------

def initialize_knowledge_base():

    if not st.session_state.vector_store_ready:

        try:

            with st.spinner(
                "Initializing knowledge base..."
            ):

                initialize_vector_store()

                st.session_state.vector_store_ready = True

            st.success("Knowledge base ready!")

        except Exception as e:

            st.error(
                f"Knowledge base initialization failed: {e}"
            )

            st.stop()


# --------------------------------------------------
# 9. Main application
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title="ShopEase Customer Support",
        page_icon="🤖",
        layout="wide"
    )

    # Load environment variables
    load_dotenv()

    # Initialize session
    init_session()

    st.title("🤖 ShopEase Customer Support")

    st.caption(
        "AI-powered customer support using LangChain 1.x"
    )

    # Initialize policy knowledge base
    initialize_knowledge_base()

    # Login screen
    if not st.session_state.user_email:

        render_login()

        return

    # Sidebar
#     render_sidebar()

#     # User information
#     st.info(
#         f"Logged in: {st.session_state.user_email} | "
#         f"Role: {st.session_state.user_role} | "
#         f"Conversation ID: "
#         f"{st.session_state.conversation_id or '—'}"
#     )

#     # Display previous messages
#     render_history()

#     # Chat input
#     prompt = st.chat_input(
#         "Ask ShopEase a question..."
#     )

#     if prompt:

#         with st.chat_message("assistant"):

#             with st.spinner("Thinking..."):

#                 try:

#                     response = chat_round(prompt)

#                     st.markdown(response)

#                 except Exception as e:

#                     st.error(
#                         f"Agent error: {e}"
#                     )

#                     # Remove failed customer message
#                     if (
#                         st.session_state.messages
#                         and isinstance(
#                             st.session_state.messages[-1],
#                             HumanMessage
#                         )
#                     ):

#                         st.session_state.messages.pop()

#         st.rerun()

        
# def load_conversation(conv_id):

#     st.session_state.conversation_id = conv_id



# # --------------------------------------------------
# # 10. Entry point
# # --------------------------------------------------

# if __name__ == "__main__":
    # main()



    
import streamlit as st
from uuid import uuid4

from dotenv import load_dotenv

from langchain_bot.auth import authenticate_user

from langchain_bot.agent import (
    get_agent,
    get_thread_config
)

from langchain_bot.rag_tool import initialize_vector_store

from langchain_bot.thread_store import (
    load_threads,
    add_thread
)


# --------------------------------------------------
# 1. Initialize session
# --------------------------------------------------

def init_session():

    st.session_state.setdefault("user_email", None)
    st.session_state.setdefault("user_role", None)
    st.session_state.setdefault("conversation_id", None)

    # Store thread IDs and labels only
    st.session_state.setdefault("threads", [])

    # Knowledge base initialization
    st.session_state.setdefault("vector_store_ready", False)


# --------------------------------------------------
# 2. Render chat history from checkpointer
# --------------------------------------------------

def render_history():

    user_email = st.session_state.user_email
    conversation_id = st.session_state.conversation_id

    if not user_email or not conversation_id:
        return

    config = get_thread_config(
        user_email,
        conversation_id
    )

    snapshot = get_agent().get_state(config)

    messages = snapshot.values.get("messages", [])

    for msg in messages:

        if msg.type == "human":

            with st.chat_message("user"):
                st.markdown(msg.content)

        elif msg.type == "ai" and msg.content:

            with st.chat_message("assistant"):
                st.markdown(msg.content)


# --------------------------------------------------
# 3. Start a new conversation
# --------------------------------------------------

def start_new_conversation():

    conversation_id = str(uuid4())

    st.session_state.conversation_id = conversation_id

    # Save only conversation ID and label
    threads = add_thread(
        st.session_state.user_email,
        conversation_id
    )

    st.session_state.threads = threads


# --------------------------------------------------
# 4. Load an existing conversation
# --------------------------------------------------

def load_conversation(conv_id):

    st.session_state.conversation_id = conv_id


# --------------------------------------------------
# 5. Handle chat round using LangChain agent
# --------------------------------------------------

def chat_round(user_input):

    user_email = st.session_state.user_email
    conversation_id = st.session_state.conversation_id

    if not user_email or not conversation_id:
        raise ValueError("No active conversation found.")

    config = get_thread_config(
        user_email,
        conversation_id
    )

    # LangChain checkpointer automatically loads and saves history
    get_agent().invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )


# --------------------------------------------------
# 6. Login screen
# --------------------------------------------------

def render_login():

    st.title("ShopEase Customer Support")

    st.subheader("Customer / Admin Login")

    with st.form("login_form"):

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        role = st.selectbox(
            "Select Role",
            ["customer", "admin"]
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if submitted:

            user = authenticate_user(
                email.strip(),
                password,
                role
            )

            if user:

                st.session_state.user_email = user["email"]
                st.session_state.user_role = user["role"]

                # Load this customer's existing conversations
                threads = load_threads(user["email"])

                st.session_state.threads = threads

                if threads:

                    # Resume first conversation
                    st.session_state.conversation_id = (
                        threads[0]["id"]
                    )

                else:

                    # Create first conversation
                    start_new_conversation()

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid email, password, or role."
                )


# --------------------------------------------------
# 7. Sidebar - Conversation management
# --------------------------------------------------

def render_sidebar():

    with st.sidebar:

        st.title("🛍️ ShopEase")

        st.header("Conversations")

        # Start new conversation
        if st.button(
            "＋ Start new conversation",
            use_container_width=True
        ):

            start_new_conversation()

            st.rerun()

        threads = st.session_state.threads

        if threads:

            thread_ids = [
                thread["id"]
                for thread in threads
            ]

            thread_labels = {
                thread["id"]: thread["label"]
                for thread in threads
            }

            current_id = st.session_state.conversation_id

            selected_index = (
                thread_ids.index(current_id)
                if current_id in thread_ids
                else 0
            )

            selected_id = st.selectbox(
                "Select conversation",
                thread_ids,
                index=selected_index,
                format_func=lambda x: thread_labels[x]
            )

            if selected_id != current_id:

                load_conversation(selected_id)

                st.rerun()

        else:

            st.caption("No conversations available.")

        st.divider()

        st.subheader("Account")

        st.write(
            f"**Email:** {st.session_state.user_email}"
        )

        st.write(
            f"**Role:** {st.session_state.user_role}"
        )

        if st.button(
            "Logout",
            use_container_width=True
        ):

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()


# --------------------------------------------------
# 8. Initialize ChromaDB
# --------------------------------------------------

def initialize_knowledge_base():

    if not st.session_state.vector_store_ready:

        try:

            with st.spinner(
                "Initializing knowledge base..."
            ):

                initialize_vector_store()

                st.session_state.vector_store_ready = True

            st.success("Knowledge base ready!")

        except Exception as e:

            st.error(
                f"Knowledge base initialization failed: {e}"
            )

            st.stop()


# --------------------------------------------------
# 9. Main application
# --------------------------------------------------

def main():

    st.set_page_config(
        page_title="ShopEase Customer Support",
        page_icon="🤖",
        layout="wide"
    )

    load_dotenv()

    init_session()

    st.title("🤖 ShopEase Customer Support")

    st.caption(
        "AI-powered customer support using LangChain 1.x"
    )

    # Initialize policy knowledge base
    initialize_knowledge_base()

    # Login screen
    if not st.session_state.user_email:

        render_login()

        return

    # Sidebar
    render_sidebar()

    # User information
    st.info(
        f"Logged in: {st.session_state.user_email} | "
        f"Role: {st.session_state.user_role} | "
        f"Conversation ID: "
        f"{st.session_state.conversation_id or '—'}"
    )

    # Display history from LangChain checkpointer
    render_history()

    # Chat input
    prompt = st.chat_input(
        "Ask ShopEase a question..."
    )

    if prompt:

        try:

            with st.spinner("Thinking..."):

                chat_round(prompt)

        except Exception as e:

            st.error(f"Agent error: {e}")

        st.rerun()


# --------------------------------------------------
# 10. Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()

