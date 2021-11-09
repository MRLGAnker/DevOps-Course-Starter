import os
import requests
from flask import Flask, render_template, request, redirect
from datetime import datetime
from todo_app.data.session_items import check_default_lists, create_card, get_lists, get_cards, move_card, remove_card, ViewModel
from todo_app.user import User
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    github_client =  WebApplicationClient(os.environ.get('OAUTH_CLIENT_ID'))
    github_redirect = github_client.prepare_request_uri("https://github.com/login/oauth/authorize")

    return redirect(github_redirect)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('OAUTH_CLIENT_SECRET')
    login_manager.init_app(app)

    check_default_lists()

    @app.route('/')
    @login_required
    def index():
        item_view_model = ViewModel(get_cards(),get_lists())
        return render_template('index.html', view_model=item_view_model)


    @app.route('/',methods=['POST'])
    @login_required
    def test():
        create_card(request.form.get("card_desc"),request.form.get('submit_button'),request.form.get('card_name'),request.form.get('card_due'))
        return redirect('/')


    @app.route('/move/<card_id>/<list_id>',methods=['GET','POST'])
    @login_required
    def move(card_id,list_id):
        move_card(card_id,list_id)
        return redirect('/')


    @app.route('/remove/<card_id>',methods=['GET','POST'])
    @login_required
    def remove(card_id):
        remove_card(card_id)
        return redirect('/')

    @app.route('/login/callback', methods=['GET', 'POST'])
    def callback():
        github_code = request.args.get('code')
        client =  WebApplicationClient(os.environ.get('OAUTH_CLIENT_ID'))
        token = client.prepare_token_request('https://github.com/login/oauth/access_token',code=github_code)
        access = requests.post(token[0],headers=token[1],data=token[2],auth=(os.environ.get('OAUTH_CLIENT_ID'),os.environ.get('OAUTH_CLIENT_SECRET')))
        client.parse_request_body_response(access.text)
        user = client.add_token("https://api.github.com/user")
        user_id = requests.get(user[0], headers=user[1]).json()['login']
        
        login_user(User(user_id))

        return redirect('/')

    return app

if __name__ == '__main__':
    create_app().run()
