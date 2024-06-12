Array(...document.querySelectorAll("img.install_qr")).forEach(elem_image => {
    elem_image = elem_image.parentElement
    elem_image.onclick = () => {
        elem_image.requestFullscreen()
    }

    elem_image.onfullscreenchange = () => {
        if (document.fullscreenElement) {
            console.log("Entered fullscreen", elem_image)
        } else {
            console.log("Left fullscreen", elem_image)
        }
    }

    elem_image.addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
          // Cancel the default action, if needed
          event.preventDefault();
          // Trigger the button element with a click
          elem_image.click();
        }
      });
})

Array(...document.querySelectorAll(".exit_fullscreen")).forEach((p) => {
    p.onclick = () => {
        document.exitFullscreen()
    }
})