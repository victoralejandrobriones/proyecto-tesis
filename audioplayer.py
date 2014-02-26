import Tkinter
from threading import Thread, Event
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy import *
import wave, sys, pyaudio, time, audioop, math, datetime, glob, os, random
files = glob.glob(os.path.join(sys.argv[1], '*.wav'))
print files
chunk = 1024

class Audio:
    def __init__(self, file):
        self.file_name = file
        self.file = wave.open(self.file_name, 'rb')
        p = pyaudio.PyAudio()
        self.stream = p.open(format = 
                             p.get_format_from_width(self.file.getsampwidth()),
                             channels = self.file.getnchannels(),
                             rate = self.file.getframerate(),
                             output = True)
        self.duration = self.file.getnframes()/self.file.getframerate()
    def get_data(self):
        self.data = self.file.readframes(chunk)
        return self.data

class Player:
    def __init__(self, master):
        self.times = 0
        self.size = 4
        self.beat_counter = [0,0]
        self.beat_buffer = [0,0]
        self.beat_time = time.time()
        self.my_values = [0 for i in range(self.size)]
        self.current_time = 0
        self.time_counter = 0
        self.window = master
        self.time_label = Tkinter.StringVar()
        self.file_label = Tkinter.StringVar()
        Tkinter.Label(self.window, textvariable=self.file_label).grid(row=0)
        self.button_pp = Tkinter.Button(self.window,text=u"\u25B6",
                                        command=self.threading)
        self.button_pp.grid(row=1,column=0)
        Tkinter.Label(self.window, textvariable=self.time_label).grid(row=1,column=1)
        self.frame = 0
        self.set_track(files[random.randint(0, len(files)-1)])
        self.window.mainloop()

    def stop_threading(self):
        self.current_time = self.time_counter
        self.button_pp["text"] = u"\u25B6"
        self.button_pp["command"] = self.threading
        self.event = False

    def set_track(self, file):
        print "Playing:",file.split("/")[-1]
        self.file_label.set(file.split("/")[-1])
        self.audio = Audio(file)
        self.filedata = open(file+".dat", "w")
    
    def threading(self):
        self.time = time.time()
        self.button_pp["text"] = u"\u2758"+""+u"\u2758"
        self.button_pp["command"] = self.stop_threading
        self.audio_thread = Thread(target = self.update_audio)
        self.event = True
        self.audio_thread.start()

    def fft(self, pcm, real = False, imaginary = False, both = False):
        #triangle=np.array(range(len(pcm)/2)+range(len(pcm)/2)[::-1])
        #pcm = pcm * triangle
        fft=np.fft.fft(pcm)
        freq=np.fft.fftfreq(np.arange(len(pcm)).shape[-1])[:len(pcm)/2]
        freq=freq * self.audio.file.getframerate()/1000
        if real:
            fftr=10*np.log10(np.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2]
            defv = len(fftr)/self.size
            deff = 0
            defl = len(fftr)/self.size
            bpm = [False for i in range(self.size)]
            for i in range(self.size):
                fftr[deff:defl] = np.average(fftr[deff:defl])
                value = (math.ceil(np.average(fftr[deff:defl])*100)/100)
                mult = 5
                if self.my_values[i] > value:#\
                        #or self.my_values[i] > mult+value:
                    bpm[i]=True
                else:
                    bpm[i]=False
                self.my_values[i] = value
                if np.isinf(value):
                    value = 0
                deff+=(defv)
                defl+=(defv)
            if bpm.count(True)>=bpm.count(False):
                self.times+=1
                if self.times == 1:
                    self.beat_counter[0] = self.beat_counter[1]
                    self.beat_counter[1] = time.time()-self.beat_time
                    self.filedata.write(str(self.time_counter)+", "+str(60/(self.beat_counter[1]-self.beat_counter[0]))+"\n")
            else:
                self.times=0
            return (freq, fftr)

    def update_audio(self):
        self.data = self.audio.get_data()
        while self.data != "" and self.event != False:
                self.time_counter = (time.time()-self.time)+self.current_time
                self.time_label.set(str(datetime.timedelta(seconds=self.audio.duration-int(self.time_counter))))
                pcm = np.fromstring(self.data, "Int16")
                self.fft(pcm, real = True)
                self.audio.stream.write(self.data)
                self.data = self.audio.get_data()
        if self.data == "":
                self.filedata.close()
                self.set_track(files[random.randint(0, len(files)-1)])
                self.time_counter = 0
                self.current_time = 0
                self.threading()

root = Tkinter.Tk()
play = Player(root)
print
