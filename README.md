@app.route('/saveReviewerComments', methods=['POST'])
def saveReviewerComments():
    conn = get_db()
    cursor = conn.cursor()

    qid_keys = [key for key in request.form.keys() if key.startswith('qid')]
    for qid_key in qid_keys:
        index = qid_key[3:]  # Get the index part of the key
        qid = request.form[qid_key]
        makercomments = request.form.get(f'makercomments{index}', '')
        checkercomments = request.form.get(f'checkercomments{index}', '')

        cursor.execute(
            'UPDATE TBL_AUDIT SET MAKER_COMMENTS = ?, CHECKER_COMMENTS = ? WHERE ID = ?',
            (makercomments, checkercomments, qid)
        )

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(request.referrer)
