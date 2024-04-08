from flask import Flask, url_for, render_template, request, flash, get_flashed_messages, redirect, session
import sqlite3
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def dbconn():
    conn = sqlite3.connect('wfm.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
    
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/userlogin', methods=['POST'])
def userlogin():
    uid = request.form['usersid'].lower()
    upass = request.form['userpassword']

    qry = '''
        SELECT USERSID, USERNAME, ACCESS_LEVEL, DEPARTMENT, WORKGROUP FROM TBL_USERS WHERE LOWER(USERSID) = ? AND USER_PASSWORD = ?
                '''

    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute(qry, (uid, upass))

    result = cursor.fetchone()
    conn.close()

    if result:
        # Register user to session storage
        usersid, username, access_level, dept, wgroup = result

        session['sess_usersid'] = usersid
        session['sess_username'] = username
        session['sess_accesslevel'] = access_level
        session['sess_department'] = dept
        session['sess_workgroup'] = wgroup

        return redirect('/home')
    else:
        flash('Invalid User SID/Password')
        return render_template('login.html')


@app.route('/home')
def home():
    uid = session.get('sess_usersid')
    if uid:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')
        
        return render_template('home.html',usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup)
    else:
        return redirect('/login')
    
@app.route('/adminchecklist')
def adminchecklist():
    access_level = session.get('sess_accesslevel')
    if access_level == 5:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')

        conn = dbconn()
        cursor = conn.cursor()
        qry = '''SELECT c.DEPARTMENT, 
       c.WORKGROUP, 
       c.CHECKLIST, 
       COALESCE(COUNT(cp.CHKPT_ID), 0) AS Total_Checkpoints 
FROM TBL_CHECKLIST c 
LEFT JOIN TBL_CHECKLIST cp ON c.CHECKLIST = cp.CHECKLIST AND cp.CHKPT_ID IS NOT NULL
GROUP BY c.DEPARTMENT, c.WORKGROUP, c.CHECKLIST;'''
        
        cursor.execute(qry)
        list_checklist = cursor.fetchall()
        
        return render_template('adminchecklist.html',usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup,list_checklist=list_checklist)
    else:
        session.pop('_flashes', None)
        flash('You do not have access to Administrator - Checklist')
        return redirect('/home')
    
@app.route('/createchecklist', methods=['POST'])
def createchecklist():
    
    dept = request.form.get('dept')
    wgroup = request.form.get('wgroup')
    checklist = request.form['checklist']

    conn = dbconn()
    cursor = conn.cursor()
    #check first if checklist name exists
    cursor.execute("SELECT CHECKLIST FROM TBL_CHECKLIST WHERE CHECKLIST = ?", (checklist,))

    r = cursor.fetchone()

    if r:
        flash('Checklist already exists in the database.')
    else:
        qry = '''
        INSERT INTO TBL_CHECKLIST (
            DEPARTMENT,
            WORKGROUP,
            CHECKLIST
        )
        VALUES (
            ?,
            ?,
            ?
        );
        '''
        cursor.execute(qry,(dept,wgroup,checklist))
        conn.commit()
        
        #get checklist

       
        conn.close()
        return redirect('/adminchecklist')

@app.route('/admincheckpoint')
def admincheckpoint():
    var_checklist = request.args.get('checklist')
    var_dept = request.args.get('dept')
    var_wgroup = request.args.get('wgroup')

    access_level = session.get('sess_accesslevel')
    if access_level == 5:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')

        conn = dbconn()
        cursor = conn.cursor()
        qry = '''SELECT * FROM TBL_CHECKLIST
WHERE DEPARTMENT = ? AND WORKGROUP = ? AND CHECKLIST = ? AND CHKPT_ID IS NOT NULL
GROUP BY CATEGORY
ORDER BY SORT ASC;

'''
        
        cursor.execute(qry,(var_dept,var_wgroup,var_checklist))
        list_checkpoints = cursor.fetchall()
        
        return render_template('admincheckpoints.html',usersid=usersid,username=username,access_level=access_level,
                               var_dept=var_dept,var_wgroup=var_wgroup,var_checklist=var_checklist,
                               dept=dept,wgroup=wgroup,list_checkpoints=list_checkpoints)
    else:
        session.pop('_flashes', None)
        flash('You do not have access to Administrator - Checklist')
        return redirect('/home')

@app.route('/createcheckpoint', methods=['POST'])
def createcheckpoint():

    eastern = pytz.timezone('US/Eastern')
    dt_today = datetime.now(eastern).date()
    usersid = session.get('sess_usersid')  

    var_dept = request.form['var_dept']
    var_wgroup = request.form['var_wgroup']
    var_checklist = request.form['var_checklist']
    category = request.form['category']
    question = request.form['question']
    obstemplate = request.form['obstemplate']
    iop = request.form['iop']
    actionitem = request.form['actionitem']
    sort = request.form['sort']
    var_active = 1
    logtype = "CREATE"
    logdate = dt_today
    logby = usersid
    logcomments = "New Checkpoint"
    conn = dbconn()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(MAX(CHKPT_ID), 0) + 1 AS Next_CHKPT_ID FROM TBL_CHECKLIST;")
    var_chkptid = cursor.fetchone()[0]

    qry = '''
        INSERT INTO TBL_CHECKLIST (
CHKPT_ID, DEPARTMENT, WORKGROUP, CHECKLIST, CATEGORY, QUESTION, OBS_TEMPLATE, IOP,
ACTION_ITEM, SORT, ACTIVE, LOG_TYPE, DATE_LOGGED, LOGGED_BY, LOG_COMMENTS
  )
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''
    cursor.execute(qry,(var_chkptid,var_dept,var_wgroup,var_checklist,category,question,obstemplate,iop,
                        actionitem,sort,var_active,logtype,logdate,logby,logcomments))

    conn.commit()
    conn.close()

    return redirect('/admincheckpoint')
if __name__ == '__main__':
    app.run(debug=True, port=8020, host='0.0.0.0')