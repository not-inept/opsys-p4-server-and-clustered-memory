#!/usr/bin/env python 
n_blocks = 128
blocksize = 4096

import threading
import socket 

class Server:
  backlog = 5 

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

  def store(client, args):
    print "Not yet implemented."
  def read(client, args):
    print "Not yet implemented."
  def delete(client, args):
    print "Not yet implemented."
  def dir(client, args):
    print "Not yet implemented."

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
        self.dir(client, args)
      else:
        print "[thread",thread+"] Error: Invalid command."
      cmd = self.process_line(client).strip()

    print "[thread",thread+"] Client closed its socket....terminating"
    client.close()


if __name__ == "__main__":
  s = Server(8765)
  s.listen()