;AutoHotkey

enabled := 1

initialize(){
    SetImage("mic-on.png")
    SoundSet, 0, MASTER, mute, 6
    Return
}


on_pressed(){
    global enabled
    if (enabled = 1) {
        ;Mute Mic
        SoundSet, 1, MASTER, mute, 6
        SetImage("mic-off.png")
        enabled := 0
    }else{
        ;Unmute Mic
        SoundSet, 0, MASTER, mute, 6
        SetImage("mic-on.png")
        enabled := 1
    }
    Return
}

