from flask import render_template  
from flask import Flask, request, jsonify
from flask_cors import CORS  
import cv2
import numpy as np
import torch

app = Flask(__name__)
CORS(app)  # Allowing CORS for all routes

# Load YOLOv5 PyTorch model
model = torch.hub.load('WongKinYiu/yolov7', 'yolov7', pretrained=True)  # Change 'yolov7' to your specific model

# Label map to convert label numbers to text
# The label map for YOLOv5's pre-trained model on the COCO dataset contains 80 classes.
# Here is a dictionary that maps the label indices to their respective names.

label_map = {
    "0": "person",
    "1": "bicycle",
    "2": "car",
    "3": "motorcycle",
    "4": "airplane",
    "5": "bus",
    "6": "train",
    "7": "truck",
    "8": "boat",
    "9": "traffic light",
    "10": "fire hydrant",
    "11": "stop sign",
    "12": "parking meter",
    "13": "bench",
    "14": "bird",
    "15": "cat",
    "16": "dog",
    "17": "horse",
    "18": "sheep",
    "19": "cow",
    "20": "elephant",
    "21": "bear",
    "22": "zebra",
    "23": "giraffe",
    "24": "backpack",
    "25": "umbrella",
    "26": "handbag",
    "27": "tie",
    "28": "suitcase",
    "29": "frisbee",
    "30": "skis",
    "31": "snowboard",
    "32": "sports ball",
    "33": "kite",
    "34": "baseball bat",
    "35": "baseball glove",
    "36": "skateboard",
    "37": "surfboard",
    "38": "tennis racket",
    "39": "bottle",
    "40": "wine glass",
    "41": "cup",
    "42": "fork",
    "43": "knife",
    "44": "spoon",
    "45": "bowl",
    "46": "banana",
    "47": "apple",
    "48": "sandwich",
    "49": "orange",
    "50": "broccoli",
    "51": "carrot",
    "52": "hot dog",
    "53": "pizza",
    "54": "donut",
    "55": "cake",
    "56": "chair",
    "57": "couch",
    "58": "potted plant",
    "59": "bed",
    "60": "dining table",
    "61": "toilet",
    "62": "TV",
    "63": "laptop",
    "64": "mouse",
    "65": "remote",
    "66": "keyboard",
    "67": "cell phone",
    "68": "microwave",
    "69": "oven",
    "70": "toaster",
    "71": "sink",
    "72": "refrigerator",
    "73": "book",
    "74": "clock",
    "75": "vase",
    "76": "scissors",
    "77": "teddy bear",
    "78": "hair drier",
    "79": "toothbrush",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file:
        # Convert to an OpenCV image
        nparr = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perform object detection using YOLOv7 PyTorch model
        results = model(frame)
        detected_objects = []
        for label, confidence, box in zip(results.xyxy[0][:, -1], results.xyxy[0][:, -2], results.xyxy[0][:, :-2]):
            detected_objects.append({
                "label": label_map.get(str(int(label)), "Unknown"),
                "confidence": float(confidence),
                "box": [float(x) for x in box]
            })

        return jsonify({'result': detected_objects})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
