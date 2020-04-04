from cms import *
import os
import fnmatch
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


posts_list = read_json_data()
posts_list['posts'].reverse()
page_limit = 10


@app.route('/')
def index():
    return render_template('about.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/project')
def project():
    return render_template('project.html')


@app.route('/blog')
@app.route('/blog/<page>')
def blog(page=1):
    start = 0
    if page != 1:
        start = page_limit*(page-1) - 1
    end = page_limit*page
    posts = posts_list['posts'][start:end]
    return render_template('blog.html', posts=posts)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/resume')
def resume():
    return render_template('profile/index.html')


@app.route('/post/<year>/<title>')
def post(year, title):
    cwd = os.path.dirname(os.path.abspath(__file__))
    template_folder = app.template_folder
    for file in os.listdir(os.path.join(cwd, template_folder, 'posts', year)):
        if fnmatch.fnmatch(file, '*' + title + '*'):
            return render_template('posts/' + year + '/' + file)
    return render_template('common/404.html'), 404


@app.errorhandler(404)
def page_not_found(error):
    return render_template('common/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
