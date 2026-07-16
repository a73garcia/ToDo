/*
tasks_v2.txt
Renombrar a: static/js/tasks.js

Gestión de la tabla de tareas - Versión 2.0.
*/

"use strict";

window.TasksUI = (() => {

    let tasks = [];
    let tableBody = null;

    function init() {
        tableBody = document.querySelector("#taskTable tbody");
        bindStaticEvents();
    }

    function bindStaticEvents() {
        [
            "filterStatus",
            "filterPriority",
            "filterResponsible",
            "sortTasks"
        ].forEach(id => {
            document.getElementById(id)
                ?.addEventListener("change", render);
        });

        document.getElementById("txtSearch")
            ?.addEventListener(
                "input",
                window.Utils?.debounce(render, 200) || render
            );

        document.getElementById("btnClearFilters")
            ?.addEventListener("click", clearFilters);

        document.getElementById("btnExportCsv")
            ?.addEventListener("click", exportCSV);
    }

    function setTasks(data = []) {
        tasks = Array.isArray(data) ? [...data] : [];
        populateResponsibleFilter();
        render();
    }

    function getTasks() {
        return [...tasks];
    }

    function getFilteredTasks() {
        let result = [...tasks];

        const search = (
            document.getElementById("txtSearch")?.value || ""
        ).trim().toLowerCase();

        const status =
            document.getElementById("filterStatus")?.value || "";

        const priority =
            document.getElementById("filterPriority")?.value || "";

        const responsible =
            document.getElementById("filterResponsible")?.value || "";

        const sortMode =
            document.getElementById("sortTasks")?.value || "id-desc";

        if (search) {
            result = result.filter(task => {
                const comments = Array.isArray(task.comentarios)
                    ? task.comentarios.map(item => item.text).join(" ")
                    : "";

                const values = [
                    task.titulo,
                    task.descripcion,
                    task.responsable,
                    task.estado,
                    task.prioridad,
                    task.observaciones,
                    task.proyecto,
                    Array.isArray(task.etiquetas)
                        ? task.etiquetas.join(" ")
                        : task.etiquetas,
                    comments
                ];

                return values.some(value =>
                    String(value || "")
                        .toLowerCase()
                        .includes(search)
                );
            });
        }

        if (status) {
            result = result.filter(
                task => task.estado === status
            );
        }

        if (priority) {
            result = result.filter(
                task => task.prioridad === priority
            );
        }

        if (responsible) {
            result = result.filter(
                task => task.responsable === responsible
            );
        }

        result.sort((a, b) => {
            switch (sortMode) {
                case "id-asc":
                    return Number(a.id) - Number(b.id);

                case "title-asc":
                    return String(a.titulo || "").localeCompare(
                        String(b.titulo || ""),
                        "es",
                        { sensitivity: "base" }
                    );

                case "date-asc":
                    return String(
                        a.fecha_prevista || "9999-12-31"
                    ).localeCompare(
                        String(
                            b.fecha_prevista || "9999-12-31"
                        )
                    );

                case "progress-desc":
                    return Number(b.avance || 0) -
                        Number(a.avance || 0);

                case "id-desc":
                default:
                    return Number(b.id) - Number(a.id);
            }
        });

        return result;
    }

    function render(customList = null) {
        if (!tableBody) {
            tableBody = document.querySelector("#taskTable tbody");
        }

        if (!tableBody) {
            return;
        }

        const list = customList || getFilteredTasks();
        tableBody.innerHTML = "";

        if (!list.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="10">
                        <p class="empty-state">
                            No hay tareas que coincidan con los filtros.
                        </p>
                    </td>
                </tr>
            `;
            return;
        }

        const fragment = document.createDocumentFragment();

        list.forEach(task => {
            fragment.appendChild(createRow(task));
        });

        tableBody.appendChild(fragment);
        bindRowEvents();
    }

    function createRow(task) {
        const row = document.createElement("tr");

        const progress = window.Utils
            ? window.Utils.clamp(Number(task.avance || 0), 0, 100)
            : Math.max(0, Math.min(100, Number(task.avance || 0)));

        const commentsCount = Array.isArray(task.comentarios)
            ? task.comentarios.length
            : 0;

        const tags = Array.isArray(task.etiquetas)
            ? task.etiquetas
            : [];

        row.innerHTML = `
            <td>
                <button
                    class="favorite-button ${task.favorito ? "active" : ""}"
                    type="button"
                    data-task-favorite="${task.id}"
                    title="Favorito"
                >
                    ${task.favorito ? "★" : "☆"}
                </button>

                <span>${task.id}</span>
            </td>

            <td>
                <div class="task-title-cell">
                    <strong>${escapeHtml(task.titulo)}</strong>

                    <small class="task-description">
                        ${escapeHtml(
                            task.descripcion || "Sin descripción"
                        )}
                    </small>

                    ${
                        tags.length
                            ? `
                                <div class="tag-list">
                                    ${tags.map(tag => `
                                        <span class="tag-badge">
                                            ${escapeHtml(tag)}
                                        </span>
                                    `).join("")}
                                </div>
                              `
                            : ""
                    }

                    ${
                        task.proyecto
                            ? `
                                <small class="task-project">
                                    Proyecto: ${escapeHtml(task.proyecto)}
                                </small>
                              `
                            : ""
                    }
                </div>
            </td>

            <td>
                ${escapeHtml(task.responsable || "Sin asignar")}
            </td>

            <td>
                <span class="priority-badge ${priorityClass(
                    task.prioridad
                )}">
                    ${escapeHtml(task.prioridad)}
                </span>
            </td>

            <td>
                <div class="status-cell">
                    <span class="status-badge ${statusClass(
                        task.estado
                    )}">
                        ${escapeHtml(task.estado)}
                    </span>

                    <select
                        class="compact-select"
                        data-task-status="${task.id}"
                        aria-label="Cambiar estado"
                    >
                        ${statusOptions(task.estado)}
                    </select>
                </div>
            </td>

            <td>${escapeHtml(task.fecha_inicio || "-")}</td>

            <td>
                <div class="due-date-cell">
                    <span class="${dueDateClass(task)}">
                        ${escapeHtml(task.fecha_prevista || "-")}
                    </span>

                    ${
                        task.recordatorio
                            ? `
                                <small>
                                    Recordatorio:
                                    ${escapeHtml(task.recordatorio)}
                                </small>
                              `
                            : ""
                    }
                </div>
            </td>

            <td>
                <div class="progress-wrapper">
                    <progress
                        value="${progress}"
                        max="100">
                    </progress>

                    <input
                        class="compact-progress"
                        type="number"
                        min="0"
                        max="100"
                        value="${progress}"
                        data-task-progress="${task.id}"
                        aria-label="Cambiar avance"
                    >

                    <span class="progress-value">
                        ${progress}%
                    </span>
                </div>

                ${
                    Number(task.tiempo_estimado || 0) ||
                    Number(task.tiempo_empleado || 0)
                        ? `
                            <small class="time-summary">
                                ${Number(task.tiempo_empleado || 0)} h /
                                ${Number(task.tiempo_estimado || 0)} h
                            </small>
                          `
                        : ""
                }
            </td>

            <td>
                <button
                    class="btn btn-secondary btn-comments"
                    type="button"
                    data-task-comments="${task.id}"
                >
                    💬 ${commentsCount}
                </button>
            </td>

            <td>
                <div class="action-group">
                    <button
                        class="icon-button"
                        type="button"
                        data-task-edit="${task.id}"
                        title="Editar tarea"
                    >
                        ✏
                    </button>

                    <button
                        class="icon-button"
                        type="button"
                        data-task-history="${task.id}"
                        title="Ver historial"
                    >
                        📋
                    </button>

                    <button
                        class="icon-button danger"
                        type="button"
                        data-task-delete="${task.id}"
                        title="Eliminar tarea"
                    >
                        🗑
                    </button>
                </div>
            </td>
        `;

        return row;
    }

    function bindRowEvents() {
        document.querySelectorAll("[data-task-edit]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    window.App?.editTask(
                        Number(button.dataset.taskEdit)
                    );
                });
            });

        document.querySelectorAll("[data-task-delete]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    window.App?.deleteTask(
                        Number(button.dataset.taskDelete)
                    );
                });
            });

        document.querySelectorAll("[data-task-comments]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    window.CommentsUI?.open(
                        Number(button.dataset.taskComments)
                    );
                });
            });

        document.querySelectorAll("[data-task-history]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    openHistory(
                        Number(button.dataset.taskHistory)
                    );
                });
            });

        document.querySelectorAll("[data-task-favorite]")
            .forEach(button => {
                button.addEventListener("click", async () => {
                    await toggleFavorite(
                        Number(button.dataset.taskFavorite)
                    );
                });
            });

        document.querySelectorAll("[data-task-status]")
            .forEach(select => {
                select.addEventListener("change", async () => {
                    await updateTask(
                        Number(select.dataset.taskStatus),
                        { estado: select.value }
                    );
                });
            });

        document.querySelectorAll("[data-task-progress]")
            .forEach(input => {
                input.addEventListener("change", async () => {
                    const value = Math.max(
                        0,
                        Math.min(100, Number(input.value) || 0)
                    );

                    await updateTask(
                        Number(input.dataset.taskProgress),
                        { avance: value }
                    );
                });
            });
    }

    async function updateTask(id, payload) {
        try {
            await window.Api.Tasks.update(id, payload);

            window.Notifications?.success(
                "Tarea actualizada."
            );

            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo actualizar la tarea."
            );
        }
    }

    async function toggleFavorite(id) {
        try {
            await window.Api.request(
                `/tasks/${id}/favorite`,
                { method: "POST" }
            );

            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo cambiar el favorito."
            );
        }
    }

    async function openHistory(id) {
        try {
            const history = await window.Api.History.list(id);

            const text = history.length
                ? history.map(item =>
                    `${item.fecha} · ${item.accion}\n${item.observaciones || ""}`
                ).join("\n\n")
                : "No hay historial para esta tarea.";

            window.alert(text);

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                "No se pudo cargar el historial."
            );
        }
    }

    function populateResponsibleFilter() {
        const select =
            document.getElementById("filterResponsible");

        if (!select) {
            return;
        }

        const currentValue = select.value;

        const responsibleNames = [
            ...new Set(
                tasks
                    .map(task => task.responsable)
                    .filter(Boolean)
            )
        ].sort((a, b) =>
            a.localeCompare(
                b,
                "es",
                { sensitivity: "base" }
            )
        );

        select.innerHTML =
            '<option value="">Todos los responsables</option>' +
            responsibleNames.map(name => `
                <option value="${escapeHtml(name)}">
                    ${escapeHtml(name)}
                </option>
            `).join("");

        select.value = currentValue;
    }

    function clearFilters() {
        [
            "txtSearch",
            "filterStatus",
            "filterPriority",
            "filterResponsible"
        ].forEach(id => {
            const element = document.getElementById(id);

            if (element) {
                element.value = "";
            }
        });

        const sort =
            document.getElementById("sortTasks");

        if (sort) {
            sort.value = "id-desc";
        }

        render();
    }

    function applyStatusFilter(status) {
        const select =
            document.getElementById("filterStatus");

        if (select) {
            select.value = status || "";
        }

        render();
    }

    function applyOverdueFilter() {
        const today = window.Utils
            ? window.Utils.toISODate(new Date())
            : new Date().toISOString().slice(0, 10);

        const list = tasks.filter(task =>
            task.fecha_prevista &&
            task.fecha_prevista < today &&
            !["Finalizada", "Cancelada"].includes(task.estado)
        );

        render(list);
    }

    function exportCSV() {
        const rows = getFilteredTasks();

        const headers = [
            "ID",
            "Título",
            "Descripción",
            "Responsable",
            "Prioridad",
            "Estado",
            "Fecha inicio",
            "Fecha prevista",
            "Avance",
            "Proyecto",
            "Etiquetas",
            "Tiempo estimado",
            "Tiempo empleado"
        ];

        const body = rows.map(task => [
            task.id,
            task.titulo,
            task.descripcion,
            task.responsable,
            task.prioridad,
            task.estado,
            task.fecha_inicio,
            task.fecha_prevista,
            task.avance,
            task.proyecto,
            Array.isArray(task.etiquetas)
                ? task.etiquetas.join(", ")
                : "",
            task.tiempo_estimado,
            task.tiempo_empleado
        ].map(csvValue).join(";"));

        const csv = [
            headers.join(";"),
            ...body
        ].join("\n");

        if (window.Utils) {
            window.Utils.download(
                "tareas.csv",
                "\uFEFF" + csv,
                "text/csv;charset=utf-8"
            );
            return;
        }

        const blob = new Blob(
            ["\uFEFF" + csv],
            { type: "text/csv;charset=utf-8" }
        );

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "tareas.csv";
        link.click();

        URL.revokeObjectURL(url);
    }

    function statusOptions(selected) {
        const states = [
            "Pendiente",
            "En curso",
            "Bloqueada",
            "Finalizada",
            "Cancelada"
        ];

        return states.map(state => `
            <option
                value="${state}"
                ${state === selected ? "selected" : ""}
            >
                ${state}
            </option>
        `).join("");
    }

    function statusClass(status) {
        return {
            "Pendiente": "pending",
            "En curso": "running",
            "Bloqueada": "blocked",
            "Finalizada": "finished",
            "Cancelada": "cancelled"
        }[status] || "pending";
    }

    function priorityClass(priority) {
        return {
            "Baja": "priority-low",
            "Media": "priority-medium",
            "Alta": "priority-high",
            "Crítica": "priority-critical"
        }[priority] || "priority-medium";
    }

    function dueDateClass(task) {
        if (
            !task.fecha_prevista ||
            ["Finalizada", "Cancelada"].includes(task.estado)
        ) {
            return "";
        }

        const today = window.Utils
            ? window.Utils.toISODate(new Date())
            : new Date().toISOString().slice(0, 10);

        return task.fecha_prevista < today
            ? "due-overdue"
            : "";
    }

    function csvValue(value) {
        const text =
            String(value ?? "").replaceAll('"', '""');

        return `"${text}"`;
    }

    function escapeHtml(value) {
        if (window.Utils) {
            return window.Utils.escapeHtml(value);
        }

        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    return {
        init,
        setTasks,
        getTasks,
        getFilteredTasks,
        render,
        clearFilters,
        applyStatusFilter,
        applyOverdueFilter,
        exportCSV
    };

})();
