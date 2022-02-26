from flask import Flask, request,send_file
from flask_cors import CORS
import os
from PIL import Image
import json
import requests
from pipeline.openpose import open_pose
from pipeline.human_parser import human_parser
from pipeline.clothe_mask import generate_clothe_mask
from binascii import a2b_base64
from datauri import DataURI



# Flask Config
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))

UPLOAD_PATH = f"{os.getcwd()}/data"

@app.route("/api", methods=["POST"])
def endpoint():
    req_file = request.form["human"]
    uri = DataURI(req_file)
    print(uri.mimetype)
    human_filepath = f"{UPLOAD_PATH}/human.jpg"
    with open(human_filepath, "wb") as f:
        f.write(uri.data)

    cloth_url = request.form["clotheUrl"]
    clothe_path = f"{UPLOAD_PATH}/cloth_img.jpg"
    response = requests.get(cloth_url)
    with open(clothe_path, "wb") as f:
        f.write(response.content)

    open_pose_json = open_pose(human_filepath)
    human_parser(human_filepath)
    generate_clothe_mask(clothe_path)

    return send_file(human_filepath)

if __name__ == "__main__":
    if(not os.path.isdir(UPLOAD_PATH)):
        os.makedirs(UPLOAD_PATH)

    app.run(host="0.0.0.0", port=PORT)