import streamlit as st
import os
from dotenv import load_dotenv


def set_open_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_KEY"] = api_key
    st.session_state["OPENAI_API_CONFIGURED"] = True
    print('OPENAI API key is Configured Successfully!')


def sidebar():
    load_dotenv()
    with st.sidebar:

        try:
            api_key = os.getenv("OPENAI_API_KEY")
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state["OPENAI_API_CONFIGURED"] = True
            st.markdown("Open API Key Configured!")
        except:
            st.markdown(
                "## How to use\n"
                "Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
                
            )
            open_api_key_input = st.text_input(
                "Openai API Key",
                type="password",
                placeholder="Paste your API key here (sk-...)",
                help="You can get your API key from https://platform.openai.com/account/api-keys.",
                value=st.session_state.get("OPEN_API_KEY", ""),
            )
            if open_api_key_input:
                set_open_api_key(open_api_key_input)

            if not st.session_state.get("OPENAI_API_CONFIGURED"):
                st.error("Please configure your Open API key!")
            else:
                st.markdown("Open API Key Configured Successfully!")

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖 This App uses embedchain and streamlit as chatbot"
        )
        st.markdown("By [Muhammad Badran](https://www.linkedin.com/in/muhammad-badran-5b6645189/)")
        st.markdown("By [Bahaa Ismail](https://www.linkedin.com/)")
        st.markdown("---")

        st.markdown(" # Example: Sample Data")
        st.markdown(
            """
            | Source    | URL |
            | -------- | ------- |
            | youtube  | https://www.youtube.com/watch?v=arDEcQNJVTY   |
            | pdf_file | https://navalmanack.s3.amazonaws.com/Eric-Jorgenson_The-Almanack-of-Naval-Ravikant_Final.pdf    |
            | web    | https://nav.al/feedback  |
            |qna_pair| "What does GERD stand for?", "GERD, or Gastroesophageal Reflux Disease, is a medical condition where the reflux of stomach contents into the esophagus." |
            
            Question: What are symptoms of reflux? 
            """
            )
