document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('sendMessageForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(form);
            fetch('/message/send_message', {
                method: 'POST',
                body: formData
            }).then(response => response.json())
              .then(data => {
                  console.log(data);  // Debugging: Log the response data
                  if (data.error) {
                      console.error(data.error);
                  } else {
                      const messagesDiv = document.getElementById('messages');
                      const newMessage = document.createElement('p');
                      newMessage.innerHTML = `${data.sender_username}: ${data.content}`;
                      messagesDiv.appendChild(newMessage);
                      form.reset(); // Clear the form after submission
                  }
              })
              .catch(error => console.error('Error:', error));
        });
    }
});
