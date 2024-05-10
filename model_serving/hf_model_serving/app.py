"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, jsonify, request
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


# pylint: disable=C0103
app = Flask(__name__)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

model = AutoModel.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True, safe_serialization=True)

def get_embeddings(sentences):

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    #model = AutoModel.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True, safe_serialization=True)
    model.eval()

    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    matryoshka_dim = 512

    with torch.no_grad():
        model_output = model(**encoded_input)

    embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
    embeddings = embeddings[:, :matryoshka_dim]

    embeddings = F.normalize(embeddings, p=2, dim=1)
    print(embeddings)

    return(embeddings)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

sentences = ['search_query: What is Liferay?', 'search_query: Who is Laurens van der Maaten?']

@app.route('/embeddings', methods=['POST'])
def get_embeddings2():
    data = request.get_json()
    text = data.get('text')
    
    print(eval(text))


    if not text:
        return jsonify({'error': 'Missing text in request'}), 400

    try:
        response = get_embeddings(eval(text))

        return jsonify({'embeddings': response.tolist()})
    except ValueError:
            return jsonify({'error': 'Invalid input'}), 400

    
    
@app.route('/add', methods=['POST'])
def add_numbers():
    if request.method == 'POST':
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')
        if num1 is None or num2 is None:
            return jsonify({'error': 'Missing parameters'}), 400
        try:
            result = int(num1) + int(num2)
            return jsonify({'result': result})
        except ValueError:
            return jsonify({'error': 'Invalid input'}), 400
    else:
        return jsonify({'error': 'Method not allowed'}), 405 
    
    
#    except Exception as e:
#        return jsonify({'error': str(e)}), 500





if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
