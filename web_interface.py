import state
import utils
from flask import Flask, render_template, request, redirect, cli
from werkzeug.utils import secure_filename
from nfc_reader import start_nfc_thread

DEVENV = False
try:
    # pylint: disable=import-error
    import RPi.GPIO as GPIO
except:
    DEVENV = True

app = Flask(__name__)
cli.show_server_banner = lambda *_: None

def init():
    print('Initializing web interface...')
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    print('Ready!')

def run_wait():
    if DEVENV:
        app.run(host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', port=80)

@app.route('/')
def index():
    player = state.get_player()
    vm = {
        'nfc_status': state.get_nfc_status(),
        'song_name': state.get_song_name(),
        'is_playing': player.is_state(player.STATE_PLAYING),
        'is_paused': player.is_state(player.STATE_PAUSED),
        'is_stopped': player.is_state(player.STATE_STOPPED)
    }
    return render_template('index.html', vm=vm)

# ACTIONS

@app.route('/actions/initnfc')
def action_initnfc():
    if not state.get_nfc_status():
        start_nfc_thread()
    return redirect('/')

@app.route('/actions/reloadsongs')
def action_reloadsongs():
    player = state.get_player()
    player.reload_songs()
    return redirect('/tags')

@app.route('/actions/stop')
def action_stop():
    player = state.get_player()
    player.stop()
    return redirect('/')

@app.route('/actions/play')
def action_play():
    player = state.get_player()
    player.play()
    return redirect('/')
   
@app.route('/actions/pause')
def action_pause():
    player = state.get_player()
    player.pause()
    return redirect('/')

@app.route('/actions/vol')
def action_vol():
    try:
        vol = float(request.args.get('vol'))
        player = state.get_player()
        player.set_vol(vol)
    except:
        pass
    return redirect('/')
    
# TAGS

@app.route('/tags')
def tags():
    storage = state.get_storage()
    tags = storage.get_tags()
    vm = {
        'tags': tags
    }
    return render_template('tags.html', vm=vm)

@app.route('/tags/add', methods=['GET'])
def tags_add():
    return render_template('tags_add.html', vm={
        'error': request.args.get('error'),
        'last_tag': state.get_last_tag()
    })

@app.route('/tags/add', methods=['POST'])
def tags_add_post():
    storage = state.get_storage()

    songfile = request.files['song']
    songname = songfile.filename.replace(' ', '_')
    if songfile is not None \
       and request.form['uid'] is not None \
       and len(request.form['uid']) > 0 \
       and songname.lower().endswith('.mp3'):
        storage.add_song(songfile, secure_filename(songname))
    else:
        return redirect('/tags/add?error=1')

    newtag = {
        'uid': request.form['uid'],
        'name': songname
    }
    try:
        storage.add_tag(newtag)
    except:
        pass
    return redirect('/tags')

@app.route('/actions/tags/play')
def tags_play():
    storage = state.get_storage()
    tags = storage.get_tags()
    uid = request.args.get('uid')
    tag = utils.select_tag(tags, uid)
    if tag is not None:
        player = state.get_player()
        player.load(name=storage.to_full_path(tag['name']))
        player.play()
    return redirect('/tags')

@app.route('/actions/tags/delete')
def tag_delete():
    uid = request.args.get('uid')
    try:
        storage = state.get_storage()
        storage.remove_tag(uid)
    except Exception as e:
        print(e)
    return redirect('/tags')