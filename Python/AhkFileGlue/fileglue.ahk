#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
;#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance Force
#Persistent

;#NoTrayIcon

#Include sizeof.ahk
#Include _Struct.ahk
#Include WatchDirectory.ahk

;#Include ${PATH}
#Include CustomAction.ahk

pipe_name := "/pipe/pmdeck/button1"

WatchDirectory(A_ScriptDir "\|events.pipe\", "__Callback", 0x10)
return

__Callback(param1, param2) {
	FileRead newFileContent, %param1%
	if (!(newFileContent = ""))
	{
		__MessageReceived(newFileContent)
		f := FileOpen(param1, "w")
		f.Write()
		f.Close()
	}
	
}

SetImage(s){
	f := FileOpen("image.pipe", "w")
	f.Write(s)
	f.Close()
}

__MessageReceived(s) {
	if (s = "initialize")
		initialize()

	if (s = "on_pressed")
		on_pressed()

	if (s = "on_released")
		on_released()


}

