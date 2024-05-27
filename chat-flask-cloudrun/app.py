import os

from flask import Flask, jsonify, render_template, request
import vertexai
from vertexai.preview.language_models import ChatModel

#added
from flask_socketio import SocketIO, emit


app = Flask(__name__)

#added
socketio = SocketIO(app)

#PROJECT_ID = os.environ.get("GCP_PROJECT")  # Your Google Cloud Project ID
#LOCATION = os.environ.get("GCP_REGION")  # Your Google Cloud Project Region


PROJECT_ID = "jsb-alto"  # Your Google Cloud Project ID
LOCATION = "us-central1"  # Your Google Cloud Project Region

#added
current_image = 'hyundai_home.png'


vertexai.init(project=PROJECT_ID, location=LOCATION)


def create_session():
    chat_model = ChatModel.from_pretrained("chat-bison@002")
    chat = chat_model.start_chat()
    return chat


def response(chat, message):
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }
    result = chat.send_message(message, **parameters)
    return result.text


#@app.route("/")
#def index():
#    ###
#    return render_template("index.html")

#added
@app.route('/')
def index():
    return render_template('index.html', image_name=current_image)

#added
@app.route('/change_image', methods=['POST'])
def change_image():
    global current_image
    data = request.get_json()
    image_type = data['image_type']
    if image_type == 'kona':
        current_image = 'kona.png'
    elif image_type == 'santafe':
        current_image = 'santafe.png'
    elif image_type == 'hyundai_home':
        current_image = 'hyundai_home.png'
    elif image_type == 'ioniq':
        current_image = 'ioniq.png'
    socketio.emit('image change', {'new_image': current_image})
    return jsonify({'message': 'Image changed successfully', 'new_image': current_image})


@app.route("/palm2", methods=["GET", "POST"])
def vertex_palm():
    user_input = ""
    if request.method == "GET":
        user_input = request.args.get("user_input")
    else:
        user_input = request.form["user_input"]
    chat_model = create_session()
    content = response(chat_model, user_input)
    return jsonify(content=content)


if __name__ == "__main__":
    #app.run(debug=True, port=8080, host="0.0.0.0")

    server_port = int(os.getenv('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=server_port, debug=True, allow_unsafe_werkzeug=True) 
