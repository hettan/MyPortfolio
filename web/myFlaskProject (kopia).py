#coding: UTF-8
import csv

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#config
DATABASE = 'data.csv'
globdb = None
app = Flask(__name__)


@app.route("/")
def show_projects(db):
    show_db = [] #Denna variabel kommer användas för datan som skickas till Jinja2
    #db = read_db()
    #db = conv_to_utf8(db)
    #db = search_db(db, 'project_no', '2')
    show_db.append(db[0].keys()) #Lägger till nycklarna först i listan
    for rows in db:
        show_db.append(rows.values())
    print show_db
    #return render_template('show_entries.html', entries=show_db)


def init():
    global globdb #globala databasen
    globdb = []
    f = open(DATABASE)
    reader = csv.DictReader(f)
    for rows in reader:
        globdb.append(rows)
    globdb = conv_to_utf8(globdb)
  
 
def conv_to_utf8(data): #Konverterar listan med dicts till UTF-8
    converted_db = []
    for rows in data:
        conv_dict = {}
        for k in rows:
             conv_dict[unicode(k, 'utf-8').lower()] = unicode(rows[k].lower(), 'utf-8')
        converted_db.append(conv_dict)    
    return converted_db
   

def search_db(db, field, value):
    x = [rows for rows in db if rows[field] == value]
    return x

def project_count():
    if globdb != None:
        return (0, len(globdb))
    else: return (1 , None)

def lookup_project(search_id):
    if globdb != None:
        db = globdb
        try:
            db = [rows for rows in db if rows['project_no'] == str(search_id)]
            show_projects(db)
            return (0, db)
        except: return (2, None)
    else: return (1, None)

def retrive_techniques():
    if globdb != None:
        techs = []
        test = []
        for rows in globdb:
            test.append([value for value in rows['techniques_used'].split(',')])
        for i in test:
            for z in i:
                if not z in techs:
                    techs.append(z)              
        return (0, techs)
    else: return (1, None)

def retrive_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    if globdb != None:
        try:
            db = globdb
            #techniques
            if techniques != None:
                db = [rows for rows in db if not len(set(rows['techniques_used'].split(',')) & set(techniques.split(','))) == len(techniques.split())]
            #search & search_fields
            if search != None and search_fields != None:
                db = [rows for rows in db if rows[search_fields] == search]
            #sort_by & sort_order
            if sort_order == 'acs': 
                db.sort(key=operator.itemgetter(sort_by))
            elif sort_order == 'desc': 
                db.sort(key=operator.itemgetter(sort_by), reverse=True)
            return (0 , db)
        except: return(2, None)
    else: return (1, None)


if __name__ == '__main__': #MÅSTE TYDLIGEN VARA LÄNGST NER!!!
    app.run()
