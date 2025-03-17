1. Open GitHub desktop 
   1. pull origin
1. Start google cloud instance 
   1. copy external IP address
1. Open VSCode (cmd for mac, ctrl for windows)
   1. Cmd/ctrl+shift+p > Remote-SSH > enter [username]@[externalIP]
   1. Click: Clone Git Repository
   1. Cmd/ctrl+shift+p > Python: Create Environment > venv
   1. Open terminal
      1. source .venv/bin/activate
      1. cd cccSite
      1. pip install -r requirements.txt
      1. python3 manage.py makemigrations
      1. python3 manage.py migrate
      1. python3 manage.py runserver 8080
1. The admin site can be accessed by localhost:8080/DJadmin, username: admin, password: admin is an admin account.
