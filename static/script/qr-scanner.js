function loadScript(url, callback) {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.src = url;
    script.onload = callback
    document.body.appendChild(script);
}
loadScript("https://cdn.rawgit.com/mebjas/html5-qrcode/master/minified/html5-qrcode.min.js", qr_scanner)


const dialog = document.getElementById("qrResultModal");
const result = document.getElementById("qrResultField");
const sendQrBtn = document.getElementById('sendQrButton');
const camera_select = document.getElementById('devices');


function qr_scanner() {
    var qrReader = new Html5Qrcode("qr-reader");
    let modal = bootstrap.Modal.getOrCreateInstance(dialog);

    camera_select.addEventListener('change', e => {
        qrReader.stop().then(
            () => startCamera(qrReader, e.target.value, modal)
        );
    });

    Html5Qrcode.getCameras().then(cameras => {
        /** 
          * devices would be an array of objects of type: 
          * { id: "id", label: "label" }
        */
        let camera_target = cameras.length - 1;
        if (cameras && cameras.length) {
            for (const camera of cameras) {
                const opt = document.createElement('option');
                opt.value = camera.id;
                opt.textContent = camera.label;
                camera_select.appendChild(opt);
            }
            camera_select.options[camera_target].selected = true;
            let cameraId = cameras[camera_target].id;

            dialog.addEventListener("hidden.bs.modal", function () {
                setTimeout(() => qrReader.resume(), 1000)
            });

            startCamera(qrReader, cameraId, modal);
            document.getElementById('qr-sendler').style.display = "none";
        }
    }).catch(err => {
        console.log(`Proccess stoped by error: ${err}`);
    });
}

function startCamera(qrReader, cameraId, modal) {
    qrReader.start(
        cameraId,
        {
            fps: 10,
            qrbox: 220
        },
        qrCodeMessage => {
            sendQrBtn.addEventListener("click", sendler);
            sendQrBtn.email = qrCodeMessage;
            sendQrBtn.modal = modal;

            result.textContent = qrCodeMessage;
            qrReader.pause();
            modal.show();
        }
    ).catch(err => {
        alert(`Unable to start scanning, error: ${err}`);
    });
}

function sendler(event) {
    const email = event.currentTarget.email;
    const modal = event.currentTarget.modal;

    console.log(`QR Code send: ${email}`);
    sendQrCodeResult(email);
    setTimeout(() => modal.hide(), 300);
}

document.getElementById('sendByEmail').addEventListener('click', () => {
    const email_data = document.getElementById('manualEmailInput').value;
    sendQrCodeResult(email_data);
});

async function sendQrCodeResult(qrCodeMessage) {
    const url = "qrCodeResult/";
    const event = document.getElementById("event").value;
    const data = { 'email': qrCodeMessage, 'event': event }

    const response = await request_json(url, data);
    const notification = document.getElementById('notification');

    if ('error' in response) {
        notification.className = 'error';
        notification.textContent = `${qrCodeMessage}: ${response.error}`;
    } else {
        notification.className = 'success';
        notification.textContent = `${qrCodeMessage}: ${response.detail}`;
    }
    notification.style.opacity = '1';
    notification.style.zIndex  = '100';

    setTimeout(() => {
        notification.className = '';
        notification.textContent = '';
        notification.style.opacity = "0";
        notification.style.zIndex = "-1";
    }, 3000)
}