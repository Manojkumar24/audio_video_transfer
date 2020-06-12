import pyaudio
import socket
from threading import Thread
import json
import sys
import cv2
import math
import struct
import numpy as np

frames = []

def getIP():
    return socket.gethostbyname(socket.gethostname())

def udpAudioStream(send_ip):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        if len(frames) > 0:
            udp.sendto(frames.pop(0), (send_ip, config_data["connection"]["AUDIO_PORT"]))

    udp.close()

def recordAudio(stream, CHUNK):    
    while True:
        frames.append(stream.read(CHUNK))

recv_frames = []

def udpAudioReceiver(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = getIP()
    udp.bind((ip_address,  config_data["connection"]["AUDIO_PORT"]))
    # print(config_data["audio_features"]["CHANNELS"])
    while True:
        soundData, addr = udp.recvfrom(CHUNK * config_data["audio_features"]["CHANNELS"] * 2)
        recv_frames.append(soundData)

    udp.close()

def playAudio(stream, CHUNK):
    BUFFER = 10
    while True:
        if len(recv_frames) > 1:
            stream.write(recv_frames.pop(0), CHUNK)

def recordAndSendVideo(send_ip):
    udpvideo = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cap = cv2.VideoCapture(0)
    # if(cap.isOpened()):
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 1280 
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 720 
    
    while (cap.isOpened()):
        _, video_frame = cap.read()
        compress_img = cv2.imencode('.jpg', np.flip(video_frame, 1))[1]
        dat = compress_img.tostring()
        size = len(dat)
        count = math.ceil(size/(eval(config_data["video_features"]["MAX_IMAGE_DGRAM"])))
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + eval(config_data["video_features"]["MAX_IMAGE_DGRAM"]))
            udpvideo.sendto(struct.pack("B", count) +
                dat[array_pos_start:array_pos_end], 
                (send_ip, config_data["connection"]["VIDEO_PORT"])
                )
            array_pos_start = array_pos_end
            count -= 1
    cap.release()
    cv2.destroyAllWindows()

def recieveAndDisplayVideo():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = getIP()
    udp.bind((ip_address,  config_data["connection"]["VIDEO_PORT"]))
    dat = b''
    # while True:
    #     seg, addr = udp.recvfrom(eval(config_data["video_features"]["MAX_DGRAM"]))
    #     if struct.unpack("B", seg[0:1])[0] == 1:
    #         break
    while True:
        seg, addr = udp.recvfrom(eval(config_data["video_features"]["MAX_DGRAM"]))
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            if(np.count_nonzero(img)!=0):
                cv2.imshow('frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if(len(sys.argv) == 1):
        print("Enter IP address of other UE in command line argument")
        sys.exit()
    send_ip = sys.argv[1]
    try:
        socket.inet_aton(send_ip)
    except:
        print("Enter IP address of other UE in command line argument")
        sys.exit()

    config = {}

    f = open("config.json", 'r')
    config_data = json.load(f)



    p = pyaudio.PyAudio()

    stream = p.open(format = eval(config_data["audio_features"]["FORMAT"]),
                    channels = config_data["audio_features"]["CHANNELS"],
                    rate = config_data["audio_features"]["RATE"],
                    input = True,
                    output = True,
                    frames_per_buffer = config_data["audio_features"]["CHUNK"],
                    )

    record_audio_thread = Thread(target = recordAudio, args = (stream, config_data["audio_features"]["CHUNK"],))
    send_audio_thread = Thread(target = udpAudioStream, args=(send_ip,))
    receive_audio_thread = Thread(target = udpAudioReceiver, args=(config_data["audio_features"]["CHUNK"],))
    play_audio_thread = Thread(target = playAudio, args=(stream, config_data["audio_features"]["CHUNK"],))

    receive_video_thread = Thread(target= recieveAndDisplayVideo)
    send_video_thread = Thread(target= recordAndSendVideo , args=(send_ip,))
    
    receive_audio_thread.start()
    play_audio_thread.start()
    record_audio_thread.start()
    send_audio_thread.start()
    receive_video_thread.start()
    send_video_thread.start()