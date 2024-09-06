from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

App = Flask(__name__)
client = MongoClient('localhost', 27017)


@App.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        timeline = request.form['timeline']
        additional = request.form.getlist('additional')
        deadline = request.form.get('deadline', None)
        todos.insert_one({
            'content': content,
            'degree': degree,
            'timeline': timeline,
            'additional': additional if additional else None,
            'deadline': deadline})
        return redirect(url_for('index'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@App.post("/<id>/delete/")
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))


@App.template_filter('join_with_pipe')
def join_with_pipe(value):
    if isinstance(value, list):
        return ' | '.join(value)
    return value

@App.template_filter('format_datetime')
def format_datetime(value):
    if value:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%d %B %Y, %H:%M')


db = client.task_tracker_database
todos = db.todo_list

if __name__ == "__main__":
    App.run(debug=True)
