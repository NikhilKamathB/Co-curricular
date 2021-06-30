from setuptools import setup
from setuptools import find_packages


REQUIRED_PACKAGES = [
    "numpy==1.21.0",
    "matplotlib==3.4.2",
    "opencv-python==4.5.2.54",
    "torch==1.9.0",
    "torchvision==0.10.0",
    "easydict==1.9",
    "pillow==8.2.0",
    "python-dotenv==0.18.0",
    "google-cloud-storage==1.39.0",
    "google-cloud-aiplatform==1.1.1"
]

setup(
    name='trainer',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(include=['trainer','trainer.*']),
    include_package_data=True,
    description='Flower classification application.'
)