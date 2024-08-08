<form action="/saveReviewerComments" method="post">
  <input type="hidden" value="{{ q.ID }}" name="qid">
  <input type="hidden" name="reviewtype" value="{{ reviewtype }}">
  <div class="mb-2 row">
    <label class="col-sm-2 col-form-label">MAKER COMMENTS</label>
    <div class="col-sm-10">
      <textarea class="form-control" rows="8" name="makercomments" id="makercomments{{ loop.index }}">{{ q.MAKER_COMMENTS }}</textarea>
    </div>    
  </div>                        
  <div class="mb-2 row">
    <label class="col-sm-2 col-form-label">CHECKER COMMENTS</label>
    <div class="col-sm-10"> 
      <textarea class="form-control" rows="8" name="checkercomments" id="checkercomments{{ loop.index }}">{{ q.CHECKER_COMMENTS }}</textarea>
    </div>
  </div>
  <div class="d-flex justify-content-end mb-2">
    <button type="submit" class="btn btn-sm btn-success"><i class="fa-solid fa-floppy-disk me-1"></i>SAVE</button>
  </div>
</form>
