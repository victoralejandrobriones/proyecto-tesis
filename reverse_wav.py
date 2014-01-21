import wave, audioop
from sys import argv

#Se debe añadir el nombre del archivo .wav como argumento
if len(argv) > 1:
    file_name = argv[1]
    wav_file = wave.open(file_name, "rb")
    frames = wav_file.readframes(wav_file.getnframes())
    rev = audioop.reverse(frames, wav_file.getsampwidth())
    wav_rv = wave.open("REVERSED_"+argv[1], "wb")
    wav_rv.setnchannels(wav_file.getnchannels())
    wav_rv.setsampwidth(wav_file.getsampwidth())
    wav_rv.setframerate(wav_file.getframerate())
    wav_rv.setcomptype(wav_file.getcomptype(), wav_file.getcompname())
    wav_rv.writeframes(rev)
    wav_file.close()
    wav_rv.close()
