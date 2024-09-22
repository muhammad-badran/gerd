"""Python file to serve as the frontend"""
import sys
import os
import time

config = {
    'app': {
        'config': {
            'name': 'full-stack-app'
        }
    },
    'llm': {
        'provider': 'openai',
        'config': {
            'model': 'gpt-4o-mini',
            'temperature': 0.5,
            'max_tokens': 1000,
            'top_p': 1,
            'stream': False,
            'prompt': (
                "Use the following pieces of context to answer the query at the end.\n"
                "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n"
                "$context\n\nQuery: $query\n\nHelpful Answer:"
            ),
            'system_prompt': (
                "Act as William Shakespeare. Answer the following questions in the style of William Shakespeare."
            ),
            'api_key': api_key,
            "model_kwargs": {"response_format": {"type": "json_object"}},
        }
    },
    'vectordb': {
        'provider': 'pinecone',
        'config': {
            'metric': 'dotproduct',
            'vector_dimension': 1536,
            'index_name': 'my-index',
            'serverless_config': {
                'cloud': 'aws',
                'region': 'us-west-2'
            },
            'hybrid_search': True, # Remember to set this for hybrid search
        }
    },
    'embedder': {
        'provider': 'openai',
        'config': {
            'model': 'text-embedding-3-small',
            'api_key': api_key,
        }
    },
    'chunker': {
        'chunk_size': 2000,
        'chunk_overlap': 100,
        'length_function': 'len',
        'min_chunk_size': 0
    },
    'cache': {
      'similarity_evaluation': {
          'strategy': 'distance',
          'max_distance': 1.0,
      },
      'config': {
          'similarity_threshold': 0.8,
          'auto_flush': 50,
      },
    },
}


sys.path.append(os.path.abspath('.'))

import streamlit as st
from app.components.sidebar import sidebar

def ingest_data_dynamic(n):
    print(f'Number of Data Sources are {n}')
    for r in range(n):
        url_= st.session_state.get(f"value_{r}")
        print(f"Ingestion {r+1}/{n}: {url_}")
        gerd.add(url_)

    st.session_state["IS_CHATBOT_READY"] = True

def response_embedchain(query):
    """Logic for loading the chain you want to use should go here."""
    print(f'Calling response on: {query}')
    query_config = QueryConfig(stream = True)
    response = gerd.query(query, query_config)
    return response

def add_data_form(r):
    st.session_state[f"url_{r}"] = [st.session_state.get(f"value_{r}")]
    print(st.session_state.get(f"{r}"))


def add_form_row(row):
    # Inputs listed within a form
    # loaders_type = ["youtube_video", "pdf_file", "web_page", "qna_pair", "text"]
    data_form = st.form(key=f'{row}-Form')
    with data_form:
        data_columns = st.columns(1)
        with data_columns[0]:
            st.text_input(f"Enter Doc URL: {row}",
                            value="https://www.youtube.com/watch?v=Xg1bqjKv-zg",
                            key=f"value_{row}")
        st.form_submit_button(on_click=add_data_form(row))


def provide_data_dynamic():
    
    with st.expander("Sources Data Form", expanded=st.session_state["expander_state"]):
        num_data_sources = st.slider('Number of Data Sources', min_value=1, max_value=10)
        for r in range(num_data_sources):
            add_form_row(r)
        submit_data_form = st.button("Submit Data", on_click=toggle_closed)
        if submit_data_form:
            st.session_state["submit_data_form"] = True
        return num_data_sources


def toggle_closed():
    st.session_state["expander_state"] = False


if __name__ == "__main__":

    st.set_page_config(
        page_title="GRED Assistant Chatbot",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded", )
    st.header("GRED Assistant Chatbot ")

    sidebar()

    if "expander_state" not in st.session_state:
        st.session_state["expander_state"] = True

    num_data_sources = provide_data_dynamic()

    if not st.session_state.get("OPENAI_API_CONFIGURED"):
        st.error("Please configure your API Keys!")

    if not st.session_state.get("submit_data_form"):
        st.error("Please Submit the Data Form")

    if st.session_state.get("OPENAI_API_CONFIGURED") and st.session_state.get("submit_data_form"):
        st.markdown("Main App: Started")
        from embedchain import App
        gerd = App()
        # ingesting data
        if not st.session_state.get("IS_CHATBOT_READY"):
            with st.spinner('Ingesting Data! Please Wait!'):
                # ingest_data(data_dict)
                ingest_data_dynamic(num_data_sources)
            st.success('Data ingestion has finished successfully!')

        if st.session_state.get("IS_CHATBOT_READY"):

            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "How can I help you?"}]

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_input := st.chat_input("What is your question?"):
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(user_input)
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    with st.spinner('CHAT-BOT is at Work ...'):
                        assistant_response = response_embedchain(user_input)
                    # Simulate stream of response with milliseconds delay
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
