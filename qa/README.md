#What you might want to learn to help solve issues:

1. Python basics:
   - How to write simple functions
   - How to run a script
   - Basic syntax

2. Vitrual environments:
   - Covered below...
  
3. Creating a new smoke test:
   - Add test to qa/ui/
   - Use ./qa/run_all.sh to run the test
   - Open Pull Request into development
   - Delete the branch after 

4. pytest:
   - Tests are functions that start with 'test_'
   - Assertions use:
      - assert 'something'
   - Tests live within 'qa/ui/'
   - Run tests manually with:
      - pytest qa/ui

5. Opening the CCC website:
   python3.10 manage.py makemigrations
   python3.10 manage.py migrate
   python3.10 manage.py runserver 8080

#Example of a route smoke test:
   import os
   import requests

   def test_homepage_responds():
       base_url = os.getenv("QA_BASE_URL", "http://127.0.0.1:8080")
         r = requests.get(base_url + "/", timeout=5)
         assert r.status_code < 200

#How to delete branch:
-On github use the "delete branch" button, or
-Run git branch -d <your-branch-name> in VS code

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
