#!/usr/bin/env python 
# Mason Cooper (coopem4) & John Drogo (drogoj)
n_blocks = 128
blocksize = 4096

import threading
import socket 
import shutil
import os

# get our memory module
from memory import Memory

class Server:
  backlog = 5 
  # this set will serve as a filesystem index
  files = set()

  def __init__(self, port):
    # creates server object
    global blocksize, n_blocks
    path = ".storage"
    try:
        os.makedirs(path)
    except OSError as exception:
        shutil.rmtree(path)
        os.makedirs(path)
    host = '' 
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.s.bind((host,port)) 
    self.port = port
    self.memory = Memory(n_blocks, blocksize)
    print "Block size is", blocksize
    print "Number of blocks is", n_blocks

  def process_line(self, client):
    # recv's until \n
    recieved = ''
    while True:
      cur = client.recv(1)
      if cur == "\n":
        break
      elif not cur:
        return cur
      else:
        recieved += cur
    return recieved

  def listen(self):
    # Handles initial client connections and thread creation
    self.s.listen(self.backlog)
    print "Listening on port", self.port
    while True: 
      client, address = self.s.accept()
      print "Received incoming connection from", address[0]
      cmd = self.process_line(client)
      thread = threading.Thread(target=self.handler, args=(cmd, client))
      thread.start()

  # the following functions implement the server functionality requested
  def store(self, client, args):
    thread = str(threading.current_thread().ident)
    if len(args) != 3:
      client.send("ERROR: INVALID COMMAND.\n")
      print "[thread",thread+"] Sent: ERROR: INVALID COMMAND."
      return
    if args[1] in self.files:
      client.send("ERROR: FILE EXISTS.\n")
      print "[thread",thread+"] Sent: ERROR: FILE EXISTS."
      data = client.recv(args[2]) # can we assume data will be sent regardless of error?
      return
    args[2] = int(args[2])
    response = self.memory.alloc(args[1], args[2])
    if not response[0]:
      client.send("ERROR: INSUFFICIENT DISK SPACE.\n")
      print "[thread",thread+"] Sent: ERROR: INSUFFICIENT DISK SPACE."
      data = client.recv(args[2]) # can we assume data will be sent regardless of error?
      return
    # actually do the storing stuff
    data = client.recv(args[2])
    f = open(".storage/"+args[1], 'w')
    f.write(data)
    self.files.add(args[1])
    print "[thread",thread+"] Stored file '%s' (%s bytes; %s blocks; %s" % response, ("cluster" if response[3] == 1 else "cluster") + ")"
    print "[thread",thread+"] Simulated Clustered Disk Space Allocation:"
    print self.memory
    client.send("ACK\n")
    print "[thread",thread+"] Sent: ACK"

  def read(self, client, args):
    thread = str(threading.current_thread().ident)
    if len(args) != 4:
      client.send("ERROR: INVALID COMMAND.\n")
      print "[thread",thread+"] Sent: ERROR: INVALID COMMAND."
      return
    if args[1] not in self.files:
      client.send("ERROR: NO SUCH FILE.\n")
      print "[thread",thread+"] Sent: ERROR: NO SUCH FILE."
      return
    args[2] = int(args[2])
    args[3] = int(args[3])
    data = open(".storage/"+args[1], "r").read()
    if args[2]+args[3] > len(data) or args[2] < 0 or args[3] < 0:
      client.send("ERROR: INVALID BYTE RANGE.\n")
      print "[thread",thread+"] Sent: ERROR: INVALID BYTE RANGE."
      return
    # TODO: (1) Memory dump / print output
    result = "ACK " + str(args[3])+"\n"+data[args[2]:args[2]+args[3]]
    print "[thread",thread+"] Sent: ACK", args[3]
    client.send(result)
    response = self.memory.read(args[1], args[2], args[3])
    print "[thread",thread+"] Sent %s bytes (from %s '%s' blocks) from offset %s." % response

  def delete(self, client, args):
    thread = str(threading.current_thread().ident)
    if len(args) != 2:
      client.send("ERROR: INVALID COMMAND.\n")
      print "[thread",thread+"] Sent: INVALID COMMAND."
      return
    if args[1] not in self.files:
      client.send("ERROR: NO SUCH FILE.\n")
      print "[thread",thread+"] Sent: ERROR: NO SUCH FILE."
      return
    os.remove(args[1])
    self.files.remove(args[1])
    response = self.memory.deleteFile(args[1])
    client.send("ACK\n")
    print "[thread",thread+"] Deleted", args[1],"file '%s' (deallocated %s blocks)" % response
    print "[thread",thread+"] Simulated Clustered Disk Space Allocation:"
    print self.memory
    print "[thread",thread+"] Sent: ACK"

  def dir(self, client):
    thread = str(threading.current_thread().ident)
    files_sorted = sorted(self.files, key=str.lower)
    result = str(len(self.files))+"\n"
    for f in files_sorted:
      result += f + "\n"
    print "[thread",thread+"] Sent list of %d" % len(self.files), ("file" if len(self.files) == 1 else "files") + "."
    client.send(result)

  def handler(self, cmd, client):
    # Handles specific client connections until they close
    thread = str(threading.current_thread().ident)
    while cmd:
      print "[thread",thread+"] Rcvd:", cmd
      args = cmd.split(' ').strip()
      if args[0] == "STORE":
        self.store(client, args)
      elif args[0] == "READ":
        self.read(client, args)
      elif args[0] == "DELETE":
        self.delete(client, args)
      elif args[0] == "DIR":
        self.dir(client)
      else:
        client.send("ERROR: INVALID COMMAND.\n")
        print "[thread",thread+"] Sent: ERROR: INVALID COMMAND."
      cmd = self.process_line(client).strip()
    print "[thread",thread+"] Client closed its socket....terminating."
    client.close()

if __name__ == "__main__":
  s = Server(8765)
  s.listen()