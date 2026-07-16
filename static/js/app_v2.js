/*
====================================================
app.js - Versión 2.0 (Parte 1)
Guardar como: static/js/app.js

Esta parte incluye:
- Inicialización general.
- Comunicación con la API.
- Navegación.
- Dashboard clicable.
- Filtros compactos.
- Tabla con estados y prioridades por color.
- Alta, edición y borrado.
- Seguimiento básico mediante observaciones.
====================================================
*/

"use strict";

window.App = {

    apiBase: "/api",
    tasks: [],
    editingId: null,
    currentView: "dashboard",
    dashboardFilter: null,

    init() {
        this.cache();
        this.bindEvents();
        this.showCurrentDate();
        this.loadTasks();
    },

    cache() {
        this.views = document.querySelectorAll(".view");
        this.navItems = document.querySelectorAll(".nav-item");

        this.pageTitle = document.getElementById("pageTitle");
        this.currentDate = document.getElementById("currentDate");

        this.searchInput = document.getElementById("txtSearch");
        this.taskTableBody = document.querySelector("#taskTable tbody");

        this.filterStatus = document.getElementById("filterStatus");
        this.filterPriority = document.getElementById("filterPriority");
        this.filterResponsible = document.getElementById("filterResponsible");
        this.sortTasks = document.getElementById("sortTasks");

        this.taskModal = document.getElementById("taskModal");
        this.taskForm = document.getElementById("taskForm");
        this.taskModalTitle = document.getElementById("taskModalTitle");

        this.commentsModal = document.getElementById("commentsModal");
        this.commentsTaskTitle = document.getElementById("commentsTaskTitle");
        this.commentsList = document.getElementById("commentsList");
        this.commentForm = document.getElementById("commentForm");

        this.notifyBox = document.getElementById("notify");
    },

    bindEvents() {
        this.navItems.forEach(button => {
            button.addEventListener("click", () => {
                this.changeView(button.dataset.view);
            });
        });

        document.getElementById("btnNewTask")
            ?.addEventListener("click", () => this.openTaskModal());

        document.getElementById("btnCloseTaskModal")
            ?.addEventListener("click", () => this.closeTaskModal());

        document.getElementById("btnCancel")
            ?.addEventListener("click", () => this.closeTaskModal());

        document.getElementById("btnCloseCommentsModal")
            ?.addEventListener("click", () => this.closeCommentsModal());

        this.taskForm?.addEventListener("submit", event => {
            event.preventDefault();
            this.saveTask();
        });

        this.searchInput?.addEventListener("input", () => {
            this.renderTasks();
        });

        [
            this.filterStatus,
            this.filterPriority,
            this.filterResponsible,
            this.sortTasks
        ].forEach(control => {
            control?.addEventListener("change", () => this.renderTasks());
        });

        document.getElementById("btnClearFilters")
            ?.addEventListener("click", () => this.clearFilters());

        document.getElementById("btnExportCsv")
            ?.addEventListener("click", () => this.exportCSV());

        document.getElementById("avance")
            ?.addEventListener("input", event => {
                document.getElementById("avanceOutput").value =
                    `${event.target.value}%`;
            });

        document.querySelectorAll("[data-dashboard-filter]")
            .forEach(card => {
                card.addEventListener("click", () => {
                    this.applyDashboardFilter(
                        card.dataset.dashboardFilter
                    );
                });
            });

        this.taskModal?.addEventListener("click", event => {
            if (event.target === this.taskModal) {
                this.closeTaskModal();
            }
        });

        this.commentsModal?.addEventListener("click", event => {
            if (event.target === this.commentsModal) {
                this.closeCommentsModal();
            }
        });
    },

    async api(path, options = {}) {
        const config = {
            headers: {
                "Content-Type": "application/json"
            },
            ...options
        };

        const response = await fetch(this.apiBase + path, config);

        const contentType =
            response.headers.get("content-type") || "";

        const payload = contentType.includes("application/json")
            ? await response.json()
            : await response.text();

        if (!response.ok) {
            throw new Error(
                payload?.error ||
                payload?.message ||
                `Error HTTP ${response.status}`
            );
        }

        return payload;
    },

    async loadTasks() {
        try {
            this.tasks = await this.api("/tasks");

            this.populateResponsibleFilter();
            this.renderDashboard();
            this.renderTasks();

            if (window.DashboardUI?.render) {
                window.DashboardUI.render(this.tasks);
            }

            if (window.CalendarUI?.render) {
                window.CalendarUI.render(this.tasks);
            }

        } catch (error) {
            console.error(error);
            this.showNotification(
                "No se pudieron cargar las tareas.",
                "error"
            );
        }
    },

    changeView(view) {
        this.currentView = view;

        this.views.forEach(section => {
            section.classList.toggle(
                "active",
                section.id === view
            );
        });

        this.navItems.forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.view === view
            );
        });

        const titles = {
            dashboard: "Dashboard",
            tasks: "Tareas",
            calendar: "Calendario",
            reports: "Informes",
            settings: "Configuración"
        };

        if (this.pageTitle) {
            this.pageTitle.textContent = titles[view] || "ToDo";
        }

        if (view === "calendar" && window.CalendarUI?.render) {
            window.CalendarUI.render(this.tasks);
        }
    },

    showCurrentDate() {
        if (!this.currentDate) {
            return;
        }

        this.currentDate.textContent =
            new Intl.DateTimeFormat(
                "es-ES",
                {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                }
            ).format(new Date());
    },

    applyDashboardFilter(filter) {
        this.dashboardFilter = filter;

        this.changeView("tasks");

        if (filter === "all") {
            this.filterStatus.value = "";
            this.sortTasks.value = "id-desc";
        } else if (filter === "overdue") {
            this.filterStatus.value = "";
        } else if (filter === "progress") {
            this.filterStatus.value = "";
            this.sortTasks.value = "progress-desc";
        } else {
            this.filterStatus.value = filter;
        }

        this.renderTasks();
    },

    clearFilters() {
        this.dashboardFilter = null;
        this.searchInput.value = "";
        this.filterStatus.value = "";
        this.filterPriority.value = "";
        this.filterResponsible.value = "";
        this.sortTasks.value = "id-desc";
        this.renderTasks();
    },

    getFilteredTasks() {
        let result = [...this.tasks];

        const text =
            (this.searchInput?.value || "").trim().toLowerCase();

        if (text) {
            result = result.filter(task => {
                const values = [
                    task.titulo,
                    task.descripcion,
                    task.responsable,
                    task.prioridad,
                    task.estado,
                    task.observaciones
                ];

                return values.some(value =>
                    String(value || "")
                        .toLowerCase()
                        .includes(text)
                );
            });
        }

        const status = this.filterStatus?.value || "";
        const priority = this.filterPriority?.value || "";
        const responsible = this.filterResponsible?.value || "";

        if (status) {
            result = result.filter(task => task.estado === status);
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

        if (this.dashboardFilter === "overdue") {
            const today = this.toISODate(new Date());

            result = result.filter(task =>
                task.fecha_prevista &&
                task.fecha_prevista < today &&
                !["Finalizada", "Cancelada"].includes(task.estado)
            );
        }

        const sortMode = this.sortTasks?.value || "id-desc";

        result.sort((a, b) => {
            switch (sortMode) {
                case "id-asc":
                    return Number(a.id) - Number(b.id);

                case "title-asc":
                    return String(a.titulo).localeCompare(
                        String(b.titulo),
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
                    return Number(b.avance) - Number(a.avance);

                default:
                    return Number(b.id) - Number(a.id);
            }
        });

        return result;
    },

    renderDashboard() {
        const count = state =>
            this.tasks.filter(task => task.estado === state).length;

        const total = this.tasks.length;
        const today = this.toISODate(new Date());

        const overdue = this.tasks.filter(task =>
            task.fecha_prevista &&
            task.fecha_prevista < today &&
            !["Finalizada", "Cancelada"].includes(task.estado)
        ).length;

        const average = total
            ? Math.round(
                this.tasks.reduce(
                    (sum, task) => sum + Number(task.avance || 0),
                    0
                ) / total
            )
            : 0;

        this.setText("totalTasks", total);
        this.setText("pendingTasks", count("Pendiente"));
        this.setText("runningTasks", count("En curso"));
        this.setText("blockedTasks", count("Bloqueada"));
        this.setText("finishedTasks", count("Finalizada"));
        this.setText("cancelledTasks", count("Cancelada"));
        this.setText("overdueTasks", overdue);
        this.setText("averageProgress", `${average}%`);

        this.renderUpcomingTasks();
    },

    renderUpcomingTasks() {
        const container = document.getElementById("upcomingTasks");

        if (!container) {
            return;
        }

        const today = new Date();
        const limit = new Date();
        limit.setDate(limit.getDate() + 14);

        const items = this.tasks
            .filter(task => {
                if (
                    !task.fecha_prevista ||
                    ["Finalizada", "Cancelada"].includes(task.estado)
                ) {
                    return false;
                }

                const due = new Date(
                    `${task.fecha_prevista}T12:00:00`
                );

                return due >= today && due <= limit;
            })
            .sort((a, b) =>
                String(a.fecha_prevista)
                    .localeCompare(String(b.fecha_prevista))
            )
            .slice(0, 6);

        if (!items.length) {
            container.innerHTML =
                '<p class="empty-state">No hay tareas próximas.</p>';
            return;
        }

        container.innerHTML = items.map(task => `
            <button
                class="stack-card"
                type="button"
                data-open-task="${task.id}"
            >
                <strong>${this.escapeHtml(task.titulo)}</strong>
                <small>
                    ${this.escapeHtml(task.fecha_prevista)}
                    ·
                    ${this.escapeHtml(task.responsable || "Sin responsable")}
                </small>
            </button>
        `).join("");

        container.querySelectorAll("[data-open-task]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    this.editTask(
                        Number(button.dataset.openTask)
                    );
                });
            });
    },

    renderTasks() {
        if (!this.taskTableBody) {
            return;
        }

        const tasks = this.getFilteredTasks();
        this.taskTableBody.innerHTML = "";

        if (!tasks.length) {
            this.taskTableBody.innerHTML = `
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

        tasks.forEach(task => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${task.id}</td>

                <td>
                    <strong>${this.escapeHtml(task.titulo)}</strong>
                    <small class="task-description">
                        ${this.escapeHtml(
                            task.descripcion || "Sin descripción"
                        )}
                    </small>
                </td>

                <td>
                    ${this.escapeHtml(
                        task.responsable || "Sin asignar"
                    )}
                </td>

                <td>
                    <span class="priority-badge ${this.priorityClass(
                        task.prioridad
                    )}">
                        ${this.escapeHtml(task.prioridad)}
                    </span>
                </td>

                <td>
                    <select
                        class="compact-select status-select"
                        data-status-id="${task.id}"
                    >
                        ${this.statusOptions(task.estado)}
                    </select>

                    <span class="status-badge ${this.statusClass(
                        task.estado
                    )}">
                        ${this.escapeHtml(task.estado)}
                    </span>
                </td>

                <td>${task.fecha_inicio || "-"}</td>
                <td>${task.fecha_prevista || "-"}</td>

                <td>
                    <div class="progress-wrapper">
                        <progress
                            value="${Number(task.avance || 0)}"
                            max="100"
                        ></progress>

                        <input
                            class="compact-progress"
                            type="number"
                            min="0"
                            max="100"
                            value="${Number(task.avance || 0)}"
                            data-progress-id="${task.id}"
                        >

                        <span class="progress-value">
                            ${Number(task.avance || 0)}%
                        </span>
                    </div>
                </td>

                <td>
                    <button
                        class="btn btn-secondary btn-comments"
                        type="button"
                        data-comments-id="${task.id}"
                    >
                        Seguimiento
                    </button>
                </td>

                <td>
                    <div class="action-group">
                        <button
                            class="icon-button"
                            type="button"
                            data-edit-id="${task.id}"
                            title="Editar"
                        >
                            ✏
                        </button>

                        <button
                            class="icon-button"
                            type="button"
                            data-delete-id="${task.id}"
                            title="Eliminar"
                        >
                            🗑
                        </button>
                    </div>
                </td>
            `;

            this.taskTableBody.appendChild(row);
        });

        this.bindTableActions();
    },

    bindTableActions() {
        document.querySelectorAll("[data-edit-id]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    this.editTask(Number(button.dataset.editId));
                });
            });

        document.querySelectorAll("[data-delete-id]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    this.deleteTask(Number(button.dataset.deleteId));
                });
            });

        document.querySelectorAll("[data-comments-id]")
            .forEach(button => {
                button.addEventListener("click", () => {
                    this.openCommentsModal(
                        Number(button.dataset.commentsId)
                    );
                });
            });

        document.querySelectorAll("[data-status-id]")
            .forEach(select => {
                select.addEventListener("change", () => {
                    this.patchTask(
                        Number(select.dataset.statusId),
                        { estado: select.value }
                    );
                });
            });

        document.querySelectorAll("[data-progress-id]")
            .forEach(input => {
                input.addEventListener("change", () => {
                    this.patchTask(
                        Number(input.dataset.progressId),
                        { avance: Number(input.value) }
                    );
                });
            });
    },

    populateResponsibleFilter() {
        if (!this.filterResponsible) {
            return;
        }

        const currentValue = this.filterResponsible.value;

        const names = [...new Set(
            this.tasks
                .map(task => task.responsable)
                .filter(Boolean)
        )].sort((a, b) =>
            a.localeCompare(b, "es", { sensitivity: "base" })
        );

        this.filterResponsible.innerHTML =
            '<option value="">Todos los responsables</option>' +
            names.map(name => `
                <option value="${this.escapeHtml(name)}">
                    ${this.escapeHtml(name)}
                </option>
            `).join("");

        this.filterResponsible.value = currentValue;
    },

    openTaskModal(task = null) {
        this.taskForm.reset();

        if (task) {
            this.editingId = task.id;
            this.taskModalTitle.textContent = "Editar tarea";

            this.setValue("titulo", task.titulo);
            this.setValue("descripcion", task.descripcion);
            this.setValue("responsable", task.responsable);
            this.setValue("prioridad", task.prioridad || "Media");
            this.setValue("estado", task.estado || "Pendiente");
            this.setValue("avance", Number(task.avance || 0));
            this.setValue("fechaInicio", task.fecha_inicio || "");
            this.setValue(
                "fechaPrevista",
                task.fecha_prevista || ""
            );
            this.setValue(
                "observaciones",
                task.observaciones || ""
            );

            document.getElementById("avanceOutput").value =
                `${Number(task.avance || 0)}%`;

        } else {
            this.editingId = null;
            this.taskModalTitle.textContent = "Nueva tarea";

            this.setValue("prioridad", "Media");
            this.setValue("estado", "Pendiente");
            this.setValue("avance", 0);

            document.getElementById("avanceOutput").value = "0%";
        }

        this.taskModal.classList.remove("hidden");
    },

    closeTaskModal() {
        this.taskModal.classList.add("hidden");
        this.editingId = null;
        this.taskForm.reset();
    },

    editTask(id) {
        const task = this.tasks.find(
            item => Number(item.id) === Number(id)
        );

        if (task) {
            this.openTaskModal(task);
        }
    },

    async saveTask() {
        const payload = {
            titulo: this.getValue("titulo").trim(),
            descripcion: this.getValue("descripcion").trim(),
            responsable: this.getValue("responsable").trim(),
            prioridad: this.getValue("prioridad"),
            estado: this.getValue("estado"),
            avance: Number(this.getValue("avance") || 0),
            fecha_inicio: this.getValue("fechaInicio"),
            fecha_prevista: this.getValue("fechaPrevista"),
            observaciones: this.getValue("observaciones").trim()
        };

        if (!payload.titulo) {
            this.showNotification(
                "El título es obligatorio.",
                "error"
            );
            return;
        }

        try {
            if (this.editingId !== null) {
                await this.api(
                    `/tasks/${this.editingId}`,
                    {
                        method: "PATCH",
                        body: JSON.stringify(payload)
                    }
                );

                this.showNotification(
                    "Tarea actualizada.",
                    "success"
                );

            } else {
                await this.api(
                    "/tasks",
                    {
                        method: "POST",
                        body: JSON.stringify(payload)
                    }
                );

                this.showNotification(
                    "Tarea creada.",
                    "success"
                );
            }

            this.closeTaskModal();
            await this.loadTasks();

        } catch (error) {
            console.error(error);
            this.showNotification(error.message, "error");
        }
    },

    async patchTask(id, payload) {
        try {
            await this.api(
                `/tasks/${id}`,
                {
                    method: "PATCH",
                    body: JSON.stringify(payload)
                }
            );

            await this.loadTasks();

        } catch (error) {
            console.error(error);
            this.showNotification(error.message, "error");
        }
    },

    async deleteTask(id) {
        if (!confirm("¿Eliminar esta tarea?")) {
            return;
        }

        try {
            await this.api(
                `/tasks/${id}`,
                { method: "DELETE" }
            );

            this.showNotification(
                "Tarea eliminada.",
                "success"
            );

            await this.loadTasks();

        } catch (error) {
            console.error(error);
            this.showNotification(error.message, "error");
        }
    },

    openCommentsModal(id) {
        const task = this.tasks.find(
            item => Number(item.id) === Number(id)
        );

        if (!task) {
            return;
        }

        this.commentsTaskTitle.textContent = task.titulo;

        const text = task.observaciones?.trim();

        if (text) {
            this.commentsList.innerHTML = `
                <article class="comment-card">
                    <div class="comment-header">
                        <span class="comment-author">
                            Seguimiento actual
                        </span>
                        <span>
                            ${this.escapeHtml(
                                task.ultima_actualizacion || ""
                            )}
                        </span>
                    </div>

                    <div class="comment-body">
                        ${this.escapeHtml(text)}
                    </div>
                </article>
            `;
        } else {
            this.commentsList.innerHTML =
                '<p class="empty-state">No hay comentarios.</p>';
        }

        this.commentsModal.classList.remove("hidden");
    },

    closeCommentsModal() {
        this.commentsModal.classList.add("hidden");
        this.commentForm?.reset();
    },

    exportCSV() {
        const tasks = this.getFilteredTasks();

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

        const rows = tasks.map(task => [
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
        ].map(this.csvValue).join(";"));

        const csv = [
            headers.join(";"),
            ...rows
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
    },

    statusOptions(selected) {
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
    },

    statusClass(status) {
        return {
            "Pendiente": "pending",
            "En curso": "running",
            "Bloqueada": "blocked",
            "Finalizada": "finished",
            "Cancelada": "cancelled"
        }[status] || "pending";
    },

    priorityClass(priority) {
        return {
            "Baja": "priority-low",
            "Media": "priority-medium",
            "Alta": "priority-high",
            "Crítica": "priority-critical"
        }[priority] || "priority-medium";
    },

    showNotification(message, type = "info") {
        if (!this.notifyBox) {
            return;
        }

        this.notifyBox.textContent = message;
        this.notifyBox.className = `notify ${type}`;

        clearTimeout(this.notifyTimer);

        this.notifyTimer = setTimeout(() => {
            this.notifyBox.classList.add("hidden");
        }, 3000);
    },

    setText(id, value) {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    },

    setValue(id, value) {
        const element = document.getElementById(id);

        if (element) {
            element.value = value ?? "";
        }
    },

    getValue(id) {
        return document.getElementById(id)?.value ?? "";
    },

    toISODate(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");

        return `${year}-${month}-${day}`;
    },

    csvValue(value) {
        const text = String(value ?? "").replaceAll('"', '""');
        return `"${text}"`;
    },

    escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

};

window.addEventListener(
    "DOMContentLoaded",
    () => window.App.init()
);
