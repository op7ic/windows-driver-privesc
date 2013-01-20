print "[+] List System driver and Check file access permissions "
print "[+]             By op7ic(op7ica@gmail.com)               " 
print "[+] If you know me then give me a shout                  "

import os
import win32com.client
import stat
import time
 
class driver():
    def getSystemDrivers(self):
        print "[+] Dumping System Drivers And Their Location"
        # function reference : http://msdn.microsoft.com/en-us/library/windows/desktop/aa394472%28v=vs.85%29.aspx
        strComputer = "."
        WmiServiceConnector = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = WmiServiceConnector.ConnectServer(strComputer,"root\CIMV2")
        listOfDrivers = objSWbemServices.ExecQuery("SELECT * FROM Win32_SystemDriver")
        for objItem1 in listOfDrivers:
            print "\t[+] Dumping info for driver : " , objItem1.PathName
            if objItem1.PathName is not None:
                print "\t\tDriver Path : " , objItem1.PathName
            if objItem1.Description is not None:
                print "\t\tDescription : " , objItem1.Description
            if objItem1.InstallDate is not None:
                print "\t\tInstallation Date : ", objItem1.InstallDate
            if objItem1.ServiceType is not None:
                print "\t\tService Type : ", objItem1.ServiceType
            if objItem1.StartMode is not None:
                print "\t\tStart Mode : ", objItem1.StartMode
            if objItem1.DesktopInteract is not None:
                print "\t\tDesktop Interaction : ", objItem1.DesktopInteract
            if objItem1.Name is not None:
                print "\t\tDriver Name : ", objItem1.Name
            if objItem1.Started is not None:
                print "\t\tDriver started :" , objItem1.Started
            if objItem1.State is not None:
                print "\t\tCurrent Driver State : ",  objItem1.State
            if objItem1.ErrorControl is not None:
                print "\t\tErrorControl : ", objItem1.ErrorControl
            
            fileChecks().checkPermission(objItem1.PathName)
            fileChecks().getBasicInfo(objItem1.PathName)



class fileChecks():
    def checkPermission(self,filePath):
        # based on http://www.ibm.com/developerworks/aix/library/au-python/
        mode=stat.S_IMODE(os.lstat(filePath)[stat.ST_MODE])
        print "\t\t\t[+] Permissions for file ", filePath
        for level in "USR", "GRP", "OTH":
            for perm in "R", "W", "X":
                if mode & getattr(stat,"S_I"+perm+level):
                    print "\t\t\t\t",level, " has ", perm, " permission"
                else:
                    print "\t\t\t\t",level, " does NOT have ", perm, " permission"
    
    def getBasicInfo(self,file_name):
        time_format = "%m/%d/%Y %I:%M:%S %p"
        file_stats = os.stat(file_name)
        modification_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_MTIME]))
        access_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_ATIME]))
        creation_time = time.strftime(time_format,time.localtime(file_stats[stat.ST_CTIME]))
        print "\t\t\t[+] Basic File Information "
        print "\t\t\t\t Modification time: " , modification_time
        print "\t\t\t\t Access time: " , access_time
        print "\t\t\t\t Creation time: " , creation_time
        print "\t\t\t\t Owner UID : ", file_stats[stat.ST_UID]
        print "\t\t\t\t Owner GID : ",  file_stats[stat.ST_GID]   

drivers = driver()
drivers.getSystemDrivers()