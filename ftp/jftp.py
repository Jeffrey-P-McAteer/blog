
# We use https://github.com/giampaolo/pyftpdlib
# python3 -m pip install --user pyftpdlib

#from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, BufferedIteratorProducer
from pyftpdlib.servers import FTPServer

import logging
import time
import os
import sys
from threading import Thread
import signal
import traceback

# Everyone shares these files
JFTP_FILES = '/opt/jftp/data/' if os.path.exists('/opt/jftp/data/') else '/tmp/'

ftp_server_o = None

class JAuth(object):
  """
  This authorizes everyone + stores their IP and username data
  for later fine-grained permissions and mostly audit purposes.
  """
  def __init__(self):
    self.user_history = []
    # [(timestamp_ms: int, username: str, password: str, src_addr: str)]

  def validate_authentication(self, username, password, handler):
    now_ms = int(round(time.time() * 1000))
    self.user_history.append((
      now_ms, username, password, handler.addr[0]
    ))
    print('New user: {} / {} from {}'.format(username, password, handler.addr[0]))
    if len(self.user_history) > 10:
      self.user_history.pop(0)

  def impersonate_user(self, username, password):
    pass # these fns are only used to switch to diff unix users before fs access

  def terminate_impersonation(self, username):
    pass # these fns are only used to switch to diff unix users before fs access

  def get_home_dir(self, username):
    return JFTP_FILES

  def get_msg_login(self, username):
    return "Welcome to ftp.jmcateer.pw!"

  def get_msg_quit(self, username):
    print('{} quit'.format(username))
    return "Goodbye!"

  def get_perms(self, username):
    return 'elradfmwMT'

  def has_perm(self, username, perm, path=None):
    if not path:
      path = JFTP_FILES
    if path:
      path = os.path.normpath(path)
    # Path is now always JFTP_FILES + <user data>
    
    # For the moment we allow everyone to see everything
    return True

class JFTPHandler(FTPHandler):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
  def pre_process_command(self, line, cmd, arg):
    print('pre_process_command({}, {}, {})'.format(line, cmd, arg), file=sys.stderr)
    super().pre_process_command(line, cmd, arg)
    
  # def ftp_LIST(self, path):
  #   print('{} asked to see files in {}'.format(None, path))

  #   def list_files(*files):
  #     for f in files:
  #       yield bytes(f, 'utf-8')

  #   iterator = list_files('a', 'b', 'c', 'd')
  #   producer = BufferedIteratorProducer(iterator)
  #   self.push_dtp_data(producer, isproducer=True, cmd="LIST")
  #   return path

def ftp_svr_t():
  global ftp_server_o
  h = JFTPHandler
  h.authorizer = JAuth()
  #h.masquerade_address = '10.142.0.7' # pulled from live VM
  h.passive_ports = list(range(9128, 65535))

  ftp_server_o = FTPServer(("0.0.0.0", 21), h)
  ftp_server_o.serve_forever(timeout=0.5)

def http_svr_t():
  pass

def on_sigint(sig, frame):
  try:
    ftp_server_o.close_all()
  except:
    traceback.print_exc() 
  print('Exiting...')
  sys.exit(0)

def main():
  signal.signal(signal.SIGINT, on_sigint)
  threads = []

  threads.append(Thread(target=ftp_svr_t, args=() ))
  threads.append(Thread(target=http_svr_t, args=() ))

  for t in threads:
    t.start()

  for t in threads:
    t.join()

  print('Done!')



if __name__ == '__main__':
  main()
