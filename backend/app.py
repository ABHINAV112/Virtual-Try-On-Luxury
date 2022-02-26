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
import cv2
from pipeline.final_step import main as final
from config import UPLOAD_PATH,RESULT_PATH

# Flask Config
app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

# Environment Variables
PORT = int(os.environ.get("PORT", 10000))


@app.route("/api", methods=["POST"])
def endpoint():
    req_file = request.form["human"]
    uri = DataURI(req_file)
    human_filepath = f"{UPLOAD_PATH}/image/human.jpg"
    with open(human_filepath, "wb") as f:
        f.write(uri.data)
    img = cv2.imread(human_filepath)
    img = cv2.resize(img, ((192, 256)))
    cv2.imwrite(human_filepath,img)
    
    cloth_url = request.form["clotheUrl"]
    clothe_path = f"{UPLOAD_PATH}/cloth/cloth.jpg"
    response = requests.get(cloth_url)
    with open(clothe_path, "wb") as f:
        f.write(response.content)
    img = cv2.imread(clothe_path)
    img = cv2.resize(img, ((192, 256)))
    cv2.imwrite(clothe_path,img)

    open_pose(human_filepath)
    human_parser(human_filepath)
    generate_clothe_mask(clothe_path)
    final("GMM")
    final("TOM")
    return send_file(RESULT_PATH)

if __name__ == "__main__":
    if(not os.path.isdir(UPLOAD_PATH)):
        os.makedirs(UPLOAD_PATH)
        os.makedirs(f"{UPLOAD_PATH}/cloth")
        os.makedirs(f"{UPLOAD_PATH}/cloth-mask")
        os.makedirs(f"{UPLOAD_PATH}/image")
        os.makedirs(f"{UPLOAD_PATH}/image-mask")
        os.makedirs(f"{UPLOAD_PATH}/image-parse-new")
        os.makedirs(f"{UPLOAD_PATH}/warp-cloth")
        os.makedirs(f"{UPLOAD_PATH}/warp-mask")
        os.makedirs(f"{UPLOAD_PATH}/pose")
        os.makedirs(f"{UPLOAD_PATH}/result")
        with open("data/test_pairs.txt","w") as f:
            f.write("human.jpg cloth.jpg")

    app.run(host="0.0.0.0", port=PORT)