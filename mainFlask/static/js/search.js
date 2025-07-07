document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("toggle-annotation");
    const highlightedElems = document.querySelectorAll(".message-highlighted");
    const annotatedElems = document.querySelectorAll(".message-annotated");

    checkbox.addEventListener("change", function () {
        const showAnnotated = checkbox.checked;
        highlightedElems.forEach(el => el.style.display = showAnnotated ? "none" : "block");
        annotatedElems.forEach(el => el.style.display = showAnnotated ? "block" : "none");
    });
});