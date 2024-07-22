document.addEventListener('DOMContentLoaded', function() {
    
    const socket = new WebSocket('ws://' + window.location.host + '/dallechat/');

    console.log(socket)

    socket.onopen = function(e) {
        console.log('WebSocket connection established');
    };

    socket.onclose = function(e) {
        console.log('WebSocket connection closed');
    };

    socket.onmessage = function(e) {
        console.log(e.data);
        const data = JSON.parse(e.data);
        
        if (data.type === 'chat_message') {
            const messages = document.getElementById('messages');
            const messageItem = document.createElement('li');
            messageItem.innerHTML = `<p></strong> ${data.message}</p><p><small>${data.datetime}</small></p>`;
            messages.appendChild(messageItem);
            
            if (data.image) {
                const imageItem = document.createElement('img');
                imageItem.src = data.image;
                imageItem.alt = 'Generated Image';
                imageItem.style.maxWidth = '200px';
                messages.appendChild(imageItem);
            }

            messages.scrollTop = messages.scrollHeight;
        }
    };

    socket.onerror = function(e) {
        console.error('WebSocket error:', e);
    };

    document.getElementById('chatForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevents the form from submitting the traditional way
        const input = document.getElementById('messageInput');
        const message = input.value;
        socket.send(JSON.stringify({
            'message': message
        }));
        input.value = ''; // Clear input field
    });

    document.getElementById('uploadPhoto').addEventListener('click', function() {
        document.getElementById('photoUpload').click();
    });

    // Add functionality for taking photo if needed
    document.getElementById('takePhoto').addEventListener('click', function() {
        document.getElementById('camera').style.display = 'block';
    });

})

