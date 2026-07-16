/*
filters_revisado.txt
Renombrar a: static/js/filters.js
*/

"use strict";

window.Filters = (() => {

    let dashboardFilter = null;

    function init() {
        document.querySelectorAll("[data-dashboard-filter]")
            .forEach(card => {
                card.addEventListener("click", () => {
                    applyDashboard(
                        card.dataset.dashboardFilter
                    );
                });
            });
    }

    function applyDashboard(filter) {
        dashboardFilter = filter || null;

        window.App?.changeView("tasks");

        const status =
            document.getElementById("filterStatus");

        const sort =
            document.getElementById("sortTasks");

        if (status) {
            status.value = "";
        }

        if (filter === "all") {
            clear();
            return;
        }

        if (
            status &&
            [
                "Pendiente",
                "En curso",
                "Bloqueada",
                "Finalizada",
                "Cancelada"
            ].includes(filter)
        ) {
            status.value = filter;
        }

        if (filter === "progress" && sort) {
            sort.value = "progress-desc";
        }

        apply();
    }

    function clear() {
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

        dashboardFilter = null;
        window.TasksUI?.render();
    }

    function apply() {
        if (dashboardFilter === "overdue") {
            window.TasksUI?.applyOverdueFilter();
            return;
        }

        window.TasksUI?.render();
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
