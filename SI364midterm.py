###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
import json, urllib, requests
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import random




## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

API_KEY = "oo7VkYgXjWWI1dnOt3LMK9Uf6iV8XjxzP2fkT6nPa7PQYKQ4GeLli58Bp6AlKn0eKVjafFEkX_r2vD54VNd6mLBqR5o02v1ClFRcgYG2V_2SsAIFjnDW0XnGDrucWnYx"
# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
headers ={
        'Authorization': 'Bearer %s' % API_KEY,
    }
SEARCH_LIMIT = 5

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/midterm1"
## Provided:
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer,primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    rating = db.Column(db.Integer)
    review = db.Column(db.String(500))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    price = db.Column(db.Integer)
    zipcode = db.Column(db.String(5))
    food_type = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    reviews = db.relationship('Review',backref='Restaurant')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    reviews = db.relationship('Review',backref='User')





###################
###### FORMS ######
###################



def validate_price(form,field):
    if str(field.data).isdigit() is False:
        raise ValidationError('Please enter a valid price!')


class UserForm(FlaskForm):
    name = StringField("Please enter your name:",validators=[Required()])
    location = StringField("Please enter current location(city):",validators=[Required()])
    type = StringField("Favorite food type(Italian, Mexican etc.):",validators=[Required()])
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    reviewer = StringField("Please enter your name:",validators=[Required()])
    restaurant_name = StringField("Please enter restaurant name:",validators=[Required()])
    restaurant_type = StringField("Please enter restaurant type(Italian, Mexican etc.):",validators=[Required()])
    price = IntegerField("Please enter price(1($),2($$),3($$$)):",validators=[Required(),validate_price])
    location = IntegerField("Please enter zipcode:",validators=[Required()])
    rating = IntegerField("Rate your restaurant:",validators=[Required()])
    comments = StringField("Please enter your comments:", validators=[Required()])
    submit = SubmitField("Submit")





class FinderForm(FlaskForm):
    location = IntegerField('Please enter your zipcode:',validators=[Required()])
    price = IntegerField("Please enter price(1($),2($$),3($$$)):",validators=[Required(),validate_price])
    type = StringField("Type of food wanted(Italian, Mexican etc.):",validators=[Required()])

    submit = SubmitField("Submit")



#######################
###### VIEW FXNS ######
#######################

@app.errorhandler(404)
def page_na(error):
    return render_template('404.html',404)


@app.route('/login',methods=['GET','POST'])
def login():
    form = UserForm()
    return render_template('login.html',form=form)

@app.route('/welcome',methods=['GET','POST'])
def welcome():
    if request.args:
        result = request.args
        name = result.get('name')
        location = result.get('location')
        n_name = Name.query.filter_by(name=name).first()
        if not n_name:
            n_name = Name(name=name,location=location)
            db.session.add(n_name)
            db.session.commit()
        # user with same name and location can enter data, but this will not bse saved


        params = {}
        params['location'] = location
        params['limit'] = SEARCH_LIMIT + 5
        params['sort_by'] = 'rating'
        params['term'] = 'restaurants'
        url = API_HOST + SEARCH_PATH
        resp = requests.get(url, params=params, headers=headers)

        search_list = []
        data = json.loads(resp.text)
        for term in data['businesses']:
            res = {}
            res['name'] = term['name']
            res['rating'] = term['rating']
            res['price'] = term['price']
            res['type'] = term['categories'][0]['title']
            search_list.append(res)
        return render_template('welcome.html',name=name,location=location,data=search_list)


    return redirect(url_for('login'))
    # else:
    #     flash('Please enter a valid city')





@app.route('/enter_review',methods=['GET','POST'])
def enter_review():
    form = ReviewForm()

    if form.validate_on_submit():
        reviewer = form.reviewer.data # needed for User db column username
        res_name = form.restaurant_name.data
        res_type = form.restaurant_type.data
        price = form.price.data
        rating = form.rating.data
        location = form.location.data
        comments = form.comments.data

        user = User.query.filter_by(username=reviewer).first()
        if not user:
            n_user = User(username=reviewer)
            db.session.add(n_user)
            db.session.commit()

        restaurant = Restaurant(name=res_name, price=price, zipcode=location, food_type=res_type,rating=rating)
        db.session.add(restaurant)
        db.session.commit()

        review = Review(user_id=user.id,rating=rating,price=price,review=comments,restaurant_id = restaurant.id)
        db.session.add(review)
        db.session.commit()


        flash('Review Added!')
    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("FORM SUBMISSION FAILED. PLEASE CORRECT AND RE-SUBMIT" + str(errors))

    return render_template('review_form.html',form=form)

@app.route('/find_restaurant',methods=['GET','POST'])
def find_restaurant():
    form = FinderForm()

    return render_template('find_restaurant_form.html',form=form)

@app.route('/match_results',methods=['GET','POST'])
def restaurant_match():
    form = FinderForm()
    if form.validate_on_submit():
        location = form.location.data
        res_type = form.type.data
        price = form.price.data
        params = {}
        params['location'] = location
        params['limit'] = SEARCH_LIMIT
        params['price'] = price
        params['categories'] = res_type
        params['sort_by'] = 'rating'
        url = API_HOST + SEARCH_PATH
        resp = requests.get(url, params=params, headers=headers)

        search_list = []
        data = json.loads(resp.text)
        for term in data['businesses']:
            res = {}
            res['name'] = term['name']
            res['rating'] = term['rating']
            res['price'] = term['price']

            search_list.append(res)
        return render_template('match_results.html',data=search_list)
    return redirect(url_for(find_restaurant))


@app.route('/feeling_lucky', methods = ['GET', 'POST'])
def feeling_lucky():
    form = UserForm()
    print (form.validate_on_submit())
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        location = form.name.data
        res_type = form.type.data

        params = {}
        params['location'] = location
        params['limit'] = SEARCH_LIMIT
        params['sort_by'] = 'rating'
        params['categories'] = res_type

        url = API_HOST + SEARCH_PATH
        resp = requests.get(url, params=params, headers=headers)

        search_list = []
        data = json.loads(resp.text)

        for term in data['businesses']:
            res = {}
            res['name'] = term['name']

            search_list.append(res)
        random_selection = random.choice(search_list)
        restaurant = random_selection['name']

        return render_template('feeling_lucky.html',form=form,name=name,restaurant=restaurant)
    flash ('All fields are required')
    return render_template('feeling_lucky.html',form=form)


@app.route('/feeling_lucky_result', methods = ['GET', 'POST'])
def feeling_lucky_result():
    form = UserForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        location = form.name.data
        res_type = form.type.data

        params = {}
        params['location'] = location
        params['limit'] = SEARCH_LIMIT
        params['sort_by'] = 'rating'
        params['categories'] = res_type

        url = API_HOST + SEARCH_PATH
        resp = requests.get(url, params=params, headers=headers)

        search_list = []
        data = json.loads(resp.text)

        for term in data['businesses']:
            res = {}
            res['name'] = term['name']

            search_list.append(res)
        random_selection = random.choice(search_list)
        restaurant = random_selection['name']
        print (restaurant)

        return "Hi, {0}! The algorithm has chosen {1}. Enjoy!".format(name,restaurant)
    flash ('All fields are required')
    return redirect(url_for('login'))


@app.route('/all_reviews')
def all_reviews():
    reviews = Review.query.all()

    return render_template('all_reviews.html',reviews=reviews)

@app.route('/all_restaurants')
def all_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('all_restaurants.html',restaurants=restaurants)

@app.route('/all_reviewers')
def all_reviewers():
    reviewers = User.query.all()
    return render_template('all_reviewers.html',reviewers=reviewers)


@app.route('/all_names')
def all_names():
    names = Name.query.all()
    print (names)

    return render_template('all_names.html',names=names)









## Code to run the application...

if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual


# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
