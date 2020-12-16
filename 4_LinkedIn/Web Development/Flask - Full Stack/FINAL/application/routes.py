from flask import render_template, request, json, Response, redirect, flash, url_for, session, jsonify
from flask_restplus import Resource
from application import app, api
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm


#-------------------------------------------------------------------------------------
# ROUTES
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("index.html", index = True)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    # session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # If already Logged In and we call the page
    if session.get('username'):
        return redirect(url_for('index'))
    # Log In
    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        user = User.objects(email = email).first()
        if not user:
            flash('This email address is not recognised. Please register first', 'danger')
        else:
            if not user.get_password(password):
                flash('Incorrect password', 'danger')
            else:
                session['user_id'] = user.user_id
                session['username'] = user.first_name
                flash('You are successfully logged in !!!', 'success')
                return redirect(url_for('index'))
    return render_template("login.html", title = 'Login', formx = form, login = True)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    # If already Logged In and we call the page
    if session.get('username'):
        return redirect(url_for('index'))
    # Register
    form = RegisterForm()
    if form.validate_on_submit():
        user_id     = User.objects.count() + 1
        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data
        # area        = form.area.data
        inst_user = User(user_id = user_id, email = email, first_name = first_name, last_name = last_name) #, area = area
        inst_user.set_password(password)
        inst_user.save()
        flash('You are successfully registered! \n Please Login now...', 'success')
        return redirect(url_for('index'))
    return render_template("register.html", title = 'Register', formx = form, register = True)
    # return render_template("register.html", register = True)

@app.route('/courses/')
@app.route('/courses/<term>')
def courses(term = None):
    if term is None:
        term = 'Spring 2019'
    classes = Course.objects.order_by('+courseID')      # + is like ASC in SQL
    return render_template("courses.html", courseData = classes, courses = True, term = term)
    # return render_template("courses.html", courseData = courseData, courses = True, term = term)


@app.route('/enrollment', methods = ['GET', 'POST'])
def enrollment():
    # If NOT Logged In : go to login
    if not session.get('username'):
        return redirect(url_for('login'))
    # If Logged In
    courseID = request.form.get("courseID")
    title = request.form.get("title")
    user_id = session.get('user_id')
    # Only if its from the page Courses, so we add the course to the existing Enrollment (in db)
    if courseID:
        if Enrollment.objects(user_id = user_id, courseID = courseID):
            flash(f"Oops ! You are already enrolled in this course {title}", 'danger')
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id = user_id, courseID = courseID).save()
            flash('You are successfully enrolled ! ', 'success')
    classes = list(User.objects.aggregate(*[{'$lookup': {'from': 'enrollment', 'localField': 'user_id', 'foreignField': 'user_id', 'as': 'r1'}},
                                            {'$unwind': {'path': '$r1', 'includeArrayIndex': 'r1_id', 'preserveNullAndEmptyArrays': False}},
                                            {'$lookup': {'from': 'course', 'localField': 'r1.courseID', 'foreignField': 'courseID', 'as': 'r2'}},
                                            {'$unwind': {'path': '$r2', 'preserveNullAndEmptyArrays': False}},
                                            {'$match': {'user_id': user_id}},
                                            {'$sort': {'courseID': 1}}
                                            ]))
    return render_template("enrollment.html", enrollment = True, title = 'Enrollment', classes = classes)
    # # POST method => use form instead of args
    # idd = request.form.get("courseID")
    # title = request.form.get("title")
    # term = request.form.get("term")
    # d_data = {'id': idd, 'title': title, 'term': term}
    # return render_template("enrollment.html", enrollment = True, data = d_data)
    # # GET Method
    # @app.route('/enrollment', methods = ['GET', 'POST'])
    # def enrollment():
    #     idd = request.args.get("courseID")
    #     title = request.args.get("title")
    #     term = request.args.get("term")
    #     d_data = {'id': idd, 'title': title, 'term': term}
    #     return render_template("enrollment.html", enrollment = True, data = d_data)



#-------------------------------------------------------------------------------------
# API
@api.route('/api', '/api/')
class GetAndPost(Resource):
    def get(self):
        return jsonify(User.objects.all())
    def post(self):
        # Param
        data = api.payload
        user_id = data['user_id']
        # create Object to save in DB
        inst_user = User(user_id = user_id, email = data['email'], first_name = data['first_name'], last_name = data['last_name'])  # , data['area = area']
        inst_user.set_password(data['password'])
        inst_user.save()
        return jsonify(User.objects(user_id = user_id))

@api.route('/api/<idx>')
class GetUpdateDelete(Resource):
    def get(self, idx):
        return jsonify(User.objects(user_id = idx))
    def put(self, idx):
        data = api.payload
        User.objects(user_id = idx).update(**data)
        return jsonify(User.objects(user_id = idx))
    def delete(self, idx):
        User.objects(user_id = idx).delete()
        return jsonify("User is deleted !")

# # API: Send JSON response
# @app.route('/api/')
# @app.route('/api/<idx>')
# def api(idx = None):
#     courseData = [{"courseID": "1111", "title": "PHP 111", "description": "Intro to PHP", "credits": "3", "term": "Fall, Spring"},
#                   {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": "4","term": "Spring"},
#                   {"courseID": "3333", "title": "Adv PHP 201", "description": "Advanced PHP Programming", "credits": "3","term": "Fall"},
#                   {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": "3","term": "Fall, Spring"},
#                   {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": "4", "term": "Fall"}]
#     if idx is None:
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]
#     return Response(json.dumps(jdata), mimetype = 'application/json')



#-------------------------------------------------------------------------------------
# Mongo DB management - page
@app.route("/user")
def user():
    # # Creating 2 User just like this
    # User(user_id = 1, first_name = "Christian", last_name = 'Hur', email = 'Christian.Hur@google.com', password = 'abc1234').save()
    # User(user_id = 2, first_name="Mary", last_name='Hur', email='Mary.Hur@google.com', password='abc1234').save()
    users = User.objects.all()
    return render_template("user.html", user = users)
