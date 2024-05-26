from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
socketio = SocketIO(app)

current_image = 'cat.jpg'

@app.route('/')
def index():
    return render_template('index.html', image_name=current_image)

@app.route('/change_image', methods=['POST'])
def change_image():
    global current_image
    data = request.get_json()
    image_type = data['image_type']
    if image_type == 'dog':
        current_image = 'dog.jpg'
    elif image_type == 'cat':
        current_image = 'cat.jpg'
    socketio.emit('image change', {'new_image': current_image})
    return jsonify({'message': 'Image changed successfully', 'new_image': current_image})

if __name__ == '__main__':
    #server_port = os.environ.get('PORT', '8080')
    server_port = int(os.getenv('PORT', 8080))
    socketio.run(app, host='0.0.0.0', port=server_port, debug=False, allow_unsafe_werkzeug=True)   
