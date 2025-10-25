from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Card {self.id}>'


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/informacion")
def about():
    return render_template("informacion.html")

@app.route("/enviar", methods=['GET', 'POST'])
def enviar():
    if request.method == 'POST':
        text = request.form['text']
        card = Card(text=text)
        db.session.add(card)
        db.session.commit()
        return redirect('/chat')
    else:
        return render_template("Enviar.html")

@app.route("/chat")
def chat():
    cards = Card.query.order_by(Card.id).all()
    
    return render_template("Chat.html", cards=cards)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)