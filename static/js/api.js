"use strict";

window.Api = (() => {
    const BASE = "/api";

    async function request(path, options = {}) {
        const response = await fetch(BASE + path, {
            headers: {"Content-Type": "application/json"},
            ...options
        });
        const type = response.headers.get("content-type") || "";
        const data = type.includes("application/json")
            ? await response.json()
            : await response.text();
        if (!response.ok) {
            throw new Error(data?.error || data?.message || `HTTP ${response.status}`);
        }
        return data;
    }

    return {
        request,
        Tasks: {
            all: () => request("/tasks"),
            get: id => request(`/tasks/${id}`),
            create: task => request("/tasks", {method: "POST", body: JSON.stringify(task)}),
            update: (id, task) => request(`/tasks/${id}`, {method: "PATCH", body: JSON.stringify(task)}),
            replace: (id, task) => request(`/tasks/${id}`, {method: "PUT", body: JSON.stringify(task)}),
            remove: id => request(`/tasks/${id}`, {method: "DELETE"})
        },
        Dashboard: {summary: () => request("/dashboard")},
        Calendar: {month: (year, month) => request(`/calendar?year=${year}&month=${month}`)},
        History: {list: taskId => request(`/history${taskId ? `?task_id=${taskId}` : ""}`)},
        Health: {check: () => request("/health")}
    };
})();
