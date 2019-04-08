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
            for(let i = 0;i<e.dataTransfer.files.length;i++){
                let file = e.dataTransfer.files[i];
                console.log('File(s) you dragged here: ', file.path);
            }
            
            return false;
        };

        const {ipcRenderer}=require('electron')

        let actions = Array.from(<HTMLScriptElement[]><any>document.getElementsByClassName("action")); 
        
        actions.forEach(elem => {
            
            //elem.addEventListener('dragstart', function(e){
            //    e.dataTransfer.setData('path', 'foo');
            //});
            elem.ondragstart = (event) => {
                event.preventDefault();
                ipcRenderer.send('ondragstart', "/stuff/asd");
            }

        });

        ipcRenderer.on('ping', (event:any, arg:any) => {
            console.log(arg)
            

         })

    }
}

function setKeyAction(deck_id:string, key_index:number, action_id:string) {
    
}

function getActionList() {
    
    let list = [{"action_id":"asdsa","action_icon":"asd","name":"open"}];
    return list;
}

function sendKeyEvent(deck_id:string, key_index:number, is_pressed_or_released:string) {
    
}

//Server side event
function receiveKeyImage(deck_id:string, key_index:number, base64string:string) {
    
}

function receiveDeckSize(deck_id:string, dim_x:number, dim_y:number) {

}

function sendDeckSize(deck_id:string, dim_x:number, dim_y:number) {

}






