procedure for deploying/installing ckan and ckanexts

## DEFINITIONS
# REPONAME = the name of the repository to clone from github
# DEPLOY_TARGET = the name of the server (ckan instance) to deploy to


## Setup
on ${DEPLOY_TARGET} as user ckan:
1. create bare repository (git init --bare ~/git/${REPONAME}.git)
2. create hooks/post-receive (cp ~/git/ckan.git/hooks/post-receive ~/git/${REPONAME}.git/hooks)

on local machine
3. pull repo from github (git clone https://github.com/ckan/${REPONAME})
4. create branch deploy-int and checkout (git branch deploy && git checkout deploy-int)
5. add remote (git remote add deploy-int ckan@${DEPLOY_TARGET}:git/${REPONAME}.git)
6. set upstream and push (git push --set-upstream deploy-int deploy-int:main) 

## Usage
to deploy changes:
7. git push deploy-int deploy-int:main

Repeat for eric open (but use branch deploy-ext)

## Development
git branch dev && git checkout dev

#do the work, when done:

git checkout deploy-int && git merge dev deploy-int
