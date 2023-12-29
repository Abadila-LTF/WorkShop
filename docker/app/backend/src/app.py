from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)




db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_port = os.environ["DB_PORT"]



app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description


@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = []
    for item in items:
        item_data = {}
        item_data['id'] = item.id
        item_data['name'] = item.name
        item_data['description'] = item.description
        item_list.append(item_data)
    return jsonify({'items': item_list})


@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)

