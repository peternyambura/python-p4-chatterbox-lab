from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:message_id>', methods=['PATCH'])
def update_message(message_id):
    message = Message.query.get(message_id)
    data = request.get_json()
    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted successfully.'})

if __name__ == '__main__':
    app.run(port=5555)
    app.run(debug=True)



