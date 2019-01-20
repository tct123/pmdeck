;AutoHotkey

enabled := 1

initialize(){
    SetImage("mic-on.png")
    SoundBeep
return
}


on_pressed(){
    global enabled
    if (enabled = 1) {
        SetImage("mic-off.png")
        enabled := 0
    }else{
        SetImage("mic-on.png")
        enabled := 1
    }

    SoundBeep
Return
}

