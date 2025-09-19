Set objShell = CreateObject("WScript.Shell") 
WScript.Sleep 2000 
objShell.Run "chrome.exe --new-window --incognito --no-cache http://localhost:5050", 1, False 
