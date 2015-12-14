# Mason Cooper (coopem4) & John Drogo (drogoj)
import socket 

host = 'localhost' 
port = 8765 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
# # s.send('KILL\n') 
# s.send('derp derp\n') 
# print s.recv(1024)
# s.send('KILL\n') 
# print s.recv(1024)
# print "about to close"
# s.close() 



i=0
s.send("STORE xyz.txt 14\nABCDEFGHIJKLMN")
should_be = "ACK\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("STORE abc.txt 12\nABCDEFG\0\0\0\nZ")
should_be = "ACK\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("READ xyz.txt 4 5\n")
should_be = "ACK 5\nEFGHI"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("DIR\n")
should_be = "2\nabc.txt\nxyz.txt\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("DELETE xyz.txt\n")
should_be = "ACK\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("DIR\n")
should_be = "1\nabc.txt\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("DELETE abc.txt\n")
should_be = "ACK\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is

i+=1
s.send("DIR\n")
should_be = "0\n"
really_is = s.recv(1024)
print "Beginning transanction #"+str(i)
if should_be == really_is:
	print "VALID TRANSACTION"
else:
	print "INVALID"
print "Should be:\n"+should_be
print "Really is:\n"+really_is
s.close()
