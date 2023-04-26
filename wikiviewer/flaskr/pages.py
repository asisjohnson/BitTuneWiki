from flask import render_template, request, redirect, url_for, session
from flaskr.backend import Backend
from flaskr.backend import User
from werkzeug.utils import secure_filename
import base64
import io
import os

def make_endpoints(app):
    """Sets up routing"""
    backend = Backend()
    current_user = User(None, None)


    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        """Renders the main page of the wiki"""
        return render_template("main.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route("/pages") #Danny
    def pages():
        """Renders a specific page that the user selected from the available pages"""
        page_name_list = backend.get_all_page_names()
        return render_template("pages.html", name_lst=page_name_list)

    @app.route("/about")  #Enrique
    def about():
        """Sets up image rendering for the about page"""
        img1 = backend.get_image("asis.jpeg")
        img2 = backend.get_image("daniel.JPG")
        img3 = backend.get_image("enrique.jpg")
        img1 = img1.decode('UTF-8')
        img2 = img2.decode('UTF-8')
        img3 = img3.decode('UTF-8')
        return render_template("about.html", img1=img1, img2=img2, img3=img3)

    @app.route("/signup", methods=['GET', 'POST'])  #Asis
    def sign_up_page():
        """Allows user to sign up to access wikiviewer's functionalities"""
        msg = ''

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            user = request.form['username']
            password = request.form['password']

            if not backend.sign_up(user, password):
                msg = 'You already have an account, Click Login!'
            else:
                msg = 'Your sign up was successful, Click Login!'

        return render_template("signup.html", msg=msg)  #Asis

    @app.route("/login", methods=['GET', 'POST'])  #Asis
    def login_page():
        """Allows user to login once they have an account available."""
        msg = ''

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            user = request.form['username']
            password = request.form['password']

            current_user.username = user

            if backend.sign_in(user, password) is True:
                return render_template('logged_in.html', msg=msg, name=user)
            else:
                msg = 'Incorrect username or password'

        return render_template("login.html", msg=msg)  #Asis

    @app.route("/logout")  #Asis
    def logout_page():
        """Allows user to logout after being logging in"""

        current_user.username = None
        return render_template('main.html')

    @app.route("/upload", methods=['GET', 'POST'])  #Enrique
    def uploadPage():
        """Once logged in, allows user to upload their own html files"""
        #app.config['UPLOAD_FILE'] = "/home/username/project/"
        if request.method == "POST":

            if request.files:
                f = request.files["myfile"]

                if f.filename == '':
                    print("File cannot be empty")
                    return redirect(request.url)

                basedir = os.path.abspath(os.path.dirname(__file__))
                filename = secure_filename(f.filename) #add to list

                if not backend.user_add_file(current_user.username, filename):
                    return render_template("page_exists.html", display_name=filename, name=current_user.username)

                basedir = os.path.dirname(basedir)
                f.save(os.path.join(os.path.join(basedir), filename))
                backend.upload(filename)
                os.remove(f.filename)
                return render_template("upload.html", name=current_user.username)

        return render_template("upload.html", name=current_user.username)

    @app.route("/logged_in") #Danny
    def logged_in():
        return render_template("logged_in.html", name=current_user.username)
    
    #--
    @app.route("/logged_about")  #Danny
    def logged_about():
        """Sets up image rendering for the about page"""
        img1 = backend.get_image("asis.jpeg")
        img2 = backend.get_image("daniel.JPG")
        img3 = backend.get_image("enrique.jpg")
        img1 = img1.decode('UTF-8')
        img2 = img2.decode('UTF-8')
        img3 = img3.decode('UTF-8')
        return render_template("logged_about.html", img1=img1, img2=img2, img3=img3, name=current_user.username)
    #--

    #--
    @app.route("/logged_pages") #Danny
    def logged_pages():
        """Renders a specific page that the user selected from the available pages"""
        page_name_list = backend.get_all_page_names()
        return render_template("logged_pages.html", name_lst=page_name_list, name=current_user.username)
    #--

    @app.route("/pages/<stored>")  #Danny
    def grabUploaded(stored):
        """Renders specific selected page"""
        neededPage = backend.get_wiki_page(stored)
        return neededPage  #render_template(neededPage)

    #--
    @app.route("/user_page", methods = ['GET', 'POST']) #Danny
    def grabUser():
        #check request
        if request.method == 'POST' and 'user' in request.form:

        #set variables
            user = request.form['user']

        #check if user exists
        if backend.user_exists(user):
        #  if they do
        #   get user page
            user_page_lst = backend.get_user_pages(user)        
        #   return user page
            return render_template("user_page.html", upl=user_page_lst, display_name=user)
        #  else
        else:
        #   return dont exist page
            return render_template("no_matches.html", display_name=user)
    #--


    #--
    @app.route("/logged_user_page", methods = ['GET', 'POST']) #Danny
    def loggedGrabUser():
        #check request
        if request.method == 'POST' and 'user' in request.form:

        #set variables
            user = request.form['user']

        #check if user exists
        if backend.user_exists(user):
        #  if they do
        #   get user page
            user_page_lst = backend.get_user_pages(user)        
        #   return user page
            return render_template("logged_user_page.html", upl=user_page_lst, display_name=user, name=current_user.username)
        #  else
        else:
        #   return dont exist page
            return render_template("logged_no_matches.html", display_name=user, name=current_user.username)
    #--
    @app.route("/search")
    def search_bar(): #Asis
        '''Loads the search bar onto the wiki once Search is clicked in the Nav Bar'''
        return render_template("search.html")

    @app.route("/search", methods=['GET', 'POST'])
    def lookup(): #Asis
        '''Takes in a keyword from the user and loads a list of unique articles onto the wiki once a valid keyword is input into the search bar'''
        if request.method == 'POST' and 'keyword' in request.form:
            keyword = request.form['keyword']
            if backend.search_keyword(keyword) != False:
                valid_lst = backend.search_keyword(keyword)
                if valid_lst != []:
                    msg = 'Your Results:'
                else:
                    msg = 'Your topic has no results. You can upload an article on your topic by logging in and clicking Upload!'
        return render_template("lookup.html", valid_lst=valid_lst, msg=msg)
    
    @app.route("/discussion") #Enrique
    def discussion_posts():
        """Shows user all available discussion posts"""
        discussion_posts = backend.get_all_discussion_posts()
        return render_template("discussion.html", discussion_list=discussion_posts)

    @app.route("/discussion", methods=['GET', 'POST']) #Enrique
    def discussion():
        """Allows user to upload discussion post"""
        if request.method == "POST":

            if request.files:
                f = request.files["myfile"]

                if f.filename == '':
                    print("File cannot be empty")
                    return redirect(request.url)

                basedir = os.path.abspath(os.path.dirname(__file__))
                filename = secure_filename(f.filename)
                basedir = os.path.dirname(basedir)
                f.save(os.path.join(os.path.join(basedir), filename))
                backend.upload_discussion_post(filename)
                os.remove(f.filename)
                discussion_posts = backend.get_all_discussion_posts()
                return render_template("discussion.html", discussion_list=discussion_posts)

        discussion_posts = backend.get_all_discussion_posts()
        return render_template("discussion.html", discussion_list=discussion_posts)
    

    @app.route("/discussion/<stored>") #Enrique
    def get_discussion_post(stored):
        """Allows user to select a specific discussion posts to access"""
        discussion_posts = backend.get_discussion_post(stored)
        return discussion_posts

    @app.route("/create_discussion",methods=['GET', 'POST']) #Enrique
    def create_post():
        """Allows user to create a discussion post"""

        if request.method == 'POST' and 'userTitle' in request.form and 'userBody' in request.form:
            title = request.form["userTitle"]
            body = request.form["userBody"]
            file_name = title+".txt"
            backend.create_discussion(file_name,title,body)
            backend.upload_discussion_post(file_name)
            os.remove(file_name)
            discussion_posts = backend.get_all_discussion_posts()
            return render_template("discussion.html",discussion_list=discussion_posts)
            
        return render_template("create_discussion.html")
