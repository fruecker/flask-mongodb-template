# flask-mongodb-template
A flask template with mongodb and vue-js for quick start of development.

## Included (preset) dependencies
- bootstrap v5.0
- bootstrap icons v1.9
- vue v2.7

## Create a new project from this template
```bash
# Set the new project name & remote repo path
new_project_name = 'my_project'
project_remote_repo_path = 'project_repo_url'
# Clone the template repo
git clone https://github.com/fruecker/flask-mongodb-template.git
# Create the new project dir
mkdir $new_project_name
# Copy all template files to new project dir
cp -r flask-mongodb-template/ $new_project_name
# Cleanup the template
rm -r flask-mongodb-template
# Init new github repo
cd $new_project_name
git init
git add . && git commit -m "initial commit"
# If project remote path was set push to remote repository
if [ -z "$project_remote_repo_path" ]
then
    git remote add origin $project_remote_repo_path
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
