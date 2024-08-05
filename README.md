<div class="row">
    <div class="mb-3 col-3">
        <label class="form-label" style="margin: 0 !important; font-size: small; font-weight: bold;">WORKGROUP</label>
        <select id="workgroupSelect" class="form-select form-select-sm">
            <option value="ALL">ALL</option>
            <option value="DOC CREATE">DOC CREATE</option>
            <option value="DOC REVIEW">DOC REVIEW</option>
        </select>
    </div>
    <div class="mb-3 col-3">
        <label class="form-label" style="margin: 0 !important; font-size: small; font-weight: bold;">CHECKLIST</label>
        <select id="checklistSelect" class="form-select form-select-sm">
            <option value="ALL">ALL</option>
            {% for i in checklist_name %}
            <option value="{{i.CHECKLIST}}">{{i.CHECKLIST}}</option>
            {% endfor %}
        </select>
    </div>
</div>

<div class="table-responsive table-div">
    <table class="table" id="dataTable" style="table-layout: fixed; width: 100%;">
        <thead>
            <tr>
                <th class="bg-secondary txt-white" style="width: 40px !important; text-align: center;">VIEW</th>
                <th class="bg-secondary txt-white" style="width: 200px;">CHECKLIST</th>
                <th class="bg-secondary txt-white" style="width: 40px;">CHKPT ID</th>
                <th class="bg-secondary txt-white" style="width: 150px;">CATEGORY</th>
                <th class="bg-secondary txt-white" style="width: 500px;">CHECKPOINT</th>
            </tr>
        </thead>
        <tbody>
            {% for i in checklist_data %}
            <tr>
                <td style="text-align: center;" data-bs-toggle="modal" data-bs-target="#assignModal{{loop.index}}"><i class="fa-solid fa-folder-open txt-grey"></i></td>
                <td class="td-sm">{{i.CHECKLIST}}</td>
                <td class="td-sm">{{i.CHKPT_ID}}</td>
                <td class="td-sm">{{i.CATEGORY}}</td>
                <td class="td-sm">{{i.CHECKPOINT}}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>



<script>
document.addEventListener('DOMContentLoaded', (event) => {
    const workgroupSelect = document.getElementById('workgroupSelect');
    const checklistSelect = document.getElementById('checklistSelect');
    const dataTable = document.getElementById('dataTable');
    const tableRows = dataTable.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    workgroupSelect.addEventListener('change', filterTable);
    checklistSelect.addEventListener('change', filterTable);

    function filterTable() {
        const selectedWorkgroup = workgroupSelect.value;
        const selectedChecklist = checklistSelect.value;

        for (let i = 0; i < tableRows.length; i++) {
            const row = tableRows[i];
            const checklist = row.cells[1].textContent;
            const workgroup = row.cells[1].dataset.workgroup; // Assuming you have a data-workgroup attribute

            let showRow = true;

            if (selectedWorkgroup !== 'ALL' && workgroup !== selectedWorkgroup) {
                showRow = false;
            }

            if (selectedChecklist !== 'ALL' && checklist !== selectedChecklist) {
                showRow = false;
            }

            if (showRow) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    }
});
</script>


