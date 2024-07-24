document.addEventListener('DOMContentLoaded', function() {
    
    var video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    const takePhotoButton = document.getElementById('takePhoto');
 
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        video.srcObject = stream;
    })
    .catch(function(error) {
        console.log("Ha ocurrido un error con la cámara: ", error);
        alert(error)
    });

    takePhotoButton.addEventListener('click', function() {
        if (video.srcObject){
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            const image = canvas.toDataURL('image/jpeg');
        }
    })

    const socket = new WebSocket('ws://' + window.location.host + '/dallechat/');

    console.log(socket)

    socket.onopen = function(e) {
        console.log('Conexión establecida con el WebSocket');
    };

    socket.onclose = function(e) {
        console.log('Se cerró la conexión con el WebSocket');
    };

    socket.onmessage = function(e) {
        console.log(e.data);
        const data = JSON.parse(e.data);
        const input = document.getElementById('messageInput');
        const button = document.getElementById('sendPrompt')

        if (data.type === 'chat_message') {

            if (!data.success) {
                const messages = document.getElementById('messages');
                const messageItem = document.createElement('li');
                messageItem.innerHTML = `<p><strong>Ocurrió un error al momento hacer la petición, intentalo nuevamente</strong></p>`;
                messages.appendChild(messageItem);
                messages.scrollTop = messages.scrollHeight;
                input.disabled = false
                button.disabled = false
                return
            }
                const messages = document.getElementById('messages');
                const messageItem = document.createElement('li');
                messageItem.innerHTML = `<p></strong> ${data.message}</p><p><small>${data.datetime}</small></p>`;
                messages.appendChild(messageItem);
                const imageUrl = data.img
                const imageItem = document.createElement('img');
                imageItem.src = imageUrl;
                imageItem.alt = 'Imagen generada';
                imageItem.style.maxWidth = '200px';
                messages.appendChild(imageItem);
                messages.scrollTop = messages.scrollHeight;
                input.disabled = false
                button.disabled = false

        }
    };

    socket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    document.getElementById('sendPrompt').addEventListener('click', function(event) {
        event.preventDefault();
        const input = document.getElementById('messageInput');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const button = document.getElementById('sendPrompt')
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const isCanvasEmpty = imageData.data.every(value => value === 0);

        if (input.value.trim() === '') {
            const messages = document.getElementById('messages');
            const messageItem = document.createElement('li');
            messageItem.innerHTML = `<p></strong>No puedes enviar mensajes vacios!</p>`;
            messages.appendChild(messageItem);
            return
        }

        if (isCanvasEmpty) {
            const messages = document.getElementById('messages');
            const messageItem = document.createElement('li');
            messageItem.innerHTML = `<p><strong>No puedes enviar mensajes sin haber tomado una foto!</strong></p>`;
            messages.appendChild(messageItem);
            return
        }

        const message = input.value;
        const canvasDataURL = canvas.toDataURL('image/jpeg');

        socket.send(JSON.stringify({
            'message': message,
            'img64': canvasDataURL
        }));
        input.value = ''; 

        input.disabled = true
        button.disabled = true

    });

})

