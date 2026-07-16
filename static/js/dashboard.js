/*
dashboard.js - Versión 2.0
Gestiona la parte visual del Dashboard.
*/
"use strict";

window.DashboardUI = (() => {

    let tasks = [];

    function render(data = []) {
        tasks = [...data];
        renderStatusChart();
        renderRecentActivity();
    }

    function renderStatusChart() {
        const container = document.getElementById("statusChart");
        if (!container) return;

        const states = [
            "Pendiente",
            "En curso",
            "Bloqueada",
            "Finalizada",
            "Cancelada"
        ];

        const counts = {};
        states.forEach(s => counts[s] = 0);

        tasks.forEach(t => {
            if (counts[t.estado] !== undefined) counts[t.estado]++;
        });

        const total = Math.max(tasks.length, 1);

        container.innerHTML = states.map(state => {
            const value = counts[state];
            const pct = Math.round(value * 100 / total);
            return `
            <div class="chart-row">
                <div class="chart-label">${state}</div>
                <div class="chart-bar">
                    <div class="chart-fill" style="width:${pct}%"></div>
                </div>
                <div class="chart-value">${value}</div>
            </div>`;
        }).join("");
    }

    function renderRecentActivity() {
        const container = document.getElementById("recentActivity");
        if (!container) return;

        const ordered = [...tasks]
            .sort((a,b)=>
                String(b.ultima_actualizacion||"")
                    .localeCompare(String(a.ultima_actualizacion||""))
            )
            .slice(0,10);

        if (!ordered.length) {
            container.innerHTML =
                '<p class="empty-state">No hay actividad registrada.</p>';
            return;
        }

        container.innerHTML = ordered.map(task => `
            <article class="activity-item">
                <span class="activity-dot"></span>
                <div>
                    <strong>${escape(task.titulo)}</strong>
                    <div>${escape(task.estado)} · ${escape(task.responsable||"Sin responsable")}</div>
                    <small>${escape(task.ultima_actualizacion||"")}</small>
                </div>
            </article>
        `).join("");
    }

    function escape(v){
        return String(v??"")
        .replaceAll("&","&amp;")
        .replaceAll("<","&lt;")
        .replaceAll(">","&gt;");
    }

    return {render};

})();
