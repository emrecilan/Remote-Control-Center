import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = "192.168.1.101"
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():

    while True:
        cmd2 = input('turtle> ')
        if cmd2== 'list':
            list_connections()
        elif 'select' in cmd2:
            conn = get_target(cmd2)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        """try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_address[i]
            continue"""
    
        results += str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"
    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):

    while True:
        try:
            #burdan kodları seçerek devam et
            cmd = input("İşlem Numaranızı Seçin: \n1) Kullanıcı Ekleme \n2) Kullanıcı Silme \n3) Kullanıcı Düzenleme \n4) Dosya Yetkisi Ekleme ve Kaldırma\n5) Servis İşlemleri\n6) Reboot\nquit)Sunucudan Çıkış Yap \n>>>")
            if cmd == "1":
                cmd += ","
                cmd += input("Kullanıcı Adı: ")
                cmd += ","
                cmd += input("Parola: ")
                cmd += ","
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
                cmd += input("Eklemek istediğiniz Grubu Yazınız:")
            
            
            elif cmd == "2":
                cmd += ","
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
                cmd += input("Kullanıcı Adı: ")

                
            elif cmd == "3":
                cmd += ","
                if len(str.encode(cmd)) > 0:
                    conn.send(str.encode(cmd))
                    client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")

                cmd += input("Kullanıcı Adını Giriniz\n>>> ")
                cmd += ","
                cmd += input("İşlem Seçiniz: \n 1) Parola Değiştirme \n 2) Enable \n 3) Disable \n 4) Gruba Ekle \n 5) Grubtan Çıkar\n>>> ")
                if cmd.split(",")[2] == "1":
                    cmd += input("Yeni Parola: ")
                elif cmd.split(",")[2] == "4":
                    cmd += ","
                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
                    cmd += input("Grup Seçiniz\n>>>")
                    
                elif cmd.split(",")[2] == "5":
                    cmd += ","
                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
                    cmd += input("Grup Seçiniz\n>>>")
            
            elif cmd == "4":
                cmd += ","
                cmd += input("1) Yetki Ekle\n2) Yetki Kaldır\n>>>")
                if cmd.split(",")[1] == "1":
                    cmd += ","
                    cmd += input("Kullanıcı Adı: ")
                    cmd += ","
                    cmd += input("Dosya Yolu: ")
                elif cmd.split(",")[1] == "2":
                    cmd += ","
                    cmd += input("Kullanıcı Adı: ")
                    cmd += ","
                    cmd += input("Dosya Yolu: ")
            elif cmd == "5":
                cmd += ","
                cmd += input("1) Restart\n2) Stop\n3) Start\n>>>")
                if cmd.split(",")[1] == "1":
                    cmd += ","
                    
                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")

                    cmd += input("Servis Adını Giriniz\n>>>")

                elif cmd.split(",")[1] == "2":
                    cmd += ","

                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")
                    
                    cmd += input("Servis Adını Giriniz\n>>>")
                elif cmd.split(",")[1] == "3":
                    cmd += ","
        
                    if len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
                    print(client_response, end="")

                    cmd += input("Servis Adını Giriniz\n>>>")
            
            elif cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
            #print(cmd)
        except:
            print("Error sending commands")
            break



# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
