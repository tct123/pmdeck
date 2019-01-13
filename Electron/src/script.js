const remote = require('electron').remote

console.log('Initializing app')

document.onreadystatechange = () => {
    if (document.readyState === 'complete') {
        document
            .getElementById('minimize-btn')
            .addEventListener('click', function(e) {
                const window = remote.getCurrentWindow()
                window.minimize()
            })

        document
            .getElementById('close-btn')
            .addEventListener('click', function(e) {
                const window = remote.getCurrentWindow()
                window.close()
            })
    }
}
