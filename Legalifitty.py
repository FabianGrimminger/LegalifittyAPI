from flask import *
import os
app = Flask(__name__)

import generate



path = os.path.dirname(os.path.abspath(__file__))
@app.route('/qrcode/<uuid>', methods = ['GET'])
def download_qrcode(uuid):
    logo = os.path.join(path, 'marker-borderless.svg')
    png = generate.createQR(uuid, logo)

    return Response(png, mimetype='image/png')

@app.route('/graffiti', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(path, f.filename))
        return 'SUCCESS'

@app.route('/graffiti/<uuid>', methods = ['GET'])
def download_graffity(uuid):
    for file in os.listdir(os.path.dirname(__file__)):
        splits = file.split('.')
        if len(splits)==2:
            filename = splits[0]
            extension = splits[1]
            if filename == uuid and extension == 'png':
                response = send_from_directory(directory=path, filename=file)
                return response

    return "ERROR"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)