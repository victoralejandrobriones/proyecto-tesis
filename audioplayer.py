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

        self.window = Tkinter.Frame(master)

        self.button_pp = Tkinter.Button(self.window,text=u"\u25B6",
                                        command=self.threading)
        self.button_pp.pack(side="left")

        self.audio = Audio()

        fig = Figure()

        self.ax1 = fig.add_subplot(411)
        self.ax2 = fig.add_subplot(412)
        self.ax3 = fig.add_subplot(413)
        self.ax4 = fig.add_subplot(414)

        self.ax1.axis([0,chunk*2,-50000,50000])
        self.ax2.axis([0,20,0,100])
        self.ax3.axis([0,20,0,100])
        self.ax4.axis([0,20,0,100])

        self.line, = self.ax1.plot(range(0))
        self.line2, = self.ax2.plot(range(0))
        self.line3, = self.ax3.plot(range(0))        
        self.line4, = self.ax4.plot(range(0))

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

        self.window.pack()

        self.frame = 0
        self.data = self.audio.get_data()

    def stop_threading(self):
        self.button_pp["text"] = u"\u25B6"
        self.button_pp["command"] = self.threading
        self.event = False

    def threading(self):
        self.button_pp["text"] = u"\u2758"+""+u"\u2758"
        self.button_pp["command"] = self.stop_threading
        self.audio_thread = Thread(target = self.update_audio)
        self.plot_thread = Thread(target = self.update_plot)
        self.event = True
        self.audio_thread.start()
        self.plot_thread.start()

    def fft(self, pcm, real = False, imaginary = False, both = False):
        triangle=np.array(range(len(pcm)/2)+range(len(pcm)/2)[::-1])+1
        pcm = pcm * triangle
        fft=np.fft.fft(pcm)
        freq=np.fft.fftfreq(np.arange(len(pcm)).shape[-1])[:len(pcm)/2]
        freq=freq * self.audio.file.getframerate()/1000 #make the frequency scale
        if real:
            fftr=10*np.log10(abs(fft.real))[:len(pcm)/2]
            return (freq, fftr)
        elif imaginary:
            ffti=10*np.log10(abs(fft.imag))[:len(pcm)/2]
            return (freq, ffti)
        elif both:
            fftb=10*np.log10(np.sqrt(fft.imag**2+fft.real**2))[:len(pcm)/2]
            return (freq, fftb)
        else:
            fftr=10*np.log10(abs(fft.real))[:len(pcm)/2]
            ffti=10*np.log10(abs(fft.imag))[:len(pcm)/2]
            fftb=10*np.log10(np.sqrt(fft.real**2+fft.imag**2))[:len(pcm)/2]
            return (freq, fftr, ffti, fftb)
    
    def update_plot(self):
        while self.data != "" and self.event != False:
            pcm = np.fromstring(self.data, "Int16")
            CurrentXAxis=np.arange(self.frame, len(pcm)+self.frame)
            fft_data = self.fft(pcm)
            self.line.set_data(CurrentXAxis, np.array(pcm))
            self.line2.set_data(fft_data[0], fft_data[1])
            self.line3.set_data(fft_data[0], fft_data[2])
            self.line4.set_data(fft_data[0], fft_data[3])
            self.ax1.axis([CurrentXAxis.min(),CurrentXAxis.max(),-50000,50000])
            self.frame+=(chunk*2)
            self.canvas.draw()

    def update_audio(self):
        while self.data != "" and self.event != False:
            self.audio.stream.write(self.data)
            self.data = self.audio.get_data()

root = Tkinter.Tk()
plot = Plot(root)
root.mainloop()
