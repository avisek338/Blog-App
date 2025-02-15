from flask import Blueprint,url_for,redirect,render_template,abort,flash,request
from flask_login import login_required,current_user
from MyBlog.models import BlogPost
from MyBlog.blog_posts.forms import BlogPostForm
from MyBlog import db

blog_posts = Blueprint('blog_posts',__name__)


@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form  = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        user_id = current_user.id
        blog_post = BlogPost(title=title,text = text,user_id=user_id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html',form=form)


@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.filter_by(id=blog_post_id).first_or_404()
    return render_template('blog_post.html',title = blog_post.title,date = blog_post.date,post = blog_post)

  
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.filter_by(id = blog_post_id).first_or_404()
    if current_user.id !=  blog_post.author.id:
        abort(403)

    form  = BlogPostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data

        blog_post.title = title
        blog_post.text = text

        db.session.commit()
        flash('Blog Post updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text

    return render_template('create_post.html',form=form,title='updating')
          

@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.filter_by(id = blog_post_id).first_or_404()
    if current_user.id !=  blog_post.author.id:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()

    flash('Blog Post Deleted')
    return redirect(url_for('core.index'))




    

