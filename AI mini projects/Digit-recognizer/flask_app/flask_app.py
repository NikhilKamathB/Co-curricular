# run-> export PYTHONPATH=.
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from config import config
from net import LeNet5
from flask import Flask, request, Response


app = Flask(__name__)

def load_model():
    global model
    model = LeNet5().to("cpu")
    checkpoint = torch.load(f"{config.save_path}")
    model.load_state_dict(checkpoint['model_state_dict'])

@app.route('/')
def welcome():
    return f'''
    <h1>Welcome.</h1><br>
    <h4>The available endpoints are:</h4><br>
    *  {request.base_url}digit-recognizer/
    '''

@app.route('/digit-recognizer/', methods = ['POST'])
def digit_recognizer():
    if request.files.get('image', None) is not None:
        file_bytes = request.files["image"]
        image = Image.open(file_bytes).convert('1')
        image_resized = image.resize((32, 32))
        transformation_1 = transforms.ToTensor()
        image_processed = transformation_1(image_resized)
        image_tensor =  image_processed.unsqueeze(1)
        output = model(image_tensor)
        output_numpy = output.detach().numpy()
        pred_val = np.argmax(output_numpy)
        return Response(
            f'''{{
                "Predicted number":"{str(pred_val)}"
            }}''',
            status=200
        )
    else:
        return Response(
            '''{
                "Error":"Invalid input"
            }''',
            status=200
        )


if __name__=="__main__":
    load_model()
    app.run(host ='0.0.0.0', port = 8008, debug = True)