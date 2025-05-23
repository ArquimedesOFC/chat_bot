
# 🤖 ChatBot com Python a

Este projeto é um chatbot simples desenvolvido em Python, utilizando a biblioteca `openai` para interações com modelos de linguagem.

## 📁 Estrutura do Projeto

```
chat_bot/
├── .env
├── projeto2.py
└── README.md
```

- **`.env`**: Arquivo contendo variáveis de ambiente, como a chave da API da OpenAI.
- **`projeto2.py`**: Script principal que executa o chatbot.
- **`README.md`**: Este arquivo de documentação.

## ⚙️ Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina.

## 🚀 Instalação e Execução

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ArquimedesOFC/chat_bot.git
   cd chat_bot
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv
   # Ative o ambiente virtual
   # No Windows:
   venv\Scripts\activate
   # No macOS/Linux:
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   Crie um arquivo `requirements.txt` com o seguinte conteúdo:

   ```txt
   openai
   python-dotenv
   ```

   Em seguida, execute:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Substitua `your_openai_api_key_here` pela sua chave de API da OpenAI.

5. **Execute o chatbot:**

   ```bash
   python projeto2.py
   ```

## 🧠 Funcionamento

O script `projeto2.py` carrega a chave da API da OpenAI a partir do arquivo `.env` e utiliza a biblioteca `openai` para interagir com o modelo de linguagem.
O usuário pode inserir mensagens, e o chatbot responderá com base na resposta gerada pelo modelo.

## 📝 Exemplo de Uso

```
Usuário: Olá, chatbot!
Chatbot: Olá! Como posso ajudá-lo hoje?
```

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
