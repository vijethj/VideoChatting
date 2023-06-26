import socket
import cv2
import pickle
import struct
import threading

def client():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip_server = '192.168.56.1' 
    port = 9999
    print("Socket Created Successfully")


    client_socket.connect((host_ip_server,port))
    data = b""
    payload_size = struct.calcsize("Q")
    print("Socket Accepted")

    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(2160) 
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(2160)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break
            client_socket.close()
client()
'''
def server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:',host_ip)

    port = 1800
    socket_address = (host_ip,port)
    print("Socket Created Successfully")


    server_socket.bind(socket_address)
    print("Socket Bind Successfully")


    server_socket.listen(5)
    print("LISTENING AT:",socket_address)

    print("Socket Accept")
    
    

    while True:
        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                print("Server running")
                img,frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
            
                cv2.imshow('TRANSMITTING VIDEO',frame)
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()
                    #server_socket.close()
server()
'''
t1=threading.Thread(target=client)
t2=threading.Thread(target=server)

t1.start()
t2.start()

