#!/usr/bin/env python 
n_blocks = 128
blocksize = 4096

import threading
import socket 
import os

class Server:
  backlog = 5 
  # this set will serve as a filesystem index
  files = set()

  def __init__(self, port):
    # creates server object
    global blocksize, n_blocks
    host = '' 
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.s.bind((host,port)) 
    self.port = port
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
  def store(client, args):
    if len(args) != 3:
      client.send("ERROR: INVALID COMMAND.\n")
      return
    if args[1] in files:
      client.send("ERROR: FILE EXISTS.\n")
      data = client.recv(args[2]) # can we assume data will be sent regardless of error?
      return
    # actually do the storing stuff
    data = client.recv(args[2]) 
    f = open(args[1], 'w')
    f.write(data)
    files.add(args[1])
    client.send("ACK\n")

  def read(client, args):
    print "Not yet implemented."

  def delete(client, args):
    if len(args) != 2:
      client.send("ERROR: INVALID COMMAND.\n")
      return
    if args[1] not in files:
      client.send("ERROR: NO SUCH FILE\n")
      return
    os.remove(args[1])
    files.remove(args[1])

  def dir(client):
    files_sorted = sorted(lst, key=str.lower)
    result = str(len(files))+"\n"
    for f in files_sorted:
      result += f + "\n"
    client.send(result)

  def handler(self, cmd, client):
    # Handles specific client connections until they close
    thread = str(threading.current_thread().ident)
    while cmd:
      print "[thread",thread+"] Rcvd:", cmd
      args = cmd.split(' ')
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
      cmd = self.process_line(client).strip()

    print "[thread",thread+"] Client closed its socket....terminating"
    client.close()


if __name__ == "__main__":
  s = Server(8765)
  s.listen()