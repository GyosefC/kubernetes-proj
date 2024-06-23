cd "D:\OpenSSH-Win64";

setx PATH "$env:path;D:\OpenSSH-Win64" -m

.\install-sshd.ps1

Set-Service sshd -StartupType Automatic; Set-Service ssh-agent -StartupType Automatic; Start-Service sshd; Start-Service ssh-agent

New-NetFirewallRule -DisplayName "OpenSSH-Server-In-TCP" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Allow


download from :  https://github.com/PowerShell/Win32-OpenSSH/releases