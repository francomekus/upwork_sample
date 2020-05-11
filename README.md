# upwork_sample
A simple django rest framework API for  POST and GET methods deployed on Heroku.
## set up
The first thing is to create a virtual environment to install dependencies in and activate it.
```
$ mkdir upwork_sample
$ cd upwork_sample
$ pip install virtualenv
$ python -m venv venv
$ venv\Scripts\activate
```
## creating a new django project and app
```$ pip install django==3.0.6
$ django-admin startproject django_api
$ cd django_api
$ python manage.py startapp post
$ pip install djangorestframework
```
add the `post` and `rest_framework` to `INSTALLED_APPS` in settings.py
```INSTALLED_APPS = [
    # 3rd party apps
    'rest_framework',

    # local apps
    'post.apps.PostConfig',
]
```
## create your models
add the database model to `post/models.py` 
```from django.db import model

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title
```
Then makemigrations and migrate
```$ python manage.py makemigrations post
$ python manage.py migrate
```
## Add database to admin panel
Add this to the `post/admin.py`
```from django.contrib import admin
from .models import Post

admin.site.register(Post)
```
create a superuser to use in logging in to the admin panel
```$ python manage.py createsuperuser```
and follow the instructions.
## Adding Urls
First, add this to the project level  urls at `django_api/urls.py`.
it should look like this
```from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls')),
]
```
#### Adding app level urls
create a new `urls.py` file in the post folder and add this
```from django.urls import path
from .views import ListPost, DetailPost

urlpatterns = [
    path('', ListPost.as_view()),
    path('<int:pk>/', DetailPost.as_view()),
]
```
Note: we have not created the views yet.
## Creating the Serailizers.
We have to create a serializer, which translates data into a format that is easy to consume over the internet,
typically JSON, and is displayed at an API endpoint.
So create a `serializers.py` in the post folder. and add this.
```from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body')
   ```
## Create Views.
Add this to the `post/views.py` file.
```from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class DetailPost(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

## Tests
we are done for now, but we have to test the app. Writing tests is important because it automates the process of confirming that the
code works as expected.
Add this to the `post/test.py` file.
```from django.test import TestCase, Client
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        Post.objects.create(title='This is the title', body='This is the body')

    def test_text_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f'{post.title}', 'This is the title')
        self.assertEqual(f'{post.body}', 'This is the body')

    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the body')

    def test_post_detail_view(self):
        response = self.client.get('/1/')
        no_response = self.client.get('/post/450000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'This is the body')
  ```
 ### Testing our API endpoint with cURL locally.
 ``` $ python manage.py runserver
 for Post request:
 ``` $ curl http://127.0.0.1:8000 -d "title=add your title here&body=add you body here" 
 ```
 for GET request:
  ```$ curl http://127.0.0.1:8000
  ```
  ## Getting ready for deployment
  1. first install
  ```$ pip install gunicorn
     $ pip install whitenoise
   ```
  2. Add a **Procfile** file with no extension(e.e txt) in the project root directoty.
  Open the **Procfile** and add
   ```web: gunicorn django_api.wsgi --log-file -```
   3. Add a **runtime.txt** file in the project root and specify the correct python version.
   Open it and add
   ```python-3.7.2```
   4. Add a **requirements.txt** file.
    ```pip freeze > requirements.txt```
 ## Set up the static Assets
 open `settings.py` file and add the following changes at the bottom.
  ```STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')```
  Add whitenoise middleware on the middleware in `settings.py`
  ```'whitenoise.middleware.WhiteNoiseMiddleware',```
  Make a on line change to `settings.py` file
  ```ALLOWED_HOSTS = ['*']```
  The asterisks which means all domains are accepted just to keep things simple. 
  you can still replace it with the domain name of your heroku app.
  
  ## Adding to Github
  ```$ git init
  $ git add -A
  $ git commit -m "initial commit"
  $ git remote add origin https://github.com/francomekus/francomekus_sample.git
  $ git push -u origin master 
  ```
  ## Deploying to Heroku
  Sign up for heroku free account and download Heroku CLI.
  ```$ heroku login```
  you will be prompted to login, after that
  ```$ heroku create franco-sample
  $ heroku git: remote -a franco-sample
  $ heroku git push heroku master
  $ heroku open
  ```
  if you get error message with `collectstatic`  simply ignore it for now bydisapplying it.
   ```$ heroku config:set DISABLE_COLLECTSTATIC=1
   $ git push heroku master
   $ heroku open
   ```
   ## Fnal Test
   Our app in now online and can also be accessed form **curl**
   For POST request:
 ``` $ curl https://franco-sample.herokuapp.com/ -d "title=add your title here&body=add you body here" ```
 For GET request: list of all post
  ```$ curl https://franco-sample.herokuapp.com/```
  For GET request: detail of single post
  ```$ curl https://franco-sample.herokuapp.com/id/```
