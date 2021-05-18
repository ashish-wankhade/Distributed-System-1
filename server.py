import socket
import threading
import csv
import datetime
import os

PORT = 8010
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

HEADER = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def clients(conn, addr, clients_conn):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        msg = conn.recv(HEADER).decode(FORMAT)
        msg = int(msg)
        print(f"[{addr}] just send {msg}")
        fileNAME = conn.recv(HEADER).decode(FORMAT)
        if msg == 1:
            print("CHECKING IF FOLDER NAMED--->> SERVER <<---EXISTS or NOT")
            cwd = os.getcwd()
            listDIR = os.listdir()
            if str('server') not in listDIR:
                FolderNotExist = f"FOLDER NAMED - SERVER DOES NOT EXISTS!"
                print(FolderNotExist)
                # conn.send((FolderNotExist).encode())
                print("MAKING FOLDER NAMED - SERVER")
                folderNAME = "server"
                os.mkdir(folderNAME)
            else:
                FolderExist = f"FOLDER EXISTS\nCHECKING IF FILE NAMED {fileNAME} EXISTS INSIDE SERVER FOLDER!"
                print(FolderExist)
                # conn.send((FolderExist).encode())

            serverFolder = str(cwd) + str("\server")
            os.chdir(
                serverFolder)  # file = str(folder + "\\" + fileNAME)    # or can write --->>> str(folder) + str("\\") + str(fileNAME)
            listSERVER = os.listdir()
            print(listSERVER)
            action = conn.recv(HEADER).decode(FORMAT)
            if str(fileNAME) in listSERVER and action == "SEND FILE":
                print(f"Sending FileName {fileNAME} to {addr}")
                conn.send(("SERVER IS SENDING FILE...").encode())
                with open(fileNAME, 'rb') as fs:
                    data = fs.read(HEADER * 5)
                    conn.send(data)
                    print('FILE SENT')
                    if not data:
                        print('Breaking from sending data')
                        break
                fs.close()
            if str(fileNAME) in listSERVER and action == f"FILE NAMED - {fileNAME} ALREADY EXISTS WITH CLIENT!!!":
                print(action)
            if str(fileNAME) not in listSERVER and action == "SEND FILE":
                conn.send(("FILE NOT AT SERVER").encode())
                FileNotExist = f"FILE NAMED - {fileNAME} DOES NOT EXIST INSIDE SERVER FOLDER! "
                print(FileNotExist)
            os.chdir(cwd)

        if msg == 2:
            connected = False

        # maintaining log file
        with open('log.csv', mode='a') as log:
            fieldnames = ['address', 'date', 'time', 'message', 'filename']
            write = csv.DictWriter(log, fieldnames=fieldnames)
            address = str(addr[0]), str(addr[1])
            current_time = datetime.datetime.now()
            date = current_time.date()
            time = current_time.time()
            message = msg
            filename = fileNAME

            fill = {
                'address': address,
                'date': date,
                'time': time,
                'message': message,
                'filename': fileNAME
            }
            write.writerow(fill)

    print(f'Disconnected {addr}')
    clients_conn.remove(str(addr))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    clients_conn = []
    while True:
        conn, addr = server.accept()
        clients_conn.append(str(addr))
        thread = threading.Thread(target=clients, args=(conn, addr, clients_conn))
        thread.start()

        print(
            f"[ACTIVE CONNECTIONS] = {threading.activeCount() - 1}")  # -1 because one active thread is already running ie. start()


print("[STARTING] server is starting...")
start()
