function check() {
    let typeEvent = document.querySelector('#id_typeEvent_2');
    let valueEvent = document.querySelector('#id_valueEvent');

    if (typeEvent.checked) {
        valueEvent.setAttribute('disabled', 'disabled');
        valueEvent.removeAttribute('required');
        valueEvent.value = null;
        
    } else {
        valueEvent.removeAttribute('disabled');
        valueEvent.setAttribute('required', 'required');
    }
}

var typeList = document.querySelector('#id_typeEvent');
typeList.addEventListener('click', check);
document.addEventListener('DOMContentLoaded', check);