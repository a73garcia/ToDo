/*
comments.txt
Renombrar a: static/js/comments.js

Gestión del seguimiento de tareas.
*/

"use strict";

window.CommentsUI = (() => {

    let currentTask = null;

    function open(taskId) {

        currentTask = window.App?.tasks?.find(
            t => Number(t.id) === Number(taskId)
        );

        if (!currentTask) return;

        document.getElementById("commentsTaskTitle").textContent =
            currentTask.titulo;

        renderComments();

        document
            .getElementById("commentsModal")
            .classList.remove("hidden");

        bindForm();
    }

    function close() {
        document
            .getElementById("commentsModal")
            .classList.add("hidden");

        currentTask = null;
    }

    function renderComments() {

        const list =
            document.getElementById("commentsList");

        list.innerHTML = "";

        if (
            !currentTask.observaciones ||
            !currentTask.observaciones.trim()
        ) {
            list.innerHTML =
                '<p class="empty-state">No hay comentarios.</p>';
            return;
        }

        const blocks =
            currentTask.observaciones
                .split("----------------------------------------")
                .filter(Boolean)
                .reverse();

        blocks.forEach(block => {

            const card = document.createElement("article");

            card.className = "comment-card";

            card.innerHTML = `
                <div class="comment-body">
                    ${escape(block)}
                </div>
            `;

            list.appendChild(card);

        });

    }

    function bindForm() {

        const form =
            document.getElementById("commentForm");

        form.onsubmit = async e => {

            e.preventDefault();

            const author =
                document.getElementById("commentAuthor").value.trim();

            const text =
                document.getElementById("commentText").value.trim();

            if (!text) return;

            const now = new Date();

            const stamp =
                now.toLocaleDateString("es-ES") +
                " " +
                now.toLocaleTimeString("es-ES",{
                    hour:"2-digit",
                    minute:"2-digit"
                });

            const entry =
`${stamp}
${author || "Usuario"}

${text}
----------------------------------------`;

            const comments =
                currentTask.observaciones
                ? currentTask.observaciones + "\n\n" + entry
                : entry;

            try{

                await window.Api.Tasks.update(
                    currentTask.id,
                    {
                        observaciones:comments,
                        ultima_actualizacion:stamp
                    }
                );

                window.Notifications?.success(
                    "Comentario añadido."
                );

                await window.App.reloadData();

                currentTask =
                    window.App.tasks.find(
                        t=>t.id===currentTask.id
                    );

                renderComments();

                form.reset();

            }catch(ex){

                console.error(ex);

                window.Notifications?.error(
                    "No se pudo guardar el comentario."
                );

            }

        };

    }

    function escape(v){
        return String(v??"")
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;")
        .replaceAll("\n","<br>");
    }

    return{
        open,
        close,
        renderComments
    };

})();
