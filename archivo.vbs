set cmd = createobject("wscript.shell")
Set shell = CreateObject("Scripting.FileSystemObject")
dta=" @echo off"&vbcrlf& _
"%C:\Users\Nicolas Granada\Desktop%"&vbcrlf& _
""
cmd.run "SGE.bat", vbHide
