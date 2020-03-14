import pyautogui as pgui
import numpy as np
from matplotlib import pyplot as plt

view_data = np.array([0.2,0.2,0.2])#中心座標(x,y)サイズ
mouse_move = np.array([0.2,0.2])#移動方向0~1

if view_data[2] > view_data[0]:
    view_data[2] = view_data[0]
elif view_data[2] > 1 - view_data[0]:
    view_data[2] = 1 - view_data[0]
elif view_data[2] > view_data[1]:
    view_data[2] = view_data[1]
elif view_data[2] > 1 - view_data[1]:
    view_data[2] = 1 - view_data[1]

#画面サイズ取得
img_width, img_height = pgui.size()
#スクショを撮る
screendata = pgui.screenshot()
#データをカットする
cut_data = screendata.crop((round((view_data[0]-view_data[2]) * img_width),round((view_data[1]-view_data[2]) * img_height),round((view_data[0]+view_data[2]) * img_width),round((view_data[1]+view_data[2]) * img_height)))
cut_data = cut_data.resize((int(img_width/4),int(img_height/4)))#定格サイズに変更
cut_data = np.asarray(cut_data)

# 画像をリサイズ
resize_width = img_width/8
resize_height = resize_width / img_width * img_height
screendata = screendata.resize((int(resize_width),int(resize_height)))
screendata = np.asarray(screendata)

#命令どおりにマウスカーソルを移動
pgui.moveTo(mouse_move[0]*img_width, mouse_move[1]*img_height, duration=0)

plt.imshow(screendata)
plt.show()
plt.imshow(cut_data)
plt.show()

import pyaudio
import time
import wave
from scipy.fftpack import fft, ifft
from scipy import signal

N=23*1#一秒23
CHUNK=1024*N
RATE=22050 #11025 #22050  #44100
CHANNELS = 1             # 1;monoral 2;ステレオ-
p=pyaudio.PyAudio()
WAVE_OUTPUT_FILENAME = "output.wav"
FORMAT = pyaudio.paInt16 #int16型

stream=p.open(  format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True) # inputとoutputを同時にTrueにする


start=time.time()
stop_time=time.time()

while stream.is_active():

    start_time=time.time()
    print(start_time-stop_time)
    
    stop_time=time.time()
    input = stream.read(CHUNK)
    
    frames = []
    frames.append(input)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    wavfile = WAVE_OUTPUT_FILENAME
    wr = wave.open(wavfile, "rb")
    ch = CHANNELS #wr.getnchannels()
    width = p.get_sample_size(FORMAT) #wr.getsampwidth()
    fr = RATE  #wr.getframerate()
    fn = wr.getnframes()
    fs = fn / fr
    print("fn,fs",fn,fs,stop_time-start_time)

    origin = wr.readframes(wr.getnframes())
    data = origin[:fn]
    wr.close()

    sig = np.frombuffer(data, dtype="int16")  /32768.0
    t = np.linspace(0,fs, fn/2, endpoint=False)

    nperseg = 1024
    f, t, Zxx = signal.stft(sig, fs=fn/2, nperseg=nperseg)
    #Zxxが出力のスペクトラム
    Zxx = np.abs(Zxx)
    volume = np.max(Zxx) * 3#あとで小さい音を大きくするから元の音の大きさを取得して再入力(最大音量は0.4)
    if volume > 1:#音量大きすぎるときに戻す
        volume = 1
    Zxx = Zxx * (1/np.max(Zxx))
    print(Zxx.shape)

    #plt.pcolormesh(fs*t, f*RATE/N/200, np.abs(Zxx), cmap='hsv')
    #plt.pause(0.01)
