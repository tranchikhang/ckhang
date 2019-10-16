from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def index():
    return render_template('about.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/resume')
def resume():
    return render_template('profile/index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('common/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)