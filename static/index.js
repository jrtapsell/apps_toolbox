Array(...document.querySelectorAll("img.install_qr")).forEach(p => {
    p.onclick = () => {
        p.blur()
        p.requestFullscreen()
    }

    p.addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
          // Cancel the default action, if needed
          event.preventDefault();
          // Trigger the button element with a click
          p.click();
        }
      });
})