from setuptools import setup
from setuptools import find_packages


REQUIRED_PACKAGES = []
setup(
    name='setup',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Flower classification application.'
)