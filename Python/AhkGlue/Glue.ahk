#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#NoTrayIcon

;#Include ${PATH}


pipe_name := "/pmdeck/ahk/button1"

SetTimer, timer_DetectChange, 0
return

HandleExit:
	return
ExitApp

listener:
    loop,
    {

        While !DllCall("WaitNamedPipe", "Str", pipe_name, "UInt", 0xffffffff)
            Sleep, 500

        Loop, read, %pipe_name%
            MSgBox, %A_LoopReadLine%

    }

return





ptr := A_PtrSize ? "Ptr" : "UInt"
char_size := A_IsUnicode ? 2 : 1


InputBox, PipeMsg, Create a pipe message, Enter a message to write in %pipe_name%.,,, 160,,,,, This is a message
If ErrorLevel
    ExitApp

pipe := CreateNamedPipe(pipe_name, 2)
If pipe = -1
{
    MsgBox CreateNamedPipe failed.
    ExitApp
}

DllCall("ConnectNamedPipe", ptr, pipe, ptr, 0)

;MsgBox, Connected

PipeMsg := (A_IsUnicode ? chr(0xfeff) : chr(239) chr(187) chr(191)) . PipeMsg
If !DllCall("WriteFile", ptr, pipe, "str", PipeMsg, "uint", (StrLen(PipeMsg)+1)*char_size, "uint*", 0, ptr, 0)
    MsgBox WriteFile failed: %ErrorLevel%/%A_LastError%

;MsgBox, Click OK to close handle

DllCall("CloseHandle", ptr, pipe)
ExitApp

CreateNamedPipe(Name, OpenMode=3, PipeMode=0, MaxInstances=255)
{
    global ptr
    return DllCall("CreateNamedPipe", "str", Name, "uint", OpenMode, "uint", PipeMode, "uint", MaxInstances, "uint", 0, "uint", 0, "uint", 0, ptr, 0, ptr)
}









