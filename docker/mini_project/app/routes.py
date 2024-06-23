from flask import render_template, request, redirect, url_for
from docker.mini_project.app import app

from docker.mini_project.app.models import get_users, save_user


@app.route('/')
def index():
    users = get_users()
    return render_template('index.html', users=users)


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        save_user(username, email)
        return redirect(url_for('index'))
    return render_template('form.html')


@app.route('/test')
def test():
    return 'Test route is working!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
