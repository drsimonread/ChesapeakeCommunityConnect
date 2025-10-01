Git Commands Reference
======================

Order of Operations: 
----------------------
cd repo-name
# Get into correct repository
git branch
# Checks which branch you're on
git pull origin main
# Pulls files from main branch
git checkout -b [your_branch]
# will make a new branch after this the first time do git switch [your_branch]
git status
# Checks current status; once changes are made they will be highlighted in red
git add filename.txt
# Adds that file to the branch changes
git add .   
# stages all changes
git commit -m "[Add detailed explanation of the change]"
# Commits those changes to the branch
git push -u origin feature-branch-name
# Pushes changes to that branch

Cheat Sheet:
----------------------
git init
    Initializes a new Git repository in the current directory.

git clone <repository_url>
    Creates a local copy of a remote repository.

git status
    Shows the status of changes as untracked, modified, or staged.

git add <file>
    Stages a file for the next commit.

git add .
    Stages all modified and new files in the current directory.

git commit -m "message"
    Commits the staged changes with a descriptive message.

git log
    Displays the commit history.

git diff
    Shows changes between working directory and the staging area.

git diff --staged
    Shows changes between staging area and the last commit.

git branch
    Lists all local branches.

git branch <branch_name>
    Creates a new branch.

git checkout <branch_name>
    Switches to the specified branch.

git checkout -b <branch_name>
    Creates a new branch and switches to it immediately.

git merge <branch_name>
    Merges the specified branch into the current branch.

git pull
    Fetches changes from the remote repository and merges them into the current branch.

git fetch
    Downloads objects and refs from a remote repository without merging.

git push
    Uploads local commits to the remote repository.

git remote -v
    Displays remote repositories linked to the project.

git reset <file>
    Unstages a file without deleting its changes.

git reset --hard <commit>
    Resets the repository to the specified commit, discarding all changes.

git rm <file>
    Removes a file from the working directory and stages the deletion.

git stash
    Temporarily saves uncommitted changes.

git stash pop
    Restores the most recently stashed changes.

git tag <tag_name>
    Creates a tag for the current commit.

git show <commit_or_tag>
    Displays information about a commit or tag.

git reflog
    Shows a log of all actions (useful for finding lost commits).
