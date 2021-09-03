# onlineshop
An e-commerce API backend with django and drf.
it's still in progress and it isn't completed.


# Installation

Create a database named `onlineshop` in your mysql db (I personally use xampp for db)<br>
Install pipenv with cmd `py -m pip install pipenv`<br>
Then open console in cloned folder and write `pipenv install`. 
after that, active environment shell with `pipenv shell`<br>
Now, migrate database with command `py manage.py migrate`, 
and run the server with command `py manage.py runserver`<br>
I used drf_spectacular in my project so you can easily use this link to see all of api links and their docs `http://127.0.0.1:8000/api/v1/docs/`<br>
