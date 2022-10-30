
const flashSelector = ".flash-container .flash"
const dismissSelector = "i"

document.addEventListener("DOMContentLoaded", (evt) => {
    initFlashMessages()
})

function initFlashMessages() {

    document.querySelectorAll(flashSelector).forEach(
        elem => {
            // Initalizes dismiss
            elem.querySelector(dismissSelector).addEventListener("click", (evt) => {
                elem.remove()
            })
        }
    )

}