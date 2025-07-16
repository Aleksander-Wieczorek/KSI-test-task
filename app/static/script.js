async function load() {
    try {
        const res = await fetch("/api/todos");
        const todos = await res.json();

        const list = document.getElementById("todoList");
        list.innerHTML = "";

        todos.forEach(todo => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";
            li.innerHTML = `
                ${todo.title}
                <button class="btn btn-sm btn-danger" onclick="deleteTodo(${todo.id})">Usuń</button>
            `;
            list.appendChild(li);
        });
    } catch (err) {
        console.error("Błąd przy ładowaniu todos:", err);
    }
}
load();
