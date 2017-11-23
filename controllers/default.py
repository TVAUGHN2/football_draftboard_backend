# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.is_logged_in():
        return dict()
    else:
        redirect(URL('user', args='logout', scheme='https'))
        return dict()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

@auth.requires_login()
def save_to_db():
    """
    saves application's state to database (dashboards and player rankings)
    for the current logged in user
    not fully vetted yet as ran out of time
    need enhance so that not inserting user on every save, rather
    updating
    """
    value = request.vars.value
    dbType = request.vars.requestType
    if dbType == 'dashboard':
        db.dashboards.insert(userID = auth.user.email, db_data = value);
    elif dbType == 'ranking':
        db.player_rankings.insert(userID = auth.user.email, ranking_data = value);
    else:
        value = "error: invalid dbType; dbType = " + (dbType + "")
    #redirect(URL('index'), client_side=True);
    return "value = " + value;

@auth.requires_login()
def get_data():
    """
    get either dashboard information or 
    player ranking information form database
    for the logged in user
    not fully vetted as ran out of time
    """
    
    dbType = request.vars.requestType
    if dbType == 'dashboard':
        if db(db.dashboards.userID==auth.user.email).count() > 0:
            ff_data = db(db.dashboards.userID==auth.user.email).select(db.dashboards.db_data).last().as_dict();
        else:
            ff_data = "no data";
    elif dbType == 'ranking':
        if db(db.dashboards.userID==auth.user.email).count() > 0:
            ff_data = db(db.player_rankings.userID==auth.user.email).select(db.player_rankings.ranking_data).last().as_dict();
        else:
            ff_data = "no data";
    else:
        ff_data = "error: invalid dbType"

    return TAG(ff_data);

@auth.requires_login()
def logout():
    """
    logs out user and redirects to https login site
    May be deprecated
    """
    redirect(URL('user', args='logout', scheme='https'))
    return dict()
