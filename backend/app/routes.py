from flask import Blueprint, jsonify, request
from .models import Item
from . import db

api = Blueprint('api', __name__)

@api.route('/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'POST':
        data = request.json
        new_item = Item(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created'}), 201

    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])
