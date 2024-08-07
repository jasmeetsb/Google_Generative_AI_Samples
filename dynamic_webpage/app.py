from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

from google.cloud import aiplatform

app = Flask(__name__)
socketio = SocketIO(app)



current_image = 'cat.jpg'
current_image = 'hyundai_home.png'

@app.route('/')
def index():
    return render_template('index.html', image_name=current_image)

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



# Your model endpoint ID
endpoint = "projects/your-project-id/locations/your-location-id/endpoints/your-endpoint-id"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json['message']
    parameters = {
        "text": user_input
    }
    response = client.predict(name=endpoint, parameters=parameters)
    return jsonify({'reply': response.predictions})



if __name__ == '__main__':
    #server_port = os.environ.get('PORT', '8080')
    server_port = int(os.getenv('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=server_port, debug=False, allow_unsafe_werkzeug=True)   
 