from flask import Flask, render_template, request
import chatbt
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('landing.html')

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():
    userText = request.args.get('msg')
    print('Pregunta: ',userText)
    resp = chatbt.trabaja_bot(userText)
    print('Respuesta: ',resp)
    return resp

if __name__ == '__main__':
    app.run()