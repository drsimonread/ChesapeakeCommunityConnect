# **GitHub General Notes**

## **Core concepts**

**Repository (repo)** \-  a project folder tracked by git

- contains your files plus the entire history of changes. repos live on GitHub remotely and can be copied locally.

**Commit** \-  a saved snapshot of your changes, with a message describing what you did 

- commits are the atomic unit of history. each one has a unique ID (ex. a hash)

**Branch**  \- a parallel version of the codebase. 

- you create a branch to work on a feature or fix without touching the main code, when done, you merge it back.

**Clone** \- downloading a full copy of a remote repo to your machine

**Pull / Push**  \- pull brings remote changes down to you; `push` sends your local commits up to GitHub.

**Pull Request (PR)**  \- a proposal to merge your branch into another 

- this is where code review happens (teammates comment, request changes, and approve)

**Fork** \- your own copy of someone else's repo. Common in open source: you fork, make changes, then submit a PR back to the original

**Merge** \- combining the commit history and changes from one branch into another

## **Best practices**

**Commits**

* Write clear, present-tense messages: "Fix null pointer in auth" not "stuff"  
* Commit small and often (one change per commit)  
* Never commit secrets, API keys, or passwords (use .gitignore and environment variables)

**Branching**

* Keep main (or master) always deployable; don’t commit broken code directly to it  
* Use short-lived feature branches; long-lived branches drift and create painful merges  
* Common naming: feature/login, bugfix/crash-on-load, chore/update-deps

**Pull Requests**

* Keep PRs small and focused; easier to review, faster to merge  
* Write a clear description of what changed and why  
* Link to the related issue (ex. Closes \#42)  
* Request review from the right people; don't leave PRs sitting for days

**Code review**

* Review the logic, not just the style  
* Use GitHub's suggestion feature to propose exact code fixes

**General hygiene**

* Add a .gitignore file to exclude build artifacts, node\_modules, .env files, etc.  
* Use a README.md to explain what the project does and how to set it up  
* Tag releases with semantic versioning (v1.2.0) so you can always find stable points in history

## **Key GitHub Tabs**

(still working on)

**Issues** \- Bug reports, feature requests, and to-do items. You can label, assign, and milestone them

## **General practices**

(Taken from Issue branch Instructions.txt)

Here are the instructions for making a new branch PER ISSUE in your GitHub repository:

**1\. Navigate to Your Repository**  
   \- Go to your repository on GitHub: \[swbn1/ChesapeakeCommunityConnect-FA24\](https://github.com/swbn1/ChesapeakeCommunityConnect-FA24).  
   \- Open your terminal (on macOS or Linux) or Command Prompt (on Windows).

**2\. Clone the Repository (if not already done)**  
   \- If you haven't cloned the repository to your local machine, do so: (If you are writing code you probably have this)  
     git clone https://github.com/swbn1/ChesapeakeCommunityConnect-FA24.git  
     cd ChesapeakeCommunityConnect-FA24

**3\. Create a New Branch**  
   \- To create a new branch, use the \`git checkout \-b\`followed by the name of your issue with your name  
     git checkout \-b the-name-of-your-issue-Gus

After you fix your issue, this is how you will push it back to the main  
     git add .  
     git commit \-m "Fixed this issue: \[This is a short description of what i fixed\]"  
     git push origin the-name-of-your-issue-Gus

After this you will need to do a pull request for the push  
   \- Go to your repository on GitHub.  
   \- You should see a prompt to create a pull request for the newly pushed branch. Click on the "Compare & pull request" button.  
   \- Fill in the details for the pull request, making sure to reference the issue number in the description (e.g., "Fixes \#5").  
   \- Submit the pull request for review.

## **More General Notes**

(Taken from [GitHubCheetsheet.md](http://GitHubCheetsheet.md)) \- added some commands

## **Branch Structure**

* Overview  
  * Branches are separate lines of development within the same repository.  
  * They allow multiple developers to work on features or fixes simultaneously without interfering with each other.  
* Main Branch  
  * Often named `main`, `production`, or `deployed`.  
  * Represents the stable, deployed version of the project.  
  * Do not push or pull directly without permission.  
  * Serves as the final, working version of the code used in production.  
* Integration Branch  
  * Serves as the shared development branch for all contributors.  
  * Pull from this branch when beginning your own development.  
  * Acts as a middle ground between personal branches and `main`.  
  * Everyone’s completed and reviewed work is typically merged here before `main`.  
* Personal Development Branch (`your-branch-name`)  
  * Created from `integration` (or another relevant base).  
  * Used for developing or fixing a specific issue assigned to you.  
  * Do not modify other people’s branches without permission.  
  * Only push to your own branch.  
  * When work is complete, it can be reviewed and merged into `integration`.

## **Issues (Task Management)**

* Purpose  
  * Issues track bugs, feature requests, or tasks in the project.  
  * Each issue represents a specific task to be solved.  
* Claiming Issues  
  * Assign the issue to yourself (or request assignment).  
  * Prevents multiple people from working on the same issue.  
* Creating a Branch for an Issue  
  * In the GitHub issue “Development” section, create a branch.  
  * Set the source branch (usually `integration`).  
  * Locally checkout your branch with: git checkout \-b your-branch-name origin/your-branch-name  
  * This creates a local branch that tracks the remote branch.

## **Basic commands**

**Committing and Pushing Changes**

| git add . | Stages modified files for commit |
| :---- | :---- |
| git commit \-m "Your descriptive commit message" | Records your changes locally with message about commit |
| git push \-u `origin your-branch-name` | Uploads your changes to GitHub |

**Useful GitHub Commands**

| git clone `repository-link` | Clones a GitHub repository to your machine |
| :---- | :---- |
| git branch \-r | Lists all remote branches on GitHub |
| git branch | Lists all branches on your machine, the branch you are on is marked with an asterisk \* |
| git checkout \-b `your-branch-name` | Creates a new local branch and switches to it |
| git fetch origin | Fetches remote updates without changing local files |
| git pull | update your local project with the latest changes from a remote repository |
| git pull origin `branchname` | Fetches and merges updates from a remote branch to your current branch |
| git checkout \-b `branchname origin/branchname` | Creates a local branch that tracks an existing remote branch Useful for viewing or referencing another developers work safely |
| git clone “https repo link” | copy repo locally (once) |
| git checkout \-b “my-feature”   | create & switch to new branch |
| git checkout origin “branch name” | switches you to the branch locally |
| git checkout main (git pull origin main) | Switch to the main branch |
| git merge “branch-name” | Merge branch into main |
| git push origin main | Push changes back into the remote server |
| Git status | Tells if you have uncommitted things that need to be committed, or if there are things that need to be pulled down |

# **Set up VM and VS Code (MAC)**

- Steps I found helpful running the servers on my MacBook

1. **Setting up VM cloud**  
   1. Open google VM   
   2. Go to VM instances tab  
   3. Click the three dots and click start/run machine  
   4. Wait for it to say its started  
2. **Setting up VS code**  
   1. Open VS code  
   2. Go to view and open terminal window  
   3. Next to the \+ icon, hover over the arrow and make sure you’re in pwsh (powershell)  
3. **In terminal screen A (instance-00):**  
   1. Run this command: ssh jyh@35.208.44.247  
      1. **Copy external IP address for instance-00**  
      2. You should now have this as your name in terminal: jyh@jiyoung-hartman-**instance-00**:\~$

4. **In terminal screen B (instance-01):**  
   1. Run this command: ssh jyh@35.208.140.150  
      1. **Copy external IP address for instance-01**  
      2. You should now have this as your name in terminal: jyh@jiyoung-hartman-**instance-01**:\~$

## Accessing websites

1. **CDSpec (instance-01:\~$)**  
   1. **In VS code:**   
      1. cd /home/shared\_workspace/COSC4012020/cd\_spec\_viewer\_web  
      2. python3 manage.py makemigrations  
      3. python3 manage.py migrate  
      4. python3 manage.py runserver  
   2. **In Mac Terminal:**   
      1. ssh \-N \-L 8000:127.0.0.1:8000 jyh@35.208.233.209  
- Note: check external IP address it may change

2. **CCC (instance-00:\~$)**  
   1. **In VS code:**   
      1. cd /home/shared\_workspace/ChesapeakeCommunityConnect/cccSite  
      2. python3 manage.py makemigrations  
      3. python3 manage.py migrate  
      4. python3.10 manage.py runserver 8080  
   2. **In Mac Terminal:**   
      1. ssh \-N \-L 8080:127.0.0.1:8080 jyh@35.208.48.120  
- Note: check external IP address it may change

## To stop websites

1. **In mac terminal,**  
   1.  CTRL+C  
2. **In VS code terminal,**   
   1. CTRL+C  
   2. Exit  
3. **In VM instances**  
   1. Stop all instances  
   2. Wait for them to close

