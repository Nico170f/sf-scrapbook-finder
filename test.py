import win32com.client as comclt

wsh = comclt.Dispatch("WScript.Shell")
wsh.AppActivate("8224")  # select another application
wsh.SendKeys("{DOWN}", 0)  # send the keys you want
