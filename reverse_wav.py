import wave, audioop
from sys import argv

#Se agrega el nombre del archivo .wav como argumento
if len(argv) > 1:
    file_name = argv[1]
    wav_file = wave.open(file_name, "rb")
    frames = wav_file.readframes(wav_file.getnframes())
    """    file = open("numbers.txt", "w")                                                                                                                                           
    for i in range(wav_file.getnframes()):                                                                                                                                           
        file.write(str(ord(frames[i])+ord(frames[i+1]))+"\n")                                                                                                                        
        i+=1                                                                                                                                                                         
    file.close()"""
    file = open("numbers.txt", "w")
    samples = []
    for i in range(wav_file.getnframes()):
        samples.append(audioop.getsample(frames, wav_file.getsampwidth(), i))
        file.write(str(samples[i])+"\n")
    file.close()
    rev = audioop.reverse(frames, wav_file.getsampwidth())
    print "Samples: "+str(wav_file.getnframes())+" Sa"
    print "Sampling rate / Frecuencia: "+str(wav_file.getframerate())+" Hz"
    print "Duracion: "+str(wav_file.getnframes()/wav_file.getframerate())+" s"
    wav_rv = wave.open("REVERSED_"+argv[1], "wb")
    wav_rv.setnchannels(wav_file.getnchannels())
    wav_rv.setsampwidth(wav_file.getsampwidth())
    wav_rv.setframerate(wav_file.getframerate())
    wav_rv.setcomptype(wav_file.getcomptype(), wav_file.getcompname())
    wav_rv.writeframes(rev)
    wav_file.close()
    wav_rv.close()
