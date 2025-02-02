
import flask
from flask import Blueprint
from flask_paginate import Pagination
import pandas as pd
import os

from flask_login import login_required, current_user
from app.database.models.user import User

from app.decorators import admin_only, under_construction
from app.utils.sites import site_map
from app.utils.times import get_utc_now


# Import module forms
module = Blueprint("admin", __name__, url_prefix="/admin")

@module.route("/")
@login_required
@admin_only
def home():
    return flask.render_template("admin/home.html")


@module.route("/users")
@login_required
@admin_only
def users_list():

    ITEMS_PER_PAGE = 5

    page = flask.request.args.get('page', type=int, default=1)
    items_per_page = flask.request.args.get('ipp', type=int, default=ITEMS_PER_PAGE)
    query = flask.request.args.get('q', '').strip()
    
    if query:
        db_query = User.objects.search_text(query).order_by('$text_score')
    else:
        db_query = User.objects
        
    total_users = db_query.count()
    users = db_query.skip((page - 1) * items_per_page).limit(items_per_page)
    pagination = Pagination(page=page, total=total_users, record_name='users', per_page=items_per_page)
    
    return flask.render_template('admin/user_list.html', users=users, pagination=pagination, last_query=query)
