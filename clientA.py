import socket, cv2, pickle, struct, threading, time, pyaudio
# Socket Create
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Socket Accept
def sender():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('Host IP:',host_ip)
    port = 1700
    socket_address = ('192.168.185.77',port)
# Socket Bind
    s.bind(socket_address)
# Socket Listen
    s.listen(5)
    print("Listening at:",socket_address)
    while True:
        client_socket,addr = s.accept()
        print('Connection to:',addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
  
            while(vid.isOpened()):
                ret,image = vid.read()
                img_serialize = pickle.dumps(image)
                message = struct.pack("Q",len(img_serialize))+img_serialize
                client_socket.sendall(message)
   
                cv2.imshow('Video from server', image)
                key = cv2.waitKey(10) 
                if key == 13:
                    client_socket.close()
sender()
#Audio
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)
#Audio Socket Initialization
audioSocket = socket.socket()
port1 = 5000
audioSocket.bind(('192.168.185.77',port1))
audioSocket.listen(5)
cAudio, addr = audioSocket.accept()
def recordAudio():
    while True:
        data = stream.read(chunk)
        if data:
            cAudio.sendall(data)
recordAudio()
def rcvAudio():
     while True:
          audioData = audioSocket.recv(size)
          stream.write(audioData)
rcvAudio()
def connect_server():
    host_ip = '192.168.185.174' 
    port = 1234
    s.connect((host_ip,port)) 
    data = b""
    metadata_size = struct.calcsize("Q")
    while True:
        while len(data) < metadata_size:
            packet = s.recv(4*1024) 
            if not packet: break
            data+=packet
        packed_msg_size = data[:metadata_size]
        data = data[metadata_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
 
        while len(data) < msg_size:
            data += s.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Receiving Video",frame)
        key = cv2.waitKey(10) 
        if key  == 13:
            break
    s.close()
connect_server()
t1 = threading.Thread(target = sender)
t2 = threading.Thread(target = connect_server)
t3 = threading.Thread(target = recordAudio)
t4 = threading.Thread(target = rcvAudio)
# start a thread
t1.start()
t2.start()
t3.start()
t4.start()
print('done')