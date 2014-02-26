import Tkinter
from threading import Thread, Event
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy import *
import wave, sys, pyaudio, time, audioop, math, datetime

chunk = 1024

class Audio:
    def __init__(self):
        self.file = wave.open(sys.argv[1], 'rb')
        p = pyaudio.PyAudio()
        self.stream = p.open(format = 
                             p.get_format_from_width(self.file.getsampwidth()),
                             channels = self.file.getnchannels(),
                             rate = self.file.getframerate(),
                             output = True)
        print self.file.getframerate()
        print self.file.getsampwidth()
        self.duration = self.file.getnframes()/self.file.getframerate()
    def get_data(self):
        self.data = self.file.readframes(chunk)
        return self.data

class Plot:
    def __init__(self, master):
        self.filedata = open(sys.argv[1]+".dat", "w")
        self.times = 0
        self.size = 4
        self.beat_counter = [0,0]
        self.beat_buffer = [0,0]
        self.beat_time = time.time()
        self.my_values = [0 for i in range(self.size)]
        self.current_time = 0
        self.time_counter = 0
        self.window = Tkinter.Frame(master)
        self.time_label = Tkinter.StringVar()
        Tkinter.Label(master, textvariable=self.time_label).pack()
        self.button_pp = Tkinter.Button(self.window,text=u"\u25B6",
                                        command=self.threading)
        self.button_pp.pack(side="left")
        
        self.audio = Audio()

        fig = Figure()

        #self.ax1 = fig.add_subplot(411)
        #self.ax2 = fig.add_subplot(412)
        #self.ax3 = fig.add_subplot(413)
        self.ax3 = fig.add_subplot(111)
        #self.ax4 = fig.add_subplot(212)
        #self.ax1.axis([0,chunk*2,-50000,50000])
        #self.ax2.axis([0,20,0,100])
        self.ax3.axis([0,22,0,100])
        #self.ax4.axis([0,2500,0,60000])

        #self.line, = self.ax1.plot(range(0))
        #self.line2, = self.ax2.plot(range(0))
        self.line3, = self.ax3.plot(range(0))        
        #self.line4, = self.ax4.plot(range(0))

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.window.pack()

        self.frame = 0
        self.data = self.audio.get_data()

    def stop_threading(self):
        self.current_time = self.time_counter
        self.button_pp["text"] = u"\u25B6"
        self.button_pp["command"] = self.threading
        self.event = False

    def threading(self):
        self.time = time.time()
        self.button_pp["text"] = u"\u2758"+""+u"\u2758"
        self.button_pp["command"] = self.stop_threading
        self.audio_thread = Thread(target = self.update_audio)
        self.plot_thread = Thread(target = self.update_plot)
        self.event = True
        self.audio_thread.start()
        #self.plot_thread.start()


    def fft(self, pcm, real = False, imaginary = False, both = False):
        #triangle=np.array(range(len(pcm)/2)+range(len(pcm)/2)[::-1])
        #pcm = pcm * triangle
        fft=np.fft.fft(pcm)
        freq=np.fft.fftfreq(np.arange(len(pcm)).shape[-1])[:len(pcm)/2]
        freq=freq * self.audio.file.getframerate()/1000
        
        if real:
            #fftr=10*np.log10(abs(fft.real))[:len(pcm)/2]
            fftr=10*np.log10(np.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2]
            defv = len(fftr)/self.size
            deff = 0
            defl = len(fftr)/self.size
            self.time_counter = (time.time()-self.time)+self.current_time
            self.time_label.set(str(datetime.timedelta(seconds=self.audio.duration-int(self.time_counter))))
            #print "Duracion: ", datetime.timedelta(seconds=self.audio.duration-int(self.time_counter)), "\t",
            bpm = [False for i in range(self.size)]
            for i in range(self.size):
                fftr[deff:defl] = np.average(fftr[deff:defl])
                #real_v = (math.ceil(np.average(fftr[deff:defl])*100)/100)
                #value = 1*int((math.ceil(np.average(fftr[deff:defl])*100)/100)/1)
                value = (math.ceil(np.average(fftr[deff:defl])*100)/100)
                mult = 5
                if self.my_values[i] > value:#\
                        #or self.my_values[i] > mult+value:
                    bpm[i]=True
                else:
                    bpm[i]=False
                self.my_values[i] = value
                strcolor = ("[0;34m", 20) \
                    if value <=20 else ("[0;36m",40) \
                    if value <=40 else ("[0;32m",60) \
                    if value <=60 else ("[0;33m",80) \
                    if value <=80 else ("[0;31m",0)
                #print strcolor, 
                if np.isinf(value):
                    value = 0
                #print chr(27)+strcolor[0]+str(int(math.ceil(value)))+chr(27)+"[0m","    \t",
                deff+=(defv)
                defl+=(defv)
            #print bpm.count(True),"\t",
            if bpm.count(True)>=bpm.count(False):
                self.times+=1
                #print "OOO",#self.times,
                #if self.beat_counter[1]!=0:
                #    print 60/(self.beat_counter[1]-self.beat_counter[0]),
                #self.beat_buffer[0] = self.beat_buffer[1]
                #self.beat_buffer[1] = 60/(self.beat_counter[1]-self.beat_counter[0])
                #print np.average(self.beat_buffer),
                if self.times == 1:
                    self.beat_counter[0] = self.beat_counter[1]
                    self.beat_counter[1] = time.time()-self.beat_time
                    self.filedata.write(str(self.time_counter)+", "+str(60/(self.beat_counter[1]-self.beat_counter[0]))+"\n")
                    #print time.time()-self.beat_time,
                    #self.beat_time = time.time()
            else:
                self.times=0
                #print "---",
            #print self.beat_counter*((time.time()-self.beat_time)*60),
            #self.beat_counter = 0
            #self.beat_time = time.time()
            #sys.stdout.write('\r')
            #sys.stdout.flush()
            return (freq, fftr)
        """elif imaginary:
            ffti=10*np.log10(abs(fft.imag))[:len(pcm)/2]
            return (freq, ffti)
        elif both:
            fftb=10*np.log10(np.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2]
            return (freq, fftb)
        else:
            fftr=10*np.log10(abs(fft.real))[:len(pcm)/2]
            ffti=10*np.log10(abs(fft.imag))[:len(pcm)/2]
            fftb=10*np.log10(np.sqrt(fft.real**2+fft.imag**2))[:len(pcm)/2]
            return (freq, fftr, ffti, fftb)"""

    def update_plot(self):
        list = []
        i=0
        while self.data != "" and self.event != False:
            pcm = np.fromstring(self.data, "Int16")
            CurrentXAxis=np.arange(self.frame, len(pcm)+self.frame)
            fft_data = self.fft(pcm, real = True)
            #self.line.set_data(CurrentXAxis, np.array(pcm))
            #self.line2.set_data(fft_data[0], fft_data[1])
            #self.line3.set_data(fft_data[0], fft_data[2])
            self.line3.set_data(fft_data[0], fft_data[1])
            #test = 7*audioop.avgpp(pcm, self.audio.file.getsampwidth())
            #list = range(10*int(self.bassIntensity))
            #if test > 32000:
            #    print test
            #else:
            #    print 
            #self.line4.set_ydata(list)
            #self.line4.set_xdata([100]*len(list))
            #i+=10
            #self.ax4.axis([CurrentXAxis.min(),CurrentXAxis.max(),-50000,50000])
            #self.frame+=(len(list))
            self.canvas.draw()

    def update_audio(self):
        mytime = time.time()
        while self.data != "" and self.event != False:
            #if time.time() - mytime > 0.01:
            pcm = np.fromstring(self.data, "Int16")
            self.fft(pcm, real = True)
            self.audio.stream.write(self.data)
            self.data = self.audio.get_data()

root = Tkinter.Tk()
plot = Plot(root)
root.mainloop()
plot.filedata.close()
print 
