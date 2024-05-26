document.addEventListener('DOMContentLoaded', () => {
    const notificationCountElement = document.getElementById('notificationCount');
    const notificationsContainer = document.getElementById('notifications');
    const notificationIcon = document.getElementById('notification-icon');

    async function fetchNotifications() {
        try {
            const response = await fetch('/customer/notifications');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    }

    function showNotifications(notifications) {
        notificationsContainer.innerHTML = '';  
        notifications.forEach(notifications => {
            const notificationElement = document.createElement('div');
            notificationElement.className = 'notifications';
            notificationElement.innerHTML = `
                <div>Message: ${notifications[1]}</div>
                <div>Time: ${notifications[3]}</div>
            `;
            notificationsContainer.appendChild(notificationElement);
        });
        notificationsContainer.style.display = 'block';
    }

    function updateNotificationIcon(unreadCount) {
        if (unreadCount > 0) {
            notificationCountElement.textContent = unreadCount;
            notificationCountElement.style.display = 'inline';
        } else {
            notificationCountElement.style.display = 'none';
        }
    }

    notificationIcon.addEventListener('click', async () => {
        const notifications = await fetchNotifications();
        if (notifications) {
            const unreadCount = notifications.filter(notification => !notification[2]).length;
            showNotifications(notifications);
            updateNotificationIcon(unreadCount);
        }
    });

    // Initial fetch to check if there are any notifications
    (async () => {
        const notifications = await fetchNotifications();
        if (notifications) {
            const unreadCount = notifications.filter(notification => !notification[2]).length;
            updateNotificationIcon(unreadCount);
        }
    })();
});

