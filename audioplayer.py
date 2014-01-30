import pyaudio
import wave
import sys
import pylab
from pylab import *
import time

#Tamano de muestra
chunk = 1024

pylab.ion()
if len(sys.argv) < 2:
    print "Uso: %s archivo.wav" % sys.argv[0]
    sys.exit(-1)

#Ventana del graficador
xAx=arange(0,10,1)
yAx=array([0]*10)

fig = figure(1)
ax = fig.add_subplot(111)
ax.set_title("Analizador de ondas de sonido")
ax.set_xlabel("Muestra")
ax.grid(True)
ax.axis([0,10,0,30])
line1=ax.plot(xAx,yAx,'-')
manager = get_current_fig_manager()

#Se abre el archivo de sonido
wf = wave.open(sys.argv[1], 'rb')

#Se inicia pyAudio
p = pyaudio.PyAudio()

#Se crea un flujo con los datos del archivo de sonido
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

#Se leen los frames del archivo
data=wf.readframes(chunk)
t0 = time.time()
i = 0
while data != "":
    #Se grafican los frames limitando los FPS's
    if time.time()-t0 > 0.001:
        #CurrentXAxis=pylab.arange(len(fromstring(data, "Int16")),len(fromstring(data, "Int16"))+500,1)
        CurrentXAxis=pylab.arange(i, len(fromstring(data, "Int16"))+i)
        line1[0].set_data(CurrentXAxis,pylab.array(fromstring(data, "Int16")))
        ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-50000,50000])
        i+=(chunk*2)
        manager.canvas.draw()
        t0 = time.time()
    #Los frames se escriben al flujo
    stream.write(data)
    #Se leen los frames siguientes
    data = wf.readframes(chunk)

stream.close()
p.terminate()
