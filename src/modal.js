/*
modal.txt
Renombrar a: static/js/modal.js

Gestión de los modales de ToDo - Versión 2.0.
*/

"use strict";

window.Modals = (() => {

    let editingTaskId = null;

    function init() {
        bindTaskModal();
        bindCommentsModal();
    }

    function bindTaskModal() {
        const modal = document.getElementById("taskModal");
        const form = document.getElementById("taskForm");

        document.getElementById("btnNewTask")
            ?.addEventListener("click", () => openTask());

        document.getElementById("btnCloseTaskModal")
            ?.addEventListener("click", closeTask);

        document.getElementById("btnCancel")
            ?.addEventListener("click", closeTask);

        modal?.addEventListener("click", event => {
            if (event.target === modal) {
                closeTask();
            }
        });

        form?.addEventListener("submit", async event => {
            event.preventDefault();
            await saveTask();
        });

        document.getElementById("avance")
            ?.addEventListener("input", event => {
                const output =
                    document.getElementById("avanceOutput");

                if (output) {
                    output.value = `${event.target.value}%`;
                }
            });
    }

    function bindCommentsModal() {
        const modal = document.getElementById("commentsModal");

        document.getElementById("btnCloseCommentsModal")
            ?.addEventListener("click", () => {
                window.CommentsUI?.close();
            });

        modal?.addEventListener("click", event => {
            if (event.target === modal) {
                window.CommentsUI?.close();
            }
        });
    }

    function openTask(task = null) {
        const modal = document.getElementById("taskModal");
        const form = document.getElementById("taskForm");
        const title = document.getElementById("taskModalTitle");

        if (!modal || !form) {
            return;
        }

        form.reset();

        if (task) {
            editingTaskId = Number(task.id);

            if (title) {
                title.textContent = "Editar tarea";
            }

            setValue("titulo", task.titulo);
            setValue("descripcion", task.descripcion);
            setValue("responsable", task.responsable);
            setValue("prioridad", task.prioridad || "Media");
            setValue("estado", task.estado || "Pendiente");
            setValue("avance", Number(task.avance || 0));
            setValue("fechaInicio", task.fecha_inicio || "");
            setValue("fechaPrevista", task.fecha_prevista || "");
            setValue("proyecto", task.proyecto || "");
            setValue(
                "etiquetas",
                Array.isArray(task.etiquetas)
                    ? task.etiquetas.join(", ")
                    : task.etiquetas || ""
            );
            setValue(
                "tiempoEstimado",
                Number(task.tiempo_estimado || 0)
            );
            setValue(
                "tiempoEmpleado",
                Number(task.tiempo_empleado || 0)
            );
            setValue("recordatorio", task.recordatorio || "");
            setValue("observaciones", task.observaciones || "");

            const output =
                document.getElementById("avanceOutput");

            if (output) {
                output.value = `${Number(task.avance || 0)}%`;
            }

        } else {
            editingTaskId = null;

            if (title) {
                title.textContent = "Nueva tarea";
            }

            setValue("prioridad", "Media");
            setValue("estado", "Pendiente");
            setValue("avance", 0);
            setValue("tiempoEstimado", 0);
            setValue("tiempoEmpleado", 0);

            const output =
                document.getElementById("avanceOutput");

            if (output) {
                output.value = "0%";
            }
        }

        modal.classList.remove("hidden");

        setTimeout(() => {
            document.getElementById("titulo")?.focus();
        }, 50);
    }

    function closeTask() {
        const modal = document.getElementById("taskModal");
        const form = document.getElementById("taskForm");

        modal?.classList.add("hidden");
        form?.reset();

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
            etiquetas: parseTags(getValue("etiquetas")),
            tiempo_estimado: Number(
                getValue("tiempoEstimado") || 0
            ),
            tiempo_empleado: Number(
                getValue("tiempoEmpleado") || 0
            ),
            recordatorio: getValue("recordatorio"),
            observaciones: getValue("observaciones").trim()
        };

        if (!payload.titulo) {
            window.Notifications?.error(
                "El título es obligatorio."
            );
            return;
        }

        try {
            if (editingTaskId !== null) {
                await window.Api.Tasks.update(
                    editingTaskId,
                    payload
                );

                window.Notifications?.success(
                    "Tarea actualizada."
                );
            } else {
                await window.Api.Tasks.create(payload);

                window.Notifications?.success(
                    "Tarea creada."
                );
            }

            closeTask();

            await window.App?.reloadData();

        } catch (error) {
            console.error(error);

            window.Notifications?.error(
                error.message || "No se pudo guardar la tarea."
            );
        }
    }

    function editTask(taskId) {
        const task = window.App?.tasks?.find(
            item => Number(item.id) === Number(taskId)
        );

        if (task) {
            openTask(task);
        }
    }

    function getEditingTaskId() {
        return editingTaskId;
    }

    function parseTags(value) {
        return String(value || "")
            .split(",")
            .map(item => item.trim())
            .filter(Boolean);
    }

    function setValue(id, value) {
        const element = document.getElementById(id);

        if (element) {
            element.value = value ?? "";
        }
    }

    function getValue(id) {
        return document.getElementById(id)?.value ?? "";
    }

    return {
        init,
        openTask,
        closeTask,
        editTask,
        getEditingTaskId
    };

})();
