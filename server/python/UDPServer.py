import socket
import time

class UDP_Server:
    def __init__(self):
        self.maxPacket = 1000
        self.socket=None
        self.openSocket()

    def openSocket(self):
        print("Starting server...")
        if (self.socket): 
            self.socket.close()
            self.socket=None
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Wer als erster herausfindet, was es mit dieser Port-Nummer auf sich hat
        # kriegt ein kleines Geschenk von mir
        self.socket.bind(('', 15878))
        self.socket.settimeout(0)
        self.client = None
        self.lastSeen = 0
        self.startCounter=5

    # First byte is packet number (0 to n-1), last packet is 255, non-data packets are 254
    def send(self, msg:bytearray, start=0) -> None:
        if (self.client!=None):
            if start==254:
                m = bytearray([start])+msg
                self.socket.sendto(m, self.client)                
            elif len(msg)>self.maxPacket-1:
                m = bytearray([start])+msg[0:self.maxPacket-1]
                self.socket.sendto(m, self.client)
                time.sleep(0.001) # Wait before sending next packet, not sure if needed...
                self.send(msg[self.maxPacket-1:], start+1)
            else:
                m = bytearray([255])+msg
                self.socket.sendto(m, self.client)

#        else:
#            print("no client")


    def loop(self) -> None:
        if (self.client and time.time()-self.lastSeen>5): # No more client after 5 secs
            print("client silent for more than 5 secs")
            self.openSocket()
            
        try:
            message, address = self.socket.recvfrom(1024)
            if (self.client==None):
                print("New client at")
                print(address)
                self.client = address
                print(self.client)
            self.lastSeen = time.time()
            if message == b"ping" or message == b"start":
                if message == b"start":
                    self.startCounter-=1
                    print(f"startCounter={self.startCounter}")
                    if (self.startCounter==0):
                        self.openSocket()
                        return
                self.send(b"pong", 254)
                print("sent pong to "+message.decode())
                
        except socket.timeout: 
            pass
            #print('no data available')
        except BlockingIOError:
            pass

