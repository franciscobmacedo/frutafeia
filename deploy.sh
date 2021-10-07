#! /bin/bash

# change to deploy branch
git rev-parse --quiet --verify deploy && git checkout deploy|| git checkout -b deploy

# clean static and build the frontend on it
rm -r static
mkdir static
cd frontend && yarn build

# push it and delete branch
git add  ../.
git add -f ../static
git commit -m "deploy"
git push origin deploy
git checkout main
git branch -D deploy

# source env/bin/activate
# python manage.py collectstatic