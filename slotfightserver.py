import socket
import threading
import sys

ip=''
port=5555
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    sock.bind((ip,port))
except socket.error as err:
    str(err)

sock.listen(2)
print('waiting for connection')
pos=[[50,560,100,0],[910,560,100,0]]
p_conn=[False,False,False,False]

def client(connection,p_num):
    p_num=p_num%2
    connection.send(str.encode(make_data(pos[p_num])))
    reply=''
    while True:
        try:
            data=read_data(connection.recv(2048).decode())
            pos[p_num]=data
            p_conn[p_num]=True
            if p_conn[0] and p_conn[1] and (not p_conn[2] or not p_conn[3]):
                connection.sendall(str.encode('GO'))
                print('both players connected')
                if p_num==0:
                    p_conn[2]=True
                else:
                    p_conn[3]=True
            if not data:
                print('disconnected')
                break
            else:
                if p_num==0:
                    reply=pos[1]
                else:
                    reply=pos[0]

                #print('recieved',data)
                #print('send',reply)
            connection.sendall(str.encode(make_data(reply)))
        except:
            break
    print('connection ended')
    connection.close()
    if p_num==0:
        p_conn[0]=False
        p_conn[2]=False
    else:
        p_conn[1]=False
        p_conn[3]=False
    if not p_conn[0] and not p_conn[1] and not p_conn[2] and not p_conn[3]:
        pos[0]=[50,560,100,0]
        pos[1]=[910,560,100,0]

def make_data(player):
    #print(player)
    return str(player[0])+','+str(player[1])+','+str(player[2])+','+str(player[3])

def read_data(player):
    #print(player)
    player_lst=player.split(',')
    return int(player_lst[0]),int(player_lst[1]),int(player_lst[2]),int(player_lst[3])


player_num=0
while True:
    connection,address=sock.accept()
    print('connected to: ',address)
    threading.Thread(target=client,args=(connection,player_num)).start()
    player_num+=1

