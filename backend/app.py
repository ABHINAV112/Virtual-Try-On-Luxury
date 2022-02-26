from flask import Flask, request
from flask_cors import CORS
import os
from PIL import Image
import json
import requests
from pipeline.openpose import open_pose
from pipeline.human_parser import human_parser
from pipeline.clothe_mask import generate_clothe_mask

# Flask Config
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))

UPLOAD_PATH = f"{os.getcwd()}/data"

@app.route("/api", methods=["POST"])
def endpoint():
    req_file = request.files["human"]
    cloth_url = request.form["clotheUrl"]
    clothe_path = f"{UPLOAD_PATH}/cloth_img.jpg"
    human_filename = req_file.filename
    human_filepath = f"{UPLOAD_PATH}/{human_filename}"
    req_file.save(human_filepath) 
    response = requests.get(cloth_url)
    with open(clothe_path, "wb") as f:
        f.write(response.content)

    open_pose_json = open_pose(human_filepath)
    human_parser(human_filepath)
    generate_clothe_mask(clothe_path)
    print(open_pose_json)
    return json.dumps(open_pose_json)

if __name__ == "__main__":
    if(not os.path.isdir(UPLOAD_PATH)):
        os.makedirs(UPLOAD_PATH)

    app.run(host="0.0.0.0", port=PORT)