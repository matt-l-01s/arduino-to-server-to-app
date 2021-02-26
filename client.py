#-*- coding: UTF-8 -*- 
import sys
import socket
HOST='localhost'
PORT = 8880

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
s.connect((HOST,PORT))       # 依照 HOST PORT連接server
while 1:
       data=input("Please input cmd:")   
       data = str(data).encode('utf-8')    #輸入傳給server的data
       s.sendall(data)      #把data發送給server
       data=s.recv(2048)     #把接收的數據變為變數data
       print (data)         #print data
s.close()   #關閉連線