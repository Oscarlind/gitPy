import argparse
import os
import sys
from github import Github
import github
import configparser


config = configparser.ConfigParser()
config.read("config.ini")
gToken = config.get("variables", "token")
g = Github(gToken)
#g = Github('<TOKEN>')
user = g.get_user()

# Create the parser
parser = argparse.ArgumentParser(prog='gitPy',
                                 usage='%(prog)s [options] ',   
                                 description='Browse your git through the terminal',
                                 formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=80))
# Adding arguments
parser.add_argument('-l', '--repos', 
                    action='store_true',
                    help='List all your repos')
parser.add_argument('-b', '--branches',
                    help='get all branches of a repository',
                    type=str)
parser.add_argument('-r', '--releases',
                    help='get all releases of a repository',
                    type=str)
parser.add_argument('-i', '--issues',
                    help='Get open issues from a repository',
                    type=str)
parser.add_argument('-pr', '--prequest',
                    help='Get open PR\'s from a repository',
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
# Print all repositories with time of last update
  string = "Updated at:"
  for repo in g.get_user().get_repos():
     print(f'{repo.full_name.ljust(50)} {string} {repo.updated_at.strftime("%Y-%m-%d %H:%M:%S").rjust(15)}')
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
# List releases for selected Repository
# -----------------------
def get_releases():
    repo = g.get_repo(args.releases)
    string = "Release:"
    releases = repo.get_releases()
    if releases.totalCount == 0:
        print(f'\033[1m{repo.full_name}\033[0m does not have any releases')
    for release in releases:
        try:
            print(f'{string.ljust(15)} {release.title.center(15)[:15]} {release.created_at.strftime("%Y-%m-%d").rjust(15)}')
        except AttributeError:
            print("Could not catch all releases, aborting")
            sys.exit(1)

# ========================================= #
# List active PR's for selected Repository
# -----------------------
def get_pullRequests():
    repo = g.get_repo(args.prequest)
    string = "Created at:"
    pulls = repo.get_pulls()
    print("Open Pull Requests...")
    print("-"*30)
    if pulls.totalCount == 0:
        print("No Pull Requests found")
    else:
        for pull in pulls:
            print('\x1b]8;;%s\x1b\\%s\x1b]8;;\x1b\\' % ( pull.html_url, pull.title.ljust(70)[:70]), string.center(15), pull.created_at.strftime("%Y-%m-%d"))
        
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
            ( issue.html_url , str(issue.number).center(30) ), "Last update: ", issue.updated_at.strftime("%Y-%m-%d"))
            
# ========================================= #
# Delete a repository
# -----------------------
def delete_repository():
    repo = user.login + "/" + args.delete.replace(" ", "")
    print("Preparing to delete repository ", repo)
    answer = input("Continue? (yes/no) \n")
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
      try:
        get_repos()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.branches:
      try:
        get_branches()
      except github.UnknownObjectException:
          print("Repository not found, please try again") 
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.releases:
      try:
        get_releases()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.issues:
      try:
        list_issues()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.clone:
      try:
        repo_clone()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.init:
      try:
        repo_init()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.delete:
      try:
        delete_repository()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")
    if args.prequest:
      try:
        get_pullRequests()
      except github.BadCredentialsException:
          print("Incorrect or expired token, please add a new one ")

if __name__ == "__main__":
    main()