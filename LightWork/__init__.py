from flask import Flask
from LightWork.helper import exerciseData


app = Flask(__name__)
data = exerciseData()

from LightWork import routes


