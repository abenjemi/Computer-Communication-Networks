# The code is subject to Purdue University copyright policies.
# DO NOT SHARE, DISTRIBUTE, OR POST ONLINE
#

import sys
import time
from switch import Switch
from link import Link
from client import Client
from packet import Packet


class STPswitch(Switch):
    """MAC learning and forwarding implementation."""

    ROOT = '1'

    def __init__(self, addr, heartbeatTime):
        Switch.__init__(self, addr, heartbeatTime)  # initialize superclass - don't remove
        """TODO: add your own class fields and initialization code here"""
        self.table = {}
        self.init_content = self.addr + ',' + self.addr + ',' + '0'
        self.control = Packet(Packet.CONTROL, self.addr, 'a', content=self.init_content)
        self.isUpdated = 1
        # self.first_iter = 1
        
        
    # def updateView(self, )

    def handlePacket(self, port, packet):
        """TODO: process incoming packet"""

        # Forwarding table
        if packet.isData():
            if (packet.srcAddr in self.table.keys() and self.links[port].status == Link.INACTIVE):
                self.table = {addr:p for addr,p in self.table.items() if addr != packet.srcAddr}
                #print(self.addr)
            s = packet.srcAddr
            if s not in self.table.keys():
                self.table[s] = port
            if packet.dstAddr== "X":
                p = packet.copy()
                coming_addr = self.links[port].get_e2(self.addr)
                for send_port in self.links.keys():
                    e2 = self.links[send_port].get_e2(self.addr)
                    if e2 != coming_addr:
                        if self.links[send_port].status == Link.ACTIVE:
                            self.send(send_port, p)
                
            else:
                if packet.dstAddr in self.table.keys():
                    
                    destPort = self.table[packet.dstAddr]
                    if port != destPort:
                        if self.links[destPort].status == Link.ACTIVE:
                            #p = packet.copy()
                            self.send(destPort, packet)
                        # elif (packet.srcAddr in self.table.keys() and self.links[port].status == Link.INACTIVE):
                        #     self.table = {addr:p for addr,p in self.table.items() if addr != packet.srcAddr}
                        #     #print(self.addr)
                else:
                    p = packet.copy()
                    coming_addr = self.links[port].get_e2(self.addr)
                    for send_port in self.links.keys():
                        e2 = self.links[send_port].get_e2(self.addr)
                        if e2 != coming_addr:
                            if self.links[send_port].status == Link.ACTIVE:
                                self.send(send_port, p)

        # STP
        elif packet.isControl():
            if (self.control.content.split(',')[1] == packet.srcAddr):
                if packet.content.split(',')[0] < self.control.content.split(',')[0]:
                    cost = int(float(packet.content.split(',')[2])) + self.links[port].get_cost()
                    self.control.content = packet.content.split(',')[0] + ',' + packet.srcAddr + ',' + str(cost)

            # case 2
            else:
                if (packet.content.split(',')[0] < self.control.content.split(',')[0]):
                    # self.isUpdated = 1
                    cost = int(float(packet.content.split(',')[2])) + self.links[port].get_cost()
                    self.control.content = packet.content.split(',')[0] + ',' + packet.srcAddr + ',' + str(cost)
                    # self.links[port].status == Link.ACTIVE

                elif packet.content.split(',')[0] == self.control.content.split(',')[0]:
                    if int(float(packet.content.split(',')[2])) + self.links[port].get_cost() < int(float(self.control.content.split(',')[2])):
                        self.isUpdated = 1
                        cost = int(float(packet.content.split(',')[2])) + self.links[port].get_cost()
                        self.control.content = self.control.content.split(',')[0] + ',' + packet.srcAddr + ',' + str(cost)
                        # self.links[port].status == Link.ACTIVE
                        
                    elif int(float(packet.content.split(',')[2])) + self.links[port].get_cost() == int(float(self.control.content.split(',')[2])):
                        if packet.srcAddr < self.control.content.split(',')[1]:
                            #self.isUpdated = 1
                            self.control.content = self.control.content.split(',')[0] + ',' + packet.srcAddr + ',' + self.control.content.split(',')[2]
                            # self.links[port].status == Link.ACTIVE


            
            if (self.control.content.split(',')[1] != packet.srcAddr and packet.content.split(',')[1] != self.addr):
                self.links[port].status = Link.INACTIVE
            else:
                self.links[port].status = Link.ACTIVE
                # self.removeLink(port) 


    def handleNewLink(self, port, endpoint, cost):
        """TODO: handle new link"""
        # self.links[port].status = Link.ACTIVE
        self.table = {addr:p for addr,p in self.table.items() if p != port}
        #if (self.control.content.split(',')[1] == endpoint and cost + int(float(endpoint.control.content.split(',')[2])) > int(float(self.control.content.split(',')[2]))):
        self.control = Packet(Packet.CONTROL, self.addr, 'a', content=self.init_content)
        for p in self.links.keys():
            e2 = self.links[p].get_e2(self.addr)
            # if not e2.isalpha():
            self.control.dstAddr = e2
            self.send(p, self.control)

        # pass



    def handleRemoveLink(self, port, endpoint):
        """TODO: handle removed link"""

        #self.links[port].status = Link.INACTIVE
        self.table = {addr:p for addr,p in self.table.items() if p != port}
        if self.control.content.split(',')[1] == endpoint:
            self.control = Packet(Packet.CONTROL, self.addr, 'a', content=self.init_content)
            for p in self.links.keys():
                e2 = self.links[p].get_e2(self.addr)
                # if not e2.isalpha():
                self.control.dstAddr = e2
                self.send(p, self.control)




    def handlePeriodicOps(self, currTimeInMillisecs):
        for p in self.links.keys():
            e2 = self.links[p].get_e2(self.addr)
            # if not e2.isalpha():
            self.control.dstAddr = e2
            self.send(p, self.control)
        
        for p in self.table.values():
            if self.links[p].status == Link.INACTIVE:
                self.table = {addr:port for addr,port in self.table.items() if port != p}
        """TODO: handle periodic operations. This method is called every heartbeatTime.
        You can change the value of heartbeatTime in the json file."""

