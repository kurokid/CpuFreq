#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess
import os
from gi.repository import Unity, Gio, GObject, Dbusmenu

### Fungsi untuk membuat item pada quicklist
def quicklist(tipe, label=None, aksi=None):
	item = Dbusmenu.Menuitem.new ()
	if tipe == 0:
		item.property_set (Dbusmenu.MENUITEM_PROP_LABEL, label)
		item.property_set_bool (Dbusmenu.MENUITEM_PROP_VISIBLE, True)
		item.connect (Dbusmenu.MENUITEM_SIGNAL_ITEM_ACTIVATED, actions, aksi)
	elif tipe == 1:
		### Membuat pemisah pada quicklist
		item.property_set (Dbusmenu.MENUITEM_PROP_TYPE, Dbusmenu.CLIENT_TYPES_SEPARATOR)
		item.property_set_bool (Dbusmenu.MENUITEM_PROP_VISIBLE, True)
	ql.child_append (item)
def badges():	
	try:
		curGovFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
		curGovernor = curGovFile.read().strip("\n")
		curGovFile.close()
	except IOError:
		curGovernor = 00
	### Menampilkan badge pada launcher
	launcher.set_property("count", govList.index(curGovernor))
	launcher.set_property("count_visible", True)
	
def actions(menuitem, a, gov):
	if gov == "ondemand":
		cpuCmd = "pkexec --disable-internal-agent cpupower frequency-set -g "+gov+">/dev/null"
		if(subprocess.check_call(cpuCmd, shell=True)==0):
			successFlag=1
	if gov == "conservative":
		cpuCmd = "pkexec --disable-internal-agent cpupower frequency-set -g "+gov+">/dev/null"
		if(subprocess.check_call(cpuCmd, shell=True)==0):
			successFlag=1
	elif gov == "performance":
		cpuCmd = "pkexec --disable-internal-agent cpupower frequency-set -g "+gov+">/dev/null"
		if(subprocess.check_call(cpuCmd, shell=True)==0):
			successFlag=1
	elif gov == "powersave":
		cpuCmd = "pkexec --disable-internal-agent cpupower frequency-set -g "+gov+">/dev/null"
		if(subprocess.check_call(cpuCmd, shell=True)==0):
			successFlag=1
	elif gov == "userspace":
		freqFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies")
		frequencies = freqFile.readline().strip("\n")
		freqFile.close()
		freqList = frequencies.split(" ")
		del freqList[-1]
		for i in range(len(freqList)):
			freqList[i]=int(freqList[i])/1000
		print("#\n# CPU Clocks: %s" % freqList)
		newFreq = raw_input("#\n# Insert new clock [copy from Cpu Clocks]: ")
		for i in range(int(cpuCores)):
			cpuCmd = "pkexec --disable-internal-agent cpupower frequency-set -f "+newFreq+"Mhz >/dev/null"
			if(subprocess.check_call(cpuCmd, shell=True)==0):
				successFlag=1
			break
	elif gov == "run":
		subprocess.call("i-nex")
	elif gov == "exit":
		loop.quit()
	if successFlag != 1:
		subprocess.call(["zenity", "--error", "--text='Gagal melakukakan perubahan pada frekuensi CPU'", "--window-icon='/opt/cpuMonitor/img/CPU-Z.png'"])
	else:
		badges()
		subprocess.call(["zenity", "--info", "--text='Berhasil melakukakan perubahan pada frekuensi CPU'", "--window-icon='/opt/cpuMonitor/img/CPU-Z.png'"])

loop = GObject.MainLoop()
cpuCores = os.sysconf('SC_NPROCESSORS_ONLN')	
govFile = open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors")
governors = govFile.readline().strip("\n")
govList = governors.split(" ")
del govList[-1]
launcher = Unity.LauncherEntry.get_for_desktop_id ("cpuz.desktop")

### Membuat daftar quicklist berdasarkan urutan
ql = Dbusmenu.Menuitem.new ()
quicklist(0, "I-nex", "run")
quicklist(1)
for gov in govList:	
	LABEL = str(govList.index(gov)) + " - " + gov
	quicklist(0, LABEL, gov)
quicklist(0, "Keluar", "exit")
launcher.set_property("quicklist", ql)

badges()
loop.run()
