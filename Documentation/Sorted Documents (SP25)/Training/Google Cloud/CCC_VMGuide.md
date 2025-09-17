# Setting Up Your Google Cloud VM for CCC

After you have set up your VM, you will need to do a CCC-specific setup to ensure that you have
all the requirements to run CCC.

## 1. Connecting to your VM

1.1 Enter the console for your VM by doing one of the following:<br>
1.1.1 Open a Windows Powershell and type the command “ssh johndoe@123.456.78.901” wherein you replace <br>
johndoe@123.456.78.901 with your credentials and the ip address you want to connect to (this should be
the external IP address you found in the previous instructions) <br>
1.1.2 Connect to the virtual machine on Visual Studio and open terminal, which will automatically enter
the VM <br>
1.1.3 On the google cloud console where you activate the VM, click on the ssh button. This will open a 
new window that is linked to the VM <br>

## 2. Creating a Shared Workspace

### 2.1 This is where your GitHub clone will live<br>
2.1.1 Open terminal (CTRL+J on Windows and Chromebook, CMD+J on Macbook)<br>
2.1.2 sudo mkdir /home/shared_workspace<br>
2.1.3 sudo groupadd sharedgroup<br>
2.1.4 sudo usermod -aG sharedgroup name (repeat for however many users need access, where name <br>
is the name of the users youve connected from)<br>
2.1.5 sudo chown -R root:sharedgroup /home/shared_workspace<br>
2.1.6 sudo chmod -R 2770 /home/shared_workspace<br>
2.1.7 sudo chmod g+s /home/shared_workspace<br>
2.1.8 This creates a folder in the home directory called shared_workspace where all users added
in step C are able to access and modify files<br>
2.1.9 Restart your Google Cloud VM Session to update user permissions<br>

Note: If you create multiple VMs, you do not need to create a new keypair.<br>

## 3. Installing CCC

### 3.1 Set up VM to use python 3.10 (our VM is in Ubuntu which doesn't support past 3.8)<br>
3.1.1. cd /home/shared_workspace<br>
3.1.2 sudo apt update<br>
3.1.3 sudo apt upgrade -y<br>
3.1.4 sudo apt install -y software-properties-common<br>
3.1.5 sudo add-apt-repository -y ppa:deadsnakes/ppa<br>
3.1.6 sudo apt update<br>
3.1.7 sudo apt install -y python3.10 python3.10-venv python3.10-dev<br>
### 3.2 Install GitHub and clone the repository<br>
3.2.1 sudo apt install git<br>
3.2.2 git config --global user.name "****" (between “” needs to be the github username”<br>
3.2.3 git config --global user.email "****" (between the “” needs to be the github email address”<br>
3.2.4 git init<br>
3.2.5 git clone https://github.com/swbn1/ChesapeakeCommunityConnect-FA24 (if you are
working on this in FA25 or beyond, have your Project Lead fork the repo and change the link to the fork)<br>
### 3.3 Install dependencies<br>
3.3.1 python3.10 -m ensurepip<br>
3.3.2 python3.10 -m pip install --upgrade pip <br>
3.3.3 sudo apt install libapache2-mod-wsgi-py3<br>
3.3.3a Select Y to continue<br>
3.3.4 sudo apt install mariadb-server<br>
3.3.4a Select Y to continue<br>
3.3.5 sudo mysql_secure_installation<br>
3.3.5a Return for no current password<br>
3.3.5b Select Y to set the new root password to software_startup_simulator<br>
3.3.5c Select Y to remove anonymous users<br>
3.3.5d Select Y to disallow remote root login<br>
3.3.5e Select Y to remove test database<br>
3.3.5f Select Y to reload data table privileges<br>
3.3.6 sudo apt install -y postgresql<br>
### 3.4 Install requirements.txt<br>
3.4.1 cd /home/shared_workspace/ChesapeakeCommunityConnect-FA24/cccSite<br>
3.4.2 python3.10 -m pip install -r requirements.txt<br>
3.4.3 python3.10 -m pip install python-magic<br>
3.4.4 python3.10 -m pip install googlemaps<br>

## 4. Running CCC

### 4.1 cd /home/shared_workspace/ChesapeakeCommunityConnect-FA24/cccSite (the directory where manage.py is)<br>
### 4.2 python3.10 manage.py makemigrations<br>
### 4.3 python3.10 manage.py migrate<br>
### 4.4 python3.10 manage.py runserver 8080<br>
4.4.1 If you’re using Visual Studio Code, this should give you a prompt that says “Your application 
running on port 8080 is available”. Click on “Open in Browser”<br>
4.4.2 Alternatively, enter “http://127.0.0.1:8080/” in your browser<br>

## 5. GitHub and VM Usage

### 5.1 Update your local development branch before starting any work<br>
5.1.1 git checkout development<br>
5.1.2 git pull origin development<br>
### 5.2 Create a new branch for each issue<br>
5.1.1 git checkout -b the-name-of-your-issue-Name<br>
### 5.3 After you fix your issue, push it back to the main<br>
5.3.1 git add .<br>
5.3.2 git commit -m "Fixed this issue: [description of the issue]"<br>
5.3.2 git push origin the-name-of-your-issue-Name<br>
### 5.4 After this you will need to do a pull request for the push<br>
5.4.1 Go to your repository on GitHub.<br>
5.4.2 You should see a prompt to create a pull request for the newly pushed branch. Click on the "Compare & pull request" button.<br>
5.4.3 Fill in the details for the pull request, making sure to reference the issue number in the description (e.g., "Fixes #5").<br>
5.4.4 Submit the pull request for review.<br>



