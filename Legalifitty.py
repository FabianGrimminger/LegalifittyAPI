from flask import *
import os
app = Flask(__name__)

import generate

@app.route('/qrcode/<uuid>', methods = ['GET'])
def download_qrcode(uuid):
    logo = os.path.join(os.path.dirname(__file__), 'marker-borderless.svg')
    png = generate.createQR(uuid, logo)

    return Response(png, mimetype='image/png')

@app.route('/graffiti', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(os.path.dirname(__file__), f.filename))
        return 'SUCCESS'

@app.route('/graffiti/<uuid>', methods = ['GET'])
def download_graffity(uuid):
    result = ""
    for file in os.listdir(os.path.dirname(__file__)):
        filename = file.split('.')[0]
        if filename == uuid:
            response = send_from_directory(directory=os.path.dirname(__file__), filename=file)
            return response

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
