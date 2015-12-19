import Tkinter as tk
import thread,time
GIFS = {}
Status = True
names = ["walking","ChickenDance"]#,"BreakDance","Dance","HipHop","Samba","Swing"]
doneLoading = False

NumberofGifs = len(GIFS)
CurrentGifNumber = 0
CurrentImage = None
button = None
root = None

class AnimatedGif(object):
    """ Animated GIF Image Container. """
    def __init__(self, image_file_path):
        self.image_file_path = image_file_path
        self._frames = []
        self._load()
    def __len__(self):
        return len(self._frames)

    def __getitem__(self, frame_num):
        return self._frames[frame_num]

    def _load(self):
        """ Read in all the frames of a multi-frame gif image. """
        while True:
            frame_num = len(self._frames)  # number of next frame to read
            try:
                frame = tk.PhotoImage(file=self.image_file_path,
                                   format="gif -index {}".format(frame_num))
            except tk.TclError:
                break
            self._frames.append(frame)
        

def updatePicture(frame_num):

    if(doneLoading):
        global Status
        ms_delay = 1000 // len(CurrentImage)
        

        button.configure(image=CurrentImage[frame_num])

        
        frame_num += 1
        if(frame_num >= len(CurrentImage)):
            frame_num = 0
            
        if(Status == False):
            Status = True
            return
            
        else:
            root.after(ms_delay, updatePicture, frame_num)

def startAnimation():
    
    
    updatePicture(0)

def nextAnimation():

    global CurrentImage, CurrentGifNumber,Status
    name =names[CurrentGifNumber]
    CurrentGifNumber += 1
    
    if(CurrentGifNumber >= NumberofGifs):
        CurrentGifNumber = 0
    CurrentImage = GIFS[names[CurrentGifNumber]]
    
    updatePicture(0)
    Status = False





def GetGif():


    global doneLoading, CurrentImage, NumberofGifs,GIFS
    

    for name in names:
        image_file_path = "ICONS/"+name+".gif"
        ani_img = AnimatedGif(image_file_path)
        print(len(ani_img))
        GIFS[name] = ani_img
        
    print("done")
    doneLoading = True
    CurrentImage=GIFS[names[0]]
    NumberofGifs = len(GIFS)
        

        


def Start(mroot):
    global button,root
    root = mroot
    name =names[CurrentGifNumber]
     
    button = tk.Button(root,relief = tk.FLAT,command = nextAnimation)  # display first frame initially
    button.pack()

    GetGif()
    startAnimation()

##    
##root = tk.Tk()
##root.title("Animation Demo")
##Start(root)
##root.mainloop()


##changeAnimation = Button(root, text="Next", command=nextAnimation)
##changeAnimation.pack()
##stop_animation = Button(root, text="stop animation", command=cancel_animation)
##stop_animation.pack()



