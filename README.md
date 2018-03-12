# SI 364 - Winter 2018 - Midterm Assignment

#### Introduction
This is a restaurant application built using the Yelp API. Users can search for restaurants near them, provide reviews for restaurants they have visited as well as read other user reviews. 

#### Routes and Views
1)http://localhost:5000/login -> login.html
- This serves as the first page of the application. User completes the form to "login" and upon successful completion of the form is sent to the welcome page.
- **Accepts duplicate data to be submitted, but this data is not saved in db. View function still functions as it would for non-duplicate data as well**

2)http://localhost:5000/welcome -> welcome.html
- Form data from UserForm() is used to curate restaurant results based on user's entered location from login page using YELP API. User should have access to navigation links now.
- User goes from http://localhost:5000/login to http://localhost:5000/welcome via **GET request to new page**


3)http://localhost:5000/enter_review -> review_form.html
- Uses the ReviewForm() WTForm to prompt a reviewer to leave a restaurant review.

4)http://localhost:5000/find_restaurant -> find_restaurant_form.html
- Uses the FinderForm() WTForm to help user find a restaurant based on their preferred cuisine type, price and location using the YELP API.
- **Custom validator in WTForm** checks that price entered is price and not symbol($)


5)http://localhost:5000/match_results -> match_results.html
- Serves results of the find_restaurant. Displays Top 5 matches in a table


6)http://localhost:5000/feeling_lucky -> feeling_lucky.html
- Uses UserForm() WTForm to be matched with a restaurant based only on their location and cuisine preference. Returns one random restaurant from YELP API for a user "feeling lucky".
- Implements **POST request to same page**

7)http://localhost:5000/all_reviews -> all_reviews.html
- uses **query.all()**

8)http://localhost:5000/all_restaurants -> all_restaurants.html

9)http://localhost:5000/all_reviewers -> all_reviewers.html

10)http://localhost:5000/all_names -> all_names.html


#### Code Requirements Met


- [ ]**Ensure that the `SI364midterm.py` file has all the setup (`app.config` values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on `http://localhost:5000` (and the other routes you set up)**
- [ ]**Add navigation in `base.html` with links (using `a href` tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, [like this](https://www.dropbox.com/s/hjcls4cfdkqwy84/Screenshot%202018-02-15%2013.26.32.png?dl=0) )**
- [ ]**Ensure that all templates in the application inherit (using template inheritance, with `extends`) from `base.html` and include at least one additional `block`.**
- [ ]**Include at least 2 additional template `.html` files we did not provide.**
- [ ]**At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.**
    - **These could be in the same template, and could be 1 of the 2 additional template files.**
- [ ] **At least one errorhandler for a 404 error and a corresponding template.**
- [ ] **At least one request to a REST API that is based on data submitted in a WTForm.**
- [ ] **At least one additional (not provided) WTForm that sends data with a `GET` request to a new page.**
- [ ] **At least one additional (not provided) WTForm that sends data with a `POST` request to the *same* page.**
- [ ] **At least one custom validator for a field in a WTForm.**
- [ ] **At least 2 additional model classes.**
- [ ] **Have a one:many relationship that works properly built between 2 of your models.**
- [ ] **Successfully save data to each table.**
- [ ] **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
- [ ] **Query data using an `.all()` method in at least one view function and send the results of that query to a template.**
- [ ] **Include at least one use of `redirect`. (HINT: This should probably happen in the view function where data is posted...)**
- [ ] **Include at least one use of `url_for`. (HINT: This could happen where you render a form...)**
- [ ] **Have at least 3 view functions that are not included with the code we have provided. (But you may have more! *Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of `base.html`.*)**

### Additional Requirements for an additional 200 points (to reach 100%) -- an app with extra functionality!

* **(100 points) Include an *additional* model class (to make at least 4 total in the application) with at least 3 columns. Save data to it AND query data from it; use the data you query in a view-function, and as a result of querying that data, something should show up in a view. (The data itself should show up, OR the result of a request made with the data should show up.)**

* **(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will *not* save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).**

