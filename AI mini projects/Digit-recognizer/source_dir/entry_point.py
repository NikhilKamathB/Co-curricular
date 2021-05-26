import os
import torch
import json
import numpy as np
from PIL import Image
from torchvision import transforms
from azureml.contrib.services.aml_request import rawhttp
from azureml.contrib.services.aml_response import AMLResponse

def init():
    global model
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'model', 'data', 'model.pth')
    model = torch.load(model_path)
    model.eval()

@rawhttp
def run(request):
    if request.method == 'POST':
        file_bytes = request.files["image"]
        image = Image.open(file_bytes).convert('1')
        image_resized = image.resize((32, 32))
        transformation_1 = transforms.ToTensor()
        image_processed = transformation_1(image_resized)
        image_tensor =  image_processed.unsqueeze(1)
        output = model(image_tensor)
        output_numpy = output.detach().numpy()
        pred_val = np.argmax(output_numpy)
        return AMLResponse(json.dumps([pred_val.item(), output.size(), str(type(output))]), 200)
    else:
        return AMLResponse("Bad request", 500)
