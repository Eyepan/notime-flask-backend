from flask import request
from db import app, db, User, Notebook, Page
from uuid import uuid4
from flask_cors import cross_origin
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def index():
    return "hi there"


@app.route("/api/users", methods=['GET'])
@cross_origin()
def get_all_users():
    users = User.query.all()
    return {'users': [{'id': user.id, 'name': user.name} for user in users]}


@app.route("/api/users/<id>", methods=['GET'])
@cross_origin()
def get_user(id):
    user = db.session.get(User, id)
    if user:
        return {'user': {
            'id': user.id,
            'name': user.name,
            'password': user.password
        }}
    else:
        return {'error': "User not found"}, 404


@app.route("/api/users", methods=['POST'])
@cross_origin()
def add_user():
    name = request.json['name']
    password = request.json['password']
    user = User(id=uuid4(), name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'password': user.password}, 201


@app.route("/api/users/signin", methods=['POST'])
@cross_origin()
def signin():
    name = request.json['name']
    password = request.json['password']
    user = User.query.filter_by(name=name, password=password).first()
    if user:
        return {'user': {
            'id': user.id,
            'name': user.name,
            'password': user.password
        }}
    else:
        return {'error': "User not found"}, 404


@app.route("/api/users/<id>", methods=['DELETE'])
@cross_origin()
def remove_user(id):
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    else:
        return {"error": "User not found"}, 404


@app.route('/api/users/<user_id>/notebooks', methods=['GET'])
@cross_origin()
def get_user_notebooks(user_id):
    notebooks = Notebook.query.filter_by(user_id=user_id).all()
    return {'notebooks': [{'id': notebook.id, 'title': notebook.title} for notebook in notebooks]}


@app.route('/api/users/<user_id>/notebooks', methods=['POST'])
@cross_origin()
def add_user_notebook(user_id):
    title = request.json['title']
    db.session.add(Notebook(id=uuid4(), user_id=user_id, title=title))
    db.session.commit()
    return {"message": "Notebook added successfully"}, 201


@app.route('/api/users/<user_id>/notebooks/<notebook_id>', methods=['DELETE'])
@cross_origin()
def delete_notebook(user_id, notebook_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if notebook:
        db.session.delete(notebook)
        db.session.commit()
        return {'message': 'Notebook deleted successfully.'}, 200
    else:
        return {'error': 'Notebook not found or user is not authorized.'}, 404


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages', methods=['GET'])
@cross_origin()
def get_notebook_pages(user_id, notebook_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {"error": "Notebook not found or user is not authorized"}, 404
    pages = Page.query.filter_by(notebook_id=notebook_id).all()
    return {'pages': [{'id': page.id, 'title': page.title, 'content': page.content} for page in pages]}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages', methods=['POST'])
@cross_origin()
def add_notebook_pages(user_id, notebook_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {"error": "Notebook not found or user is not authorized"}, 404
    title = request.json['title']
    content = request.json['content']
    db.session.add(Page(id=uuid4(), notebook_id=notebook_id,
                   title=title, content=content))
    db.session.commit()
    return {"message": "Page added successfully"}, 201


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['GET'])
@cross_origin()
def get_current_page(user_id, notebook_id, page_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if not page:
        return {'error': 'Page not found or user is not authorized.'}, 404
    return {'page': {'id': page.id, 'title': page.title, 'content': page.content}}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['PUT'])
@cross_origin()
def update_page(user_id, notebook_id, page_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if not page:
        return {'error': 'Page not found or user is not authorized.'}, 404

    page.title = request.json['title']
    page.content = request.json['content']
    db.session.commit()

    return {"message": "Page updated successfully", 'page': {'id': page.id, 'title': page.title, 'content': page.content}}


@app.route('/api/users/<user_id>/notebooks/<notebook_id>/pages/<page_id>', methods=['DELETE'])
@cross_origin()
def delete_page(user_id, notebook_id, page_id):
    notebook = Notebook.query.filter_by(
        id=notebook_id, user_id=user_id).first()
    if not notebook:
        return {'error': 'Notebook not found or user is not authorized.'}, 404
    page = Page.query.filter_by(id=page_id, notebook_id=notebook_id).first()
    if page:
        db.session.delete(page)
        db.session.commit()
        return {'message': 'Page deleted successfully.'}, 200
    else:
        return {'error': 'Page not found or user is not authorized.'}, 404


if __name__ == '__main__':
    app.run()
