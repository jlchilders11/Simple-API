# Simple-API

To install:
 
* [Download Python](https://www.python.org/)
* Use pip to install all of the dependencies with ```pip install -r "requirements.txt"```
* Apply all of the migrations with ```manage.py migrate```
* Run the server with ```manage.py runserver```

To use:

* Use migrate ```createsuperuser``` to create a login
* If you wish to use basic authentication, use your favourite api handler with your credentials
* If you want to use token authentication, go to tokens/create and select your user to get your token, and copy it from the token list
* If you do not have a prefered api handler, you can use the built in pages by navigating to api/file

URLS:
* admin/ : the django admin for our files
* login/ : login page for the token pages
* logout/ : navigate to this page to logout

* tokens/ : list our api tokens. Requires login
* tokens/create : create tokens for the api. Requires Login
* tokens/<id>/delete : remove the token of the given id. Requires login

* api/file : access the drf pages for our api
