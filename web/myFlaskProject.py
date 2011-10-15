#coding: UTF-8

from flask import Flask, request, url_for, render_template #Need this to use Flask
import data #Import the API
from time import gmtime, strftime #For timestamps in log-file

#config
app = Flask(__name__)

def add_log(log): #Used for writing in logfile
    f = open('myportfolio.log', 'a')
    f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"# " + log.encode('utf-8') + '\n')
    f.close()

def read_error_code(error_code):#Converts error-codes to error-messages
    if error_code == 0:
        return "ok"
    elif error_code == 1:
        add_log("error=1")
        return "error accessing data file"
    else:
        add_log("error=2")
        return "requested project does not exist"

@app.route("/")
def layout(): #For the static main/index page
    data.init()
    add_log('location=/')
    return render_template('main.html')

@app.route("/project/<proj_id>")
def show_project(proj_id): #Sends requested project to template
    try:
        data.init()
        dbdata = data.lookup_project(int(proj_id))
        add_log('location=/project/' + proj_id)
        if read_error_code(dbdata[0]) == "ok":
            return render_template('project.html', data = dbdata[1])
        else: return read_error_code(dbdata[0])
    except: return "Only accept digit as project number" #Exeption if string can't be converted to int, only accept digits

@app.route("/list/", methods=['GET','POST'])
def list_projects(): #Handles the search/sort/filter function and return result to template
    data.init()
    ###Standard values for data.retrieve_projects()
    sort_order = "asc"
    sort_by = "project_name"
    search_fields = []
    search = ""
    filter_techniques = []
    ###End standard values
    techniques = data.retrieve_techniques()[1]#Used for the filtering and listing all techniques

    if request.method == "POST":
        if request.form["ok"]:
            search = request.form['search']
            if len(search) > 0:
                for i in xrange(1, 14):
                    checkbox_name = 'search_field['+ str(i)+']'
                    if request.form.has_key(checkbox_name):
                        search_fields.append(request.form[checkbox_name])
            #Sort
            sort_by = request.form['sort_by_value']
            sort_order = request.form['sort_order']
            #Filter techniques
            for tech in techniques:
                if request.form.has_key(tech):
                    filter_techniques.append(tech)
            add_log('location=/list/, action initiated: sort_by=' + sort_by + ', sort_order=' + sort_order + ', search=' +search + ', search_fields=' + " ".join(search_fields) + ', techniques=' + " ".join(filter_techniques))

    else: add_log("location=/list/")
    dbdata = data.retrieve_projects(sort_order=sort_order, sort_by=sort_by, search_fields=search_fields, search=search.encode('utf-8'), techniques=filter_techniques)
    if read_error_code(dbdata[0]) == "ok":
        return render_template('list.html',data = dbdata[1], techniques = techniques)
    else: return read_error_code(dbdata[0])

@app.route("/techniques/", methods=['GET','POST'])
def techniques(): #Sends all techniques used to template
    data.init()
    dbdata = data.retrieve_technique_stats()
    add_log('location=/techniques/')
    if read_error_code(dbdata[0]) == "ok":
        return render_template('techniques.html', data = dbdata[1])
    else: return read_error_code(dbdata[0])

if __name__ == '__main__':
    add_log('****program start****')
    app.run(debug=True)
