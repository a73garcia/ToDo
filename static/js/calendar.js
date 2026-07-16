/*
calendar.js - Versión 2.0
Guardar finalmente como: static/js/calendar.js

Funcionalidades:
- Calendario mensual moderno.
- Tareas visibles dentro de cada día.
- Colores por estado.
- Navegación entre meses.
- Botón "Hoy".
- Selección de día.
- Resumen mensual.
- Apertura de tareas desde el calendario.
- Doble clic para crear una tarea en una fecha.
*/

"use strict";

window.CalendarUI = (() => {

    let tasks = [];
    let currentDate = new Date();
    let selectedDate = null;
    let initialized = false;

    function init() {
        if (initialized) {
            return;
        }

        initialized = true;

        document.getElementById("calendarPrev")
            ?.addEventListener("click", () => {
                currentDate = new Date(
                    currentDate.getFullYear(),
                    currentDate.getMonth() - 1,
                    1
                );

                render(tasks);
            });

        document.getElementById("calendarNext")
            ?.addEventListener("click", () => {
                currentDate = new Date(
                    currentDate.getFullYear(),
                    currentDate.getMonth() + 1,
                    1
                );

                render(tasks);
            });

        document.getElementById("calendarToday")
            ?.addEventListener("click", () => {
                currentDate = new Date();
                selectedDate = toISODate(currentDate);
                render(tasks);
            });
    }

    function render(data = []) {
        init();

        tasks = Array.isArray(data) ? [...data] : [];

        renderTitle();
        renderGrid();
        renderSummary();

        if (selectedDate) {
            renderSelectedDay(selectedDate);
        }
    }

    function renderTitle() {
        const title = document.getElementById("calendarTitle");

        if (!title) {
            return;
        }

        title.textContent = new Intl.DateTimeFormat(
            "es-ES",
            {
                month: "long",
                year: "numeric"
            }
        ).format(
            new Date(
                currentDate.getFullYear(),
                currentDate.getMonth(),
                1
            )
        );
    }

    function renderGrid() {
        const grid = document.getElementById("calendarGrid");

        if (!grid) {
            return;
        }

        grid.innerHTML = "";

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const previousMonthLastDay = new Date(year, month, 0);

        let startOffset = firstDay.getDay() - 1;

        if (startOffset < 0) {
            startOffset = 6;
        }

        const totalDays = lastDay.getDate();
        const previousMonthDays = previousMonthLastDay.getDate();
        const todayISO = toISODate(new Date());

        for (let index = 0; index < 42; index += 1) {

            let dayNumber;
            let cellDate;
            let outsideMonth = false;

            if (index < startOffset) {
                dayNumber =
                    previousMonthDays - startOffset + index + 1;

                cellDate = new Date(
                    year,
                    month - 1,
                    dayNumber
                );

                outsideMonth = true;

            } else if (index >= startOffset + totalDays) {
                dayNumber =
                    index - startOffset - totalDays + 1;

                cellDate = new Date(
                    year,
                    month + 1,
                    dayNumber
                );

                outsideMonth = true;

            } else {
                dayNumber = index - startOffset + 1;

                cellDate = new Date(
                    year,
                    month,
                    dayNumber
                );
            }

            const isoDate = toISODate(cellDate);
            const dayTasks = getTasksForDate(isoDate);

            const cell = document.createElement("button");

            cell.type = "button";
            cell.className = "calendarCell";

            if (outsideMonth) {
                cell.classList.add("outsideMonth");
            }

            if (isoDate === todayISO) {
                cell.classList.add("today");
            }

            if (isoDate === selectedDate) {
                cell.classList.add("selected");
            }

            cell.dataset.date = isoDate;

            cell.innerHTML = `
                <div class="calendar-day-header">
                    <span class="calendarDayNumber">
                        ${dayNumber}
                    </span>

                    ${
                        dayTasks.length
                            ? `<span class="calendar-count">${dayTasks.length}</span>`
                            : ""
                    }
                </div>

                <div class="calendarTaskList">
                    ${dayTasks.slice(0, 4).map(task => `
                        <span
                            class="calendarTask ${statusClass(task.estado)}"
                            title="${escapeHtml(task.titulo)}"
                            data-calendar-task-id="${task.id}"
                        >
                            ${escapeHtml(task.titulo)}
                        </span>
                    `).join("")}

                    ${
                        dayTasks.length > 4
                            ? `<small class="calendar-more">
                                +${dayTasks.length - 4} más
                               </small>`
                            : ""
                    }
                </div>
            `;

            cell.addEventListener("click", event => {
                const taskElement = event.target.closest(
                    "[data-calendar-task-id]"
                );

                if (taskElement) {
                    event.stopPropagation();

                    window.App?.editTask(
                        Number(taskElement.dataset.calendarTaskId)
                    );

                    return;
                }

                selectedDate = isoDate;
                renderGrid();
                renderSelectedDay(isoDate);
            });

            cell.addEventListener("dblclick", event => {
                if (
                    event.target.closest(
                        "[data-calendar-task-id]"
                    )
                ) {
                    return;
                }

                selectedDate = isoDate;

                window.App?.openTaskModal();

                const dueDateInput =
                    document.getElementById("fechaPrevista");

                if (dueDateInput) {
                    dueDateInput.value = isoDate;
                }
            });

            grid.appendChild(cell);
        }
    }

    function renderSummary() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        const monthTasks = tasks.filter(task => {
            const due = parseTaskDate(task);

            return (
                due &&
                due.getFullYear() === year &&
                due.getMonth() === month
            );
        });

        const countByState = state =>
            monthTasks.filter(
                task => task.estado === state
            ).length;

        setText(
            "calendarSummaryTitle",
            new Intl.DateTimeFormat(
                "es-ES",
                {
                    month: "long",
                    year: "numeric"
                }
            ).format(new Date(year, month, 1))
        );

        setText("calendarTotal", monthTasks.length);
        setText(
            "calendarPending",
            countByState("Pendiente")
        );
        setText(
            "calendarRunning",
            countByState("En curso")
        );
        setText(
            "calendarBlocked",
            countByState("Bloqueada")
        );
        setText(
            "calendarFinished",
            countByState("Finalizada")
        );
    }

    function renderSelectedDay(isoDate) {
        const title = document.getElementById(
            "selectedDayTitle"
        );

        const container = document.getElementById(
            "selectedDayTasks"
        );

        if (!title || !container) {
            return;
        }

        const parsedDate = new Date(
            `${isoDate}T12:00:00`
        );

        title.textContent = new Intl.DateTimeFormat(
            "es-ES",
            {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            }
        ).format(parsedDate);

        const dayTasks = getTasksForDate(isoDate);

        if (!dayTasks.length) {
            container.innerHTML = `
                <p class="empty-state">
                    No hay tareas previstas para este día.
                </p>

                <button
                    id="btnCreateTaskForSelectedDay"
                    class="btn btn-primary"
                    type="button"
                >
                    + Crear tarea
                </button>
            `;

            document.getElementById(
                "btnCreateTaskForSelectedDay"
            )?.addEventListener("click", () => {
                openNewTaskForDate(isoDate);
            });

            return;
        }

        container.innerHTML = `
            <div class="selected-day-actions">
                <button
                    id="btnCreateTaskForSelectedDay"
                    class="btn btn-primary"
                    type="button"
                >
                    + Crear tarea
                </button>
            </div>

            ${dayTasks.map(task => `
                <article class="day-task ${statusClass(task.estado)}">
                    <div class="day-task-main">
                        <strong>
                            ${escapeHtml(task.titulo)}
                        </strong>

                        <small>
                            ${escapeHtml(
                                task.responsable || "Sin responsable"
                            )}
                        </small>
                    </div>

                    <div class="day-task-meta">
                        <span class="status-badge ${statusClass(
                            task.estado
                        )}">
                            ${escapeHtml(task.estado)}
                        </span>

                        <span>
                            ${Number(task.avance || 0)}%
                        </span>
                    </div>

                    <div class="day-task-actions">
                        <button
                            class="icon-button"
                            type="button"
                            title="Editar"
                            data-selected-edit-id="${task.id}"
                        >
                            ✏
                        </button>
                    </div>
                </article>
            `).join("")}
        `;

        document.getElementById(
            "btnCreateTaskForSelectedDay"
        )?.addEventListener("click", () => {
            openNewTaskForDate(isoDate);
        });

        container.querySelectorAll(
            "[data-selected-edit-id]"
        ).forEach(button => {
            button.addEventListener("click", () => {
                window.App?.editTask(
                    Number(button.dataset.selectedEditId)
                );
            });
        });
    }

    function openNewTaskForDate(isoDate) {
        window.App?.openTaskModal();

        const dueDateInput =
            document.getElementById("fechaPrevista");

        if (dueDateInput) {
            dueDateInput.value = isoDate;
        }
    }

    function getTasksForDate(isoDate) {
        return tasks
            .filter(task => {
                const taskDate =
                    task.fecha_prevista ||
                    task.fecha ||
                    "";

                return taskDate === isoDate;
            })
            .sort((a, b) => {
                const priorityOrder = {
                    "Crítica": 1,
                    "Alta": 2,
                    "Media": 3,
                    "Baja": 4
                };

                return (
                    (priorityOrder[a.prioridad] || 5) -
                    (priorityOrder[b.prioridad] || 5)
                );
            });
    }

    function parseTaskDate(task) {
        const value =
            task.fecha_prevista ||
            task.fecha ||
            "";

        if (!value) {
            return null;
        }

        const parsed = new Date(`${value}T12:00:00`);

        return Number.isNaN(parsed.getTime())
            ? null
            : parsed;
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

    function setText(id, value) {
        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
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
        render
    };

})();
