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
powershell_exe = "powershell.exe"



while True:
    data = s.recv(1024)
    decoded_data=data.decode("utf-8").split(",")

    if len(data) > 0:
        if decoded_data[0] == '1':
            cmd2 = subprocess.Popen([powershell_exe, "$groups = Get-LocalGroup;$groups.Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
            output_str2 = str(output_byte2,"utf-8")
            s.send(str.encode(output_str2 +"\n"))

            data = s.recv(1024)
            decoded_data=data.decode("utf-8").split(",")
            cmd = subprocess.Popen([powershell_exe, "$Password = ConvertTo-SecureString " + decoded_data[2] + " -AsPlainText -Force; New-LocalUser '" + decoded_data[1] + "' -Password $Password; Add-LocalGroupMember -Group " + decoded_data[3] + " -Member " + decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)  
            
        elif decoded_data[0] == '2':
            cmd2 = subprocess.Popen([powershell_exe, "$users = Get-LocalUser;$users.Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
            output_str2 = str(output_byte2,"utf-8")
            s.send(str.encode(output_str2 +"\n"))
            
            data = s.recv(1024)
            decoded_data=data.decode("utf-8").split(",")
            cmd = subprocess.Popen([powershell_exe, "Remove-LocalUser -Name "+ decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif decoded_data[0] == '3':
            cmd2 = subprocess.Popen([powershell_exe, "$users = Get-LocalUser;$users.Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
            output_str2 = str(output_byte2,"utf-8")
            s.send(str.encode(output_str2 +"\n"))

            data = s.recv(1024)
            decoded_data=data.decode("utf-8").split(",")
            if decoded_data[2] == '1':
                cmd = subprocess.Popen([powershell_exe, "$Password = ConvertTo-SecureString " + decoded_data[3] + " -AsPlainText -Force; $UserAccount = Get-LocalUser -Name " + decoded_data[1] + "; $UserAccount | Set-LocalUser -Password $Password"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[2] == '2':
                cmd = subprocess.Popen([powershell_exe, "Enable-LocalUser -Name " + decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[2] == '3':
                cmd = subprocess.Popen([powershell_exe, "Disable-LocalUser -Name " + decoded_data[1]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            
            elif decoded_data[2] == '4':
                cmd2 = subprocess.Popen([powershell_exe, "$groups = Get-LocalGroup;$groups.Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
                output_str2 = str(output_byte2,"utf-8")
                s.send(str.encode(output_str2 +"\n" ))

                data = s.recv(1024)
                decoded_data=data.decode("utf-8").split(",")
                
                cmd = subprocess.Popen([powershell_exe, "Add-LocalGroupMember -Group '" + decoded_data[3] + "' -Member '"+ decoded_data[1] + "'"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[2] == '5':
                #print("$groups = Get-LocalGroupMember -Member '"+ decoded_data[1] + "';$groups.Name")
                cmd2 = subprocess.Popen([powershell_exe, "foreach ($localgroup in Get-LocalGroup){if(Get-LocalGroupMember $localgroup -Member '" +  decoded_data[1] + "' -ErrorAction SilentlyContinue){$localgroup.Name}}"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
                output_str2 = str(output_byte2,"utf-8")
                s.send(str.encode(output_str2 +"\n"))
                
                data = s.recv(1024)
                decoded_data=data.decode("utf-8").split(",")
            
                cmd = subprocess.Popen([powershell_exe, "Remove-LocalGroupMember -Group '" + decoded_data[3] + "' -Member '"+ decoded_data[1]  + "'"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                
        elif decoded_data[0] == '4':
            if decoded_data[1] == '1': 
                cmd = subprocess.Popen([powershell_exe, "$Acl = Get-Acl " + decoded_data[3] + "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule('" + decoded_data[2] + "', 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.SetAccessRule($Ar); Set-Acl " + decoded_data[3] + " $Acl"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '2':
                cmd = subprocess.Popen([powershell_exe, "$Acl = Get-Acl " + decoded_data[3] + "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule('" + decoded_data[2] + "', 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.RemoveAccessRule($Ar); Set-Acl " + decoded_data[3] + " $Acl"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
        elif decoded_data[0] == '5':
            if decoded_data[1] == '1':
                cmd2 = subprocess.Popen([powershell_exe, "Get-Service | Where-Object {$_.Status -eq 'Running'} | Select Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
                output_str2 = str(output_byte2,"utf-8")
                s.send(str.encode(output_str2 +"\n"))
                
                data = s.recv(1024)
                decoded_data=data.decode("utf-8").split(",")

                cmd = subprocess.Popen([powershell_exe, "Restart-Service -Name " + decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            elif decoded_data[1] == '2':
                cmd2 = subprocess.Popen([powershell_exe,"Get-Service | Where-Object {$_.Status -eq 'Running'} | Select Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
                output_str2 = str(output_byte2,"utf-8")
                s.send(str.encode(output_str2 +"\n"))
                
                data = s.recv(1024)
                decoded_data=data.decode("utf-8").split(",")

                cmd = subprocess.Popen([powershell_exe, "Stop-Service -Name " + decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            elif decoded_data[1] == '3':
                cmd2 = subprocess.Popen([powershell_exe, "Get-Service | Where-Object {$_.Status -eq 'Stopped'} | Select Name"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

                output_byte2 = cmd2.stdout.read() + cmd2.stderr.read()
                output_str2 = str(output_byte2,"utf-8")
                s.send(str.encode(output_str2 +"\n"))
                
                data = s.recv(1024)
                decoded_data=data.decode("utf-8").split(",")

                cmd = subprocess.Popen([powershell_exe, "Start-Service -Name " + decoded_data[2]],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                
        elif decoded_data[0] == '6':
            cmd = subprocess.Popen([powershell_exe, "Restart-Computer"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            
        

        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8")
        s.send(str.encode(output_str + "\nTamamlandı.\n\n"))
        #cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        print(output_str)