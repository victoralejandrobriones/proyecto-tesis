from audio import Audio
from analizer import Analizer
###
from threading import Thread, Event
import numpy as np
from operator import itemgetter
from numpy import *
import sys, time, math, datetime, random

class Player:
    def __init__(self, files):#, master):
        self.files = files
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
        print "START"
        self.file = file
        self.filename = file.split("/")[-1]
        self.audio = Audio(file)
        ###############################################################
        #Aqui va un subproceso para evitar el lag del thread
        try:
            self.next_track(file+".dat")
            print "Finished Good for",
        except:
            self.new_track = self.files[random.randint(0, len(self.files)-1)]
            print "Finished Bad for",
        print self.new_track
        #Aqui termina el subproceso
        ###############################################################
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

    ###############################################################
    #Esta funcion desaparecera, se sustituye por el subproceso
    def data_analizer(self, current_file, current_patterns):
        patterns = []
        number = 0
        list_of_selections = []
        for file_name in self.files:
            if file_name+".dat" != current_file:
                try:
                    _file = open(file_name+".dat", "r").readlines()
                    analizer = Analizer(_file)
                    analizer.find_patterns()
                    patterns.append([file_name, analizer])
                except:
                    pass
        for next_file in patterns:
            matches = next_file[1].best_match(current_patterns)
            match_filter = []
            for match in matches:
                if float(match[0]) < float(match[1]):
                    match_filter.append([match[1], match[0], len(match[2])])
            last = None
            dict_list = []
            match_dict = []
            for match in sorted(match_filter, key=itemgetter(0)):
                if last != match[0]:
                    if last!= None:
                        match_dict.append({last:dict_list})
                    last = match[0]
                    dict_list = []
                dict_list.append([match[1], match[2]])
            selection = []
            for match in reversed(match_dict):
                selection.append(self.best_option(match))
            allow_time = self.audio.real_duration
            allow_time = allow_time-(allow_time*.15)
            filter_selection = []
            for element in selection:
                if element[0] > allow_time:
                    filter_selection.append(element)
            small_time = 0
            for sel in sorted(filter_selection, key=itemgetter(1)):
                if sel[2]!=0:
                    if small_time == 0:
                        small_time = sel
                    if small_time[1] > sel[1]:
                        small_time = sel
            list_of_selections.append([next_file[0],small_time])
        best_selection = None
        small_time = None
        for i in range(len(list_of_selections)):
            if small_time == None:
                small_time = list_of_selections[i][1][1]
            if small_time < list_of_selections[i][1][1]:
                small_time = list_of_selections[i][1][1]
                best_selection = list_of_selections[i][0]
        return best_selection

    #Esta funcion desaparecera, se sustituye por el subproceso
    def best_option(self, match):
        matching = float(match.keys()[0])
        times = []
        intn = []
        for element in reversed(sorted(match[match.keys()[0]], key=itemgetter(1))):
            times.append(element[0])
            intn.append(element[1])
        max = 0
        sel_time = 0
        for i in range(len(intn)):
            if matching - times[i] > matching/3:
                if intn[i]>max:
                    max = intn[i]
                    sel_time = times[i]
        return matching, sel_time, max

    #Esta funcion desaparecera, se sustituye por el subproceso
    def next_track(self, current_file):
        _file = open(current_file, "r").readlines()
        a = Analizer(_file)
        patterns = a.find_patterns()
        self.new_track = self.data_analizer(current_file, patterns)
    ###############################################################

    def update_audio(self):
        self.data = self.audio.get_data()
        while self.data != "" and self.event != False:
            pcm = np.fromstring(self.data, "Int16")
            self.freq_analizer(pcm)
            self.audio.stream.write(self.data)
            self.data = self.audio.get_data()
        if self.data == "":
            #self.filedata.close()
            f = open(self.file+".dat", "w")
            for line in self.filedata:
                f.write(line)
            f.close()
            Thread(target = self.set_track, args = (self.new_track, )).start()
            #self.set_track(self.new_track)
            self.time_counter = 0
            self.current_time = 0
            self.play()
