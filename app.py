from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stargazing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CelestialObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    magnitude = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<CelestialObject {self.name}>'

@app.route('/')
def home():
    return "Welcome to the Stargazing App!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)
