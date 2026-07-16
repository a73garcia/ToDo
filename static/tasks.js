/*
tasks.txt
Renombrar a: static/js/tasks.js

Módulo de gestión y renderizado de tareas.
*/

"use strict";

window.TasksUI = (() => {

    let tasks = [];
    let filteredTasks = [];
    let tableBody = null;

    function init() {
        tableBody = document.querySelector("#taskTable tbody");
        bindStaticEvents();
    }

    function bindStaticEvents() {
        document.getElementById("filterStatus")
            ?.addEventListener("change", render);

        document.getElementById("filterPriority")
            ?.addEventListener("change", render);

        document.getElementById("filterResponsible")
            ?.addEventListener("change", render);

        document.getElementById("sortTasks")
            ?.addEventListener("change", render);

        document.getElementById("txtSearch")
            ?.addEventListener("input", render);

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
                const values = [
                    task.titulo,
                    task.descripcion,
                    task.responsable,
                    task.estado,
                    task.prioridad,
                    task.observaciones
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

    function render() {
        if (!tableBody) {
            tableBody = document.querySelector("#taskTable tbody");
        }

        if (!tableBody) {
            return;
        }

        filteredTasks = getFilteredTasks();
        tableBody.innerHTML = "";

        if (!filteredTasks.length) {
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

        filteredTasks.forEach(task => {
            fragment.appendChild(createRow(task));
        });

        tableBody.appendChild(fragment);
        bindRowEvents();
    }

    function createRow(task) {
        const row = document.createElement("tr");

        const progress = Math.max(
            0,
            Math.min(100, Number(task.avance || 0))
        );

        row.innerHTML = `
            <td>${task.id}</td>

            <td>
                <div class="task-title-cell">
                    <strong>${escapeHtml(task.titulo)}</strong>

                    <small class="task-description">
                        ${escapeHtml(
                            task.descripcion || "Sin descripción"
                        )}
                    </small>
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

            <td>${escapeHtml(task.fecha_prevista || "-")}</td>

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
            </td>

            <td>
                <button
                    class="btn btn-secondary btn-comments"
                    type="button"
                    data-task-comments="${task.id}"
                >
                    Seguimiento
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
                error.message || "No se pudo actualizar la tarea."
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
        const ids = [
            "txtSearch",
            "filterStatus",
            "filterPriority",
            "filterResponsible"
        ];

        ids.forEach(id => {
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
        const today = toISODate(new Date());

        filteredTasks = tasks.filter(task =>
            task.fecha_prevista &&
            task.fecha_prevista < today &&
            !["Finalizada", "Cancelada"].includes(task.estado)
        );

        renderCustom(filteredTasks);
    }

    function renderCustom(list) {
        if (!tableBody) {
            return;
        }

        tableBody.innerHTML = "";

        if (!list.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="10">
                        <p class="empty-state">
                            No hay tareas para este criterio.
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
            "Observaciones"
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
            task.observaciones
        ].map(csvValue).join(";"));

        const csv = [
            headers.join(";"),
            ...body
        ].join("\n");

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

    function toISODate(date) {
        const year = date.getFullYear();

        const month = String(
            date.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            date.getDate()
        ).padStart(2, "0");

        return `${year}-${month}-${day}`;
    }

    function csvValue(value) {
        const text =
            String(value ?? "").replaceAll('"', '""');

        return `"${text}"`;
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
