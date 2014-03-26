from analizer import Analizer
###
import Tkinter
from threading import Thread, Event
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy import *
import wave, sys, pyaudio, time, audioop, math, datetime, glob, os, random

files = glob.glob(os.path.join(sys.argv[1], '*.wav'))

class Audio:
    def __init__(self, file):
        self.chunk_counter = 0
        self.file_name = file
        self.file = wave.open(self.file_name, 'rb')
        p = pyaudio.PyAudio()
        self.stream = p.open(format =
                             p.get_format_from_width(self.file.getsampwidth()),
                             channels = self.file.getnchannels(),
                             rate = self.file.getframerate(),
                             output = True)
        self.duration = self.file.getnframes()/self.file.getframerate()
        self.chunk = self.file.getnframes()/(self.duration*1000)
    
    def get_data(self):
        self.data = self.file.readframes(self.chunk)
        self.chunk_counter += self.chunk
        self.current_time = float(self.chunk_counter)/self.file.getframerate()
        return self.data

class Player:
    def __init__(self):#, master):
        self.times = 0
        self.size = 8
        self.beat_counter = [0,0]
        self.beat_buffer = [0,0]
        self.beat_time = time.time()
        self.my_values = [0 for i in range(self.size)]
        self.current_time = 0
        self.frame = 0
        self.set_track(files[random.randint(0, len(files)-1)])

    
    def stop(self):
        self.current_time = self.audio.current_time
        self.event = False
    
    def set_track(self, file):
        self.filename = file.split("/")[-1]
        self.audio = Audio(file)
        try:
            self.next_track = self.data_analizer(file+".dat")
        except:
            pass
        self.filedata = open(file+".dat", "w")
    
    def play(self):
        self.file_label.set(self.filename)
        self.time = time.time()
        self.audio_thread = Thread(target = self.update_audio)
        self.event = True
        self.audio_thread.start()
    
    def set_gui(self, _time, _filename):
        self.t = time.time()
        self.play_time = _time
        self.file_label = _filename
    
    def freq_analizer(self, pcm):
        #triangle=np.array(range(len(pcm)/2)+range(len(pcm)/2)[::-1])
        #pcm = pcm * triangle
        fft=np.fft.fft(pcm)
        freq=np.fft.fftfreq(np.arange(len(pcm)).shape[-1])[:len(pcm)/2]
        freq=freq * self.audio.file.getframerate()/1000
        current_time = datetime.timedelta(seconds=self.audio.duration-int(self.audio.current_time))
        if time.time()-self.t >=0.3:
            self.play_time.set(str(current_time))
            self.t = time.time()
        print "Playing:",self.filename, "\tTime:", current_time,
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
                if self.my_values[i]+mult < value:#\or self.my_values[i] > mult+value:
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
                    self.beat_counter[1] = self.audio.current_time
                    self.filedata.write(str(self.audio.current_time)+", "+str(60/(self.beat_counter[1]-self.beat_counter[0]))+"\n")
            else:
                self.times=0
            sys.stdout.write('\r')
            sys.stdout.flush()
            return (freq, fftr)
    
    def next_track(self, current_file, current_patterns):
        patterns = []
        for file_name in files:
            if file_name+".dat" != current_file:
                try:
                    analizer = Analizer(file_name+".dat")
                    analizer.find_patterns()
                    patterns.append([file_name, analizer])
                except:
                    pass
        for next_file in patterns:
            matches = next_file[1].best_match(current_patterns)
            print next_file[0]
            for match in matches:
                if float(match[0]) < float(match[1]):
                    print match[0], match[1], len(match[2])
            print

    def data_analizer(self, current_file):
        a = Analizer(current_file)
        patterns = a.find_patterns()
        self.next_track(current_file, patterns)
        return patterns
    
    def update_audio(self):
        self.data = self.audio.get_data()
        while self.data != "" and self.event != False:
            pcm = np.fromstring(self.data, "Int16")
            self.freq_analizer(pcm)
            #self.audio.stream.write(self.data)
            self.data = self.audio.get_data()
        if self.data == "":
            self.filedata.close()
            #self.set_track(files[random.randint(0, len(files)-1)])
            #self.time_counter = 0
            self.current_time = 0
            #self.play()

class Window:
    
    def __init__(self, master):
        self.player = Player()
        self.window = master
        self.time_label = Tkinter.StringVar()
        self.file_label = Tkinter.StringVar()
        Tkinter.Label(self.window, textvariable=self.file_label).grid(row=0)
        self.button_pp = Tkinter.Button(self.window,text=u"\u25B6",
                                        command=self.play)
        self.button_pp.grid(row=1,column=0)
        Tkinter.Label(self.window, textvariable=self.time_label).grid(row=1,column=1)
        self.window.mainloop()
    
    def play(self):
        self.button_pp["text"] = u"\u2758"+u"\u2758"
        self.button_pp["command"] = self.stop
        self.player.set_gui(self.time_label, self.file_label)
        self.player.play()
    
    def stop(self):
        self.button_pp["text"] = u"\u25B6"
        self.button_pp["command"] = self.play
        self.player.stop()

if __name__ == '__main__':
    root = Tkinter.Tk()
    window = Window(root)
    print
