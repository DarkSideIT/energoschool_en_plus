document.querySelectorAll('.mark_visit').forEach(btn => {
    btn.addEventListener('click', async () => {
        const email = btn.getAttribute('data-user');
        const lesson_id = btn.getAttribute('data-lesson');

        const url = btn.classList.contains('presence') ? 'cancelVisit/': 'markVisit/';

        const data = { 'user_email': email, 'lesson_id': lesson_id }
        const response = await request_json(url, data);

        if (response.result) { btn.classList.toggle('presence'); }
    })
})

const menu = document.getElementById('menu');

document.getElementById('menu-open-btn').addEventListener('click', () => {
    menu.classList.add('opened');
    document.body.classList.add('mute');
});

menu.querySelector('.menu-close-btn').addEventListener('click', () => {
    menu.classList.remove('opened');
    document.body.classList.remove('mute');
});