async function request(url, data, csrftoken) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    const result = await response.text();
    return result
}


async function request_json(url, data) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    const result = await response.json();
    return result
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function showNotification(type="success", message) {
    let notification = document.getElementById("notification");   

    notification.classList.add(type);
    notification.style.opacity = '1';
    notification.style.zIndex = "1000";
    notification.textContent = message;
    
    setTimeout(function(){
        notification.style.opacity = "0";
        notification.style.zIndex = "-1";
        notification.classList.remove('error');
        notification.classList.remove('success');
        notification.classList.remove("warning");
    }, 3000);   
}