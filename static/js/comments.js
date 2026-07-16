/*
comments_v2.txt
Renombrar a: static/js/comments.js

Gestión estructurada de comentarios - Versión 2.0.
Usa los endpoints:
GET    /api/tasks/{id}/comments
POST   /api/tasks/{id}/comments
DELETE /api/tasks/{id}/comments/{index}
*/

"use strict";

window.CommentsUI = (() => {

    let currentTaskId = null;
    let currentComments = [];

    function init() {
        bindCloseEvents();
        bindForm();
    }

    function bindCloseEvents() {
        const modal = document.getElementById("commentsModal");

        document.getElementById("btnCloseCommentsModal")
            ?.addEventListener("click", close);

        modal?.addEventListener("click", event => {
            if (event.target === modal) {
                close();
            }
        });
    }

    function bindForm() {
        const form = document.getElementById("commentForm");

        if (!form) {
            return;
        }

        form.addEventListener("submit", async event => {
            event.preventDefault();

            if (currentTaskId === null) {
                return;
            }

            const author = (
                document.getElementById("commentAuthor")?.value || ""
            ).trim();

            const text = (
                document.getElementById("commentText")?.value || ""
            ).trim();

            if (!text) {
                window.Notifications?.warning(
                    "Escribe un comentario antes de guardarlo."
                );
                return;
            }

            await createComment({
                author: author || "Usuario",
                text
            });
        });
    }

    async function open(taskId) {
        currentTaskId = Number(taskId);

        const task = window.App?.tasks?.find(
            item => Number(item.id) === currentTaskId
        );

        const title = document.getElementById(
            "commentsTaskTitle"
        );

        if (title) {
            title.textContent = task?.titulo || `Tarea ${taskId}`;
        }

        document.getElementById("commentsModal")
            ?.classList.remove("hidden");

        await loadComments();
    }

    function close() {
        document.getElementById("commentsModal")
            ?.classList.add("hidden");

        document.getElementById("commentForm")
            ?.reset();

        currentTaskId = null;
        currentComments = [];
    }

    async function loadComments() {
        if (currentTaskId === null) {
            return;
        }

        setLoadingState();

        try {
            currentComments = await window.Api.request(
                `/tasks/${currentTaskId}/comments`
            );

            renderComments();

        } catch (error) {
            console.error(error);

            currentComments = [];
            renderError(
                error.message ||
                "No se pudieron cargar los comentarios."
            );
        }
    }

    async function createComment(payload) {
        try {
            await window.Api.request(
                `/tasks/${currentTaskId}/comments`,
                {
                    method: "POST",
                    body: JSON.stringify(payload)
                }
            );

            window.Notifications?.success(
                "Comentario añadido."
            );

            document.getElementById("commentForm")
                ?.reset();

            await loadComments();
            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo guardar el comentario."
            );
        }
    }

    async function deleteComment(index) {
        const comment = currentComments[index];

        if (!comment) {
            return;
        }

        const confirmed = window.Notifications?.confirm(
            "¿Eliminar este comentario?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await window.Api.request(
                `/tasks/${currentTaskId}/comments/${index}`,
                {
                    method: "DELETE"
                }
            );

            window.Notifications?.success(
                "Comentario eliminado."
            );

            await loadComments();
            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo eliminar el comentario."
            );
        }
    }

    function renderComments() {
        const container = document.getElementById(
            "commentsList"
        );

        if (!container) {
            return;
        }

        if (!Array.isArray(currentComments) || !currentComments.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <strong>Sin comentarios</strong>
                    <p>
                        Añade el primer comentario para comenzar
                        el seguimiento de esta tarea.
                    </p>
                </div>
            `;
            return;
        }

        container.innerHTML = currentComments
            .map((comment, index) => `
                <article class="comment-card">

                    <div class="comment-header">

                        <div>
                            <span class="comment-author">
                                ${escapeHtml(
                                    comment.author || "Usuario"
                                )}
                            </span>

                            <span class="comment-date">
                                ${formatDateTime(
                                    comment.created_at
                                )}
                            </span>
                        </div>

                        <button
                            class="icon-button comment-delete"
                            type="button"
                            title="Eliminar comentario"
                            data-comment-delete="${index}"
                        >
                            🗑
                        </button>

                    </div>

                    <div class="comment-body">
                        ${formatCommentText(comment.text)}
                    </div>

                </article>
            `)
            .join("");

        container.querySelectorAll(
            "[data-comment-delete]"
        ).forEach(button => {
            button.addEventListener("click", () => {
                deleteComment(
                    Number(button.dataset.commentDelete)
                );
            });
        });

        container.scrollTop = 0;
    }

    function setLoadingState() {
        const container = document.getElementById(
            "commentsList"
        );

        if (!container) {
            return;
        }

        container.innerHTML = `
            <div class="empty-state">
                Cargando comentarios...
            </div>
        `;
    }

    function renderError(message) {
        const container = document.getElementById(
            "commentsList"
        );

        if (!container) {
            return;
        }

        container.innerHTML = `
            <div class="empty-state">
                <strong>No se pudo cargar el seguimiento</strong>
                <p>${escapeHtml(message)}</p>

                <button
                    id="btnRetryComments"
                    class="btn btn-secondary"
                    type="button"
                >
                    Reintentar
                </button>
            </div>
        `;

        document.getElementById("btnRetryComments")
            ?.addEventListener("click", loadComments);
    }

    function formatDateTime(value) {
        if (!value) {
            return "";
        }

        const normalized = String(value).replace(
            " ",
            "T"
        );

        const parsed = new Date(normalized);

        if (Number.isNaN(parsed.getTime())) {
            return escapeHtml(value);
        }

        return new Intl.DateTimeFormat(
            "es-ES",
            {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            }
        ).format(parsed);
    }

    function formatCommentText(value) {
        return escapeHtml(value)
            .replaceAll("\n", "<br>");
    }

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    return {
        init,
        open,
        close,
        loadComments,
        renderComments
    };

})();
