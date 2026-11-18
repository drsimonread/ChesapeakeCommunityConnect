We need to title or name these links so we can easily identify what they are for.   
Sources:  
		Official Django documentation

* [https://docs.djangoproject.com/en/5.0/](https://docs.djangoproject.com/en/5.0/)

		Tutorial for setting up and running a Django project in vscode

* [Vs studio code Django tutorial](https://code.visualstudio.com/docs/python/tutorial-django)

  Tutorial for writing documentation in Django

* [https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/](https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/)											W3schools Tutorial and Walkthrough   
* [https://www.w3schools.com/django/](https://www.w3schools.com/django/)

  Youtube intro to Django (IBM Tech)

* [https://www.youtube.com/watch?v=t\_p4ZyAYyaY\&t=236s](https://www.youtube.com/watch?v=t_p4ZyAYyaY&t=236s)

  Youtube intro to Django (Telusko)

* [https://www.youtube.com/watch?v=SIyxjRJ8VNY\&t=29s](https://www.youtube.com/watch?v=SIyxjRJ8VNY&t=29s)

  Basic tutorial

* [https://www.geeksforgeeks.org/django-tutoria](https://www.geeksforgeeks.org/django-tutorial/)l

  This document describes Django’s file access APIs for files such as those uploaded by a user. (intro to file Interaction)

* [https://docs.djangoproject.com/en/5.0/topics/files/](https://docs.djangoproject.com/en/5.0/topics/files/)

  Document on how to install Django

* [https://docs.djangoproject.com/en/5.0/topics/install/](https://docs.djangoproject.com/en/5.0/topics/install/) 

		Django starter project tutorial

* [https://docs.djangoproject.com/en/5.0/intro/tutorial01/](https://docs.djangoproject.com/en/5.0/intro/tutorial01/) 

		

File system:  
In the cccSite folder of the project you will find the following folders and files

\>Janitor  \*\* contains the html for the admin page as well as everything that can be viewed by an admin like the different tags and contributors\*\*  
\>account  \*\* contains the html for the signing in page as well as the pages users will see for once signed in, like a my account page  
\>boiler   \*\* contains about us and contact page basically just parts of the website that are too                                                small for their own apps\*\*  
\>cccSite  \*\* is like a resource folder where a lot of static files are stored that are used in many   
                     other sites\*\*  
\>mapViewer    
App.yaml    \*\*used for the google maps api\*\*  
Db.sqlite3  \*\*sqllite file that talks to the database\*\*  
main.py      \*\* begins the running process\*\*  
manage.py   \*\* updates models and run the server\*\*  
Requirements.txt   \*\*contains all the dependencies needed to run the website\*\*

In the Account, boiler ,mapViewer you will find a similar structure to the following folders  
v Account  
\>migrations \*\*python files that help with ??  
\>static/account \*\*contains the css files that style the html files in the templates folder   
\>templates/account \*\*contains the html for the page of the parent folder (might not be true but it does hold html files)

 

Files in Django:  
(from [https://testdriven.io/blog/django-static-files/](https://testdriven.io/blog/django-static-files/) )

First off, you'll typically find these three types of files in a Django project:

1. Source code: These are your core Python modules and HTML files that make up every Django project, where you define your models, views, and templates.  
2. Static files: These are your CSS stylesheets, JavaScript files, fonts, and images. Since there's no processing involved, these files are very energy efficient since they can just be served up as is. They are also much easier to cache.  
3. Media file: These are files that a user uploads.

