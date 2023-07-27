function hide(rows) {
    if (statusSelect.value === 'Родитель') {
        rows[0].style = 'display: none';
        rows[1].style = 'display: none';
    }
    if (statusSelect.value === 'Учитель') {
        rows[1].style = 'display: none';
    }
}


const statusSelect = document.getElementById('id_status'); // Получаем статус пользователя

const rows = [
    document.getElementById('id_educational_institution').parentElement.parentElement,
    document.getElementById('id_class_number').parentElement.parentElement
]
hide(rows);

statusSelect.addEventListener('change', () => {
    rows.forEach(tr => tr.style = 'display: table-row');

    hide(rows);

});

