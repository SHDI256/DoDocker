import os
import threading

from flask import *
from pyngrok import ngrok

from data.config import NGROK_AUTHTOKEN


app = Flask(__name__, static_url_path='')
port = 5000

os.environ['FLASK_ENV'] = 'development'
ngrok.set_auth_token(NGROK_AUTHTOKEN)
public_url = ngrok.connect(port).public_url

print(public_url)

app.config['BASE_URL'] = public_url


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/process_data/', methods=['POST'])
def get_output_file():
    try:
        return send_file(f'containers/{request.form["text"]}.tar', as_attachment=True)
    except Exception:
        return render_template('index.html')


threading.Thread(target=app.run, kwargs={'use_reloader': False}).start()