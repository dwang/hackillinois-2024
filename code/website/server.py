from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS  # Import CORS
from werkzeug.utils import secure_filename
import os
import datetime

# sample command line post request
# curl -X POST -F "picture=@/path/to/picture.jpg" -F "number_of_items=5" -F "coordinates=40.45,67.89" http://127.0.0.1:5000/api/pictureitem
# to run app, run python3 server.py

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app
api = Api(app)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage for demonstration
data_storage = []

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class PictureItem(Resource):
    def get(self):
        # Return the stored data
        return jsonify(data_storage)
    
    def post(self):
        if 'picture' not in request.files:
            return {'message': 'No picture part'}, 400
        file = request.files['picture']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Save data
            item_data = {
                'timestamp': datetime.datetime.now().isoformat(),
                'number_of_items': request.form.get('number_of_items', type=int),
                'coordinates': request.form.get('coordinates'),
                'picture_url': file_path
            }
            data_storage.append(item_data)
            
            return item_data, 201

api.add_resource(PictureItem, '/api/pictureitem')

if __name__ == '__main__':
    app.run(debug=True)
