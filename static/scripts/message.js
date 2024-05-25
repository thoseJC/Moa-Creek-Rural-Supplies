document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('sendMessageForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            fetch('/message/send_message', { // Adjust the URL to match the blueprint prefix
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => {
                  if (data.error) {
                      console.error(data.error);
                  } else {
                      const messagesDiv = document.getElementById('messages');
                      const newMessage = document.createElement('p');
                      newMessage.textContent = `${data.sender_id}: ${data.content}`;
                      messagesDiv.appendChild(newMessage);
                      form.reset(); // Clear the form after submission
                  }
              })
              .catch(error => console.error('Error:', error));
        });
    }
});
