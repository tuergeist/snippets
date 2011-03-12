#!/usr/bin/env python
# wake on lan
# mount 

import socket
import struct
import subprocess
import sys 
import time

def check_alive(host):
    HOST=host
    PORT=2049
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        sys.stderr.write("[ERROR1] %s\n" % msg[1])
        return msg[0]
    try:
        sock.connect((HOST, PORT))
    except socket.error, msg:
        sys.stderr.write("[ERROR2] %s\n" % msg[1])
        return msg[0]
    return 0

def wake_on_lan(macaddress):
    """ Switches on remote computers using WOL. """

    # Check macaddress format and try to compensate.
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
 
    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = '' 

    # Split up the hex values and pack.
    for i in range(0, len(data), 2):
        send_data = ''.join([send_data,
                             struct.pack('B', int(data[i: i + 2], 16))])

    # Broadcast it to the LAN.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('<broadcast>', 7))
    

def mount(mountpoint):
    retcode = subprocess.call(["mount", mountpoint])
    if retcode == 0:
        rc = "ok"
    else:
        rc = "Fehler"
    print("Mountpoint: %s ... %s" % (mountpoint, rc)) # 32 already mounted - mount error, 1 nicht in fstab/mtab

if __name__ == '__main__':
    mounts = {'hobbit' : ['/mnt/fotos', '/mnt/musik', '/mnt/todo', '/backup', '/mnt/media', '/mnt/home_cb'], 'fritz.box':[]}
    hosts = {'hobbit'  : '00:27:0E:07:80:A3', 'fritz.box': '00:27:0E:07:80:AA'}

    # wake up
    host = 'hobbit'
    wake_on_lan(hosts[host])

    chost = check_alive(host)
    if chost == 0:
        print("Host %s is alive " % host)
    elif chost == -5:
        print("Host %s is unknown " % host)
        sys.exit(1)
    else:
        wake_on_lan(hosts[host])
        round = 0
        while (0 != check_alive(host) and round < 120):
            time.sleep(1)

    #os.path.ismount
    for m in mounts[host]:
        mount(m)
    
    

