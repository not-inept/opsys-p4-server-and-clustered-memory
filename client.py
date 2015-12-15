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
def sendCmd(s, cmd, expected):
	s.send(cmd)
	really_is = s.recv(1024)
	assert(expected == really_is)

	# print "Should be:\n"+expected
	# print "Really is:\n"+really_is

test_cmds = [
	("STORE xyz.txt 14\nABCDEFGHIJKLMN", "ACK\n"),
	("STORE abc.txt 12\nABCDEFG\0\0\0\nZ", "ACK\n"),
	("READ xyz.txt 4 5\n", "ACK 5\nEFGHI"),
	("DIR\n", "2\nabc.txt\nxyz.txt\n"),
	("DELETE xyz.txt\n", "ACK\n"),
	("DIR\n", "1\nabc.txt\n"),
	("DELETE abc.txt\n", "ACK\n"),
	("DIR\n", "0\n")
]

for t in test_cmds:
	sendCmd(s, *t)
