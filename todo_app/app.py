from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items,add_item,get_item,save_item,remove_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template('index.html', items=get_items())


@app.route('/', methods=['POST'])
def addNewItem():
    add_item(request.form.get('addItem'))
    return redirect('/')


@app.route('/complete/<id>')
def complete(id):
    item = get_item(id)
    item['status'] = 'Completed'
    save_item(item)
    return redirect('/')


@app.route('/remove/<id>')
def remove(id):
    item = get_item(id)
    remove_item(item)
    return redirect('/')


if __name__ == '__main__':
    app.run()
