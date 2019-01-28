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


        var holder = document.getElementById('button-image');

        holder.ondragleave = () => {
            console.log("NOT DRAGGING");
            return false;
        };

        holder.ondragend = () => {
            console.log("NOT DRAGGING");
            return false;
        };

        holder.ondragover = function () {
            console.log("DRAGGING");
            return false;
        };

        holder.ondrop = (e) => {
            e.preventDefault();
            console.log(e);
            for (let f of e.dataTransfer.files) {
                console.log('File(s) you dragged here: ', f.path);
            }
            
            return false;
        };

        const {ipcRenderer}=require('electron')

        var actions = document.getElementsByClassName("action"); 
        
        for (let index = 0; index < actions.length; index++) {
            const elem = actions[index];
            
            //elem.addEventListener('dragstart', function(e){
            //    e.dataTransfer.setData('path', 'foo');
            //});
            
            elem.ondragstart = (event) => {
                event.preventDefault();
                ipcRenderer.send('ondragstart', "/stuff/asd");
            }
            

        }
    }
}

function setKeyAction(deck_id, key_index, action_id) {
    
}

function getActionList() {
    
    list = [{"action_id":"asdsa","action_icon":"asd","name":"open"}];
    return list;
}

function sendKeyEvent(deck_id, key_index, is_pressed_or_released) {
    
}

//Server side event
function receiveKeyImage(deck_id, key_index, base64string) {
    
}





