import socket 

host = 'localhost' 
port = 8765 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
# s.send('KILL\n') 
s.send('derp derp\n') 
s.send('KILL\n') 
print "about to close"
s.close() 
