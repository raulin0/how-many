var textarea = document.getElementById('decklist');
var originalPlaceholder = textarea.placeholder;

textarea.addEventListener('focus', function() {
    this.placeholder = '';
});

textarea.addEventListener('blur', function() {
    this.placeholder = originalPlaceholder;
});

document.addEventListener("DOMContentLoaded", function () {
    const decklistTextarea = document.getElementById("decklist");
    const submitButton = document.querySelector("#submit-button");

    decklistTextarea.addEventListener("input", function () {
        const isEmpty = decklistTextarea.value.trim() === "";
        submitButton.disabled = isEmpty;
    });
});