#coding: UTF-8
import csv #För .csv filhantering
import operator #För sorteringen

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#config
DATABASE = 'data.csv'
globdb = None
app = Flask(__name__)


@app.route("/")


def init():
    global globdb #globala databasen
    globdb = []
    f = open(DATABASE)
    reader = csv.DictReader(f)
    for rows in reader:
        globdb.append(rows)
    globdb = conv_to_unicode(globdb)#Konvertera till UTF-8
    globdb = format_values(globdb)#Formatera databasen
  
 
def conv_to_unicode(data): #Konverterar listan med dicts till UTF-8
    converted_db = []
    for rows in data:
        conv_dict = {}
        for k in rows:
             conv_dict[unicode(k, 'utf-8')] = unicode(rows[k], 'utf-8')
        converted_db.append(conv_dict)    
    return converted_db

def format_values(db): #Formaterar databasvärden efter regler
    for i in xrange(0, len(db)):
        db[i]['project_no'] = int(db[i]['project_no'])
        db[i]['group_size'] = int(db[i]['group_size'])
        if db[i]['techniques_used'] != "":
            db[i]['techniques_used'] =  db[i]['techniques_used'].split(',')
            db[i]['techniques_used'].sort()
        else: db[i]['techniques_used'] = []
    return db
   

def project_count():
    if globdb != None:
        return (0, len(globdb))
    else: return (1 , None)

def lookup_project(search_id):
    if globdb != None:
        db = globdb
        try:
            db = [rows for rows in db if rows['project_no'] == search_id]
            return (0, db[0])
        except: return (2, None)
    else: return (1, None)

def retrieve_techniques():
    if globdb != None:
        techs = []
        temp = []
        for rows in globdb:
            temp.append(rows['techniques_used'])
        #techs = [rows['techniques_used'] for rows in globdb]
        for i in temp:
            for z in i:
                if not z in techs:
                    if z != "":
                        techs.append(z)
        techs.sort()
        return (0, techs)
    else: return (1, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    if globdb != None:
        try:
            db = globdb
            #techniques
            if techniques != None and techniques != []:
                db = [rows for rows in db if len(set(rows['techniques_used']) & set(techniques)) == len(techniques)]
            #search & search_fields
            if search != None and search_fields != None:
                mergedb = []
                # Första sorteringen är för int i dict
                db = [rows for rows in db if [value for value in search_fields if type(rows[value]) == type(1) and str(rows[value]) == search.lower()]]
                # Andra sorteringen är för strängar i dict
                mergedb = [rows for rows in globdb if [value for value in search_fields if type(rows[value]) == type(unicode("string", 'utf-8')) and rows[value].lower() == unicode(search.lower(), 'utf-8')]]
                for i in mergedb: #Lägg till alla i samma lista, db
                    for z in mergedb:
                        if not z in db:
                            db.append(z)
#sort_by & sort_order
            if sort_order == 'acs':
                db.sort(key=operator.itemgetter(sort_by))
            elif sort_order == 'desc': 
                db.sort(key=operator.itemgetter(sort_by), reverse=True)
            return (0 , db)
        except: return(2, None)
    else: return (1, None)

def retrieve_technique_stats():
    if globdb != None:
        db = []
        techs = retrieve_techniques()[1]
        for tec in techs:
            projlist = []
            counter = 0
            x = [rows for rows in globdb if len(set(rows['techniques_used']) & set(tec.split())) == len(tec.split())]
            for y in x:
                projdict = {}
                projdict['id'] = y['project_no']
                projdict['name'] = y['project_name']
                counter += 1
                projlist.append(projdict)
            projlist.sort(key=operator.itemgetter('name'))
            db.append({'count':counter, 'name':tec,'projects':projlist})
        return(0, db)     
    else: return (1, None)

if __name__ == '__main__': #MÅSTE TYDLIGEN VARA LÄNGST NER!!!
    app.run()
