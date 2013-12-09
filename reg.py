#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _winreg

def setupShell():
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
    _winreg.SetValue(key,"Shell", _winreg.REG_SZ,"python c:\detector\ui.py")
    value, type = _winreg.QueryValueEx(key, "Shell")
    print "Shell is " + value

def restoreShell():
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")

    _winreg.SetValue(key,"Shell",_winreg.REG_SZ,"explorer")

    value, type = _winreg.QueryValueEx(key, "Shell")
    print "Shell is " + value


if __name__ == "__main__":
    setupShell()
