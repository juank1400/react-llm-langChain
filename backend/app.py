from flask import Flask, request, jsonify
from langchain import LangChain, GPTModel

app = Flask(__name__)

model = GPTModel(api_key="YOUR_OPENAI_API_KEY")
chain = LangChain(model)

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    answer = chain.process_question(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
