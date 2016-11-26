# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
def index():
    form=auth.navbar()
    upload_form=SQLFORM(db.D).process()
    form1=SQLFORM.factory(db.De).process()
    reminder_form=SQLFORM(db.Reminder).process()
    search_row=()
    row1=()
    row2=()
    row3=()
    row1=db(db.Reminder.U_ID == auth.user_id).select(orderby=db.Reminder.Importance)
    print row1
    row2=db(db.D.U_ID== auth.user_id).select(orderby=db.D.Importance)
    print row2
    row3=db(db.Sha.R_ID== auth.user_id).select(orderby=db.Sha.D_ID)
    print row3
    if auth.user:
        row1=db(db.Reminder.U_ID == auth.user_id).select(orderby=db.Reminder.Importance)
        print row1
        row2=db(db.D.U_ID== auth.user_id).select(orderby=db.D.Importance)
        print row2
        if form1.accepted:
            print "form=",form1.vars
            if form1.vars.F_ID=="Delete":
                db((db.D.D_ID == form1.vars.D_ID)& (db.D.U_ID == auth.user_id)).delete()
                db((db.Reminder.D_ID == form1.vars.D_ID) & (db.Reminder.U_ID == auth.user_id)).delete()
                redirect(URL('default','index'))
            if form1.vars.F_ID=="Search":
                search_row=db((db.D.D_ID == form1.vars.D_ID) & (db.D.U_ID == auth.user_id)).select()
                if search_row:
                    response.flash="Found"
                else:
                    response.flash="Failed"
    return locals()

def sh():
    sh_form=SQLFORM.factory(db.S)
    print "values"
    row=request.vars
    print row
    if sh_form.process().accepted:
        print "Row new="
        db.D.update_or_insert(U_ID=sh_form.vars.S_ID,C_Date=row.C_Date,D_ID=row.D_ID,Doc=row.Doc,Importance=row.Importance)
        redirect(URL('default','index'))
    return locals()

def share_request():
    s_form=SQLFORM(db.Sha).process()
    if s_form.accepted:
        redirect(URL('default','index'))
    return locals()

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
    if request.args[0]=='profile':
        redirect(URL('default','index'))
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
