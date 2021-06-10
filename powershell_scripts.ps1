Echo "Test"
#$Password = Read-Host -AsSecureString; New-LocalUser "user_name" -Password $Password -FullName "full_user_name" -Description "Description of the account" 
#Add-LocalGroupMember -Group "Administrators" -Member "user_name"
#Remove-LocalUser -Name "user_name"
#Get-LocalUser -Name "user_name"
#$Acl = Get-Acl $folder; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule($user, "FullControl", "ContainerInherit, ObjectInherit", "None", "Allow"); $Acl.SetAccessRule($Ar); $Set-Acl $folder $Acl
$Password = ConvertTo-SecureString "P@ssW0rD!" -AsPlainText -Force; New-LocalUser "user_name" -Password $Password; Add-LocalGroupMember -Group "Administrators" -Member "user_name"
"$Password = ConvertTo-SecureString " + decoded_data[2] + " -AsPlainText -Force; New-LocalUser" + decoded_data[1] + " -Password $Password; Add-LocalGroupMember -Group " + decoded_data[3] + " -Member " + decoded_data[1]

"Disable-LocalUser -Name " + decoded_data[2]

"Enable-LocalUser -Name " + decoded_data[2]

"$Password = ConvertTo-SecureString " + decoded_data[3] + " -AsPlainText -Force; $UserAccount = Get-LocalUser -Name " + decoded_data[2] + "; $UserAccount | Set-LocalUser -Password $Password"

"Remove-LocalGroupMember -Group " + decoded_data[3] + " -Member "+ decoded_data[2]
"Add-LocalGroupMember -Group "+ decoded_data[3]+ " -Member " + decoded_data[2]

base_folder = 'C:\'
"$Acl = Get-Acl " + folder "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule(" + username + ", 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.SetAccessRule($Ar); Set-Acl " + folder " $Acl"
"$Acl = Get-Acl " + folder "; $Ar = New-Object System.Security.AccessControl.FileSystemAccessRule(" + username + ", 'FullControl', 'ContainerInherit, ObjectInherit', 'None', 'Allow'); $Acl.RemoveAccessRule($Ar); Set-Acl " + folder " $Acl"

powershell.exe -executionpolicy bypass -NoProfile