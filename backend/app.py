from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from PIL import Image
import requests

# Flask Config
app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app)

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))
DATA_DIR = "../data"

@app.route("/api", methods=["GET"])
def endpoint():
    params = request.args.to_dict()
    if "human_image" in params:
        f = params['human_image']  # Image
        filename = secure_filename("photo.jpeg")
        destination="/".join([DATA_DIR, filename])
        f.save(destination)
        human_image = Image.open(destination)

    if "clothes_image" in params:
        clothes_image = requests.get(params["clothes_image"], stream=True).raw

    # Process File
    
    return send_file(destination, mimetype='image/gif')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)