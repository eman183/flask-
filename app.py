from flask import Flask
from flask import request,redirect,url_for
from sqlalchemy import Column, ForeignKey, Integer, Unicode
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from flask import render_template, render_template_string, request
# from sqlalchemy_imageattach.entity import Image, image_attachment
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db=SQLAlchemy(app)

class Post(db.Model):
     __tablename__="Post"
     id=db.Column(db.Integer,primary_key=True)
     title=db.Column(db.String)
     body=db.Column(db.Text)


#      image = image_attachment('PostPicture')
    
# class PostPicture(db.Model):
#     """User picture model."""

#     user_id = db.Column(db.Integer, db.ForeignKey('Post.id'), primary_key=True)
#     user = db.relationship('Post')
#     __tablename__ = 'Post_picture'   
    #  image=
# get all posts
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
def delete_product(id):
    post= Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('posts.get'))



#create post

@app.route("/post/create",endpoint="post.create" ,methods = ["GET", "POST"])
def create_product():
    if request.method=="POST":
        print(request.form)
        post_id= request.form["id"]
        post_title= request.form["title"]
        post_body = request.form["body"]
        post = Post(title=post_title, body= post_body,id=post_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.get'))

    ## request method GET ?
    return render_template("posts/create.html")

@app.route("/post/<int:id>/update",endpoint="post.update" ,methods = ["GET", "POST"])
def update_product(id):
    if request.method=="POST":
        post= Post.query.get_or_404(id)
        print(post)
     #    Post.id= request.form["id"]
        Post.title= request.form["title"]
        Post.body = request.form["body"]
        post = Post( title= Post.title,body=Post.body)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.get'))

    ## request method GET ?
    return render_template("posts/update.html",)

if __name__=='__main__':
     app.run(debug=True)
