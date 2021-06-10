import os
import subprocess,sys
#subprocess.Popen(["D:\Entranet\control_center\Reverse-Shell-Python\Multi_Client ( ReverseShell v2)\\add_user.ps1"], stdout=sys.stdout)
#D:\Entranet\control_center\Reverse-Shell-Python\Multi_Client ( ReverseShell v2)\add_user.ps1
#subprocess.Popen(["D:\Entranet\control_center\Reverse-Shell-Python\Multi_Client\powershell_scripts.ps1"], stdout=subprocess.PIPE)
cmd = subprocess.Popen(["powershell", "$Password = Read-Host -AsSecureString;"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
output_byte = cmd.stdout.read() + cmd.stderr.read()
output_str = str(output_byte,"utf-8")
print(output_str)

"""p = subprocess.Popen(["powershell.exe", 
              "D:\Entranet\control_center\Reverse-Shell-Python\Multi_Client\powershell_scripts.ps1"], 
              stdout=sys.stdout)
p.communicate()"""