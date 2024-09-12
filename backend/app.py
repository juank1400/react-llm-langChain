from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.globals import set_verbose
from langchain.globals import set_debug


import os
import requests

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
set_verbose(True)
set_debug(True)

# Obtener la API key desde las variables de entorno
api_key = os.getenv("OPENAI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

# Definir un Tool para consultar el clima
@tool("get_weather")
def get_weather(city: str) -> str:
    """Get the weather information for a specified location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    print("Sending request to:", url)
#    response = requests.get(url)
#    if response.status_code == 200:
#        data = response.json()
#        temp = data['main']['temp']
#        description = data['weather'][0]['description']
#        return f"The current temperature in {city} is {temp}°C with {description}."
#    else:
#        return "I'm sorry, I couldn't retrieve the weather information at the moment."
    return "Es un clima esplendido."
# Configurar el modelo OpenAI con la API key
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)

search = TavilySearchResults(max_results=2)
tools = [search,get_weather]

# Agrega la tool de Weather a la lista de herramientas
llm_w_tools = llm.bind_tools(tools)

# Definir un prompt template básico
template = "Question: {question}\nAnswer:"
prompt = PromptTemplate(input_variables=["question"], template=template)

# Crear una cadena LLM usando el prompt y el modelo LLM
chain = prompt | llm_w_tools | StrOutputParser()

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')
    model = chain.get_graph()
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        print(question)
        preliminary_answer = chain.invoke(question)
        # Verificar si el modelo sugiere usar el WeatherTool
        if "use the get_weather" in preliminary_answer.lower():
            # Extraer la ciudad de la pregunta
            city = question.split("in")[-1].strip()
            answer = get_weather.invoke(city)
        else:
            answer = preliminary_answer
        return jsonify({"answer": answer})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "An error occurred while processing your request."}), 500

if __name__ == '__main__':
    app.run(debug=True)
