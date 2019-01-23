#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
;#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance Force
#Persistent

#NoTrayIcon

SetImage(s){
    Loop{
        FileGetSize size, image.pipe
        if(size = 0){
            f := FileOpen("image.pipe", "w")
            f.Write(s)
            f.Close()
            Return
        }
        Sleep 5
    }
    Return
}

#Include ${ActionPath}

${DefinitionOfUnusedFunctions}

WatchFile(filename, callback){
    Loop{
        FileGetSize size, %filename%
        if(size > 0){
            FileRead msg, %filename%
            MessageReceived(msg)
            f := FileOpen(filename, "w")
            f.Write()
            f.Close()
        }
        Sleep 5
    }
    Return
}

MessageReceived(s) {
	if (s = "initialize")
		initialize()

	if (s = "on_pressed")
		on_pressed()

	if (s = "on_released")
		on_released()

}

WatchFile("events.pipe", MessageReceived)

