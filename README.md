# gitPy
A tool for to keep track on things on github. Lets you list your own repositories, query repositories for information such as branches, PR's and issues. Also allow for cloning and creating new repositories.


Currently very much a work in progress :)
## How it works
Currently you will have to add an GitHub Authentication token to the script before running.

The tool expects certain arguments when run.

```bash
usage: gitPy [options] 

Browse your git through the terminal

optional arguments:
  -h, --help                         show this help message and exit
  -l, --repos                        List all your repos
  -b BRANCHES, --branches BRANCHES   get all branches of a repository
  -r RELEASES, --releases RELEASES   get all releases of a repository
  -i ISSUES, --issues ISSUES         Get open issues from a repository
  -pr PREQUEST, --prequest PREQUEST  Get open PR's from a repository
  -c CLONE, --clone CLONE            Clone a repository
  --init INIT                        Initiate a new repository
  -d DELETE, --delete DELETE         Delete a repository
```
