from flask import Flask, jsonify, request # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore

app = Flask(__name__)


# Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Apothecary Diaries.db'

db = SQLAlchemy(app)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    va_en = db.Column(db.String(100), nullable=False)
    va_jp = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float, nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'va_en': self.va_en,
            'va_jp': self.va_jp,
            'height': self.height,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color,
            'gender': self.gender
        }
    

with app.app_context():
    db.create_all()


# Route
@app.route('/')
def home(): 
    return jsonify({'message': 'Welcome to the Apothecary Diaries API :3 access /characters to see all characters'})

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.to_dict() for character in characters])

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get_or_404(id)
    if character:
        return jsonify(character.to_dict())
    else:
        return jsonify({'message': 'Character not found'}), 404
    
# Post req

@app.route('/characters', methods=['POST'])
def add_character():
    data = request.get_json()
    new_character = Character(
        name=data['name'],
        age=data['age'],
        va_en=data['va_en'],
        va_jp=data['va_jp'],
        height=data['height'],
        hair_color=data['hair_color'],
        eye_color=data['eye_color'],
        gender=data['gender']
    )


    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.to_dict()), 201


@app.route('/characters/<int:id>', methods=['PUT'])
def update_character(id):
    character = Character.query.get_or_404(id)
    data = request.get_json()
    character.name = data['name']
    character.age = data['age']
    character.va_en = data['va_en']
    character.va_jp = data['va_jp']
    character.height = data['height']
    character.hair_color = data['hair_color']
    character.eye_color = data['eye_color']
    character.gender = data['gender']
    db.session.commit()
    return jsonify(character.to_dict())

@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'})

if __name__ == '__main__':
    app.run(debug=True)