/*
utils.txt
Renombrar a: static/js/utils.js

Funciones auxiliares reutilizables.
*/

"use strict";

window.Utils = (() => {

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function toISODate(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, "0");
        const d = String(date.getDate()).padStart(2, "0");
        return `${y}-${m}-${d}`;
    }

    function parseDate(value) {
        if (!value) return null;
        const dt = new Date(`${value}T12:00:00`);
        return Number.isNaN(dt.getTime()) ? null : dt;
    }

    function formatDate(value, locale = "es-ES") {
        const dt = parseDate(value);
        return dt
            ? new Intl.DateTimeFormat(locale).format(dt)
            : "";
    }

    function formatDateTime(value, locale = "es-ES") {
        if (!value) return "";
        const dt = new Date(value);
        if (Number.isNaN(dt.getTime())) return "";
        return new Intl.DateTimeFormat(locale, {
            dateStyle: "short",
            timeStyle: "short"
        }).format(dt);
    }

    function formatNumber(value) {
        return new Intl.NumberFormat("es-ES")
            .format(Number(value || 0));
    }

    function csvValue(value) {
        const text = String(value ?? "")
            .replaceAll('"', '""');
        return `"${text}"`;
    }

    function clamp(value, min, max) {
        return Math.min(max, Math.max(min, value));
    }

    function debounce(fn, delay = 300) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => fn(...args), delay);
        };
    }

    function unique(array) {
        return [...new Set(array)];
    }

    function byId(id) {
        return document.getElementById(id);
    }

    function qs(selector, parent = document) {
        return parent.querySelector(selector);
    }

    function qsa(selector, parent = document) {
        return [...parent.querySelectorAll(selector)];
    }

    function create(tag, className = "") {
        const el = document.createElement(tag);
        if (className) {
            el.className = className;
        }
        return el;
    }

    function download(filename, content, mime = "text/plain;charset=utf-8") {
        const blob = new Blob([content], { type: mime });
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        a.click();

        URL.revokeObjectURL(url);
    }

    function uuid() {
        if (crypto?.randomUUID) {
            return crypto.randomUUID();
        }

        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
            .replace(/[xy]/g, c => {
                const r = Math.random() * 16 | 0;
                const v = c === "x"
                    ? r
                    : (r & 0x3 | 0x8);
                return v.toString(16);
            });
    }

    return {
        escapeHtml,
        toISODate,
        parseDate,
        formatDate,
        formatDateTime,
        formatNumber,
        csvValue,
        clamp,
        debounce,
        unique,
        byId,
        qs,
        qsa,
        create,
        download,
        uuid
    };

})();
