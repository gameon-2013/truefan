# First things first
Install heroku toolbelt, pip and virtualenv

# Clone the truefan repository 
If you are reading this then am assuming this is already done :)

    $ git clone https://gameon@bitbucket.org/gameon/truefan.git

# Setup virtualenv

    $ cd truefan
    $ virtualenv --distribute venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt

# Setting up staging and production to work together
Ideally what we want is staging branch pushes to staging environment while master branch pushes to production environment.
We also want to make sure that we can push to both bitbucket and heroku.

  * Setup the git remotes

#

    $ heroku git:remote -a truefan
    $ heroku git:remote -r heroku-staging -a truefan-staging

  * Create a staging branch and set it to track staging on bitbucket.

#

    $ git branch --set-upstream-to staging origin/staging


# Working on and committing your code
  * Remember that you should **ALWAYS** be working from the staging branch

#

    $ git checkout staging
    $ git pull

  * When done working on your code and ready to push, **ALWAYS** push to staging first for testing before pushing to production

#  
    $ git push origin staging
    $ git push heroku-staging staging:master

  * Once things have been tested you can then push to production

#

    $ git checkout master
    $ git merge staging
    $ git push origin master
    $ git push heroku master

# Recommended
  * Install SublimeText
  * Using SublimeText
    * Install package control. http://wbond.net/sublime_packages/package_control#Features
    * Use package control to install the sublimelinter plugin

