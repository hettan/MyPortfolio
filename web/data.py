#coding: UTF-8
import csv #For the .csv data
import operator #Used in the sorting

DATABASE = 'data.csv' #Defines the name of the datafile
globdb = None #Storing the database

def init(): #Initialize the database
    global globdb #global database
    globdb = []
    f = open(DATABASE)
    reader = csv.DictReader(f)
    for rows in reader:
        globdb.append(rows)
    globdb = conv_to_unicode(globdb)#Convert to UTF-8
    globdb = format_values(globdb)#Format database to correct format
  
 
def conv_to_unicode(data): #Convert all dicts to UTF-8
    converted_db = []
    for dic in data:
        conv_dict = {}
        for row in dic:
             conv_dict[unicode(row, 'utf-8')] = unicode(dic[row], 'utf-8')
        converted_db.append(conv_dict)    
    return converted_db

def format_values(db): #Format database values according to rules in this function
    for i in xrange(0, len(db)):
        db[i]['project_no'] = int(db[i]['project_no'])
        db[i]['group_size'] = int(db[i]['group_size'])
        if db[i]['techniques_used'] != "":
            db[i]['techniques_used'] =  db[i]['techniques_used'].split(',')
            db[i]['techniques_used'].sort()
        else: db[i]['techniques_used'] = []
    return db
   

def project_count(): #Count all projects
    if globdb != None:
        return (0, len(globdb))
    else: return (1 , None)

def lookup_project(search_id): #Lookup a specified project
    if globdb != None:
        db = globdb
        try:
            db = [rows for rows in db if rows['project_no'] == search_id]
            return (0, db[0])
        except: return (2, None)
    else: return (1, None)

def retrieve_techniques(): #Lists all techniques
    if globdb != None:
        techs = []
        compare_techs = [] #Used as a temporary variable
        for dic in globdb:
            compare_techs.append(dic['techniques_used'])
        for row in compare_techs:
            for value in row:
                if not value in techs:
                    if value != "":
                        techs.append(value)
        techs.sort()
        return (0, techs)
    else: return (1, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None): #Search/sort all projects matching criterias
    if globdb != None:
        try:
            db = globdb
            #techniques
            if techniques != None and techniques != []:
                db = [rows for rows in db if len(set(rows['techniques_used']) & set(techniques)) == len(techniques)]
                db_tech = db #db_tech is used for the search
            else: db_tech=globdb
        
            #search & search_fields
            if search != None and search_fields != None and search != "" and search_fields != []:
                mergedb = []
                # First sorting is for integers in dict
                db = [rows for rows in db_tech if [value for value in search_fields if type(rows[value]) == type(1) and str(rows[value]) == search.lower()]]
                # Second sorting is for strings in dict
                mergedb = [rows for rows in db_tech if [value for value in search_fields if type(rows[value]) == type(unicode("string", 'utf-8')) and rows[value].lower() == unicode(search.lower(), 'utf-8')]]
 
#Add the results to main db
                for dic in mergedb:
                    if not dic in db:
                        db.append(dic)
            #sort_by & sort_order
            if sort_order == 'asc':
                db.sort(key=operator.itemgetter(sort_by))
            elif sort_order == 'desc': 
                db.sort(key=operator.itemgetter(sort_by), reverse=True)
            return (0 , db)
        except: return(2, None)
    else: return (1, None)

def retrieve_technique_stats(): #Check the stats for each used technique
    if globdb != None:
        db = []
        techs = retrieve_techniques()[1]
        for tech in techs:
            proj_list = []
            counter = 0
            proj_match = [dic for dic in globdb if len(set(dic['techniques_used']) & set(tech.split())) == len(tech.split())] #Generates a list with all projects matching the technique
            for proj in proj_match:
                proj_dict = {}
                proj_dict['id'] = proj['project_no']
                proj_dict['name'] = proj['project_name']
                counter += 1
                proj_list.append(proj_dict)
            proj_list.sort(key=operator.itemgetter('name'))
            db.append({'count':counter, 'name':tech,'projects':proj_list})
        return(0, db)     
    else: return (1, None)
