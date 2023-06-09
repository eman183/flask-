from flask import Flask
from flask import request,redirect,url_for,session
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from flask import render_template,request
from werkzeug.utils import secure_filename
app=Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db=SQLAlchemy(app)

class Post(db.Model):
     __tablename__="Post"
     id=db.Column(db.Integer,primary_key=True)
     title=db.Column(db.String)
     body=db.Column(db.Text)
     image=db.Column(db.String)
     data=db.Column(db.LargeBinary)


@app.route("/posts",endpoint="posts.get")
def get_all_posts():
      posts=Post.query.all()
      return render_template("posts/post.html",posts=posts)



# show post
@app.route("/post/<int:id>" ,endpoint="post.show")
def show_post(id):
     post=Post.query.get_or_404(id)
     return render_template("posts/show.html",post=post)

     
 
# delete post
@app.route("/post/<int:id>/delete", endpoint="post.delete")
def delete_post(id):
    post= Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('posts.get'))



#create post

@app.route("/post/create",endpoint="post.create" ,methods = ["GET", "POST"])
def create_post():
    if request.method=="POST":
        print(request.form)
        post_id= request.form["id"]
        post_title= request.form["title"]
        post_body = request.form["body"]
        file= request.files['file']
        post = Post(title=post_title,image=file.filename,body= post_body,id=post_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.get'))

    return render_template("posts/create.html")

@app.route("/post/<int:id>/update",endpoint="post.update" ,methods = ["GET", "POST"])
def update_post(id):
     post= Post.query.filter_by(id=id).first()
     if request.method=="POST":
     #    post= Post.query.get_or_404(id)
     #    Post.id= request.form["id"]

       if post:
        db.session.delete(post)
        db.session.commit()
        title= request.form["title"]
        body = request.form["body"]
        image = request.form["file"]

        post = Post(id=id,title= title,image=image,body=body)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.get'))

 
     return render_template("posts/update.html",post=post)

if __name__=='__main__':
     app.run(debug=True)
