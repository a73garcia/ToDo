/*
dashboard_v2.txt
Renombrar a: static/js/dashboard.js

Dashboard interactivo de ToDo - Versión 2.0.
*/

"use strict";

window.DashboardUI = (() => {

    let tasks = [];

    function init() {
        bindCards();
    }

    function bindCards() {
        document.querySelectorAll(
            "[data-dashboard-filter]"
        ).forEach(card => {
            card.addEventListener("click", () => {
                const filter =
                    card.dataset.dashboardFilter;

                window.Filters?.applyDashboard(
                    filter
                );
            });
        });
    }

    async function render(data = []) {
        tasks = Array.isArray(data)
            ? [...data]
            : [];

        renderCounters();
        renderStatusChart();
        renderUpcomingTasks();

        await renderRecentActivity();
    }

    function renderCounters() {
        const total = tasks.length;

        const count = state =>
            tasks.filter(
                task => task.estado === state
            ).length;

        const today = window.Utils
            ? window.Utils.toISODate(
                new Date()
            )
            : new Date()
                .toISOString()
                .slice(0, 10);

        const overdue = tasks.filter(task =>
            task.fecha_prevista &&
            task.fecha_prevista < today &&
            ![
                "Finalizada",
                "Cancelada"
            ].includes(task.estado)
        ).length;

        const averageProgress = total
            ? Math.round(
                tasks.reduce(
                    (sum, task) =>
                        sum +
                        Number(
                            task.avance || 0
                        ),
                    0
                ) / total
            )
            : 0;

        setText(
            "totalTasks",
            total
        );

        setText(
            "pendingTasks",
            count("Pendiente")
        );

        setText(
            "runningTasks",
            count("En curso")
        );

        setText(
            "blockedTasks",
            count("Bloqueada")
        );

        setText(
            "finishedTasks",
            count("Finalizada")
        );

        setText(
            "cancelledTasks",
            count("Cancelada")
        );

        setText(
            "overdueTasks",
            overdue
        );

        setText(
            "averageProgress",
            `${averageProgress}%`
        );
    }

    function renderStatusChart() {
        const container = document.getElementById(
            "statusChart"
        );

        if (!container) {
            return;
        }

        const states = [
            {
                name: "Pendiente",
                className: "pending"
            },
            {
                name: "En curso",
                className: "running"
            },
            {
                name: "Bloqueada",
                className: "blocked"
            },
            {
                name: "Finalizada",
                className: "finished"
            },
            {
                name: "Cancelada",
                className: "cancelled"
            }
        ];

        const total = Math.max(
            tasks.length,
            1
        );

        container.classList.remove(
            "chart-placeholder"
        );

        container.innerHTML = `
            <div class="status-chart-list">
                ${states.map(item => {
                    const value = tasks.filter(
                        task =>
                            task.estado ===
                            item.name
                    ).length;

                    const percentage =
                        Math.round(
                            value * 100 /
                            total
                        );

                    return `
                        <button
                            type="button"
                            class="status-chart-row"
                            data-chart-status="${item.name}"
                        >
                            <div class="status-chart-label">
                                <span
                                    class="status-chart-dot ${item.className}"
                                ></span>

                                <span>
                                    ${item.name}
                                </span>
                            </div>

                            <div class="status-chart-bar">
                                <span
                                    class="status-chart-fill ${item.className}"
                                    style="width:${percentage}%"
                                ></span>
                            </div>

                            <strong>
                                ${value}
                            </strong>

                            <small>
                                ${percentage}%
                            </small>
                        </button>
                    `;
                }).join("")}
            </div>
        `;

        container.querySelectorAll(
            "[data-chart-status]"
        ).forEach(button => {
            button.addEventListener(
                "click",
                () => {
                    window.Filters
                        ?.applyDashboard(
                            button.dataset
                                .chartStatus
                        );
                }
            );
        });
    }

    function renderUpcomingTasks() {
        const container = document.getElementById(
            "upcomingTasks"
        );

        if (!container) {
            return;
        }

        const today = new Date();
        const limit = new Date();

        limit.setDate(
            limit.getDate() + 14
        );

        const upcoming = tasks
            .filter(task => {
                if (
                    !task.fecha_prevista ||
                    [
                        "Finalizada",
                        "Cancelada"
                    ].includes(task.estado)
                ) {
                    return false;
                }

                const dueDate = new Date(
                    `${task.fecha_prevista}T12:00:00`
                );

                return (
                    dueDate >= today &&
                    dueDate <= limit
                );
            })
            .sort((a, b) => {
                return String(
                    a.fecha_prevista
                ).localeCompare(
                    String(
                        b.fecha_prevista
                    )
                );
            })
            .slice(0, 8);

        if (!upcoming.length) {
            container.innerHTML = `
                <p class="empty-state">
                    No hay tareas próximas.
                </p>
            `;
            return;
        }

        container.innerHTML =
            upcoming.map(task => `
                <article class="upcoming-card">

                    <div class="upcoming-main">
                        <strong>
                            ${escapeHtml(
                                task.titulo
                            )}
                        </strong>

                        <small>
                            ${escapeHtml(
                                task.responsable ||
                                "Sin responsable"
                            )}
                        </small>
                    </div>

                    <div class="upcoming-meta">

                        <span
                            class="priority-badge ${priorityClass(
                                task.prioridad
                            )}"
                        >
                            ${escapeHtml(
                                task.prioridad
                            )}
                        </span>

                        <span>
                            ${formatDate(
                                task.fecha_prevista
                            )}
                        </span>

                    </div>

                    <button
                        type="button"
                        class="icon-button"
                        title="Abrir tarea"
                        data-upcoming-task="${task.id}"
                    >
                        →
                    </button>

                </article>
            `).join("");

        container.querySelectorAll(
            "[data-upcoming-task]"
        ).forEach(button => {
            button.addEventListener(
                "click",
                () => {
                    window.App?.editTask(
                        Number(
                            button.dataset
                                .upcomingTask
                        )
                    );
                }
            );
        });
    }

    async function renderRecentActivity() {
        const container = document.getElementById(
            "recentActivity"
        );

        if (!container) {
            return;
        }

        container.innerHTML = `
            <p class="empty-state">
                Cargando actividad...
            </p>
        `;

        try {
            const activity =
                await window.Api.History.list();

            const recent = Array.isArray(
                activity
            )
                ? activity.slice(0, 12)
                : [];

            if (!recent.length) {
                container.innerHTML = `
                    <p class="empty-state">
                        No hay actividad registrada.
                    </p>
                `;
                return;
            }

            container.innerHTML =
                recent.map(item => `
                    <article class="activity-item">

                        <span class="activity-dot"></span>

                        <div class="activity-content">

                            <div class="activity-heading">
                                <strong>
                                    ${escapeHtml(
                                        item.accion ||
                                        "Actividad"
                                    )}
                                </strong>

                                <span>
                                    Tarea #${escapeHtml(
                                        item.task_id
                                    )}
                                </span>
                            </div>

                            <p>
                                ${escapeHtml(
                                    item.observaciones ||
                                    ""
                                )}
                            </p>

                            <small>
                                ${escapeHtml(
                                    item.usuario ||
                                    "Sistema"
                                )}
                                ·
                                ${formatDateTime(
                                    item.fecha
                                )}
                            </small>

                        </div>

                    </article>
                `).join("");

        } catch (error) {
            console.error(error);

            container.innerHTML = `
                <div class="empty-state">
                    <strong>
                        No se pudo cargar la actividad
                    </strong>

                    <button
                        id="btnRetryActivity"
                        class="btn btn-secondary"
                        type="button"
                    >
                        Reintentar
                    </button>
                </div>
            `;

            document.getElementById(
                "btnRetryActivity"
            )?.addEventListener(
                "click",
                renderRecentActivity
            );
        }
    }

    function formatDate(value) {
        if (window.Utils) {
            return window.Utils.formatDate(
                value
            );
        }

        return value || "";
    }

    function formatDateTime(value) {
        if (window.Utils) {
            return window.Utils.formatDateTime(
                value
            );
        }

        return value || "";
    }

    function priorityClass(priority) {
        return {
            "Baja": "priority-low",
            "Media": "priority-medium",
            "Alta": "priority-high",
            "Crítica": "priority-critical"
        }[priority] || "priority-medium";
    }

    function setText(id, value) {
        const element =
            document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    }

    function escapeHtml(value) {
        if (window.Utils) {
            return window.Utils
                .escapeHtml(value);
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
