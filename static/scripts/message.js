const send_message_field = document.getElementById("send_message_field");

const createMessageElement = (sender_role_name, content, send_time) => {
  const p = document.createElement("p");
  if (sender_role_name === "staff") {
    p.className = "staff-message";
  } else {
    p.className = "customer-message";
  }
  const senderSpan = document.createElement("span");
  senderSpan.className = "sender";
  senderSpan.innerHTML = `<b>${sender_role_name}</b>`;

  const contentText = document.createTextNode(`: ${content} `);

  const timeSpan = document.createElement("span");
  timeSpan.className = "message-time";
  timeSpan.textContent = `(${send_time})`;

  p.appendChild(senderSpan);
  p.appendChild(contentText);
  p.appendChild(timeSpan);
  return p;
};

function scrollToBottom(container) {
  container.scrollTop = container.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("sendMessageForm");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(form);
      fetch("/message/send_message", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data); // Debugging: Log the response data
          if (data.error) {
            console.error(data.error);
          } else {
            send_message_field.value = "";
            msg_element = createMessageElement(
              data.sender_role_name,
              data.content,
              data.send_time
            );
            const messagesDiv = document.getElementById("messages");
            messagesDiv.appendChild(msg_element);
            scrollToBottom(messagesDiv);
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  }
});
