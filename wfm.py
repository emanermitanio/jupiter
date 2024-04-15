from flask import Flask, url_for, render_template, request, flash, get_flashed_messages, redirect, session, Response
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

        conn = dbconn()
        cursor = conn.cursor()
        cursor.execute("SELECT CHECKLIST FROM TBL_CHECKLIST WHERE CHKPT_ID > 0 GROUP BY CHECKLIST")
        check_list = cursor.fetchall()
        return render_template('home.html',check_list=check_list,usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup)
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
        qry = '''SELECT DEPARTMENT, 
       WORKGROUP, 
       CHECKLIST, 
       COALESCE(COUNT(CHKPT_ID), 0) AS Total_Checkpoints 
FROM TBL_CHECKLIST 

GROUP BY CHECKLIST;'''
        
        cursor.execute(qry)
        list_checklist = cursor.fetchall()
        
        return render_template('adminchecklist.html',usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup,list_checklist=list_checklist)
    else:
        session.pop('_flashes', None)
        flash('You do not have access to Administrator - Checklist')
        return redirect('/home')
    
@app.route('/deletechecklist', methods=['POST'])
def deletechecklist():
    checklist = request.form['checklist']
    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TBL_CHECKLIST WHERE CHECKLIST = ?", (checklist,))
    conn.commit()
    conn.close()

    return redirect(request.referrer)
    
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

@app.route('/deleteOption', methods=['POST'])
def deleteOption():
    optionid = request.form['optionid']

    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TBL_OPTION WHERE ID = ?",(optionid,))
    conn.commit()

    return redirect(request.referrer)

@app.route('/addSelection', methods=['POST'])
def addSelection():
    currURL = request.form['currURL']

    chkptid = request.form['chkptid']
    optionValue = request.form['optionValue']
    optionSort = request.form['optionSort']

    conn = dbconn()
    cursor = conn.cursor()
    qry = '''
    INSERT INTO TBL_OPTION (CHKPT_ID, SELECT_OPTION, ACTIVE, SORT)
    VALUES (
        ?,?,?,?
      );

      '''
    cursor.execute(qry,(chkptid,optionValue,1,optionSort))
    conn.commit()
    conn.close()

    return redirect(currURL)

@app.route('/editcheckpoints')
def editcheckpoints():
    access_level = session.get('sess_accesslevel')
    if access_level == 5:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')

        var_checklist = request.args.get('checklist')
        var_dept = request.args.get('dept')
        var_wgroup = request.args.get('wgroup')
        var_chkptid = request.args.get('chkpt')

        conn = dbconn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM TBL_CHECKLIST WHERE CHKPT_ID = ?", (var_chkptid,))
        checkpointDetails = cursor.fetchall()

        cursor.execute("SELECT ACTIVE FROM TBL_CHECKLIST WHERE CHKPT_ID = ?", (var_chkptid,))
        chkptactive = cursor.fetchone()[0]

        cursor.execute("SELECT o.*,c.* FROM TBL_OPTION o JOIN TBL_CHECKLIST c ON o.CHKPT_ID = c.CHKPT_ID WHERE o.CHKPT_ID = ? ORDER BY o.SORT ASC", (var_chkptid,))
        optionList = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM TBL_OPTION WHERE CHKPT_ID = ?", (var_chkptid,))
        optionCount = cursor.fetchone()[0]
        optionCount = optionCount + 1
        
        return render_template('/editcheckpoints.html',usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup,
                               chkptactive=chkptactive,optionCount=optionCount,optionList=optionList,checkpointDetails=checkpointDetails,var_checklist=var_checklist,var_chkptid=var_chkptid,var_dept=var_dept,var_wgroup=var_wgroup)
    else:
        return redirect('/home')
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
WHERE DEPARTMENT = ? AND WORKGROUP = ? AND CHECKLIST = ?  AND CHKPT_ID IS NOT NULL

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



@app.route('/updatecheckpoint', methods=['POST'])
def updatecheckpoint():
    eastern = pytz.timezone('US/Eastern')
    dt_today = datetime.now(eastern).date()
    usersid = session.get('sess_usersid')  
    
    var_dept = request.form['var_dept']
    var_wgroup = request.form['var_wgroup']
    var_checklist = request.form['var_checklist']

    chkptid = request.form['chkptid']
    category = request.form['category']
    question = request.form['question']
    iop = request.form['iop']
    sort = request.form['sort']
    active = request.form.get('active')
  
    conn = dbconn()
    cursor = conn.cursor()

    qry = '''
        UPDATE TBL_CHECKLIST 
        SET CATEGORY = ?, QUESTION = ?, IOP = ?, SORT = ?, ACTIVE = ?
        WHERE CHKPT_ID = ?

      '''
    cursor.execute(qry,(category,question,iop,sort,active,chkptid))
    conn.commit()
    conn.close()

    return redirect(url_for('admincheckpoint',dept=var_dept,wgroup=var_wgroup,checklist=var_checklist))

@app.route('/deletecheckpoint', methods=['POST'])
def deletecheckpoint():
    chkpt = request.form['chkpt']
    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TBL_CHECKLIST WHERE CHKPT_ID = ?", (chkpt,))
    conn.commit()
    conn.close()

    return redirect(request.referrer)
    

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
CHKPT_ID, DEPARTMENT, WORKGROUP, CHECKLIST, CATEGORY, QUESTION, OBS_TEMPLATE, IOP, SORT, ACTIVE, LOG_TYPE, DATE_LOGGED, LOGGED_BY, LOG_COMMENTS
  )
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
'''
    cursor.execute(qry,(var_chkptid,var_dept,var_wgroup,var_checklist,category,question,obstemplate,iop,
                        sort,var_active,logtype,logdate,logby,logcomments))

    conn.commit()
    conn.close()

    return redirect(url_for('admincheckpoint',dept=var_dept,wgroup=var_wgroup,checklist=var_checklist))


def get_questions():
    cat = session.get('filter_category')

    conn = dbconn()
    cursor = conn.cursor()

    var_checklist = request.args.get('checklist')
    var_case = request.args.get('case')
    var_sid = request.args.get('revsid')

    if cat:
        qry = '''
            SELECT c.QUESTION, a.CHKPT_ID, a.ID, a.REVIEW_RESULT, c.IOP, a.REVIEWER_COMMENTS, a.CASENUMBER, a.DT_REVIEW, c.CHECKLIST, a.SID_REVIEWER, u.USERNAME
            FROM TBL_AUDIT a 
            JOIN TBL_CHECKLIST c ON a.CHKPT_ID = c.CHKPT_ID
            JOIN TBL_USERS u ON a.SID_REVIEWER = u.USERSID
            WHERE a.CASENUMBER = ? AND c.CHECKLIST = ? AND a.SID_REVIEWER = ? AND UPPER(c.CATEGORY)= ?
        '''
        cursor.execute(qry,(var_case,var_checklist,var_sid,cat))
    else:
         qry = '''
            SELECT c.QUESTION, a.CHKPT_ID, a.ID, a.REVIEW_RESULT, c.IOP, a.REVIEWER_COMMENTS, a.CASENUMBER, a.DT_REVIEW, c.CHECKLIST, a.SID_REVIEWER, u.USERNAME
            FROM TBL_AUDIT a 
            JOIN TBL_CHECKLIST c ON a.CHKPT_ID = c.CHKPT_ID
            JOIN TBL_USERS u ON a.SID_REVIEWER = u.USERSID
            WHERE a.CASENUMBER = ? AND c.CHECKLIST = ? AND a.SID_REVIEWER = ?
        '''
         cursor.execute(qry,(var_case,var_checklist,var_sid))
    
    
    questions = cursor.fetchall()
    qna = []
    for question in questions:
        cursor.execute("SELECT SELECT_OPTION FROM TBL_OPTION WHERE CHKPT_ID=?",(question[1],))
        options = cursor.fetchall()
        qna.append((question,options))
    conn.close()  
    return qna         
    

@app.route('/viewrecords')
def viewrecords():

    uid = session.get('sess_usersid')
    if uid:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')
        

        conn = dbconn()
        cursor = conn.cursor()
        qry = '''
            SELECT 
                a.CASENUMBER,
                a.DT_REVIEW,
                a.SID_REVIEWER,
                u.USERNAME,
                c.DEPARTMENT,
                c.WORKGROUP,
                c.CHECKLIST,
                ROUND((CAST(SUM(CASE WHEN a.REVIEW_RESULT IS NOT NULL THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100, 2) AS COMPLETION_RATE
            FROM 
                TBL_AUDIT a
            JOIN 
                TBL_CHECKLIST c ON a.CHKPT_ID = c.CHKPT_ID
            JOIN 
                TBL_USERS u ON a.SID_REVIEWER = u.USERSID 
            GROUP BY 
                a.CASENUMBER, c.CHECKLIST
            ORDER BY DT_REVIEW DESC
            '''
        cursor.execute(qry)
        records = cursor.fetchall()

        cursor.execute("SELECT CHECKLIST FROM TBL_CHECKLIST WHERE CHKPT_ID > 0 GROUP BY CHECKLIST")
        check_list = cursor.fetchall()

        return render_template('viewrecords.html',check_list=check_list,records=records,usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup)

    else:
        return redirect('/login') 

@app.route('/showallcheckpoints')
def showallcheckpoints():
    session.pop('filter_category', None)
    return redirect(request.referrer)

@app.route('/filtercategory')
def filtercategory():
     session['filter_category'] = request.args.get('cat')
     return redirect(request.referrer)

@app.route('/myworkflow', methods=['GET', 'POST'])
def myworkflow():
    

    
    uid = session.get('sess_usersid')
    if uid:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')

        session['args_checklist'] = request.args.get('checklist')
        session['args_case'] = request.args.get('case')
        session['args_revsid'] = request.args.get('revsid')
        session['args_revname'] = request.args.get('revname')
        session['args_revdt'] = request.args.get('revdt')

        checklist = request.args.get('checklist')
        case = request.args.get('case')
        sid = request.args.get('revsid')
        revname = request.args.get('revname')
        revdt = request.args.get('revdt')

        
        if request.method == 'POST':
            selected_options = {key[8:]: value for key, value in request.form.items() if key.startswith('question')}
            print(selected_options)
            return redirect(url_for('/myworkflow'))
        
        questions = get_questions()

        conn = dbconn()
        cursor = conn.cursor()

        qry = '''
        SELECT UPPER(c.CATEGORY) AS CATEGORY
        FROM TBL_AUDIT a 
        JOIN TBL_CHECKLIST c ON a.CHKPT_ID = c.CHKPT_ID
        WHERE a.CASENUMBER = ? AND c.CHECKLIST = ? AND a.SID_REVIEWER = ?
        GROUP BY c.CATEGORY
        '''
        cursor.execute(qry,(case,checklist,usersid))
        category = cursor.fetchall()
        cat = session.get('filter_category')
        

        return render_template('myworkflow.html', questions=questions, usersid=usersid,username=username,access_level=access_level,dept=dept,wgroup=wgroup,
                               checklist=checklist,case=case,sid=sid,revname=revname,revdt=revdt, category=category,cat=cat)

    else:
        return redirect('/login') 
 

@app.route('/update_record', methods=['POST'])
def update_record():
    selected_option = request.form['selected_option']
    question_id = request.form['question_id']
    chkpt_id = request.form['chkpt_id']



    checklist = session.get('args_checklist')
    case = session.get('args_case')
    revdt = session.get('args_revdt')
    revsid = session.get('args_revsid')
    revname = session.get('args_revname')
   



    # Check if selected_option is None (meaning it's not a direct form field)
    if selected_option is None:
        # Try to get the selected option from the options dict
        selected_option = request.form.get('option_selected')

  
    conn = dbconn()
    cursor = conn.cursor()
    #update question level first
    cursor.execute("UPDATE TBL_AUDIT SET REVIEW_RESULT = ? WHERE ID = ?", (selected_option, question_id))
    conn.commit()  # Don't forget to commit the transaction after executing the query

   # Get list of tasks
    cursor.execute("SELECT SQLCODE FROM TBL_WORKFLOW WHERE OPTION_TRIGGER = ? AND CHKPT_TRIGGER = ?", (selected_option, chkpt_id))
    wlist = cursor.fetchall()

    #run only if there is an existing workflow
    if wlist:

        for query_row in wlist:
            sql_query = query_row[0]  # Get the SQL query for the current iteration   
            print("Executing SQL Query with Parameters:", sql_query, "(", case, ",", revdt, ")")
           
            try:
                cursor.execute(sql_query, (case, revdt))
                conn.commit()
            except sqlite3.Error as e:
                print("Error executing query:", e)
   
    conn.close()
    return redirect(url_for('myworkflow',case=case,checklist=checklist,revsid=revsid,revname=revname,revdt=revdt))


@app.route('/addrevcomments', methods=['POST'])
def addrevcomments():
     
    checklist = session.get('args_checklist')
    case = session.get('args_case')
    revdt = session.get('args_revdt')
    revsid = session.get('args_revsid')
    revname = session.get('args_revname')

    revcomments = request.form['revcomments']
    recordid = request.form['recordid']

    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute("UPDATE TBL_AUDIT SET REVIEWER_COMMENTS = ? WHERE ID = ?", (revcomments, recordid))
    conn.commit()
    conn.close()
     
    return redirect(url_for('myworkflow',case=case,checklist=checklist,revsid=revsid,revname=revname,revdt=revdt))

@app.route('/createworkflow', methods=['POST'])
def createworkflow():
    usersid = session.get('sess_usersid')
    revname = session.get('sess_username')    
    checklist = request.form.get('checklist')
    casenumber = request.form['casenumber']
    
    
    eastern = pytz.timezone('US/Eastern')
    dt_rev = datetime.now(eastern).date()

    conn = dbconn()
    cursor = conn.cursor()
    qry = '''
    INSERT INTO TBL_AUDIT (CHKPT_ID, CASENUMBER, DT_REVIEW, SID_REVIEWER)
            SELECT
                CHKPT_ID,
                ? AS CASENUMBER, 
                ? AS DT_REVIEW,
                ? AS SID_REVIEWER

            FROM TBL_CHECKLIST
            WHERE CHECKLIST = ? AND ACTIVE = 1 AND CHKPT_ID > 0
    '''
    cursor.execute(qry,(casenumber, dt_rev, usersid, checklist))
    conn.commit()

    return redirect(url_for('myworkflow', case=casenumber, checklist=checklist, revsid=usersid, revname=revname, revdt=dt_rev))


@app.route('/createtask')
def createtask():
    var_checklist = request.args.get('checklist')
    var_dept = request.args.get('dept')
    var_wgroup = request.args.get('wgroup')
    var_chkptid = request.args.get('chkpt')
    var_opt = request.args.get('opt')
    checkpoint = request.args.get('checkpoint')

    access_level = session.get('sess_accesslevel')
    if access_level == 5:
        usersid = session.get('sess_usersid')   
        username = session.get('sess_username')
        access_level = session.get('sess_accesslevel')
        dept = session.get('sess_department')
        wgroup = session.get('sess_workgroup')


        conn = dbconn()
        cursor = conn.cursor()
        q = '''
            SELECT CHKPT_ID, QUESTION FROM TBL_CHECKLIST WHERE CHECKLIST = ? AND CHKPT_ID > 0
            '''
        cursor.execute(q,(var_checklist,))
        qlist = cursor.fetchall()

        q = '''
            SELECT o.ID, o.CHKPT_ID, SELECT_OPTION FROM TBL_OPTION o JOIN TBL_CHECKLIST c ON c.CHKPT_ID = o.CHKPT_ID WHERE c.CHECKLIST = ?
            '''
        cursor.execute(q,(var_checklist,))
        olist = cursor.fetchall()

        cursor.execute("SELECT ID, SELECT_OPTION, CHKPT_ID FROM TBL_OPTION WHERE ID = ?", (var_opt,))
        result = cursor.fetchone()
        opttriggerid = result[0]
        opttrigger = result[1]
        chkpt = result[2]

        qry = '''
            SELECT w.*, c.QUESTION FROM TBL_WORKFLOW w 
            JOIN TBL_CHECKLIST c ON w.CHKPT_TARGET = c.CHKPT_ID
            WHERE w.OPTION_TRIGGER = ? AND CHKPT_TRIGGER = ?
            '''
        cursor.execute(qry,(opttrigger,var_chkptid))
        worklist = cursor.fetchall()

        conn.close()
        return render_template('createtask.html',var_dept=var_dept,var_wgroup=var_wgroup,var_checklist=var_checklist,
                            var_chkptid=var_chkptid,var_opt=var_opt,checkpoint=checkpoint,
                            qlist=qlist,olist=olist,opttrigger=opttrigger,opttriggerid=opttriggerid,chkpt=chkpt,worklist=worklist,
                            usersid=usersid,username=username,dept=dept,wgroup=wgroup)
    else:
        return redirect('/home')
@app.route('/deleteactivity', methods=['POST'])
def deleteactivity():
    id = request.form['activityid']
    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TBL_WORKFLOW WHERE ID = ?",(id,))
    conn.commit()
    conn.close()
    return redirect(request.referrer)


@app.route('/addtaskitem1', methods=['POST'])
def addtaskitem1():
    # Get form inputs

    checklist = request.args.get('checklist')
    dept = request.args.get('dept')
    wgroup = request.args.get('wgroup')
    chkpt = request.form['chkpt']
    worktype = 'AUTO UPDATE CHECKPOINT'
    targetchkpt = request.form.get('targetCheckpoint')
    targetoutput = request.form.get('targetoutput')
    targetcomments = request.form['targetcomments']
    opttrigger = request.form['opttrigger']
    opttriggerid = request.form['opttriggerid']
    currURL = request.form['currURL']

    # Concatenate SQL query string
    sqlcode = "UPDATE TBL_AUDIT SET REVIEW_RESULT = '" + targetoutput + "', REVIEWER_COMMENTS = '" + targetcomments + "' WHERE CHKPT_ID = '" + targetchkpt + "' AND CASENUMBER = ? AND DT_REVIEW = ?"

    qry = '''
INSERT INTO TBL_WORKFLOW (
    WORKFLOW_TYPE,
    TASK_CODE,
    OPTION_ID,
    OPTION_TRIGGER,
    CHKPT_TRIGGER,
    CHKPT_TARGET,
    TARGET_OUTPUT,
    TARGET_COMMENTS,
    SQLCODE
  )
VALUES (?,?,?,?,?,?,?,?,?);
            '''
    
    conn = dbconn()
    cursor = conn.cursor()
    cursor.execute(qry,(worktype,'AUTO UPDATE',opttriggerid,opttrigger,chkpt,targetchkpt,targetoutput,targetcomments,sqlcode))
    conn.commit()
    conn.close

    # Return a test response
    return redirect(currURL)



if __name__ == '__main__':
    app.run(debug=True, port=8020, host='0.0.0.0')