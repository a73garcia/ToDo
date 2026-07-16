"use strict";

window.Utils = (() => {
    const escapeHtml = value => String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

    function toISODate(date) {
        return [
            date.getFullYear(),
            String(date.getMonth() + 1).padStart(2, "0"),
            String(date.getDate()).padStart(2, "0")
        ].join("-");
    }

    function formatDate(value) {
        if (!value) return "";
        const date = new Date(`${value}T12:00:00`);
        return Number.isNaN(date.getTime()) ? String(value) : new Intl.DateTimeFormat("es-ES").format(date);
    }

    function formatDateTime(value) {
        if (!value) return "";
        const date = new Date(String(value).replace(" ", "T"));
        return Number.isNaN(date.getTime()) ? String(value) : new Intl.DateTimeFormat("es-ES", {dateStyle: "short", timeStyle: "short"}).format(date);
    }

    function clamp(value, min, max) { return Math.min(max, Math.max(min, value)); }

    function debounce(fn, delay = 250) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => fn(...args), delay);
        };
    }

    function download(filename, content, mime = "text/plain;charset=utf-8") {
        const url = URL.createObjectURL(new Blob([content], {type: mime}));
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
    }

    return {escapeHtml, toISODate, formatDate, formatDateTime, clamp, debounce, download};
})();
