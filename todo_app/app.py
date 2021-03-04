from pprint import pprint
from flask import Flask, render_template, request, redirect
import requests
from todo_app.data.session_items import create_card, get_lists, get_cards, move_card, remove_card

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', lists=get_lists(),cards=get_cards())


@app.route('/',methods=['POST'])
def test():
    name=request.form.get("card_name")
    create_card(name,request.form['submit_button'])
    return redirect('/')


@app.route('/move/<card_id>/<list_id>',methods=['GET','POST'])
def move(card_id,list_id):
    move_card(card_id,list_id)
    return redirect('/')


@app.route('/remove/<card_id>',methods=['GET','POST'])
def remove(card_id):
    remove_card(card_id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
