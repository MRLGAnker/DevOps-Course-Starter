from flask import Flask, render_template, request, redirect
from datetime import datetime
from todo_app.data.session_items import create_card, get_lists, get_cards, move_card, remove_card, ViewModel

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    def index():
        item_view_model = ViewModel(get_cards(),get_lists())
        return render_template('index.html', view_model=item_view_model)


    @app.route('/',methods=['POST'])
    def test():
        create_card(request.form.get("card_desc"),request.form.get('submit_button'),request.form.get('card_name'),request.form.get('card_due'))
        return redirect('/')


    @app.route('/move/<card_id>/<list_id>',methods=['GET','POST'])
    def move(card_id,list_id):
        move_card(card_id,list_id)
        return redirect('/')


    @app.route('/remove/<card_id>',methods=['GET','POST'])
    def remove(card_id):
        remove_card(card_id)
        return redirect('/')

    return app
        
if __name__ == '__main__':
    create_app().run()
