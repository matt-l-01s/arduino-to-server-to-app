#-*- coding: UTF-8 -*- 
import socket
import sys
from _thread import *
 
HOST = 'localhost'   
PORT = 8880
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
 
# 錯誤處理
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print ('Socket bind complete')
 
# 最多連接10個
s.listen(10)
print ('Socket now listening')

# 處理連接程序,並可創造多執行緒 
def clientthread(conn,clientaddress):

    # 一直保持接收data
    while True:
         
        # data為client所傳入的資訊
        data = conn.recv(2048)
	
        reply = 'server reply:\t' + data.decode('utf-8')
	# 在sever端print出 client傳入的data

        print(clientaddress+'\t'+'say:'+data.decode('utf-8'))
        if not data: 
            break

    	# 在該連結的client 回覆 
        conn.sendall(str.encode(reply))
     
    # 連線中斷
    conn.close()
 
# 一直等待client端連線
while 1:
    # 連線成功時出現連線資訊 
    conn, addr = s.accept()
    clientaddress = addr[0]+':'+str(addr[1])
    print ('Connected with ' + clientaddress)
     
    # 開啟一個thread(每一個新連線就會開一個thread,限制為listen參數)
    start_new_thread(clientthread ,(conn,clientaddress))
 
s.close()
