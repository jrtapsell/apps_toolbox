[...document.querySelectorAll('img.install_qr')].forEach(imageelement => {
  imageelement = imageelement.parentElement
  imageelement.onclick = () => {
    imageelement.requestFullscreen()
  }

  imageelement.onfullscreenchange = () => {
    if (document.fullscreenElement) {
      console.log('Entered fullscreen', imageelement)
    } else {
      console.log('Left fullscreen', imageelement)
    }
  }

  imageelement.addEventListener('keypress', function (event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === 'Enter') {
      // Cancel the default action, if needed
      event.preventDefault()
      // Trigger the button element with a click
      imageelement.click()
    }
  })
});

[...document.querySelectorAll('.exit_fullscreen')].forEach((p) => {
  p.onclick = () => {
    document.exitFullscreen()
  }
})
