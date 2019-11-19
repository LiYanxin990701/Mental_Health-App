from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
import datetime

from app import app, db, admin
from .models import User

from .forms import UserForm, SUserForm

admin.add_view(ModelView(User, db.session))

# homepage
@app.route("/")
def homepage():
    return render_template('index.html',
                           title='homepage',
                           )

#
@app.route('/create_task', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    form.state = "Uncompleted"
    if form.validate_on_submit():                                             # put the task input by user into form
        # assign the values in form to database
        t = Task(name=form.name.data, year=form.year.data, description=form.description.data, state=form.state)
        # assign the values in form to database
        db.session.add(t)                                                     # add a task in database
        db.session.commit()
        return redirect('/tasks')

    return render_template('create_task.html',
                           title='Create A Task',
                           form=form)


@app.route('/tasks', methods=['GET'])
def getAllTasks():
    tasks = Task.query.all()                                                  # get all tasks from database
    return render_template('task_list.html',
                           title='Task List',
                           tasks=tasks)


@app.route('/completed_task', methods=['GET'])
def getCompletedTasks():
    tasks = Task.query.filter_by(state="Completed").all()                     # get completed tasks
    return render_template('completed_task.html',
                           title='Completed Task List',
                           tasks=tasks)


@app.route('/uncompleted_task', methods=['GET'])
def getUncompletedTasks():
    tasks = Task.query.filter_by(state="Uncompleted").all()                   # get uncompleted tasks
    return render_template('uncompleted_task.html',
                           title='Uncompleted Task List',
                           tasks=tasks)


@app.route('/edit_task/<id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get(id)                                                 # get the parameters of one task
    form = TaskForm(obj=task)                                                 # put this task into form
    if form.validate_on_submit():                                             # edit this task
        t = task
        t.name = form.name.data
        t.year = form.year.data
        t.description = form.description.data
        db.session.commit()
        return redirect('/tasks')
    return render_template('edit_task.html',
                           title='Edit Task',
                           form=form)


@app.route('/delete_task/<id>', methods=['GET'])
def delete_task(id):
    task = Task.query.get(id)                                                 # get the parameters of one task
    db.session.delete(task)
    db.session.commit()                                                       # delete this task from database
    tasks = Task.query.all()                                                  # get all tasks from database now
    a = 0                                                                     # reorder tasks
    for t in tasks:
        a += 1
        t.taskNo = a
    db.session.commit()
    return redirect('/tasks')


@app.route('/change_state/<id>', methods=['GET'])
def change_state(id):
    task = Task.query.get(id)                                                # get the parameters of one task
    t = task
    if t.state == "Uncompleted":                 # change the state of task between completed and uncompleted
        t.state = "Completed"
        db.session.commit()
    elif t.state == "Completed":
        t.state = "Uncompleted"
        db.session.commit()
    return redirect('/tasks')


@app.route('/sort_by_date', methods=['GET'])
def sort_by_date():
    tasks = Task.query.all()
    ntasks = []
    nntasks = []
    for i in tasks:
        s = str(i.year)
        n1 = int(s.split('-')[0])
        n2 = int(s.split('-')[1])
        n3 = int(s.split('-')[2])
        for k in tasks:
            s = str(k.year)
            n4 = int(s.split('-')[0])
            n5 = int(s.split('-')[1])
            n6 = int(s.split('-')[2])
            if n4 < n1 or (n4 == n1 and n5 < n2) or (n4 == n1 and n5 == n2 and n6 < n3):
                ntasks.append(k)
            else:
                ntasks.append(i)
    c = []
    for m in ntasks:
        if m not in c:
            c.append(m)
    b = []
    for m in c:
        num = 0
        for n in range(len(ntasks)):
            if ntasks[n] == m:
                num += 1
        a = []
        a.append(m)
        a.append(num)
        b.append(a)
    for m in range(len(b)):
        for n in range(m,len(b)):
            if b[m][1] < b[n][1]:
                temp = b[m]
                b[m] = b[n]
                b[n] = temp
    nntasks = [x[0] for x in b]

    return render_template('task_nlist.html',
                           title='Task List',
                           tasks=nntasks)


@app.route('/sort_by_date1', methods=['GET'])
def sort_by_date1():
    tasks = Task.query.filter_by(state="Completed").all()
    ntasks = []
    nntasks = []
    for i in tasks:
        s = str(i.year)
        n1 = int(s.split('-')[0])
        n2 = int(s.split('-')[1])
        n3 = int(s.split('-')[2])
        for k in tasks:
            s = str(k.year)
            n4 = int(s.split('-')[0])
            n5 = int(s.split('-')[1])
            n6 = int(s.split('-')[2])
            if n4 < n1 or (n4 == n1 and n5 < n2) or (n4 == n1 and n5 == n2 and n6 < n3):
                ntasks.append(k)
            else:
                ntasks.append(i)
    c = []
    for m in ntasks:
        if m not in c:
            c.append(m)
    b = []
    for m in c:
        num = 0
        for n in range(len(ntasks)):
            if ntasks[n] == m:
                num += 1
        a = []
        a.append(m)
        a.append(num)
        b.append(a)
    for m in range(len(b)):
        for n in range(m,len(b)):
            if b[m][1] < b[n][1]:
                temp = b[m]
                b[m] = b[n]
                b[n] = temp
    nntasks = [x[0] for x in b]

    return render_template('task_nlist1.html',
                           title='Task List',
                           tasks=nntasks)


@app.route('/sort_by_date2', methods=['GET'])
def sort_by_date2():
    tasks = Task.query.filter_by(state="Uncompleted").all()
    ntasks = []
    nntasks = []
    for i in tasks:
        s = str(i.year)
        n1 = int(s.split('-')[0])
        n2 = int(s.split('-')[1])
        n3 = int(s.split('-')[2])
        for k in tasks:
            s = str(k.year)
            n4 = int(s.split('-')[0])
            n5 = int(s.split('-')[1])
            n6 = int(s.split('-')[2])
            if n4 < n1 or (n4 == n1 and n5 < n2) or (n4 == n1 and n5 == n2 and n6 < n3):
                ntasks.append(k)
            else:
                ntasks.append(i)
    c = []
    for m in ntasks:
        if m not in c:
            c.append(m)
    b = []
    for m in c:
        num = 0
        for n in range(len(ntasks)):
            if ntasks[n] == m:
                num += 1
        a = []
        a.append(m)
        a.append(num)
        b.append(a)
    for m in range(len(b)):
        for n in range(m,len(b)):
            if b[m][1] < b[n][1]:
                temp = b[m]
                b[m] = b[n]
                b[n] = temp
    nntasks = [x[0] for x in b]

    return render_template('task_nlist2.html',
                           title='Task List',
                           tasks=nntasks)


@app.route('/today_task', methods=['GET'])
def today_task():
    form = TaskForm()
    # set the value of year as today
    form.year.data = ((datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d"))
    # get today's tasks from database
    tasks = Task.query.filter_by(year=form.year.data).all()         #

    return render_template('today_task.html',
                           title='Today Task',
                           tasks=tasks)


@app.route('/search_task', methods=['GET', 'POST'])
def search_task():
    form = STaskForm()
    if form.validate_on_submit():                                       # input the date which user wants to search
        tasks = Task.query.filter_by(year=form.year.data).all()         # get this day's tasks from database
        return render_template('task_nlist3.html',
                               title='One Day Tasks',
                               tasks=tasks)
    return render_template('search_task.html',
                          title='Search Task',
                          form=form)




