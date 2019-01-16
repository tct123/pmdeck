
pipe_name := "\\.\pipe\pmdeck\button1"

While !DllCall("WaitNamedPipe", "Str", pipe_name, "UInt", 0xffffffff)
    Sleep, 500

Loop, read, %pipe_name%
 MSgBox, %A_LoopReadLine%

ExitApp
