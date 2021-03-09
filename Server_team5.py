
import time
import threading
import socket
import json





class Sender:

    ADDR = '180.235.234.95'
    SENDER_PORT = 9015
    JSON_DATA = {}

    def __init__(self):
        print("Sender Init")

    def _make_json(self):
        print("make json")
        new_data = Receiver.CONTABLE.copy()
        i = 0
        for feature in Sender.JSON_DATA["features"]:
            num = new_data.get(feature["properties"]["name"])
            if(num != None):
                feature["properties"]["num"] = num
            i += 1
        Sender.JSON_DATA["metadata"]["count"] = i
        fp = open("json_data.json", "w")
        json.dump(Sender.JSON_DATA, fp)
        print("write json")

    def _sendJson(self, conn):
        self._make_json()
        json_str = json.dumps(Sender.JSON_DATA)
        conn.sendall( json_str.encode("utf-8"))
        print("send json")

    def _parse(self, conn):
        data = conn.recv(1024)
        print("receive : ", data)
        self._sendJson(conn)
        conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Sender.ADDR, self.SENDER_PORT))
            s.listen(10)
            while True:
                conn, addr = s.accept()
                self._parse(conn)



class Receiver:

    ADDR = '180.235.234.95'
    RECEIVE_PORT = 9005
    CONTABLE = {}
    def __init__(self):
        print("Receiver Init")
        #self._thtable  = {}
    """
    def _show(self, buffer):
        for b in buffer:
            print("{:02x}".format(b), end=" ")
        print()
    """
    def _receiving(self, ch_name, s_conn):
        ch = Receiver.CONTABLE.get(ch_name)
        print(ch_name , "start receiving")
        while ch != None:
            #s_conn = channel.get_conn()
            data = s_conn.recv(128)
            #data_bytes = data[0 : 6].decode('ascii')
            #buf = [6]
            """
            i = 0
            for byte in data:
                if i>=6 :
                    print("unmatch data received")
                    break
                buf[i] = int.from_bytes(byte)
                i+=1
            
            IN = (buf[0] << 16) + (buf[1] << 8) + buf[2]
            OUT = (buf[3] << 16) + (buf[4] << 8) + buf[5]
            """
            IN = int.from_bytes(data[0:3], "big") #int.from_bytes(data[0:3])
            OUT = int.from_bytes(data[3:6], "big") #int.from_bytes(data[3:6])
            Receiver.CONTABLE[ch_name] = IN - OUT
            print(ch_name, ":", data , "to", IN - OUT)

    def _parse(self, conn):
        data = conn.recv(1024)
        #print(len(data))
        #print(type(data))
        print("receive ",data)

        nlen = data[1]
        channel_name = data[2 : nlen+2].decode("utf-8")

        #print("name={}".format(channel_name))
        _new_channel = False
        _channel = Receiver.CONTABLE.get(channel_name)
        if _channel == None:
            print("Create Channel: {}".format(channel_name))
            _new_channel = True
            Receiver.CONTABLE[channel_name] = 0
        
        print("create thread")
        th = threading.Thread(target=self._receiving, args=(channel_name, conn), daemon=True)
        th.setDaemon(True)
        th.start()


    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Receiver.ADDR, self.RECEIVE_PORT))
            s.listen(10)
            while True:
                conn, addr = s.accept()
                self._parse(conn)
                #self._ask_send(conn)









if __name__ == "__main__":
    print("relay server")
    json_node = open("json_data.json", "r")
    Sender.JSON_DATA = json.load(json_node)
    """
    json_str = json.dumps(json)
    rserver1 = RelayServer(9005)
    rserver2 = RelayServer(9015)
    th1 = threading.Thread(target=rserver1.start)
    th2 = threading.Thread(target=rserver2.start)
    th1.start()
    th2.start()


    print()
    print(json_dict["features"])
    for feature in json_dict["features"]:
        print(feature)
    """
    receiver = Receiver()
    sender = Sender()
    Sender_th = threading.Thread(target=sender.start, daemon=True)
    Sender_th.start()
    receiver.start()
    #sender = Sender()
    #print(Sender.JSON_DATA)
