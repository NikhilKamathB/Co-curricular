# Eyepop AI - Assessment 🧿

<p align="center">
  <img src="https://dashboard.eyepop.ai/_next/image?url=%2Fstatic%2Flogo-horizontal-800.png&w=2048&q=75" alt="image-description",>
</p>

This is an EyePop AI Assessment. The main objective is to demonstrate software engineering practices and usage of eyepop SDK. Towards the end, we will also also be packaginf our solution into a python package which can be used by others by simply installing it from pip.

## Objective 🎯
Create a CLI tool that can perform object detection on images and videos constrainted by the category associated with our EyePop AI API key.

## Prerequisites | What do I need before I start? 📜
* An EyePop AI account and API key configured - [refer this document](https://docs.eyepop.ai/developer-documentation/api-key).
* If you are planning to build the package from scratch, you will be needing [`Poetry` ](https://python-poetry.org/docs/)installed on your system.


## Folder Structure 🧱
```
EyePop AI Repo.

|- data (any data, structured/unstructured, goes here)
    |- images (holds all images)
    |- videos (holds all videos)
|- eyepopai (our package)
    |- components (holds all components specefic to UI)
    |- core (holds all core functionalites)
    |- tcss (contains styles for our UI)
    |- main.py (entry point of our package)
|- test.py (contains unit tests for our package)
|- pyproject.toml (defines dependencies)
```

## How do I run the application? 🏃🏻‍♂️
That's very simple. You can do it in two ways.

* Installing the package from pip.
    * Run `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ eyepopai` to install the package. This is currently in Test PyPI.
    * Set the environment variables - refer [Environment Variables 🤫](#environment-variables-🤫) and run `source .env` to set the environment variables.
    * Run `eyepopai` and BAM! you are done.

* Cloning the repository.
    * Clone this repository and `cd` into it.
    * Set the environment variables - refer [Environment Variables 🤫](#environment-variables-🤫) and run `source .env` to set the environment variables.
    * Install dependencies.
        * If you are using Poetry, run `poetry install` to install the dependencies.
        * Alternatively, you can run `pip install .` to install the package.
    * `cd` into the `eyepopai` folder (package) and run `python -m main` to start the application.


## How do I build the package? 🛠️
For this, you will be needing [`Poetry` ](https://python-poetry.org/docs/). Once you have installed poetry, run the following commands in your terminal.

* Clone the repository and `cd` into it.
* Run `poetry install` to install the dependencies.
* Run `poetry build` to build the package. This will create a `dist` folder containing `.whl` file, which can then be used to install using pip.

## Environment Variables 🤫
```
export EYEPOP_POP_ID=<EYEPOP_POP_ID>
export EYEPOP_SECRET_KEY=<EYEPOP_SECRET_KEY>
```