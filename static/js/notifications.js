/*
notifications.txt
Renombrar a: static/js/notifications.js

Sistema centralizado de notificaciones.
*/

"use strict";

window.Notifications = (() => {

    let timer = null;
    let container = null;

    function init() {
        container = document.getElementById("notify");

        if (!container) {
            container = document.createElement("div");
            container.id = "notify";
            container.className = "notify hidden";
            document.body.appendChild(container);
        }
    }

    function show(message, type = "info", duration = 3000) {
        if (!container) {
            init();
        }

        clearTimeout(timer);

        container.textContent = message;
        container.className = `notify ${type}`;
        container.classList.remove("hidden");

        timer = setTimeout(() => {
            hide();
        }, duration);
    }

    function hide() {
        if (!container) return;
        container.classList.add("hidden");
    }

    function success(message) {
        show(message, "success");
    }

    function error(message) {
        show(message, "error", 5000);
    }

    function warning(message) {
        show(message, "warning", 4000);
    }

    function info(message) {
        show(message, "info");
    }

    function confirmDialog(message) {
        return window.confirm(message);
    }

    return {
        init,
        show,
        hide,
        success,
        error,
        warning,
        info,
        confirm: confirmDialog
    };

})();
