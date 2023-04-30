from flask import Blueprint, render_template, request, flash, jsonify, Flask, current_app
from os import mkdir, getcwd
from pathlib import Path
import website.module.analyzer as analyzer
from threading import Thread
import time
from flask_executor import Executor

views = Blueprint('views', __name__)
analyzer = analyzer.AudienceAnalyzer()
#app = Flask(__name__)



@views.route("/")
def home():
    id = 1313
    executor = Executor(current_app)
    #id = str(int(time.time_ns()/1000))
    try:
        #mkdir(f'{getcwd()}/website/static/data/{id}')
        mkdir(f'{getcwd()}/website/static/data/{id}/img_src')
        mkdir(f'{getcwd()}/website/static/data/{id}/img_final')
    except Exception as e:
        pass

    #analyzer.FullAnalysis(id)
    #Thread(target=analyzer.FullAnalysis(id), daemon=True, name='Analyzer').start()
    with current_app.app_context():
        executor.submit(analyzer.FullAnalysis, id)
    return f"Current process id: {id}"

@views.route('/task_result/<task_id>')
def task_result(id):
    pass