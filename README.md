    <table class="table table-bordered" >
          <thead>
            <tr>
              <th class="bg-blue txt-white" style="width: 40px !important; text-align: center;">EDIT</th>
              {% if reviewtype == 'CHECKER' %}
              <th class="bg-blue txt-white" style="width: 300px;">CHECKER ANSWER</th>
              <th class="bg-secondary txt-white" style="width: 200px;">MAKER ANSWER</th>
              <th class="bg-blue txt-white" style="width: auto">CHECKPOINT</th>
             

              {% else %}
              <th class="bg-blue txt-white" style="width: 400px;">MAKER ANSWER</th>
              <th class="bg-blue txt-white" style="width: auto;">CHECKPOINT</th>

                {% if wgroup == 'DOC REVIEW' %}
                <th class="bg-blue txt-white" style="width: 200px">S&I DATE MATCH</th>
                <th class="bg-blue txt-white" style="width: 200px">S&I COC LINKED</th>
                <th class="bg-blue txt-white" style="width: 200px">DOCUMENT ID</th>
                {% endif %}

              {%endif%}





            </tr>
          </thead>
          <tbody>
            {% for q in questionset %}
            {% if q.REMEDIATED == 'YES' %}
            <tr class="chkptremediated tr-print">
            {% elif q.CHECKER_ANSWER == 'FAIL'%}
            <tr class="chkptfail tr-print">
            {% else %}
            <tr class="tr-print">
            {% endif %}  


              <td style="vertical-align: middle;">
                <i class="fa-solid fa-pen-to-square fa-lg txt-green" data-bs-toggle="modal" data-bs-target="#editCheckpointModal{{loop.index}}"></i>
                <a href="{{ url_for('resetanswer', id = q.ID, reviewtype=reviewtype) }}"><i class="fa-solid fa-rotate-left fa-lg ms-1 txt-amber ms-2"></i></a>
                
              </td>
            

              

               <!-- Edit Checkpoint Modal -->
               <div class="modal fade" id="editCheckpointModal{{loop.index}}" data-bs-backdrop="false" data-bs-keyboard="false" tabindex="-1" aria-labelledby="editCheckpointModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="editCheckpointModalLabel">Checkpoint Form</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
            
                            <ul class="nav nav-tabs">
                                <li class="nav-item">
                                    <a class="nav-link nav-link-sm active" id="review-comments-tab-{{loop.index}}" data-bs-toggle="tab" href="#review-comments-{{loop.index}}" aria-current="page">REVIEWER COMMENTS</a>
                                </li>
                                   <li class="nav-item">
                                    <a class="nav-link nav-link-sm" id="dispute-tab-{{loop.index}}" data-bs-toggle="tab" href="#dispute-{{loop.index}}">DISPUTE STATUS</a>
                                </li> 
                             
                                {% if reviewtype == 'CHECKER' %}
                                <li class="nav-item">
                                    <a class="nav-link nav-link-sm" id="remediation-tab-{{loop.index}}" data-bs-toggle="tab" href="#remediation-{{loop.index}}">REMEDIATION</a>
                                </li>
                                {% endif %}
                            </ul>
            
                            <div class="tab-content">
                                <div class="tab-pane fade show active mt-3" id="review-comments-{{loop.index}}" aria-labelledby="review-comments-tab-{{loop.index}}">
                                    <div class="mb-2 row">
                                        <label class="col-sm-2 col-form-label">CHECKPOINT</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                  
                                    <form action="/saveReviewerComments" method="post">
                                      <input type="text" value="{{q.ID}}" name="qid">
                                      <input type="hidden" name="reviewtype" value="{{ reviewtype }}">
                                    <div class="mb-2 row">
                                        <label class="col-sm-2 col-form-label">MAKER COMMENTS</label>
                                        <div class="col-sm-10">
                                      
                                            {% if reviewtype == 'MAKER' %}
                                            <textarea class="form-control" rows="8" name="makercomments" id="">{{ q.MAKER_COMMENTS }}</textarea>
                                            {% else %}
                                            <textarea class="form-control bg-light" rows="8" name="makercomments" id="" readonly>{{q.MAKER_COMMENTS}}</textarea>
                                            {% endif %}
                                        </div>    
                                    </div>                        
                                    
                                    <div class="mb-2 row">
                                        <label class="col-sm-2 col-form-label">CHECKER COMMENTS</label>
                                        <div class="col-sm-10">
                                          {% if reviewtype == 'CHECKER' %}
                                            <textarea class="form-control" rows="8" name="checkercomments" id="">{{q.CHECKER_COMMENTS}}</textarea>
                                            {% else %}
                                            <textarea class="form-control bg-light" rows="8" name="checkercomments" id="" readonly>{{q.CHECKER_COMMENTS}}</textarea>
                                            {% endif %}
                                        
                                          </div>
                                    </div>
                                    <div class="d-flex justify-content-end mb-2">
                                      <button type="submit" class="btn btn-sm btn-success"><i class="fa-solid fa-floppy-disk me-1"></i>SAVE</button>
                                   </div>
                                  </form>
                                </div>
            
                                <div class="tab-pane fade mt-3" id="dispute-{{loop.index}}">
                                    <!-- DISPUTE content here -->
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">RESOLUTION STATUS</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">DISPUTED BY</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">DATE DISPUTED</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">DISPUTE COMMENTS</label>
                                        <div class="col-sm-10">
                                            <textarea class="form-control" rows="8" name="" id="" readonly>{{q.REVIEWER_COMMENTS}}</textarea>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">RESOLVED BY</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">DATE RESOLVED</label>
                                        <div class="col-sm-10">
                                            <input type="text" class="form-control" value="{{q.CHECKPOINT}}" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">RESOLUTION COMMENTS</label>
                                        <div class="col-sm-10">
                                            <textarea class="form-control" rows="8" name="" id="" readonly>{{q.REVIEWER_COMMENTS}}</textarea>
                                        </div>
                                    </div>
                                </div>
            
                                <div class="tab-pane fade mt-3" id="remediation-{{loop.index}}">
                                    <!-- REMEDIATION content here -->
                                    <form action="/saveRemediate" method="post">
                                      <input type="text" value="{{q.ID}}" name="qid" hidden>
                                 
                                     
                                     <div class="mb-1 row">
                                      <label class="col-sm-2 col-form-label">MAKER ANSWER</label>
                                      <div class="col-sm-10">
                                          <input type="text" class="form-control" value="{{q.MAKER_ANSWER}}" readonly>
                                      </div>
                                  </div>
  
                                    <div class="mb-1 row">
                                        <label class="col-sm-2 col-form-label">REMEDIATED</label>
                                        <div class="col-sm-10">
                                            <select class="form-select form-select-sm" id="" name="remediate" required>
                                                <option selected value="{{q.REMEDIATED}}">{{q.REMEDIATED}}</option>
                                                <option value="YES">YES</option>
                                                <option value="NO">NO</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="d-flex justify-content-end mb-2">
                                      <button type="submit" class="btn btn-sm btn-success"><i class="fa-solid fa-floppy-disk me-1"></i>SAVE</button>
                                   </div>
                                    </form>
                                </div>
                            </div>
            
                        </div>
                    </div>
                </div>
            </div>
            
              <td>
                <form id="form{{ loop.index }}" method="POST" action="/updateReviewerAnswer">
                  <input type="hidden" name="id" value="{{ q.ID }}">
                  <input type="hidden" name="reviewtype" value="{{ reviewtype }}">
                  {% if reviewtype == 'CHECKER' %}
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioPASS{{ loop.index }}"
                      value="PASS" {% if q.CHECKER_ANSWER=='PASS' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioPASS{{ loop.index }}">PASS</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioFAIL{{ loop.index }}"
                      value="FAIL" {% if q.CHECKER_ANSWER=='FAIL' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioFAIL{{ loop.index }}">FAIL</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioNA{{ loop.index }}"
                      value="NA" {% if q.CHECKER_ANSWER=='NA' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioNA{{ loop.index }}">NA</label>
                  </div>

                  {% elif q.ANSWER_TYPE == 1 %}
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioYes{{ loop.index }}"
                      value="YES" {% if q.MAKER_ANSWER=='YES' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioYes{{ loop.index }}">YES</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioNo{{ loop.index }}"
                      value="NO" {% if q.MAKER_ANSWER=='NO' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioNo{{ loop.index }}">NO</label>
                  </div>

                  <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" name="radioOption" id="radioNa{{ loop.index }}"
                      value="NA" {% if q.MAKER_ANSWER=='NA' %}checked{% endif %} onchange="this.form.submit()">
                    <label class="form-check-label" for="radioNa{{ loop.index }}">NA</label>
                  </div>

                  {% elif q.ANSWER_TYPE == 2 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="EMEA" {% if q.MAKER_ANSWER=='EMEA' %}selected{% endif %}>EMEA</option>
                    <option value="Canada" {% if q.MAKER_ANSWER=='Canada' %}selected{% endif %}>Canada</option>
                    <option value="US" {% if q.MAKER_ANSWER=='US' %}selected{% endif %}>US</option>
                    <option value="Multi-location" {% if q.MAKER_ANSWER=='Multi-location' %}selected{% endif %}>Multi-location</option>                    
                  </select>
                  
                  {% elif q.ANSWER_TYPE == 3 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="Party Central" {% if q.MAKER_ANSWER=='Party Central' %}selected{% endif %}>Party Central</option>
                    <option value="Constitutional docs" {% if q.MAKER_ANSWER=='Constitutional docs' %}selected{% endif %}>Constitutional docs</option>                    
                  </select>
                  
                  {% elif q.ANSWER_TYPE == 4 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="TPA" {% if q.MAKER_ANSWER=='TPA' %}selected{% endif %}>TPA</option>
                    <option value="SADF" {% if q.MAKER_ANSWER=='SADF' %}selected{% endif %}>SADF</option>
                  </select>       
                  
                  {% elif q.ANSWER_TYPE == 5 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="Single" {% if q.MAKER_ANSWER=='Single' %}selected{% endif %}>Single</option>
                    <option value="Multiple" {% if q.MAKER_ANSWER=='Multiple' %}selected{% endif %}>Multiple</option>
                  </select> 
                  
                  {% elif q.ANSWER_TYPE == 6 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="New" {% if q.MAKER_ANSWER=='New' %}selected{% endif %}>New</option>
                    <option value="Existing" {% if q.MAKER_ANSWER=='Existing' %}selected{% endif %}>Existing</option>
                  </select>   
                  
                  {% elif q.ANSWER_TYPE == 7 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="Purchased" {% if q.MAKER_ANSWER=='Purchased' %}selected{% endif %}>Purchased</option>
                    <option value="Self Sourced" {% if q.MAKER_ANSWER=='Self Sourced' %}selected{% endif %}>Self Sourced</option>
                  </select>       
                  
                  {% elif q.ANSWER_TYPE == 8 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="New" {% if q.MAKER_ANSWER=='New' %}selected{% endif %}>New</option>
                    <option value="Duplicate" {% if q.MAKER_ANSWER=='Duplicate' %}selected{% endif %}>Duplicate</option>
                  </select>  
                  {% elif q.ANSWER_TYPE == 9 %}
                  <select class="form-select form-select-sm" name="dropdownOption" aria-label="Select option"
                    onchange="this.form.submit()">
                    <option value="" {% if q.MAKER_ANSWER=='' %}selected{% endif %}></option>
                    <option value="Full Package" {% if q.MAKER_ANSWER=='Full Package' %}selected{% endif %}>Full Package</option>
                    <option value="Incremental" {% if q.MAKER_ANSWER=='Incremental' %}selected{% endif %}>Incremental</option>
                    <option value="Cash Concentration" {% if q.MAKER_ANSWER=='Cash Concentration' %}selected{% endif %}>Cash Concentration</option>
                    <option value="Product" {% if q.MAKER_ANSWER=='Product' %}selected{% endif %}>Product</option>
                    <option value="Prefilling" {% if q.MAKER_ANSWER=='Prefilling' %}selected{% endif %}>Prefilling</option>
                  </select>                    

                  {% else %}
                  <input type="text" class="form-control form-control-sm" name="textInput" value="{{ q.MAKER_ANSWER }}"
                    placeholder="Enter your answer" onchange="this.form.submit()">
                  {% endif %}

                
              </td>

              {% if reviewtype == 'CHECKER' %}
              <td>{{ q.MAKER_ANSWER }}</td>
              {% endif %}

              <td>{{ q.CHECKPOINT }}</td>

              {% if wgroup == 'DOC REVIEW' %}
              <td>
                <select class="form-select form-select-sm" name="sni_dtmatch" aria-label="Select option"
                onchange="this.form.submit()">
                <option value="" {% if q.SNI_DATE_MATCH=='None' %}selected{% endif %}></option>
                <option value="YES" {% if q.SNI_DATE_MATCH=='YES' %}selected{% endif %}>YES</option>
                <option value="NO" {% if q.SNI_DATE_MATCH=='NO' %}selected{% endif %}>NO</option>
                <option value="NA" {% if q.SNI_DATE_MATCH=='NA' %}selected{% endif %}>NA</option>
              </select>
               
              </td>
              <td>
                <select class="form-select form-select-sm" name="sni_coclinked" aria-label="Select option"
                onchange="this.form.submit()">
                <option value="" {% if q.SNI_COC_LINKED=='None' %}selected{% endif %}></option>
                <option value="YES" {% if q.SNI_COC_LINKED=='YES' %}selected{% endif %}>YES</option>
                <option value="NO" {% if q.SNI_COC_LINKED=='NO' %}selected{% endif %}>NO</option>
                <option value="NA" {% if q.SNI_COC_LINKED=='NA' %}selected{% endif %}>NA</option>
              </select>
               
              </td>

              <td>
                <input type="text" class="form-control form-control-sm" name="sni_docid" value="{{ q.DOC_ID }}"
                placeholder="Document ID" onchange="this.form.submit()">
                
                
              </td>
            </form>
              {% endif %}



            </tr>
            {% endfor %}


          </tbody>
        </table>


@app.route('/saveReviewerComments', methods=['POST'])
def saveReviewerComments():
    qid = request.form['qid']
    print(qid)
    reviewtype = request.form.get('reviewtype')
    makercomments = request.form['makercomments']
    checkercomments = request.form['checkercomments']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE TBL_AUDIT SET MAKER_COMMENTS = ?, CHECKER_COMMENTS = ? WHERE ID = ?',(makercomments,checkercomments,qid))
    conn.commit()

    cursor.close()
    conn.close()
    return redirect(request.referrer)
