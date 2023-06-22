
# **Ecochef**

This project is for my Bachelor Degree in Software Development. It is a Data-Centric Project and the second last project for completion of this course. The project consists of Flask, Python, HTML5, SCSS, Javascript/jQuery and some Bootstrap is also included.

## **UX Design**

The initial idea of creating the Ecochef website originated from looking at cooking websites and not really finding any websites that were easy to use and fit my purpose of a recipe search with the capability of searching for recipes with ingredients.

I wanted to show how food waste could be reduced if people have the tools to manage their ingredients more efficiently. With a large database of recipes, users should consistently find recipes that match their ingredient list and if not the the system gives the user the results with the highest amount of ingredients used.

I used Bootstrap to handle the navbar, footer and grid system.  [Bootstrap](https://getbootstrap.com/). I used bootstraps grid system to define the layout of the page as well as cater for mobile/desktop responsiveness. An example of code for creating a 2-column grid is:-

```
	<div class="container"
		<div class="row">
			<div class="col">
			</div>
			<div class="col">
			</div>
		</div>
	</div>

```

I also used font-awesome icons to style buttons and other features -  [Font Awesome](https://fontawesome.com/v4.7.0/).

**User Stories**  First and foremost, the user is the primary focus of creating a website. The type of user I would expect to use Ecochef would be as follows:-

-   Someone who likes food and cooking good healthy nutritious meals, easy to cook.
-   A student
-   Stay-at-home mum
-   Working mum with kids
-   Anyone else who is interested in reducing food waste through efficient use of ingredients.

### **The Strategy**

The strategy is concerned with the goal of the project, which was to create a user-friendly, interactive recipe website with an easy-to-use search recipes function. As a user, I wish to interact with the recipe website, by being able to log in, logout, create, delete, update, favourite and search for recipes.  
CRUD functions are demonstratable throughout the project.

### **Flask**

-   What is Flask? Flask is often referred to as a micro framework. Flask is a web application framework written in Python. It is developed by Armin Ronacher, who runs Pocco (International group of Python Enthusiasts). Flask is based on the Werkzeug WSGI toolkit and Jinja2 template engine. Both are Pocco projects. Flask uses a collection of libraries and modules that enables a web application developer to write applications without having to bother about low-level details.
    
-   WSGI WSGI is a Web Server Gateway Interface (WSGI) for a universal interface between the web server and the web applications. It is a WSGI toolkit, which implements requests, response objects, and other utility functions. This enables building a web framework on top of it. The Flask framework uses Werkzeug as one of its bases.
    
-   Jinja2 Jinja2 is a popular templating engine for Python. A web templating system combines a template with a certain data source to render dynamic web pages. It aims to keep the core of an application simple yet extensible.
    

To understand more about Flask, WSGI and Jinja2, click here -[FLASK](https://www.tutorialspoint.com/flask/flask_quick_guide)

## [](https://github.com/Deirdre18/dumpdinners-recipe-app#tech-used)**Tech Used**

### [](https://github.com/Deirdre18/dumpdinners-recipe-app#technologies-used-includes)**Technologies used includes:**

-   **HTML5**,  **SCSS**,  **Javascript**,  **JQuery**,  **Python**,  **Flask**  **AWS**,  **MySQL**, **Bootstrap**

Base languages used to create website.

Used  **HTML5**  to handle page routing and to build custom directives -  [HTML5](https://www.html5rocks.com/en/)

Used  **Font Awesome**  icons to give our project an intuitive 'google style' look and feel -  [FONT AWESOME 4.7.0](https://fontawesome.com/v4.7.0/)

Used  **SCSS**  for styling and enhancing the look of the website -  [SCSS](https://sass-lang.com/)

Used  **Javascript**  (minified versions) added end of document -  [JAVASCRIPT](https://developer.mozilla.org/bm/docs/Web/JavaScript)

Used  **JQuery**  to trigger ready() functions for datepicker, collapsible side nav bar and materialise selection functions -  [JQUERY](https://jquery.com/)

Used **Bootstrap** for the navbar, footer, alerts, modals and grid system  -  [BOOTSTRAP](http://getbootstrap.com/getting-started/)

Used **Python 3.9** for developing this project -  [PYTHON](https://docs.python.org/3.9/)

Used **Flask 2.2.2** for developing this project -  [FLASK](https://flask.palletsprojects.com/en/2.2.x/)

Used **Jinja2.10** for developing this project -  [JINJA2](http://jinja.pocoo.org/docs/2.10/)

Used **Werkzeug 0.14.1** for developing this project -  [WERKZEUG](https://www.palletsprojects.com/p/werkzeug/)

## **Testing**

To test the API I used Postman to send out requests so that I could see what data my API is providing. This allowed me to create the API without creating a specifically designed frontend which sped up development time.

Postman simplifies the process of testing APIs by providing a powerful testing framework. It allows developers to send requests, inspect responses, and validate API behaviour using assertions and scripts. It supports automated testing, allowing you to create test suites and run them repeatedly to ensure the stability and correctness of your API. Postman also offers a comprehensive documentation feature that allows developers to generate API documentation directly from their Postman collections. The documentation can be customized, styled, and published for internal or external use, making it easier to share API specifications and usage details with stakeholders and in my case, my supervisor.

[Ecochef API Documentation](https://documenter.getpostman.com/view/2699874/2s93z5AQmx)

To test the front end of my application I asked 10 test participants to complete the following tasks on the website:-
1. Search for a recipe with Olives
2. Register and Login to your account
3. Go to your profile
4. Like a Recipe 
5. Create a Recipe
6. Add Ingredients from a recipe to your shopping list

In addition, I tested all links to make sure they redirected correctly and worked, such as the URL for the home page and all recipes. I also tested responsiveness on mobile versions by going through the different views on the Chrome 'Inspect Element' feature. I tested search feature, to make sure the search button functions correctly and it does. I also tested this across mobile versions and works correctly.
     
I also tested features such as 'Search' function to ensure it worked correctly and my findings are that it does work successfully (on both large and small screens). Users can search using Recipe Name or Ingredients

I've also tested responsiveness on both mobile and desktop, in a variety of screen sizes using Google Chrome Developer tools. I tested responsiveness across small, large and medium screens.

-   Google Chrome (version 68)
-   Opera (version 55)
-   Mozilla Firefox Developer (version 63)
-   Internet Explorer (version 11)

**Testing across desktop/large laptop (using developer tools) and mobile browsers**  I have tested DumpDinners website on the above desktop browsers. On Firefox developer tools, I tested mobile responsiveness for Apple iPad Air2, Apple iPad Mini2, Apple iPad iPhone 6s, Google nexus 4,5,6,7, Laptop (1280px x 720px and 1366px x 768px), Nokia Lumia 520, Samsung Galaxy Note 3, Samsung Galaxy S5 and S7. On Chrome developer tools, I tested responsiveness for mobile small (320px), Mobile medium (375 x 840 px), Mobile large (425 x 960 px), tablet (768px x 2152px), laptop medium (1024px x 2241px), laptop large/medium (1440 x 3586px), laptop large (2138px x 5977px).

Further testing has not been carried out at this stage, due to time limitations.

## **Version Control (GitHub)**

I used version control (GitHub) on an ongoing basis to back-up my code to a remote repository at regular intervals throughout development of the Ecochef website project.


## **Deployment**
This project has been deployed to AWS and is available to the public at www.ecochef.co.nz

## **How to run the code in this project**

To run Ecochef locally:-
1.  Clone the repository url link to your workspace-  [Ecochef](https://github.com/omriwebber/ecochef.git)
2.  Create a Virtual Environment by using $python -m venv venv
3.  Activate the Virtual Environment by using $venv/Scripts/activate
4.  Install the project dependencies by using $pip install -r requirements.txt
5. Run the application python file

To run the Ecochef API locally:-

1.  Clone the repository url link to your workspace-  [Ecochef-API](https://github.com/omriwebber/ecochef-api.git)
2.  Create a Virtual Environment by using $python -m venv venv
3.  Activate the Virtual Environment by using $venv/Scripts/activate
4.  Install the project dependencies by using $pip install -r requirements.txt
5. Create a Database in Xampp and modify config.py to point to your locally hosted database.
6. Initialise the database by running the following commands:-
```
	flask --app 'application' db init
	flask --app 'application' db migrate -m 'Creating Tables'
	flask --app 'application' db upgrade
```
7. Run the application python file and go to 127.0.0.1:5000/recipes to test if the API is working
8. Then go to 127.0.0.1:5000/populate to populate the database with recipe data from recipes.json