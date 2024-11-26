[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Install-PackageProvider -Name NuGet
Install-Module NTFSSecurity
Set-PSSessionConfiguration Microsoft.PowerShell -ShowSecurityDescriptorUI
