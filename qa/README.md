#What you might want to learn to help solve issues:

1. Python basics:
   - How to write simple functions
   - How to run a script
   - Basic syntax

2. Vitrual environments:
   - Covered below...

3. pytest:
   - Tests are functions that start with 'test_'
   - Assertions use:
      - assert 'something'
   - Tests live within 'qa/ui/'
   - Run tests manually with:
      - pytest qa/ui

4. Start the CCC site:
   python3.10 manage.py makemigrations
   python3.10 manage.py migrate
   python3.10 manage.py runserver 8080


#Enter QA Virtual Environment:

1. In your terminal:
   source qa/.venv/bin/activate

2. You should see:
   (venv) yourname@...

3. To exit when done:
   deactivate


#Django Admin Access (DJadmin):

Some tasks may require access to the Django admin page. If you do not already have credentials, create a local superuser:

1. Navigate to the Django project directory:
   cd /home/<your-username>/shared_workspace/ChesapeakeCommunityConnect/cccSite

2. Create a superuser:
   python3.10 manage.py createsuperuser

3. Follow the prompts to set a username/password.

Admin URL:
http://127.0.0.1:8080/DJadmin/

Log in using the credentials you created.
