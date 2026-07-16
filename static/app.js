/*
app.js
Parte 1 - Lógica principal del frontend
*/

"use strict";

const App = {

    tasks: [],

    currentView: "dashboard",

    init() {

        this.cache();

        this.bindEvents();

        this.showDate();

        this.changeView("dashboard");

        this.renderTable();

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

        this.menuButtons.forEach(btn => {

            btn.addEventListener("click", () => {
                this.changeView(btn.dataset.view);
            });

        });

        this.btnNew.addEventListener("click", () => this.openModal());

        this.btnCancel.addEventListener("click", () => this.closeModal());

        this.form.addEventListener("submit", (e) => {
            e.preventDefault();
            this.saveTask();
        });

        this.search.addEventListener("input", () => {
            this.renderTable(this.search.value);
        });

    },

    changeView(view) {

        this.currentView = view;

        this.views.forEach(v => v.classList.remove("active"));

        document.getElementById(view).classList.add("active");

        this.menuButtons.forEach(b => b.classList.remove("active"));

        document.querySelector(`[data-view="${view}"]`).classList.add("active");

    },

    showDate() {

        const d = new Date();

        document.getElementById("currentDate").textContent =
            d.toLocaleDateString("es-ES", {
                weekday: "long",
                day: "numeric",
                month: "long",
                year: "numeric"
            });

    },

    openModal() {

        this.form.reset();

        this.modal.classList.remove("hidden");

    },

    closeModal() {

        this.modal.classList.add("hidden");

    },

    saveTask() {

        const task = {

            id: Date.now(),

            titulo: document.getElementById("titulo").value,

            descripcion: document.getElementById("descripcion").value,

            responsable: document.getElementById("responsable").value,

            prioridad: document.getElementById("prioridad").value,

            fecha: document.getElementById("fechaPrevista").value,

            estado: "Pendiente",

            avance: 0

        };

        this.tasks.push(task);

        this.renderTable();

        this.updateDashboard();

        this.closeModal();

    },

    renderTable(filter = "") {

        this.table.innerHTML = "";

        let data = this.tasks;

        if (filter.trim() !== "") {

            const text = filter.toLowerCase();

            data = data.filter(t =>
                t.titulo.toLowerCase().includes(text) ||
                t.responsable.toLowerCase().includes(text)
            );

        }

        data.forEach(task => {

            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${task.id}</td>
                <td>${task.titulo}</td>
                <td>${task.responsable}</td>
                <td>${task.prioridad}</td>
                <td>${task.estado}</td>
                <td>-</td>
                <td>${task.fecha}</td>
                <td>${task.avance}%</td>
                <td>
                    <button onclick="alert('Edición en desarrollo')">✏️</button>
                </td>
            `;

            this.table.appendChild(tr);

        });

    },

    updateDashboard() {

        document.getElementById("totalTasks").textContent = this.tasks.length;

        document.getElementById("pendingTasks").textContent =
            this.tasks.filter(t => t.estado === "Pendiente").length;

        document.getElementById("runningTasks").textContent =
            this.tasks.filter(t => t.estado === "En curso").length;

        document.getElementById("finishedTasks").textContent =
            this.tasks.filter(t => t.estado === "Finalizada").length;

    }

};

window.addEventListener("DOMContentLoaded", () => App.init());
