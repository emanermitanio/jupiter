<form action="/saveReviewerComments" method="post">
                                      <input type="text" value="{{q.ID}}" name="qid">
                                      <input  name="reviewtype" value="{{ reviewtype }}">
                                    <div class="mb-2 row">
                                        <label class="col-sm-2 col-form-label">MAKER COMMENTS</label>
                                        <div class="col-sm-10">
                                            <textarea class="form-control" rows="8" name="makercomments" id="">{{ q.MAKER_COMMENTS }}</textarea>
                                        </div>    
                                    </div>                        
                                    
                                    <div class="mb-2 row">
                                        <label class="col-sm-2 col-form-label">CHECKER COMMENTS</label>
                                        <div class="col-sm-10"> 
                                            <textarea class="form-control" rows="8" name="checkercomments" id="">{{q.CHECKER_COMMENTS}}</textarea>
                                          </div>
                                    </div>
                                    <div class="d-flex justify-content-end mb-2">
                                      <button type="submit" class="btn btn-sm btn-success"><i class="fa-solid fa-floppy-disk me-1"></i>SAVE</button>
                                   </div>
                                  </form>


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
