from flask import *
import os
import base64

import generate

app = Flask(__name__)
app.secret_key = 'my unobvious secret key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'img')

@app.route('/qrcode/<uuid>', methods = ['GET'])
def download_qrcode(uuid):
    logo = os.path.join(os.path.dirname(__file__), 'marker-borderless.svg')
    png = generate.createQR(uuid, logo)

    return Response(png, mimetype='image/png')

@app.route('/graffiti', methods = ['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.form:
        print 'No file part'
        flash('No file part')
        return redirect(request.url)
    if 'name' not in request.form:
        print 'No filename part'
        flash('No filename part')
        return redirect(request.url)
    file_base64 = request.form['file']
    filename = request.form['name']
    file = base64.b64decode(file_base64)

    target = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    f = open(target, 'w')
    f.write(file)
    f.close();

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
