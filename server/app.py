from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():

    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        messages_serialized = [message.to_dict() for message in messages]

        response = make_response(
            messages_serialized,
            200
        )
        return response
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data['body'],
            username = data['username']
        )
        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            data,
            201
        )
        return response

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter(Message.id == id).first()

    if request.method == 'GET':
        pass


    elif request.method == 'PATCH':
        data =request.get_json()
        print(data['body'])
        message.body = data['body']

        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        response =make_response(
            message_dict,
            200
        )
        return response


    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful":True,
            "message":"Review deleted."
        }

        response = make_response(
            response_body,
            200
        )

        return response
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
