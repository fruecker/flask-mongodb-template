# flask-mongodb-template
A flask template with mongodb and vue-js for quick start of development.

## Included (preset) dependencies
- bootstrap v5.3
- bootstrap icons v1.9
- vue v2.7

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

EMAIL_ADDR      = "YOUR_EMAIL_ADDRESSE"
EMAIL_PW        = "YOUR_EMAIL_PW_OR_APP_PASSWORD"
EMAIL_SERVER    = "YOUR_EMAIL_HOSTING_SERVER_ADRESSE"
EMAIL_PORT      = "YOUR_EMAIL_HOSTING_PORT"
```

## Run the server (for debug)

`python3 run.py --port 5050`
