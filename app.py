import os
from flask import Flask, render_template, url_for, send_file, request, redirect
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    images = ImageTable.query.all()

    return render_template('index.html', images=images)


@app.route('/retrieve/<id>')
def retrieve(id):
    file = ImageTable.query.filter_by(id=id).first()

    return send_file(BytesIO(file.file), attachment_filename=f'{file.name}', mimetype='image/jpg')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if 'uploaded_image' not in request.files:
            return render_template('index.html')

        file = request.files['uploaded_image']
        name = file.filename

        if request.form['name']:
            name = request.form['name']
        description = request.form['description']

        try:
            db.session.add(ImageTable(name, description, file.read()))
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "There was an error uploading your image"


@app.route('/delete/<id>')
def delete(id):

    file = ImageTable.query.filter_by(id=id).first()

    try:
       db.session.delete(file)
       db.session.commit()
       return redirect(url_for('index'))
    except:
       return "There was a problem deleting that image"
    

# database schema
class ImageTable(db.Model):
    __tablename = 'USER_IMAGES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    file = db.Column(db.LargeBinary)

    def __init__(self, name, description, file):
        self.name = name
        self.description = description
        self.file = file

    def __repr__(self):
        return 'File Name: {self.name} - File Description: {self.description} \n'

db.drop_all()
db.create_all()

image_1 = open('static/media/my_shopify_visit.jpg', 'rb').read()
image_2 = open('static/media/toronto_skyline.gif', 'rb').read()
image_3 = open('static/media/shopify_logo.jpg', 'rb').read()
image_4 = open('static/media/frenzy_app.jpg', 'rb').read()
image_5 = open('static/media/shopify_waterloo.jpg', 'rb').read()

upload_1 = ImageTable('my_shopify_visit.jpg', "A pic I took on my visit to Shopify's Toronto Office", image_1)
upload_2 = ImageTable('toronto_skyline.gif', "A gif of Toronto's night skyline", image_2)
upload_3 = ImageTable('shopify_logo.jpg', "Shopify Logo", image_3)
upload_4 = ImageTable('frenzy_app.jpg', "A pic of Shopify's experimental Frenzy app", image_4)
upload_5 = ImageTable('shopify_waterloo.jpg', "Shopify's beautiful Waterloo distillery office", image_5)

db.session.add_all([upload_1, upload_2, upload_3, upload_4, upload_5])
db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)