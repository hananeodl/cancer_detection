from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
import numpy as np
from keras.preprocessing import image as keras_image
from keras.models import load_model
import logging
import requests  # Pour effectuer des requêtes HTTP depuis le backend vers le frontend
# import gdown
# model_url = 'https://drive.google.com/uc?id=YOUR_FILE_ID'
# model_path = gdown.download(model_url, '/tmp/model.h5')
# model = load_model(model_path)

app = Flask(__name__)   
CORS(app) 

UPLOAD_FOLDER = 'images_data'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = 16 * 3000 * 3000 # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_IMAGE_SIZE

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None
disease_class = ['M', 'B']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Cache model to avoid loading it on every request
def load_saved_model():
    global model
    if model is None:
        model = load_model("C:/Users/fatima ezzahra/OneDrive/Bureau/fst/s6/IHM/mon_projetIHM/training_model.h5")
    return model

def predict(image_path):
    model = load_saved_model()
    img = keras_image.load_img(image_path, grayscale= False, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255
    custom = model.predict(x)
    ind = np.argmax(custom[0])
    return disease_class[ind]

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            result = predict(filepath)
            print("ppreddictiong complete: ", result)
            os.remove(filepath)  # Clean up file after prediction
            return jsonify({'result': result}), 200
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return jsonify({'error': 'Error occurred during prediction'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
