import pyautogui as pgui
import numpy as np
from matplotlib import pyplot as plt
#音声系
import pyaudio
import time
import wave
from scipy.fftpack import fft, ifft
from scipy import signal

view_data = np.array([0.1,0.5,0.2])#中心座標(x,y)サイズ 中心座標はマウスと同じ
mouse = np.array([1,0,0.4,0.4])#左クリック 右クリック スクロール  カーソルを移動するか
keyboard = np.zeros(191)#キーボード入力
'''
keyboard[4] = 1
keyboard[5] = 0.9
keyboard[6] = 0.3
keyboard[9] = 1'''

presskey = []

keylist = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`','a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~','accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome','browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete','divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20','f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja','kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack','nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pgdn','pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator','shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen','command', 'option', 'optionleft', 'optionright']

#0.9以下の入力は取らないでそれ以上の大きさの入力で大きい順に入力されるようなキーボード入力プログラム
keyboard[keyboard<0.9] = 0
key = keyboard[~(keyboard==0)]
key = np.sort(key)
key = key[::-1]
beforenum = 0
picknum = 0
for i in range(len(key)):
    if beforenum == key[i]:#前と同じ数字だったとき
        picknum = picknum + 1
    else:
        picknum = 0
    keynum = np.where(keyboard==key[i])[0]
    presskey.append(keylist[keynum[picknum]])
    beforenum = key[i]#前の順位の数値
#入力開始
for i in range(len(presskey)):
    pgui.keyDown(presskey[i])
for i in range(len(presskey)):
    pgui.keyUp(presskey[i])

print(presskey)

#視界が枠の外に出ないようにする
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
#命令どおりにマウスカーソルを移動
if mouse[3] > 0.5:#0.5以上だとマウスを移動させる
    pgui.moveTo(view_data[0]*img_width, view_data[1]*img_height, duration=0)
#左クリック
if mouse[0] > 0.8:
    pgui.click(button='left')
#右クリック
if mouse[1] > 0.8:
    pgui.click(button='right')
#スクロール
pgui.scroll(int(img_height*2*(mouse[2]-0.5)))

#入力の順番は発火の強さの順番
#pgui.hotkey('a', 'tab', 'enter', 'b', 'o', 'tab', 'enter')

#スクショを撮る
screendata = pgui.screenshot()
#pgui.position()	#現在のマウスの座標（x,y）を取得

#データをカットする
cut_data = screendata.crop((round((view_data[0]-view_data[2]) * img_width),round((view_data[1]-view_data[2]) * img_height),round((view_data[0]+view_data[2]) * img_width),round((view_data[1]+view_data[2]) * img_height)))
cut_data = cut_data.resize((int(img_width/4),int(img_height/4)))#定格サイズに変更
cut_data = np.asarray(cut_data)

# 画像をリサイズ
resize_width = img_width/8
resize_height = resize_width / img_width * img_height
screendata = screendata.resize((int(resize_width),int(resize_height)))
screendata = np.asarray(screendata)

plt.imshow(screendata)
plt.show()
plt.imshow(cut_data)
plt.show()


N=int(24/4)#一秒23今の数だと1秒に4回更新
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

#1秒に4回更新
while True:

    start_time=time.time()
    
    input = stream.read(CHUNK)
    stop_time=time.time()
    print(start_time-stop_time)
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
