/*
====================================================
app.js - VERSIÓN CONSOLIDADA
Guardar como: static/js/app.js

Este archivo sustituye las partes 1 a 9.
====================================================
*/

"use strict";

const App = {

    apiBase: "/api",
    tasks: [],
    editingId: null,
    currentView: "dashboard",
    calendarDate: new Date(),

    init() {
        this.cache();
        this.bindEvents();
        this.showDate();
        this.ensureTaskControls();
        this.ensureCalendarLayout();
        this.changeView("dashboard");
        this.refreshFromServer();
    },

    cache() {
        this.views = document.querySelectorAll(".view");
        this.menuButtons = document.querySelectorAll(".menu-item");
        this.modal = document.getElementById("taskModal");
        this.form = document.getElementById("taskForm");
        this.table = document.querySelector("#taskTable tbody");
        this.search = document.getElementById("txtSearch");
        this.btnNew = document.getElementById("btnNewTask");
        this.btnCancel = document.getElementById("btnCancel");
    },

    bindEvents() {
        this.menuButtons.forEach(button => {
            button.addEventListener("click", () => {
                this.changeView(button.dataset.view);
            });
        });

        this.btnNew.addEventListener("click", () => {
            this.openModal();
        });

        this.btnCancel.addEventListener("click", () => {
            this.closeModal();
        });

        this.form.addEventListener("submit", event => {
            event.preventDefault();
            this.saveTask();
        });

        this.search.addEventListener("input", () => {
            this.renderTable();
        });

        this.modal.addEventListener("click", event => {
            if (event.target === this.modal) {
                this.closeModal();
            }
        });

        window.addEventListener("keydown", event => {
            if (event.key === "Escape") {
                this.closeModal();
            }

            if (
                event.ctrlKey &&
                event.key.toLowerCase() === "n"
            ) {
                event.preventDefault();
                this.openModal();
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

        const response = await fetch(
            this.apiBase + path,
            config
        );

        const contentType =
            response.headers.get("content-type") || "";

        const payload = contentType.includes("application/json")
            ? await response.json()
            : await response.text();

        if (!response.ok) {
            const message =
                payload?.error ||
                payload?.message ||
                `Error HTTP ${response.status}`;

            throw new Error(message);
        }

        return payload;
    },

    async refreshFromServer() {
        try {
            this.tasks = await this.api("/tasks");
            this.renderTable();
            this.renderDashboard();

            if (this.currentView === "calendar") {
                this.renderCalendar();
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
            section.classList.remove("active");
        });

        const selected = document.getElementById(view);

        if (selected) {
            selected.classList.add("active");
        }

        this.menuButtons.forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.view === view
            );
        });

        if (view === "calendar") {
            this.renderCalendar();
        }

        if (view === "dashboard") {
            this.renderDashboard();
        }
    },

    showDate() {
        const element = document.getElementById("currentDate");

        if (!element) {
            return;
        }

        element.textContent = new Intl.DateTimeFormat(
            "es-ES",
            {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            }
        ).format(new Date());
    },

    openModal(task = null) {
        this.form.reset();

        const title = this.modal.querySelector("h2");

        if (task) {
            this.editingId = task.id;
            title.textContent = "Editar tarea";

            document.getElementById("titulo").value =
                task.titulo || "";

            document.getElementById("descripcion").value =
                task.descripcion || "";

            document.getElementById("responsable").value =
                task.responsable || "";

            document.getElementById("prioridad").value =
                task.prioridad || "Media";

            document.getElementById("fechaPrevista").value =
                task.fecha_prevista || task.fecha || "";
        } else {
            this.editingId = null;
            title.textContent = "Nueva tarea";
        }

        this.modal.classList.remove("hidden");
        document.getElementById("titulo").focus();
    },

    closeModal() {
        this.modal.classList.add("hidden");
        this.editingId = null;
        this.form.reset();
    },

    async saveTask() {
        const payload = {
            titulo:
                document.getElementById("titulo").value.trim(),

            descripcion:
                document.getElementById("descripcion").value.trim(),

            responsable:
                document.getElementById("responsable").value.trim(),

            prioridad:
                document.getElementById("prioridad").value,

            fecha_prevista:
                document.getElementById("fechaPrevista").value
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

            this.closeModal();
            await this.refreshFromServer();

        } catch (error) {
            console.error(error);

            this.showNotification(
                error.message,
                "error"
            );
        }
    },

    editTask(id) {
        const task = this.tasks.find(
            item => Number(item.id) === Number(id)
        );

        if (task) {
            this.openModal(task);
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

            await this.refreshFromServer();

        } catch (error) {
            console.error(error);

            this.showNotification(
                error.message,
                "error"
            );
        }
    },

    async changeStatus(id, status) {
        try {
            await this.api(
                `/tasks/${id}`,
                {
                    method: "PATCH",
                    body: JSON.stringify({
                        estado: status
                    })
                }
            );

            await this.refreshFromServer();

        } catch (error) {
            console.error(error);
            this.showNotification(error.message, "error");
        }
    },

    async changeProgress(id, progress) {
        const value = Math.max(
            0,
            Math.min(100, Number(progress) || 0)
        );

        try {
            await this.api(
                `/tasks/${id}`,
                {
                    method: "PATCH",
                    body: JSON.stringify({
                        avance: value
                    })
                }
            );

            await this.refreshFromServer();

        } catch (error) {
            console.error(error);
            this.showNotification(error.message, "error");
        }
    },

    ensureTaskControls() {
        const section = document.getElementById("tasks");

        if (!section || document.getElementById("taskFilters")) {
            return;
        }

        const controls = document.createElement("div");
        controls.id = "taskFilters";

        controls.innerHTML = `
            <select id="filterStatus">
                <option value="">Todos los estados</option>
                <option>Pendiente</option>
                <option>En curso</option>
                <option>Bloqueada</option>
                <option>Finalizada</option>
                <option>Cancelada</option>
            </select>

            <select id="filterPriority">
                <option value="">Todas las prioridades</option>
                <option>Baja</option>
                <option>Media</option>
                <option>Alta</option>
                <option>Crítica</option>
            </select>

            <select id="sortTasks">
                <option value="id-desc">Más recientes</option>
                <option value="id-asc">Más antiguas</option>
                <option value="title-asc">Título A-Z</option>
                <option value="date-asc">Fecha prevista</option>
                <option value="progress-desc">Mayor avance</option>
            </select>

            <button id="btnExportCsv" type="button">
                Exportar CSV
            </button>
        `;

        section.insertBefore(
            controls,
            document.getElementById("taskTable")
        );

        controls.querySelectorAll("select").forEach(select => {
            select.addEventListener("change", () => {
                this.renderTable();
            });
        });

        document.getElementById("btnExportCsv")
            .addEventListener("click", () => {
                this.exportCSV();
            });
    },

    getFilteredTasks() {
        let list = [...this.tasks];

        const text =
            (this.search?.value || "").trim().toLowerCase();

        if (text) {
            list = list.filter(task => {
                const values = [
                    task.titulo,
                    task.descripcion,
                    task.responsable,
                    task.estado,
                    task.prioridad
                ];

                return values.some(value =>
                    String(value || "")
                        .toLowerCase()
                        .includes(text)
                );
            });
        }

        const status =
            document.getElementById("filterStatus")?.value || "";

        const priority =
            document.getElementById("filterPriority")?.value || "";

        if (status) {
            list = list.filter(
                task => task.estado === status
            );
        }

        if (priority) {
            list = list.filter(
                task => task.prioridad === priority
            );
        }

        const sortMode =
            document.getElementById("sortTasks")?.value ||
            "id-desc";

        list.sort((a, b) => {
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

        return list;
    },

    renderTable() {
        if (!this.table) {
            return;
        }

        this.table.innerHTML = "";

        const list = this.getFilteredTasks();

        list.forEach(task => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${task.id}</td>
                <td>${this.escapeHtml(task.titulo)}</td>
                <td>${this.escapeHtml(task.responsable || "-")}</td>
                <td>${this.escapeHtml(task.prioridad)}</td>
                <td>
                    <select class="statusSelect">
                        ${this.statusOptions(task.estado)}
                    </select>
                </td>
                <td>${task.fecha_inicio || "-"}</td>
                <td>${task.fecha_prevista || "-"}</td>
                <td>
                    <div class="progressWrapper">
                        <progress
                            value="${Number(task.avance) || 0}"
                            max="100">
                        </progress>

                        <input
                            class="progressInput"
                            type="number"
                            min="0"
                            max="100"
                            value="${Number(task.avance) || 0}">
                    </div>
                </td>
                <td>
                    <button
                        class="btnEdit"
                        type="button"
                        title="Editar">
                        ✏️
                    </button>

                    <button
                        class="btnDelete"
                        type="button"
                        title="Eliminar">
                        🗑️
                    </button>
                </td>
            `;

            row.querySelector(".statusSelect")
                .addEventListener("change", event => {
                    this.changeStatus(
                        task.id,
                        event.target.value
                    );
                });

            row.querySelector(".progressInput")
                .addEventListener("change", event => {
                    this.changeProgress(
                        task.id,
                        event.target.value
                    );
                });

            row.querySelector(".btnEdit")
                .addEventListener("click", () => {
                    this.editTask(task.id);
                });

            row.querySelector(".btnDelete")
                .addEventListener("click", () => {
                    this.deleteTask(task.id);
                });

            this.table.appendChild(row);
        });
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
                ${state === selected ? "selected" : ""}>
                ${state}
            </option>
        `).join("");
    },

    renderDashboard() {
        const total = this.tasks.length;

        const count = state =>
            this.tasks.filter(
                task => task.estado === state
            ).length;

        document.getElementById("totalTasks").textContent =
            total;

        document.getElementById("pendingTasks").textContent =
            count("Pendiente");

        document.getElementById("runningTasks").textContent =
            count("En curso");

        document.getElementById("finishedTasks").textContent =
            count("Finalizada");

        let extra = document.getElementById("dashboardExtra");

        if (!extra) {
            extra = document.createElement("div");
            extra.id = "dashboardExtra";
            extra.className = "cards";

            document.getElementById("dashboard")
                .appendChild(extra);
        }

        const today = this.toISODate(new Date());

        const overdue = this.tasks.filter(task =>
            task.fecha_prevista &&
            task.fecha_prevista < today &&
            !["Finalizada", "Cancelada"].includes(task.estado)
        ).length;

        const average = total
            ? Math.round(
                this.tasks.reduce(
                    (sum, task) =>
                        sum + Number(task.avance || 0),
                    0
                ) / total
            )
            : 0;

        extra.innerHTML = `
            <div class="card">
                <h3>Bloqueadas</h3>
                <span>${count("Bloqueada")}</span>
            </div>

            <div class="card">
                <h3>Canceladas</h3>
                <span>${count("Cancelada")}</span>
            </div>

            <div class="card">
                <h3>Retrasadas</h3>
                <span>${overdue}</span>
            </div>

            <div class="card">
                <h3>Avance medio</h3>
                <span>${average}%</span>
            </div>
        `;
    },

    ensureCalendarLayout() {
        const container =
            document.getElementById("calendarContainer");

        if (!container || document.getElementById("calendarGrid")) {
            return;
        }

        container.innerHTML = `
            <div class="calendarHeader">
                <button id="calendarPrev" type="button">◀</button>
                <h3 id="calendarTitle"></h3>
                <button id="calendarToday" type="button">Hoy</button>
                <button id="calendarNext" type="button">▶</button>
            </div>

            <div class="calendarWeekdays">
                <span>Lunes</span>
                <span>Martes</span>
                <span>Miércoles</span>
                <span>Jueves</span>
                <span>Viernes</span>
                <span>Sábado</span>
                <span>Domingo</span>
            </div>

            <div id="calendarGrid" class="calendarGrid"></div>
        `;

        document.getElementById("calendarPrev")
            .addEventListener("click", () => {
                this.calendarDate.setMonth(
                    this.calendarDate.getMonth() - 1
                );
                this.renderCalendar();
            });

        document.getElementById("calendarNext")
            .addEventListener("click", () => {
                this.calendarDate.setMonth(
                    this.calendarDate.getMonth() + 1
                );
                this.renderCalendar();
            });

        document.getElementById("calendarToday")
            .addEventListener("click", () => {
                this.calendarDate = new Date();
                this.renderCalendar();
            });
    },

    renderCalendar() {
        this.ensureCalendarLayout();

        const grid = document.getElementById("calendarGrid");
        const title = document.getElementById("calendarTitle");

        if (!grid || !title) {
            return;
        }

        grid.innerHTML = "";

        const year = this.calendarDate.getFullYear();
        const month = this.calendarDate.getMonth();

        title.textContent = new Intl.DateTimeFormat(
            "es-ES",
            {
                month: "long",
                year: "numeric"
            }
        ).format(new Date(year, month, 1));

        const first = new Date(year, month, 1);
        let offset = first.getDay() - 1;

        if (offset < 0) {
            offset = 6;
        }

        const daysInMonth =
            new Date(year, month + 1, 0).getDate();

        const previousMonthDays =
            new Date(year, month, 0).getDate();

        for (let index = 0; index < 42; index++) {
            let day;
            let dateValue;
            let outside = false;

            if (index < offset) {
                day = previousMonthDays - offset + index + 1;
                dateValue = new Date(year, month - 1, day);
                outside = true;
            } else if (index >= offset + daysInMonth) {
                day = index - offset - daysInMonth + 1;
                dateValue = new Date(year, month + 1, day);
                outside = true;
            } else {
                day = index - offset + 1;
                dateValue = new Date(year, month, day);
            }

            const iso = this.toISODate(dateValue);

            const dayTasks = this.tasks.filter(
                task =>
                    (task.fecha_prevista || task.fecha) === iso
            );

            const cell = document.createElement("button");
            cell.type = "button";
            cell.className = "calendarCell";

            if (outside) {
                cell.classList.add("outsideMonth");
            }

            if (iso === this.toISODate(new Date())) {
                cell.classList.add("today");
            }

            cell.innerHTML = `
                <span class="calendarDayNumber">${day}</span>

                <div class="calendarTaskList">
                    ${dayTasks.slice(0, 3).map(task => `
                        <span
                            class="calendarTask"
                            title="${this.escapeHtml(task.titulo)}">
                            ${this.escapeHtml(task.titulo)}
                        </span>
                    `).join("")}

                    ${
                        dayTasks.length > 3
                            ? `<small>+${dayTasks.length - 3} más</small>`
                            : ""
                    }
                </div>
            `;

            cell.addEventListener("dblclick", () => {
                this.openModal();
                document.getElementById("fechaPrevista").value =
                    iso;
            });

            grid.appendChild(cell);
        }
    },

    exportCSV() {
        const headers = [
            "ID",
            "Título",
            "Descripción",
            "Responsable",
            "Prioridad",
            "Estado",
            "Fecha prevista",
            "Avance"
        ];

        const rows = this.getFilteredTasks().map(task => [
            task.id,
            task.titulo,
            task.descripcion,
            task.responsable,
            task.prioridad,
            task.estado,
            task.fecha_prevista || "",
            task.avance
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

    csvValue(value) {
        const text = String(value ?? "").replaceAll('"', '""');
        return `"${text}"`;
    },

    showNotification(message, type = "info") {
        let box = document.getElementById("notify");

        if (!box) {
            box = document.createElement("div");
            box.id = "notify";
            document.body.appendChild(box);
        }

        box.className = `notify ${type}`;
        box.textContent = message;

        clearTimeout(this.notifyTimer);

        this.notifyTimer = setTimeout(() => {
            box.classList.add("hidden");
        }, 3000);
    },

    toISODate(date) {
        const year = date.getFullYear();

        const month = String(
            date.getMonth() + 1
        ).padStart(2, "0");

        const day = String(
            date.getDate()
        ).padStart(2, "0");

        return `${year}-${month}-${day}`;
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
    () => App.init()
);
