/*
app_revisado.txt
Renombrar a: static/js/app.js

Coordinador principal de ToDo - Versión 2.0 revisada.
*/

"use strict";

window.App = (() => {

    let tasks = [];

    async function init() {
        window.Notifications?.init();
        window.CommentsUI?.init();
        window.Modals?.init();
        window.TasksUI?.init();
        window.Filters?.init();

        bindNavigation();
        showCurrentDate();
        bindTheme();

        await reloadData();
        changeView("dashboard");
    }

    async function reloadData() {
        try {
            tasks = await window.Api.Tasks.all();

            window.TasksUI?.setTasks(tasks);
            await window.DashboardUI?.render(tasks);
            window.CalendarUI?.render(tasks);

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudieron cargar los datos."
            );
        }
    }

    function bindNavigation() {
        document.querySelectorAll(".nav-item")
            .forEach(button => {
                button.addEventListener("click", () => {
                    changeView(button.dataset.view);
                });
            });
    }

    function changeView(view) {
        document.querySelectorAll(".view")
            .forEach(section => {
                section.classList.toggle(
                    "active",
                    section.id === view
                );
            });

        document.querySelectorAll(".nav-item")
            .forEach(button => {
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

        const title = document.getElementById("pageTitle");

        if (title) {
            title.textContent = titles[view] || "ToDo";
        }

        if (view === "calendar") {
            window.CalendarUI?.render(tasks);
        }
    }

    function showCurrentDate() {
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
    }

    function bindTheme() {
        const select = document.getElementById("settingTheme");

        if (!select) {
            return;
        }

        const stored = localStorage.getItem("todo-theme") || "light";

        select.value = stored;
        document.body.classList.toggle(
            "dark",
            stored === "dark"
        );

        select.addEventListener("change", () => {
            const dark = select.value === "dark";

            document.body.classList.toggle("dark", dark);
            localStorage.setItem(
                "todo-theme",
                dark ? "dark" : "light"
            );
        });
    }

    function editTask(id) {
        const task = tasks.find(
            item => Number(item.id) === Number(id)
        );

        if (task) {
            window.Modals?.openTask(task);
        }
    }

    function openTaskModal() {
        window.Modals?.openTask();
    }

    async function deleteTask(id) {
        const confirmed = window.Notifications?.confirm(
            "¿Eliminar la tarea?"
        );

        if (!confirmed) {
            return;
        }

        try {
            await window.Api.Tasks.remove(id);

            window.Notifications?.success(
                "Tarea eliminada."
            );

            await reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message ||
                "No se pudo eliminar la tarea."
            );
        }
    }

    return {
        init,
        reloadData,
        changeView,
        editTask,
        openTaskModal,
        deleteTask,

        get tasks() {
            return tasks;
        }
    };

})();

window.addEventListener(
    "DOMContentLoaded",
    () => window.App.init()
);
