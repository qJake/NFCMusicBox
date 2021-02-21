from flask import Flask, render_template, request
import state

app = Flask(__name__)

def init():
    print('Initializing web interface...')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
    print('Ready!')

@app.route('/')
def index():
    vm = {
        'nfc_status': state.get_nfc_status()
    }
    return render_template('index.html', vm=vm)

@app.route('/settings')
def settings():
    
    return render_template('settings.html')