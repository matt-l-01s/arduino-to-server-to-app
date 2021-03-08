
import socket
import time
phone_clients =[]
clients = []  # 儲存用戶端socket物件的列表變數
HOST = '127.0.0.1'
PORT = 6688
s = socket.socket()
s.bind((HOST, PORT))
s.setblocking(False)  # 將此socket設成非阻塞
s.listen(5)
print('{}Server at{}The port is open!'.format(HOST, PORT))

	
while True:
    try:
        client, addr = s.accept()
        print('Client address：{}，Port number：{}'.format(addr[0], addr[1]))
        # 也把跟用戶端連線的socket設成「非阻塞」
        client.setblocking(False) 
        # 將此用戶端socket物件存入clients列表備用
        clients.append(client)
    except:
        pass  # 不理會錯誤
 
    # 逐一處理clients列表裡的每個用戶端socket…
    for client in clients:
        try:
            msg = client.recv(1024).decode('utf8')

            print('Receive message：' + msg)
            reply = ''
 
            if  'phone' in msg:
                phone_clients.append(client)
                reply = b'Hello Phone!'
            elif 'quit' in msg or len(msg)==0:

                client.send(b'Bye')
                client.close()
                # 將此用戶端socket從列表中移除
                clients.remove(client)
                break  # 退出for迴圈
            else:
                reply = b'what??'

            client.send(msg.encode('UTF-8'))
            for client in phone_clients:
                client.send(msg.encode('UTF-8'))           
        except:
            pass  # 不理會錯誤