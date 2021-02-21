from flask import Flask, render_template, request

app = Flask(__name__)

def init():
    print('Initializing web interface...')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
    print('Ready!')

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/settings')
def settings():
    
    return render_template('settings.html')