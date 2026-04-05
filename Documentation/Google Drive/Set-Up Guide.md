	  
Download Github Desktop.  
Download Git for VS Code.  
Connect Github to VS Code Git (I don’t remember how, I’ll make this better shortly).

Go to the CCC Github page.  
	Click the green `Code` button.  
	Select `Open With Github Desktop`

Clone the Repository to where you want it.

Fetch Origin from the `Development` branch.

Open the Command Palette (Ctrl+Shift+P || Cmd+Shift+P).   
	Type “env” and click “Python: Create Environment…”.  
	Select Venv.  
	Select your interpreter.   
	Click on the “requirements.txt” button.

If you’re on Windows, run the command `.venv/Scripts/Activate.ps1`.  
If you’re on Mac, run the command `source .venv/bin/activate`.

If you’re on Windows, run the command `pip install python-magic-bin`.  
If you’re on Mac, run the command `pip install python-magic` and `brew install libmagic` (or just run `pip install python-magic-bin`)  
	[https://pypi.org/project/python-magic/](https://pypi.org/project/python-magic/)

\# This changes the directory into the project file.  
`cd cccSite` 

\# This does something (it’s related to models, and I’m not entirely sure. It only has to be run after every fresh install and when models have been changed).  
`Python manage.py makemigrations`

\# This has to be run after the `makemigrations` command has been run.  
`python manage.py migrate`

\# This is what runs the server. This should be run every time the server is turned on.  
`python manage.py runserver 8080`

When you open the website, use `localhost:8080`, some things might not work if you use `127.0.0.1`.

(You may, although shouldn’t, have to replace `python` with `py` or other small differences. Please test the above first.)

When you have the code fully set-up, you only need to run `python manage.py runserver 8080` when you want to start up the website.

Any changes to a CSS or HTML file will probably require you to clear your web browser cache.

Any changes to a model will probably require you to run the commands `python manage.py makemigrations` and `python manage.py migrate`. (You may need to do `python manage.py migrate --run-syncdb`, I don’t know why or when, but if `python manage.py migrate` doesn’t work, try this instead.)

When you save a `.py` file, the website will automatically shut-off and reload. You shouldn’t have to start and reopen it, but if you’re encountering bugs, please try that.

The admin site can be accessed by `localhost:8080/DJadmin`, `username: admin`, `password: admin` is an admin account.