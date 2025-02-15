from flask import render_template,request,Blueprint,flash,redirect,url_for
from flask_login import login_required,login_user,logout_user,current_user
from MyBlog import db
from MyBlog.models import User,BlogPost
from MyBlog.users.forms import UpdateUserForm,LoginForm,RegistrationForm
from MyBlog.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

# user registration, login and logout
@users.route('/register',methods=['GET','POST'])
def register():
    form  = RegistrationForm()
    if form.validate_on_submit():
        email  = form.email.data
        password = form.password.data
        username = form.username.data
        user = User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration')
        return redirect(url_for('users.login'))
    return render_template('register.html',form = form)

@users.route('/login',methods=['GET','POST'])
def login():
    form  = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()

        if user != None and user.check_password(password):
            login_user(user)
            next = request.args.get('next')
            if next == None or next == '/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html',form=form)    

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#user account update

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author = user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog_posts.html',blog_posts=posts,user=user)







