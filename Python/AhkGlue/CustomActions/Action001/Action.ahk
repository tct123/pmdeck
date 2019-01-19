


initialize(){
    SoundBeep
    SetImage("mic-on.png")
return
}


on_pressed(){
    SetImage("mic-off.png")
    SoundBeep
return
}


on_released(){
    SetImage("mic-on.png")
return
}