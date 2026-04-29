# Development using  Google Cloud Platform And Visual Studio Code

# Table of Contents

# Setting up in the Google Cloud

## Creating Your Project

1. Claim your Education Credits as in the email you received.  
   You will need to use your smcm.edu account for all your interactions with the Google Cloud Platform.  
2. Goto [https://console.cloud.google.com](https://console.cloud.google.com) .  
3. Tick the box to accept the Terms of Service.  
4. Click Agree and Continue.  
5. Click Select a Project.  
6. Click New Project (in the top right corner.  
7. In Project Name type your name and \-00 (as in simon-read-00).  
8. Your Organization and Location should be smcm.edu.  
9. Click on the button that says Create  
10. In the Notifications panel (to the right) under your project name, click Select Project.  
11. Select the three bars in the top left of the window.  
12. Select Cloud Overview  
13. Select Dashboard

## Creating Your Server

1. From the Dashboard, under Resources click Compute Engine.  
2. Possibly click on enable  
3. In the new panel at the top, click on Create Instance.  
4. Click on Enable  
5. Navigate back to Compute Engine  
6. In name, put your name then \-instance-00 (as in simon-read-instance-00)  
7. Select Region as us-central-1 (Iowa) (probably the default).  
8. Select Any for Zone (probably the default).  
9. Ensure General purpose is selected.  
10. Ensure E2 is selected.  
11. In the left panel, select OS and Storage  
12. Select Change.  
13. Under Operating System select “Ubuntu”  
14. Ensure the Version is Ubuntu 20.04 LTS.  
15. Click Select  
16. Click on Networking in the left panel  
17. Under the Firewall heading check the boxes “Allow HTTP Traffic” and “Allow HTTPS Traffic”  
18. Scroll down click on default in Network Interfaces.  
19. Click the dropdown to expand “Default” under “Network Interfaces”  
20. Ensure under External IPv4 Address “Ephemeral” is selected. (probably default)  
21. Under Network Service Tier select Standard  
22. Click Create at the bottom of the window

## Stopping Your Instance

Remember to Stop your instance every time you have finished working with it, or it will continue to charge against your Educational Credits and you will run out\!

1. In the Compute Engine – VM Instances window  
2. Select the three dots for your instance (you may need to scroll the main screen to see all the options under this menu).  
3. Select Stop  
4. The Status icon will change from a tick mark in a green circle to a white square in a grey circle.

## Restarting Your Instance

1. In the Compute Engine – VM Instances window  
2. Select the three dots for your instance  
3. Select Start  
4. In the modal window that comes up click Start  
5. The Status icon will change from a white square in a grey circle to a tick mark in a green circle.

# Setting Up Visual Studio Code

## Installing Visual Studio Code

1. Download Visual Studio Code from [https://code.visualstudio.com/download](https://code.visualstudio.com/download) and follow the installation instructions.

### Installing Visual Studio Code Extensions

1. Open Visual Studio Code  
2. Click on View:Extensions  
3. In the Search Bar, search for the following extensions and click install for each one:  
1. Remote Development (by Microsoft)  
2. Remote – SSH (by Microsoft)  
3. Python (The Microsoft Developed Extension)  
4. Django (by Baptiste Darthenay)  
5. MarkDown All In One (by Yu Zhang)  
6. GitHub Markdown Preview (by Matt Bierner)

## Getting SSH for Windows 

You should already have SSH on your computer (applicable to macbook, windows, and Linux machines). Open a terminal and type the command “ssh”. As long as it doesn't return an error, you have an SSH client installed.

IF IT DOESN’T RETURN AN ERROR, YOU CAN SKIP ALL OF THIS AND MOVE TO FINDING YOUR EXTERNAL IP ADDRESS

### Installing PowerShell on Windows

PowerShell should already be installed on your computer, if it is not then follow the instructions at [https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.5)

### Installing the OpenSSH client on Windows

The OpenSSH client should have been installed when you installed the Remote Development plug-in for Visual Studio Code.  If that is not the case then follow the instructions at [https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh\_install\_firstuse?tabs=gui\&pivots=windows-server-2025](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=gui&pivots=windows-server-2025)

### Testing your OpenSSH installation

1. Search for and open the PowerShell application (running regular should work just fine)  
2. Type ssh \<username\>@login.cs.smcm.edu to log in to the CS server as you did in Computer Architecture and/or Programming Languages  
3. You should be asked if a key is okay, accept it.  
4. Check that you are at the server by typing hostname.  You should get the response prometheus.

### Cygwin Warning

You may have Cygwin (a Unix emulation suite) installed and this might be what’s used by Remote – SSH later.  If you think this is the case, consult an expert but you might try the following:

1. Locate the cygwin directory (usually C:\\cygwin).  
2. Copy your ed25519 key from C:\\Users\\\<username\>/.ssh  
3. Paste it into Cygwin’s .ssh directory  
4. Start bash.exe in Cygwin’s bin directory  
5. Type the command chmod 400 .ssh/ed25519

## Getting SSH for macOS

SSH is installed by default in macOS.  All you need to do is open the Terminal application to get a Unix Command line.

## Getting SSH for Linux

Most Linux distributions install the SSH client by default (but not the server, which you will not need).  If you find that your distribution has not installed the client, then use Google to find instructions specific to your distribution.  
All you need to do is to open a Terminal and type your commands there.

## To Find the External IP Address of your VM Instance

1. Make sure your instance is running.  
2. Scroll the VM instances window to the left (or is it right) until you see the External IP box.  
3. The dotted quad in that box is your external IP.

# Connecting to your Google Cloud VM through Visual Studio Code

## Setting up a SSH Keypair. 

You will need to do this for every unique computer you want to connect to the cloud. These keypairs will also work for multiple different instances, you do not have to create a new keypair for every VM instance you create.

1. Open Windows Powershell or Linux Terminal or Macbook Terminal  
   1. Run the command: ssh-keygen \-t ed25519  
      1. Click enter 3 times  
      2. Run the command: cat .ssh/id\_ed25519.pub  
      3. Copy the output of the above command  
   2. Navigate to your Google Cloud VM Dashboard  
   3. On the left side of the page, click the 3 line dropdown menu and navigate to the Compute Engine tab.   
   4. On the left side, scroll down until you see the metadata tab, click this to open it.  
   5. Click on the SSH keys tab.  
   6. Click on “Add SSH Key”  
   7. Paste in the output of the command we ran earlier that you copied, and save.

## Connecting in Visual Studio Code

8. Open the command palette by pressing F1 (Windows) or pressing CTRL+SHIFT+P (ChromeBook) or CMD+SHIFT+P (MacBook)  
   9. In the popup, enter “Remote-SSH: Connect to Host” and press enter  
   10. In the prompt to enter the host, and the username next to the key you put into the Google Cloud VM ssh key section, for example, johndoe  
   11. Then, next to your username and @, add the external IP address to your Google Cloud vm  
       1. It will look like this johndoe@123.456.78.901  
          1. Hit enter  
       2. It is important to note that if you’re working across multiple computers, you must use the name of each machine, so if machine 1 is john, and machine 2 is johndoe you must use the respective names  
   12. From here, a new Visual Studio Code window should appear. Select Linux in the drop down menu for the cloud software type  
   13. You may need to enter “yes” or “continue” into the console to accept the new SSH footprint, if prompted  
       

## Using the Visual Studio Code Editor

14. Top left of VS, press File  
    15. Click “Open Folder”  
    16. Navigate to the folder you want to open, then click “Open Folder”  
    17. In your explorer, you should now be able to access the files you want to work with\!

# Setting up your Google Cloud VM

## Installing all the dependencies and apps your Virtual Machine will need

1. Enter the console for your Virtual Machine, this can be done in various ways **YOU ONLY NEED TO FOLLOW ONE OF THESE STEPS TO OPEN YOUR TERMINAL, YOU DO NOT NEED TO DO ALL 3**  
   1. Open a Windows Powershell and type the command “ssh johndoe@123.456.78.901” where in you replace johndoe@123.456.78.901 with your credentials and the ip address you want to connect to  
      2. **Connect to the virtual machine on Visual Studio and open terminal, which will automatically enter the VM \<- Easiest Way**  
      3. On the google cloud console where you activate the VM, click on the ssh button. This will open a new window that is linked to the VM

## Creating a shared workgroup

2. Open terminal (CTRL+J on Windows and Chromebook, CMD+J on Macbook)  
   3. sudo mkdir /home/shared\_workspace  
   4. sudo groupadd sharedgroup  
   5. sudo usermod \-aG sharedgroup name (repeat for however many users need access, where name is the name of the users youve connected from)  
   6. sudo chown \-R root:sharedgroup /home/shared\_workspace  
   7. sudo chmod \-R 2770 /home/shared\_workspace  
   8. sudo chmod g+s /home/shared\_workspace  
   9. This creates a folder in the home directory called shared\_workspace where all users added in step C are able to access and modify files  
   10. Restart your Google Cloud VM Session to update user permissions

# Set Up your VM for CCC
## [here](CCC_VMGuide.md)

