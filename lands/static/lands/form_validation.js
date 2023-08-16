document.addEventListener("DOMContentLoaded", function () {
    const decklistTextarea = document.getElementById("decklist");
    const submitButton = document.querySelector(".submit-button");

    decklistTextarea.addEventListener("input", function () {
        const isEmpty = decklistTextarea.value.trim() === "";
        submitButton.disabled = isEmpty;
    });
});