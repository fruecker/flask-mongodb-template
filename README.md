# flask-mongodb-template
A flask template with mongodb and vue-js for quick start of development.

## Included (preset) dependencies
- bootstrap v5.0
- bootstrap icons v1.9
- vue v2.7

## Create a new project from this template
```bash
setopt interactive_comments
NEW_PROJECT_NAME='my_project'
PROJECT_REMOTE_REPO_PATH='project_repo_url'
git clone https://github.com/fruecker/flask-mongodb-template.git
mkdir $NEW_PROJECT_NAME
cp -r flask-mongodb-template/ $NEW_PROJECT_NAME
rm -rf flask-mongodb-template
cd $NEW_PROJECT_NAME
rm -rf .git
git init -b main
git add . && git commit -m "initial commit"
if [ "${PROJECT_REMOTE_REPO_PATH+x}" ]
then
    git remote add origin $PROJECT_REMOTE_REPO_PATH
    git push -u origin main
fi
```

## Install requirements

`pip3 install -r requirements.txt`

## Set up env variables

Create a file `.env` on root dir.
Then fill it accordingly.
```
APP_SECRET  = "SUPER_SECRET"

DB_USER     = "YOUR_DB_USER"
DB_PW       = "YOUR_DB_PASSWORD"
DB_NAME     = "YOUR_DESTINATED_DATABASE"
DB_CLUSTER  = "YOUR_DB_CLUSTER"
```

## Run the server (for debug)

`python3 run.py --port 5050`
