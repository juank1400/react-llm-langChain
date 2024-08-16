from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Obtener la API key desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")

# Configurar el modelo OpenAI con la API key
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Definir un prompt template básico
template = "Question: {question}\nAnswer:"
prompt = PromptTemplate(input_variables=["question"], template=template)

# Crear una cadena LLM usando el prompt y el modelo LLM
chain = prompt | llm | StrOutputParser()

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']

    # Hacer debug de la question
    print(question)

    # Usar la cadena LLM para obtener la respuesta
    answer = chain.invoke(question)
    
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
