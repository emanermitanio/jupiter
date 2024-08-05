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
            const workgroup = row.cells[1].textContent.trim();
            const checklist = row.cells[2].textContent.trim();

            let showRow = true;

            if (selectedWorkgroup !== 'ALL' && workgroup !== selectedWorkgroup) {
                showRow = false;
            }

            if (selectedChecklist !== 'ALL' && checklist !== selectedChecklist) {
                showRow = false;
            }

            row.style.display = showRow ? '' : 'none';
        }
    }
});
</script>
