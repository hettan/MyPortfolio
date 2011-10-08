#coding: UTF-8

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import data

#config
app = Flask(__name__)

sort_order = "asc"

@app.route("/")
def layout():
    data.init()
    return render_template('index.html', data = data.retrieve_projects(techniques=["python"])[1])

@app.route("/project/<proj_id>")
def show_project(proj_id):
    data.init()
    return render_template('project.html', data = data.lookup_project(int(proj_id))[1])

@app.route("/list/", methods=['GET','POST'])
def list_projects():
    global sort_order
    data.init()
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
                    try:
                        x = 'search_field['+ str(i)+']'
                        search_fields.append(request.form[x])
                    except:
                        pass
        except:
            return "error"
    dbdata = data.retrieve_projects(sort_order=sort_order, sort_by=sort_by, search_fields=search_fields, search=search)
    return render_template('list.html',data = dbdata[1])

      #onChange="javascript: submit()
    
    

if __name__ == '__main__':
    app.run(debug=True)
