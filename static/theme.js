function toggleTheme() {
    let theme = document.body.getAttribute("data-theme");
    let newTheme = theme === "dark" ? "light" : "dark";
    document.body.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
}

window.onload = function () {
    let savedTheme = localStorage.getItem("theme") || "dark";
    document.body.setAttribute("data-theme", savedTheme);
};
