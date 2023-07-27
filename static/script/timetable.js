const buttons = document.querySelectorAll('.btn_record_lesson');

for (btn of buttons) {
    btn.addEventListener('click', async function(event) {
        const lessonID = event.target.getAttribute('data-lesson');
        const strRecord = document.getElementById(`lesson_${lessonID}`);
        const csrftoken = getCookie('csrftoken');

        const json = await request(`record_${lessonID}/`, null, csrftoken);
        const response = JSON.parse(json);

        if (response.type == 'success') {
            strRecord.textContent = `${response.count_records}/${response.count_seats}`;
            event.target.value = 'Вы уже записаны';
            event.target.disabled = true;
        }

        showNotification(response.type, response.message);
    })
}

document.querySelectorAll('.accordion-toggler').forEach(accordion => {
    accordion.addEventListener('click', event => {
        accordionButton = event.target.closest('.accordion-toggler');

        document.getElementById(accordionButton.getAttribute('for')).classList.toggle('opened');
        accordionButton.classList.toggle('opened');
    })
})