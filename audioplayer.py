import Tkinter
from threading import Thread, Event
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy import *
import wave, sys, pyaudio, time

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
    def get_data(self):
        self.data = self.file.readframes(chunk)
        return self.data

class Plot:
    def __init__(self, master):
        # Create a container
        self.window = Tkinter.Frame(master)
        # Create 2 buttons
        self.button_pp = Tkinter.Button(self.window,text=u"\u25B6",
                                        command=self.threading)
        self.button_pp.pack(side="left")
        self.audio = Audio()
        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax.axis([0,chunk*2,-50000,50000])
        self.line, = self.ax.plot(range(10))
        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.window.pack()
        self.t0 = 0
        self.frame = 0
        self.data = self.audio.get_data()        

    def stop_threading(self):
        self.button_pp["text"] = u"\u25B6"
        self.button_pp["command"] = self.threading
        self.event = False

    def threading(self):
        self.button_pp["text"] = u"\u2758"+""+u"\u2758"
        self.button_pp["command"] = self.stop_threading
        self.thread = Thread(target = self.update)
        self.event = True
        self.thread.start()

    def update(self):
        while self.data != "" and self.event != False:
            if time.time()-self.t0 > 0.001:
                CurrentXAxis=np.arange(self.frame, len(fromstring(self.data, "Int16"))+self.frame)
                self.line.set_data(CurrentXAxis, np.array(np.fromstring(self.data, "Int16")))
                self.ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-50000,50000])
                self.frame+=(chunk*2)
                self.canvas.draw()
                self.t0 = time.time()
            self.audio.stream.write(self.data)
            self.data = self.audio.get_data()

root = Tkinter.Tk()
plot = Plot(root)
root.mainloop()
