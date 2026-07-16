/*
calendar_v2.txt
Renombrar a: static/js/calendar.js

Calendario mensual de ToDo - Versión 2.0.
*/

"use strict";

window.CalendarUI = (() => {

    let tasks = [];
    let currentDate = new Date();
    let selectedDate = null;
    let initialized = false;
    let draggedTaskId = null;

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

        tasks = Array.isArray(data)
            ? [...data]
            : [];

        renderTitle();
        renderGrid();
        renderSummary();

        if (selectedDate) {
            renderSelectedDay(selectedDate);
        }
    }

    function renderTitle() {
        const title = document.getElementById(
            "calendarTitle"
        );

        if (!title) {
            return;
        }

        title.textContent =
            new Intl.DateTimeFormat(
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
        const grid = document.getElementById(
            "calendarGrid"
        );

        if (!grid) {
            return;
        }

        grid.innerHTML = "";

        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        const firstDay = new Date(
            year,
            month,
            1
        );

        const lastDay = new Date(
            year,
            month + 1,
            0
        );

        const previousMonthLastDay = new Date(
            year,
            month,
            0
        );

        let startOffset = firstDay.getDay() - 1;

        if (startOffset < 0) {
            startOffset = 6;
        }

        const daysInMonth = lastDay.getDate();
        const previousMonthDays =
            previousMonthLastDay.getDate();

        const todayISO = toISODate(new Date());

        for (let index = 0; index < 42; index += 1) {

            let dayNumber;
            let cellDate;
            let outsideMonth = false;

            if (index < startOffset) {
                dayNumber =
                    previousMonthDays -
                    startOffset +
                    index +
                    1;

                cellDate = new Date(
                    year,
                    month - 1,
                    dayNumber
                );

                outsideMonth = true;

            } else if (
                index >= startOffset + daysInMonth
            ) {
                dayNumber =
                    index -
                    startOffset -
                    daysInMonth +
                    1;

                cellDate = new Date(
                    year,
                    month + 1,
                    dayNumber
                );

                outsideMonth = true;

            } else {
                dayNumber =
                    index -
                    startOffset +
                    1;

                cellDate = new Date(
                    year,
                    month,
                    dayNumber
                );
            }

            const isoDate = toISODate(cellDate);
            const dayTasks = tasksForDate(isoDate);

            const cell = document.createElement(
                "section"
            );

            cell.className = "calendarCell";
            cell.dataset.date = isoDate;
            cell.tabIndex = 0;

            if (outsideMonth) {
                cell.classList.add(
                    "outsideMonth"
                );
            }

            if (isoDate === todayISO) {
                cell.classList.add("today");
            }

            if (isoDate === selectedDate) {
                cell.classList.add("selected");
            }

            cell.innerHTML = `
                <div class="calendar-day-header">
                    <span class="calendarDayNumber">
                        ${dayNumber}
                    </span>

                    ${
                        dayTasks.length
                            ? `
                                <span class="calendar-count">
                                    ${dayTasks.length}
                                </span>
                              `
                            : ""
                    }
                </div>

                <div class="calendarTaskList">
                    ${dayTasks.slice(0, 4).map(
                        task => taskTemplate(task)
                    ).join("")}

                    ${
                        dayTasks.length > 4
                            ? `
                                <button
                                    type="button"
                                    class="calendar-more"
                                    data-calendar-more="${isoDate}"
                                >
                                    +${dayTasks.length - 4} más
                                </button>
                              `
                            : ""
                    }
                </div>
            `;

            bindCellEvents(
                cell,
                isoDate
            );

            grid.appendChild(cell);
        }

        bindTaskEvents(grid);
    }

    function taskTemplate(task) {
        return `
            <button
                type="button"
                class="calendarTask ${statusClass(
                    task.estado
                )}"
                title="${escapeHtml(task.titulo)}"
                draggable="true"
                data-calendar-task-id="${task.id}"
            >
                <span class="calendar-task-dot"></span>

                <span class="calendar-task-title">
                    ${escapeHtml(task.titulo)}
                </span>

                ${
                    Number(task.avance || 0)
                        ? `
                            <span class="calendar-task-progress">
                                ${Number(task.avance || 0)}%
                            </span>
                          `
                        : ""
                }
            </button>
        `;
    }

    function bindCellEvents(
        cell,
        isoDate
    ) {
        cell.addEventListener(
            "click",
            event => {
                if (
                    event.target.closest(
                        "[data-calendar-task-id]"
                    )
                ) {
                    return;
                }

                selectedDate = isoDate;

                renderGrid();
                renderSelectedDay(isoDate);
            }
        );

        cell.addEventListener(
            "dblclick",
            event => {
                if (
                    event.target.closest(
                        "[data-calendar-task-id]"
                    )
                ) {
                    return;
                }

                openNewTaskForDate(isoDate);
            }
        );

        cell.addEventListener(
            "dragover",
            event => {
                event.preventDefault();
                cell.classList.add(
                    "drag-over"
                );
            }
        );

        cell.addEventListener(
            "dragleave",
            () => {
                cell.classList.remove(
                    "drag-over"
                );
            }
        );

        cell.addEventListener(
            "drop",
            async event => {
                event.preventDefault();

                cell.classList.remove(
                    "drag-over"
                );

                if (draggedTaskId === null) {
                    return;
                }

                await moveTask(
                    draggedTaskId,
                    isoDate
                );

                draggedTaskId = null;
            }
        );

        cell.addEventListener(
            "keydown",
            event => {
                if (
                    event.key === "Enter" ||
                    event.key === " "
                ) {
                    event.preventDefault();

                    selectedDate = isoDate;
                    renderGrid();
                    renderSelectedDay(
                        isoDate
                    );
                }
            }
        );
    }

    function bindTaskEvents(container) {
        container.querySelectorAll(
            "[data-calendar-task-id]"
        ).forEach(button => {

            button.addEventListener(
                "click",
                event => {
                    event.stopPropagation();

                    window.App?.editTask(
                        Number(
                            button.dataset
                                .calendarTaskId
                        )
                    );
                }
            );

            button.addEventListener(
                "dragstart",
                event => {
                    draggedTaskId = Number(
                        button.dataset
                            .calendarTaskId
                    );

                    event.dataTransfer.effectAllowed =
                        "move";

                    event.dataTransfer.setData(
                        "text/plain",
                        String(draggedTaskId)
                    );

                    button.classList.add(
                        "dragging"
                    );
                }
            );

            button.addEventListener(
                "dragend",
                () => {
                    draggedTaskId = null;

                    button.classList.remove(
                        "dragging"
                    );

                    document.querySelectorAll(
                        ".calendarCell.drag-over"
                    ).forEach(cell => {
                        cell.classList.remove(
                            "drag-over"
                        );
                    });
                }
            );
        });

        container.querySelectorAll(
            "[data-calendar-more]"
        ).forEach(button => {
            button.addEventListener(
                "click",
                event => {
                    event.stopPropagation();

                    selectedDate =
                        button.dataset.calendarMore;

                    renderGrid();
                    renderSelectedDay(
                        selectedDate
                    );
                }
            );
        });
    }

    async function moveTask(
        taskId,
        isoDate
    ) {
        try {
            await window.Api.request(
                `/tasks/${taskId}/move`,
                {
                    method: "POST",
                    body: JSON.stringify({
                        fecha_prevista: isoDate
                    })
                }
            );

            window.Notifications?.success(
                "Tarea movida al calendario."
            );

            selectedDate = isoDate;

            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo mover la tarea."
            );
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

        const count = state =>
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
            ).format(
                new Date(
                    year,
                    month,
                    1
                )
            )
        );

        setText(
            "calendarTotal",
            monthTasks.length
        );

        setText(
            "calendarPending",
            count("Pendiente")
        );

        setText(
            "calendarRunning",
            count("En curso")
        );

        setText(
            "calendarBlocked",
            count("Bloqueada")
        );

        setText(
            "calendarFinished",
            count("Finalizada")
        );
    }

    function renderSelectedDay(
        isoDate
    ) {
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

        title.textContent =
            new Intl.DateTimeFormat(
                "es-ES",
                {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                }
            ).format(parsedDate);

        const dayTasks = tasksForDate(isoDate);

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

            ${
                dayTasks.length
                    ? dayTasks.map(
                        task => selectedDayTaskTemplate(
                            task
                        )
                    ).join("")
                    : `
                        <p class="empty-state">
                            No hay tareas previstas
                            para este día.
                        </p>
                      `
            }
        `;

        document.getElementById(
            "btnCreateTaskForSelectedDay"
        )?.addEventListener(
            "click",
            () => {
                openNewTaskForDate(
                    isoDate
                );
            }
        );

        container.querySelectorAll(
            "[data-selected-edit-id]"
        ).forEach(button => {
            button.addEventListener(
                "click",
                () => {
                    window.App?.editTask(
                        Number(
                            button.dataset
                                .selectedEditId
                        )
                    );
                }
            );
        });

        container.querySelectorAll(
            "[data-selected-comments-id]"
        ).forEach(button => {
            button.addEventListener(
                "click",
                () => {
                    window.CommentsUI?.open(
                        Number(
                            button.dataset
                                .selectedCommentsId
                        )
                    );
                }
            );
        });
    }

    function selectedDayTaskTemplate(task) {
        return `
            <article
                class="day-task ${statusClass(
                    task.estado
                )}"
            >
                <div class="day-task-main">
                    <strong>
                        ${escapeHtml(task.titulo)}
                    </strong>

                    <small>
                        ${escapeHtml(
                            task.responsable ||
                            "Sin responsable"
                        )}
                    </small>
                </div>

                <div class="day-task-meta">
                    <span
                        class="status-badge ${statusClass(
                            task.estado
                        )}"
                    >
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
                        title="Comentarios"
                        data-selected-comments-id="${task.id}"
                    >
                        💬
                    </button>

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
        `;
    }

    function openNewTaskForDate(
        isoDate
    ) {
        window.App?.openTaskModal();

        const dueDateInput =
            document.getElementById(
                "fechaPrevista"
            );

        if (dueDateInput) {
            dueDateInput.value = isoDate;
        }
    }

    function tasksForDate(
        isoDate
    ) {
        const priorityOrder = {
            "Crítica": 1,
            "Alta": 2,
            "Media": 3,
            "Baja": 4
        };

        return tasks
            .filter(task => (
                task.fecha_prevista ||
                task.fecha ||
                ""
            ) === isoDate)
            .sort((a, b) => {
                const priorityDifference =
                    (
                        priorityOrder[
                            a.prioridad
                        ] || 5
                    ) -
                    (
                        priorityOrder[
                            b.prioridad
                        ] || 5
                    );

                if (priorityDifference !== 0) {
                    return priorityDifference;
                }

                return Number(a.id) -
                    Number(b.id);
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

        const parsed = new Date(
            `${value}T12:00:00`
        );

        return Number.isNaN(
            parsed.getTime()
        )
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
        if (window.Utils) {
            return window.Utils.toISODate(
                date
            );
        }

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
        if (window.Utils) {
            return window.Utils.escapeHtml(
                value
            );
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
        render
    };

})();
