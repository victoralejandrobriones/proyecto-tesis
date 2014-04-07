from player import Player
###
import Tkinter, glob, os, sys

files = glob.glob(os.path.join(sys.argv[1], '*.wav'))

class Window:
    
    def __init__(self, master):
        self.player = Player(files)
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
