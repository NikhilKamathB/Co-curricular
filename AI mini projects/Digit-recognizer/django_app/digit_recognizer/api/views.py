import numpy as np
from PIL import Image
from torchvision import transforms
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def home(request):
    return Response({
        "Welcome message":  f"The available endpoints are: ->   {request.get_host()}/api/digit-recognizer/"
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def digit_recognizer(request):
    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            file_bytes = request.FILES["image"]
            image = Image.open(file_bytes).convert('1')
            image_resized = image.resize((32, 32))
            transformation_1 = transforms.ToTensor()
            image_processed = transformation_1(image_resized)
            image_tensor =  image_processed.unsqueeze(1)
            output = settings.MODEL(image_tensor)
            output_numpy = output.detach().numpy()
            pred_val = np.argmax(output_numpy)
            return Response({"Predicted number":f"{str(pred_val)}"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error":"Invalid input"}, status=status.HTTP_200_OK)
