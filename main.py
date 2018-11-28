from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:b@b272AzB@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'itsasecret'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET']) # direct to the newpost page
def newposts():
    return redirect('/newpost')


@app.route('/newpost', methods=['POST', 'GET'])
def add_post(): # adds the post to the database, redirects to the main blog page once added to database

    new_post = None
    title = ""
    body = ""
    title_error = ""
    post_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == "":
            title_error = "Please enter a title for your post"
            flash('Please enter a title for your post')
            
            return render_template('newpost.html', title=title, title_error=title_error, body=body, post_error=post_error)
        if len(title) > 120:
            title_error = "Blog title is limited to 120 characters"
            flash('Blog title is limited to 120 characters')
        if body == "":
            post_error = "Please enter your blog post here"
            flash('Please enter your blog post here')
            
            return render_template('newpost.html', title=title, title_error=title_error, body=body, post_error=post_error)

        if len(body) > 500:
            post_error = "Blog post is limited to 500 characters"
            flash('Blog post is limited to 500 characters')

        if title_error != "" and post_error != "":
            return render_template('newpost.html', title=title, title_error=title_error, body=body, post_error=post_error)
    
        if not title_error and not post_error:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            entry = new_post.id
            return render_template('displaypost.html', title=new_post.title, body=new_post.body)

    return render_template('newpost.html', title=title, title_error=title_error, body=body, post_error=post_error)

    if request.method == 'GET':
        return render_template('newpost.html', title=title, title_error=title_error, body=body, post_error=post_error)
   
# display all blog posts on the main page
@app.route('/blog', methods=['POST', 'GET'])
def index():

    id = request.args.get("id")
    entries = Blog.query.all()
    
    if not id:
        entries = Blog.query.order_by(Blog.id.asc()).all()
        return render_template('blog.html', entries=entries)

# displays the single post on a separate page
@app.route('/displaypost', methods=['GET'])
def displaypost():

    id = request.args.get("id")
    entry = Blog.query.filter_by(id=id).first()

    return render_template('displaypost.html', title=entry.title, body=entry.body)

if __name__=='__main__':
    app.run()