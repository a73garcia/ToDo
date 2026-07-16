/*
filters.txt
Renombrar a: static/js/filters.js

Centraliza la lógica de filtros y búsquedas.
*/

"use strict";

window.Filters = (() => {

    let dashboardFilter = null;

    function init() {
        [
            "txtSearch",
            "filterStatus",
            "filterPriority",
            "filterResponsible",
            "sortTasks"
        ].forEach(id => {
            document.getElementById(id)
                ?.addEventListener("input", apply);
            document.getElementById(id)
                ?.addEventListener("change", apply);
        });

        document.querySelectorAll("[data-dashboard-filter]")
            .forEach(card => {
                card.addEventListener("click", () => {
                    applyDashboard(card.dataset.dashboardFilter);
                });
            });

        document.getElementById("btnClearFilters")
            ?.addEventListener("click", clear);
    }

    function applyDashboard(filter) {
        dashboardFilter = filter || null;

        if (window.App?.changeView) {
            window.App.changeView("tasks");
        }

        if (filter === "all") {
            clear();
            return;
        }

        const status = document.getElementById("filterStatus");

        if (status) {
            if (["Pendiente","En curso","Bloqueada","Finalizada","Cancelada"].includes(filter)) {
                status.value = filter;
            } else {
                status.value = "";
            }
        }

        apply();
    }

    function clear() {
        ["txtSearch","filterStatus","filterPriority","filterResponsible"]
            .forEach(id => {
                const e = document.getElementById(id);
                if (e) e.value = "";
            });

        const sort = document.getElementById("sortTasks");
        if (sort) sort.value = "id-desc";

        dashboardFilter = null;
        apply();
    }

    function apply() {
        if (!window.TasksUI) return;

        if (dashboardFilter === "overdue") {
            window.TasksUI.applyOverdueFilter();
            return;
        }

        window.TasksUI.render();
    }

    function getDashboardFilter() {
        return dashboardFilter;
    }

    return {
        init,
        apply,
        clear,
        applyDashboard,
        getDashboardFilter
    };

})();
