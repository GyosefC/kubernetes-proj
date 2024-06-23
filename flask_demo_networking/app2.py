from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, this is a cooler Flask demo application!'


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        return render_template('greet.html', name=name, color=color)
    return render_template('greet_form.html')


@app.route('/about')
def about():
    return 'This is a demo Flask application created by Alexey.'


@app.route('/atech-devops')
def atech_devops():
    return render_template('atech_devops.html')


if __name__ == '__main__':
    app.run(debug=True)
