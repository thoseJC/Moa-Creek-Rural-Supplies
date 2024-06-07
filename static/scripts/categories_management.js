        function showAddModal() {
            document.getElementById('addModal').style.display = 'block';
        }

        function closeAddModal() {
            document.getElementById('addModal').style.display = 'none';
        }

    function showEditModal(id, name, description) {
        document.getElementById('id').value = id;
        document.getElementById('editName').value = name;
        document.getElementById('editDescription').value = description;
        document.getElementById('editForm').action = '/admin/edit';
        document.getElementById('editModal').style.display = 'block';
    }

    function closeEditModal() {
        document.getElementById('editModal').style.display = 'none';
    }

        window.onclick = function(event) {
            if (event.target === document.getElementById('addModal')) {
                closeAddModal();
            }
            if (event.target === document.getElementById('editModal')) {
                closeEditModal();
            }
        }