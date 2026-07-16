"use strict";

window.Modals = (() => {
    let editingTaskId = null;

    function init() {
        const modal = document.getElementById("taskModal");
        const form = document.getElementById("taskForm");

        document.getElementById("btnNewTask")?.addEventListener("click", () => openTask());
        document.getElementById("btnCloseTaskModal")?.addEventListener("click", closeTask);
        document.getElementById("btnCancel")?.addEventListener("click", closeTask);
        modal?.addEventListener("click", event => { if (event.target === modal) closeTask(); });
        form?.addEventListener("submit", async event => { event.preventDefault(); await saveTask(); });
        document.getElementById("avance")?.addEventListener("input", event => {
            const output = document.getElementById("avanceOutput");
            if (output) output.value = `${event.target.value}%`;
        });
    }

    function openTask(task = null) {
        const modal = document.getElementById("taskModal");
        const form = document.getElementById("taskForm");
        if (!modal || !form) return;

        form.reset();
        editingTaskId = task ? Number(task.id) : null;
        document.getElementById("taskModalTitle").textContent = task ? "Editar tarea" : "Nueva tarea";

        const values = task || {
            prioridad: "Media",
            estado: "Pendiente",
            avance: 0,
            tiempo_estimado: 0,
            tiempo_empleado: 0
        };

        setValue("titulo", values.titulo);
        setValue("descripcion", values.descripcion);
        setValue("responsable", values.responsable);
        setValue("prioridad", values.prioridad || "Media");
        setValue("estado", values.estado || "Pendiente");
        setValue("avance", Number(values.avance || 0));
        setValue("fechaInicio", values.fecha_inicio || "");
        setValue("fechaPrevista", values.fecha_prevista || "");
        setValue("proyecto", values.proyecto || "");
        setValue("etiquetas", Array.isArray(values.etiquetas) ? values.etiquetas.join(", ") : values.etiquetas || "");
        setValue("tiempoEstimado", Number(values.tiempo_estimado || 0));
        setValue("tiempoEmpleado", Number(values.tiempo_empleado || 0));
        setValue("recordatorio", values.recordatorio || "");
        setValue("observaciones", values.observaciones || "");

        const output = document.getElementById("avanceOutput");
        if (output) output.value = `${Number(values.avance || 0)}%`;

        modal.classList.remove("hidden");
        setTimeout(() => document.getElementById("titulo")?.focus(), 50);
    }

    function closeTask() {
        document.getElementById("taskModal")?.classList.add("hidden");
        document.getElementById("taskForm")?.reset();
        editingTaskId = null;
    }

    async function saveTask() {
        const payload = {
            titulo: getValue("titulo").trim(),
            descripcion: getValue("descripcion").trim(),
            responsable: getValue("responsable").trim(),
            prioridad: getValue("prioridad"),
            estado: getValue("estado"),
            avance: Number(getValue("avance") || 0),
            fecha_inicio: getValue("fechaInicio"),
            fecha_prevista: getValue("fechaPrevista"),
            proyecto: getValue("proyecto").trim(),
            etiquetas: getValue("etiquetas").split(",").map(item => item.trim()).filter(Boolean),
            tiempo_estimado: Number(getValue("tiempoEstimado") || 0),
            tiempo_empleado: Number(getValue("tiempoEmpleado") || 0),
            recordatorio: getValue("recordatorio"),
            observaciones: getValue("observaciones").trim()
        };

        if (!payload.titulo) {
            window.Notifications?.error("El título es obligatorio.");
            return;
        }

        try {
            if (editingTaskId !== null) {
                await window.Api.Tasks.update(editingTaskId, payload);
                window.Notifications?.success("Tarea actualizada.");
            } else {
                await window.Api.Tasks.create(payload);
                window.Notifications?.success("Tarea creada.");
            }
            closeTask();
            await window.App?.reloadData();
        } catch (error) {
            console.error(error);
            window.Notifications?.error(error.message || "No se pudo guardar la tarea.");
        }
    }

    function setValue(id, value) {
        const element = document.getElementById(id);
        if (element) element.value = value ?? "";
    }

    function getValue(id) {
        return document.getElementById(id)?.value ?? "";
    }

    return {init, openTask, closeTask};
})();
