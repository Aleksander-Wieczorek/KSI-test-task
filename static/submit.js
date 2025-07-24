document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add');
    const noteInput = document.getElementById('desc');
    const modal = new bootstrap.Modal(document.getElementById('todoModal'));

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const submitBtn = document.getElementById('submit');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Wysyłanie...';
        try {
            const note = noteInput.value.trim();
            if (!note) {
                alert('Proszę wpisać opis zadania');
                return;
            }

            const response = await fetch('http://localhost:8080/api/todos/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ note: note })
            });

            if (!response.ok) {
                throw new Error('Błąd serwera');
            }

            const result = await response.json();
            console.log('Odpowiedź:', result);
            noteInput.value = '';
            modal.hide();
            location.reload();
        } catch (error) {

            console.error('Błąd:', error);
            alert('Wystąpił błąd: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Zapisz';

        }
    });
});