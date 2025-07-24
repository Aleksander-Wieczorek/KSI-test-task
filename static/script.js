async function load() {
    try {
        const res = await fetch("/api/todos");
        const todos = await res.json();

        const list = document.getElementById("todoList");
        list.innerHTML = "";

        todos.forEach(todo => {
            const li = document.createElement("li");
            li.className = "list-group-item d-flex justify-content-between align-items-center";

            const textSpan=document.createElement("span");
            textSpan.textContent=todo.note;
            li.appendChild(textSpan);

            const delBtn=document.createElement("button");
            delBtn.textContent="Usuń";
            delBtn.className = "btn btn-danger btn-sm";
            delBtn.addEventListener("click", async ()=>{
                try{
                    const response=await fetch(`/api/delete/${todo.id}`,{
                        method: 'DELETE',
                        headers: {
                            "Content-Type": "application/json",
                        },
                    });
                    if(response.ok){
                        load();
                    }
                } catch (err){
                    console.error("Błąd")
                }

            });
            li.appendChild(delBtn);
            list.appendChild(li);

        });
    } catch (err) {
        console.error("Błąd przy ładowaniu todos:", err);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    load();
});
