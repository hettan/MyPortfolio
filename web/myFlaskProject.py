#coding: UTF-8

from flask import Flask, request, url_for, render_template #For Flask
import data #Import the API
from time import gmtime, strftime #For timestamps in log-file

#config
app = Flask(__name__)

sort_order = "asc"

def add_log(log):
    f = open('myportfolio.log', 'a')
    f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime())+"# " + log + '\n')
    f.close()

def read_error_code(error_code):
    if error_code == 0:
        return "ok"
    elif error_code == 1:
        add_log("error=1")
        return "error accessing data file"
    else:
        add_log("error=2")
        return "requested project does not exist"

@app.route("/")
def layout():
    data.init()
    add_log('database initiated')
    add_log('location=/')
    return render_template('index.html')

@app.route("/project/<proj_id>")
def show_project(proj_id):
    data.init()
    dbdata = data.lookup_project(int(proj_id))
    add_log('database initiated')
    add_log('location=/project/' + proj_id)
    if read_error_code(dbdata[0]) == "ok":
        return render_template('project.html', data = dbdata[1])
    else: return read_error_code(dbdata[0])

@app.route("/list/", methods=['GET','POST'])
def list_projects():
    global sort_order
    data.init()
    add_log('database initiated')
    sort_order = "asc"
    sort_by = "project_name"
    search_fields = []
    search = None
    if request.method == "POST":
       # try
        try:
            if request.form["ok"]:
                #Sort
                sort_by = request.form['sort_by_value']
                sort_order = request.form['sort_order']   
                #Search
                search = request.form['search']
                search = search.encode('ascii')
                for i in xrange(1, 14):
                    try:#Need try to make sure we continue to verify all the search_fields
                        x = 'search_field['+ str(i)+']'
                        search_fields.append(request.form[x])
                    except:
                        pass
                add_log('location=/list/, action initiated: sort_by=' + sort_by + ', sort_order=' + sort_order + ', search=' + search + ', search_fields=' + " ".join(search_fields))
        except: pass
    else: add_log("location=/list/")
    dbdata = data.retrieve_projects(sort_order=sort_order, sort_by=sort_by, search_fields=search_fields, search=search)
    if read_error_code(dbdata[0]) == "ok":
        return render_template('list.html',data = dbdata[1])
    else: return read_error_code(dbdata[0])

@app.route("/techniques/", methods=['GET','POST'])
def techniques():
    data.init()
    dbdata = data.retrieve_technique_stats()
    add_log('database initiated')
    add_log('location=/techniques/')
    if read_error_code(dbdata[0]) == "ok":
        return render_template('techniques.html', data = dbdata[1])
    else: return read_error_code(dbdata[0])

if __name__ == '__main__':
    add_log('****program start****')
    app.run(debug=True)
