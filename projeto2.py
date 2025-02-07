import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

# Configurações do Streamlit
st.set_page_config(page_title="Assistente Virtual 🤖", page_icon="🤖")
st.title("🦾 Seu assistente virtual")
st.sidebar.header("Escolha seu modelo de IA")

# Opções de modelo
model_class = st.sidebar.selectbox("Selecione o modelo\nem implementação", ["hf_hub", "openai", "ollama"])

def model_hf_hub(model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0.1):
    llm = HuggingFaceHub(
        repo_id=model,
        model_kwargs={
            "temperature": temperature,
            "return_full_text": False,
            "max_new_tokens": 512,
        }
    )
    return llm

def model_openai(model="gpt-4o-mini", temperature=0.1):
    llm = ChatOpenAI(
        model=model,
        temperature=temperature
    )
    return llm

def model_ollama(model="phi3", temperature=0.1):
    llm = ChatOllama(
        model=model,
        temperature=temperature,
    )
    return llm

def model_response(user_query, chat_history, model_class):
    if model_class == "hf_hub":
        llm = model_hf_hub()
    elif model_class == "openai":
        llm = model_openai()
    elif model_class == "ollama":
        llm = model_ollama()

    system_prompt = "Você é um assistente prestativo e está respondendo perguntas gerais. Responda em português."
    user_prompt = "{input}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", user_prompt)
    ])

    chain = prompt_template | llm | StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "input": user_query,
    })

# Histórico de conversa
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Menu de perguntas passadas
if st.session_state.chat_history:
    st.sidebar.subheader("Perguntas Passadas")
    for i, msg in enumerate(st.session_state.chat_history):
        if isinstance(msg, HumanMessage):
            if st.sidebar.button(f"{msg.content[:30]}..."):
                st.session_state.chat_history = st.session_state.chat_history[i:]
                break

# Entrada do usuário
user_query = st.text_area("Digite sua mensagem aqui...", height=100)

if st.button("Enviar"):
    if user_query.strip() != "":
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            resp = st.write_stream(model_response(user_query, st.session_state.chat_history, model_class))
        
        st.session_state.chat_history.append(AIMessage(content=resp))
