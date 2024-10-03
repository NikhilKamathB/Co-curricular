import os
import base64
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# LLM
_LLM = ChatOpenAI(
    model="gpt-4o",  # Updated model name
)

result = {}
images = []

# get all images in the current directory
for file in os.listdir():
    if file.endswith(".jpg") or file.endswith(".png"):
        images.append(file)

for image in images:
    print(f'Processing {image}')
    messages = [
        {"role": "system", "content": "You are a helpful assistant. What is it that you can see in the image? You can only pick one item form the following list: [Umbrella, Glass, Stick, None]. If you can't see anything in the image, respond with None."},
        {"role": "user", "content": [
            {"type": "text", "text": "What is it that you can see in the image?"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{encode_image(f'./{image}')}"}
            }
        ]}
    ]
    llm_result = _LLM.invoke(messages)
    result['.'.join(image.split('.')[:-1])] = llm_result.content

print(result)

# Update the .obj file with the new annotations
with open('Cocktail.obj', 'r') as file:
    obj_data = file.read()

with open('Cocktail_annotated.obj', 'w') as file:
    for line in obj_data.split('\n'):
        if line.startswith('o '):
            obj_name = line.split(' ')[1]
            if obj_name in result:
                line = f'o {result[obj_name]}'
        file.write(line + '\n')