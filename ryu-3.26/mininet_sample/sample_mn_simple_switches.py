#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def myNet():
    #OpenDayLight controller
    CONTROLLER1_IP='127.0.0.1'

    #Floodlight controller

    net = Mininet( topo=None, build=False)

    # Create nodes
    h1 = net.addHost( 'h1', mac='01:00:00:00:01:00', ip='192.168.0.1/24' )
    h2 = net.addHost( 'h2', mac='01:00:00:00:02:00', ip='192.168.0.2/24' )
    h3 = net.addHost( 'h3', mac='01:00:00:00:03:00', ip='192.168.0.3/24' )

    # Create switches
    s1 = net.addSwitch( 's1', listenPort=6634, mac='00:00:00:00:00:01' )
    s2 = net.addSwitch( 's2', listenPort=6634, mac='00:00:00:00:00:02' )
    
    print "*** Creating links"
    net.addLink(h1, s1 )
    net.addLink(h2, s1 )
    net.addLink(h3, s1 )
    net.addLink(s2, s1 )
  

    # Add Controllers
    c0 = net.addController( 'c0', controller=RemoteController, ip=CONTROLLER1_IP, port=6633)

    net.build()

    # Connect each switch to a different controller
    s1.start([c0])

    s1.cmdPrint('ovs-vsctl show')
    
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNet()

