import argparse
import os
import sys
from github import Github
import github


# Find a way to do this in a cleaner way?
g = Github('<ADD AUTH TOKEN HERE>')
user = g.get_user()

# Create the parser
parser = argparse.ArgumentParser(prog='gitPy',
                                 usage='%(prog)s [options] ',   
                                 description='Browse your git through the terminal')
# Adding arguments
parser.add_argument('-r', '--repos', 
                    action='store_true',
                    help='List all your repos')
parser.add_argument('-b', '--branches',
                    help='get all branches of a repository - Pass the repository\'s full name',
                    type=str)
parser.add_argument('-i', '--issues',
                    help='Get issues from repository',
                    type=str)
# Perhaps add a path?
parser.add_argument('-c', '--clone',
                    help='Clone a repository',
                    type=str)
parser.add_argument('--init',
                    help='Initiate a new repository',
                    type=str)
parser.add_argument('-d', '--delete',
                    help='Delete a repository',
                    type=str)
args=parser.parse_args()

# Check if user runs script with no arguments
if len(sys.argv) == 1:
    parser.parse_args(['-h'])
# ========================================= #
def get_repos():
# Print all repositories with prog language
  string = "Updated at:"
  for repo in g.get_user().get_repos():
     print(f'{repo.full_name.ljust(50)} {string} {repo.updated_at.strftime("%Y-%m-%d %H:%M:%S").rjust(15)}')
#     print(repo.full_name, "\tLast Update at:", repo.updated_at)
     print("-"*30)


# ========================================= #
# List branch names of selected Repository
# -----------------------
def get_branches():
    repo = g.get_repo(args.branches)
    branches = list(repo.get_branches())
    for branch in branches:
        print(branch.name)

# ========================================= #
# Clone selected Repository, works using ssh cloning
# Change to a Try except and have it try https afterwards?
# -----------------------
def repo_clone():
    repo = g.get_repo(args.clone)
    cmd = "git clone {}".format(repo.ssh_url)
    print("Starting to clone {}".format(repo.name))
    print("Running command '{}'".format(cmd), "\n")
    os.system(cmd)
    print("Finshed cloning {}".format(repo.name), "\n")
    print("#####################################")
    print("")

# ========================================= #
# Init a new repository
# -----------------------
def repo_init():
    user = g.get_user()
    print("Creating repository...")
    new_repo = user.create_repo(args.init)
    repo_path = user.login + "/" + args.init.replace(" ", "")
    repo = g.get_repo(repo_path)
    cmd = "git clone {}".format((repo.ssh_url))
    os.system(cmd)
    print("Repository", repo.name, "cloned")
    print("")

# ========================================= #
# List all (open) issues for a repository
# -----------------------
def list_issues():
    nr = "#"
    open_issues = g.get_repo(args.issues).get_issues(state='open')
    print("Checking for open issues...\n------")
    if open_issues.totalCount == 0:
        print("All clear")
    else:
        for issue in open_issues:
            print(issue.title.ljust(50)[:50], nr, '\x1b]8;;%s\x1b\\%s\x1b]8;;\x1b\\' %
            ( issue.html_url , issue.number ) )
            
# ========================================= #
# Delete a repository
# -----------------------
def delete_repository():
    repo = user.login + "/" + args.delete.replace(" ", "")
    print("Preparing to delete repository ", repo)
    answer = input("Continue? \n")
    if answer.lower() in ["y","yes"]:
        try:
            repo_to_delete = g.get_repo(repo)
            repo_to_delete.delete()
            print(repo_to_delete.full_name, "Deleted")
        except github.UnknownObjectException:
            print("Repository not found - please check the spelling")
            sys.exit(1)
    elif answer.lower() in ["n","no"]:
        print("Aborting")
        sys.exit(1)
    else:
        print("Input not recognized, please write 'y', 'yes' or 'n', 'no'")
        print("Please try again")
        sys.exit(1)

def main():
    if args.repos:
      get_repos()
    if args.branches:
      try:
        get_branches()
      except github.UnknownObjectException:
          print("Repository not found, please try again") 
          sys.exit(1) 
      except github.BadCredentialsException:
          print("Please add an Access token before running")
          sys.exit(1)
    if args.issues:
        list_issues()
    if args.clone:
        repo_clone()
    if args.init:
        repo_init()
    if args.delete:
        delete_repository()

if __name__ == "__main__":
    main()