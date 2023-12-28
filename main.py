# server.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    with app.app_context():
        messages = Message.query.all()
    return render_template('index.html', messages=messages)

@socketio.on('message')
def handle_message(data):
    with app.app_context():
        new_message = Message(content=data)
        db.session.add(new_message)
        db.session.commit()
    socketio.emit('message', data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
