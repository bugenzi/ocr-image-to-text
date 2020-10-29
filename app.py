import os
from flask import Flask, render_template, request
import index

# Folder for storing images
FILE_UPLOAD = "./uploads"
# Specific file type
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

app = Flask(__name__)
print(Flask(__name__))


# Checking for the extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# print(index.ocr_core('./ReceiptSwiss.jpg'))
# route and function that handles the main page

@app.route("/")
def home_page():
    return render_template('./index.html')


# Route for handling and uploading pages
@app.route('/uploads', methods=['POST', "GET"])
def upload_page():
    if request.method == "POST":
        # Check if there is a file in request
        if 'file' not in request.files:
            return render_template('upload.html', msg="No file selected")
        file = request.files['file']
        # If filename is empty
        if file.filename == '':
            return render_template('upload.html', msg="No file selected")
        if file and allowed_file(file.filename):
            # call index module
            text = index.ocr_core(file)
            # extract text and save it in html
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=text,
                                   img_src=FILE_UPLOAD+file.filename
                                   )
    elif request.method == "GET":
        return render_template('upload.html')


if __name__ == "__main__":
    app.run()
