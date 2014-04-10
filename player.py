from audio import Audio
from analizer import Analizer
###
from threading import Thread, Event
import numpy as np
from operator import itemgetter
from numpy import *
import sys, time, math, datetime, random, glob, os
import subprocess

class Player:
    def __init__(self, directory):#, master):
        self.directory = directory
        self.files = glob.glob(os.path.join(directory, '*.wav'))
        self.times = 0
        self.size = 8
        self.beat_counter = [0,0]
        self.beat_buffer = [0,0]
        self.beat_time = time.time()
        self.my_values = [0 for i in range(self.size)]
        self.current_time = 0
        self.frame = 0
        self.filedata = []
        Thread(target = self.set_track, args = (self.files[random.randint(0, len(self.files)-1)], )).start()
        #self.set_track(self.files[random.randint(0, len(self.files)-1)])

    def transition(old_track, new_track):
        pass
    
    def stop(self):
        self.current_time = self.audio.current_time
        self.event = False
    
    def set_track(self, file):
        self.file = file
        self.filename = file.split("/")[-1]
        self.audio = Audio(file)
        
        cmd = ['python', 'data_analizer_routine.py', self.directory, file, str(self.audio.real_duration)]
        for cm in cmd:
            print cm,
        print
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p.wait()
        self.new_track = p.communicate()[0].split("\n")[0]
        print self.new_track
        self.filedata = []

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
        current_time = datetime.timedelta(seconds=int(self.audio.duration)-int(self.audio.current_time))
        if time.time()-self.t >=0.3:
            self.play_time.set(str(current_time))
            self.t = time.time()
        #print "Playing:",self.filename, "\tTime:", current_time,
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
                    self.filedata.append(str(self.audio.current_time)+", "+str(60/(self.beat_counter[1]-self.beat_counter[0]))+"\n")
            else:
                self.times=0
            sys.stdout.write('\r')
            sys.stdout.flush()
            return (freq, fftr)

    def update_audio(self):
        self.data = self.audio.get_data()
        while self.data != "" and self.event != False:
            pcm = np.fromstring(self.data, "Int16")
            self.freq_analizer(pcm)
            self.audio.stream.write(self.data)
            self.data = self.audio.get_data()
        if self.data == "":
            #self.filedata.close()
            print self.file
            f = open(self.file+".dat", "w")
            for line in self.filedata:
                f.write(line)
            f.close()
            Thread(target = self.set_track, args = (self.new_track, )).start()
            #self.set_track(self.new_track)
            self.time_counter = 0
            self.current_time = 0
            self.play()
