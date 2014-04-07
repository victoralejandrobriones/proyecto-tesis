import wave, pyaudio

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
        self.real_duration = self.file.getnframes()/float(self.file.getframerate())
        self.chunk = self.file.getnframes()/(self.duration*1000)
    
    def get_data(self):
        self.data = self.file.readframes(self.chunk)
        self.chunk_counter += self.chunk
        self.current_time = float(self.chunk_counter)/self.file.getframerate()
        return self.data
