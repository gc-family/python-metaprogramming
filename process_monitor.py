import win32com
import win32api
import win32con
import win32security

import wmi
import os
import sys

filename = "process_monitor_log.csv"


def log_to_file(message):
    fd = open(filename, "ab")
    fd.write(message.encode())
    fd.close()
    return None


def get_process_privileges(pid):
    try:
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)

        # iterate over privileges and output the ones that are enabled
        priv_list = ""
        for i in privs:
            # check if the privilege is enabled
            if i[1] == 3:
                priv_list += "%s|" % win32security.LookupPrivilegeName(None, i[0])
    except:
        priv_list = "N/A"

    return priv_list


log_to_file("Time,User,Executable,CommandLine,PID,Parent PID,Privileges")
c = wmi.WMI()

# create process monitor

process_watcher = c.Win32_Process.watch_for("creation")


def attack():
    while True:
        try:
            new_process = process_watcher()
            proc_owner = new_process.GetOwner()
            proc_owner = "%s\\%s" % (proc_owner[0], proc_owner[2])
            create_date = new_process.CreationDate
            executable = new_process.ExecutablePath
            cmdline = new_process.CommandLine
            pid = new_process.ProcessId
            parent_pid = new_process.ParentProcessId
            privileges = get_process_privileges(pid)
            process_log_message = "%s,%s,%s,%s,%s,%s,%s\r\n" % (
                create_date, proc_owner, executable, cmdline, pid, parent_pid, privileges)
            print(process_log_message)
            log_to_file(process_log_message)
        except:
            pass


if __name__ == '__main__':
    os.system("subl {}".format(filename))
    attack()
