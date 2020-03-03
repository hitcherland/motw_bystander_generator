import json

from flask import Flask, render_template
from character_generator import CharacterGenerator

app = Flask(__name__)
generator = CharacterGenerator()

@app.route('/')
def index():
    character = generator.build_character()
    return render_template("index.html", **character)
