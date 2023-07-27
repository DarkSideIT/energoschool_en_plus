var target = document.querySelector('#globalEvents');
var key = document.querySelector('#event-filter');


function filter() {
    let rows = target.querySelectorAll('.btn');
    rows.forEach(row => {
        if (row.textContent.indexOf(key.value) < 0 && key.value) {
            row.parentNode.parentElement.style.display = 'none';
        } else {
            row.parentNode.parentElement.style.display = 'table-row';
        }
    })
}


key.addEventListener('change', filter);

document.querySelector(`#myEventListContainer`).style.display = 'none';
let eventNav = document.querySelector('.event-nav');

eventNav.addEventListener('click', function(e) {
    for (elem of eventNav.children) {
        document.querySelector(`#${elem.id}Container`).style.display = 'none';
        elem.classList.remove('active');
    }
    e.target.classList.add('active');

    document.querySelector(`#${e.target.id}Container`).style.display = "block";
})


