#!/usr/bin/python3.4
import os
import time
import sys
import subprocess as sp

config = {"timeout" : 3, "pause" : 2}

class tc:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

FNULL = open(os.devnull, 'w')
commonPorts = []
commonPortsHR = {};
openPorts = {};

#get common ports from nmap-services
with open('nmap-services') as f:
  for line in f:
    if line[0] != '#':
      chunk = line.split('\t')
      if len(chunk) > 1:
        if chunk[0] != 'unknown':
          port = chunk[1].split('/')
          commonPortsHR[port[0]] = chunk[0]
          if port[1] == 'tcp' and int(port[0]) > 1024:
            commonPorts.append(int(port[0]))

#estimatedTime = (1/6000) * 2*config['pause']*(1024 + len(commonPorts))

processes = []
print('1024 first ports ...           ', end='')
for port in range(1, 1025):
  time.sleep(config['pause']/1000)
  print("\b\b\b\b\b\b\b\b\b{0: <4}/1024".format(str(port)), end='')
  sys.stdout.flush()
  processes.append(sp.Popen(['nc', '-w', str(config['timeout']), '-vz', 'portquiz.net', str(port)], stdout=sp.DEVNULL, stderr=sp.DEVNULL))
print('\n' + len(commonPorts) + ' next common ports ...     ')
for port in commonPorts:
  time.sleep(config['pause']/1000)
  print("\b\b\b\b\b" + str(port), end='')
  sys.stdout.flush()
  processes.append(sp.Popen(['nc', '-w', str(config['timeout']), '-vz', 'portquiz.net', str(port)], stdout=sp.DEVNULL, stderr=sp.DEVNULL))

closed = []

for p in processes:
  out, err = p.communicate()
  if p.returncode == 0:
    port = p.args[len(p.args) - 1];
    openPorts[port] = True;
    print(tc.OKGREEN, 'open ', tc.ENDC, port, ' (', commonPortsHR.get(port), ')', sep='')
  else:
    closed.append(p.args[len(p.args) - 1]);

if len(closed) == 0:
  print(tc.OKGREEN, 'It looks like nothing is blocked :)', tc.ENDC);
else:
  print(tc.FAIL, 'Some ports are blocked :(', tc.ENDC)
  for p in closed:
    print(tc.FAIL, p, tc.ENDC, end=' ')
print()

