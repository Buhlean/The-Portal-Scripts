####################################################
### BEGIN MODULE PYPERCLIP
####################################################

import platform, os

def winGetClipboard():
    ctypes.windll.user32.OpenClipboard(0)
    pcontents = ctypes.windll.user32.GetClipboardData(1) # 1 is CF_TEXT
    data = ctypes.c_char_p(pcontents).value
    #ctypes.windll.kernel32.GlobalUnlock(pcontents)
    ctypes.windll.user32.CloseClipboard()
    return data
def winSetClipboard(text):
    text = str(text)
    GMEM_DDESHARE = 0x2000
    ctypes.windll.user32.OpenClipboard(0)
    ctypes.windll.user32.EmptyClipboard()
    try:
        # works on Python 2 (bytes() only takes one argument)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text))+1)
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        hCd = ctypes.windll.kernel32.GlobalAlloc(GMEM_DDESHARE, len(bytes(text, 'ascii'))+1)
    pchData = ctypes.windll.kernel32.GlobalLock(hCd)
    try:
        # works on Python 2 (bytes() only takes one argument)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text))
    except TypeError:
        # works on Python 3 (bytes() requires an encoding)
        ctypes.cdll.msvcrt.strcpy(ctypes.c_char_p(pchData), bytes(text, 'ascii'))
    ctypes.windll.kernel32.GlobalUnlock(hCd)
    ctypes.windll.user32.SetClipboardData(1, hCd)
    ctypes.windll.user32.CloseClipboard()
def macSetClipboard(text):
    text = str(text)
    outf = os.popen('pbcopy', 'w')
    outf.write(text)
    outf.close()
def macGetClipboard():
    outf = os.popen('pbpaste', 'r')
    content = outf.read()
    outf.close()
    return content
def gtkGetClipboard():
    return gtk.Clipboard().wait_for_text()
def gtkSetClipboard(text):
    global cb
    text = str(text)
    cb = gtk.Clipboard()
    cb.set_text(text)
    cb.store()
def qtGetClipboard():
    return str(cb.text())
def qtSetClipboard(text):
    text = str(text)
    cb.setText(text)
def xclipSetClipboard(text):
    text = str(text)
    outf = os.popen('xclip -selection c', 'w')
    outf.write(text)
    outf.close()
def xclipGetClipboard():
    outf = os.popen('xclip -selection c -o', 'r')
    content = outf.read()
    outf.close()
    return content
def xselSetClipboard(text):
    text = str(text)
    outf = os.popen('xsel -i', 'w')
    outf.write(text)
    outf.close()
def xselGetClipboard():
    outf = os.popen('xsel -o', 'r')
    content = outf.read()
    outf.close()
    return content
if os.name == 'nt' or platform.system() == 'Windows':
    import ctypes
    getcb = winGetClipboard
    setcb = winSetClipboard
elif os.name == 'mac' or platform.system() == 'Darwin':
    getcb = macGetClipboard
    setcb = macSetClipboard
elif os.name == 'posix' or platform.system() == 'Linux':
    xclipExists = os.system('which xclip') == 0
    if xclipExists:
        getcb = xclipGetClipboard
        setcb = xclipSetClipboard
    else:
        xselExists = os.system('which xsel') == 0
        if xselExists:
            getcb = xselGetClipboard
            setcb = xselSetClipboard
        try:
            import gtk
            getcb = gtkGetClipboard
            setcb = gtkSetClipboard
        except Exception:
            try:
                import PyQt4.QtCore
                import PyQt4.QtGui
                app = PyQt4.QApplication([])
                cb = PyQt4.QtGui.QApplication.clipboard()
                getcb = qtGetClipboard
                setcb = qtSetClipboard
            except:
                raise Exception('Pyperclip requires the gtk or PyQt4 module installed, or the xclip command.')
copy = setcb
paste = getcb

####################################################
### END PYPERCLIP
####################################################

# .config(state=DISABLED)
# .config(state=NORMAL)

# text = 'string'
# textvariable = StringVar(master, default)

## Colors
#3b3f4e various grays
#7a7e8f
#535867
#6d717e
#1d243a dark blue
#eaff68 yellow

## Button layout
#FLAT
#RAISED
#SUNKEN
#GROOVE
#RIDGE

## available dialogs:
# tkinter.filedialog.asksaveasfilename()
# tkinter.filedialog.asksaveasfile()
# tkinter.filedialog.askopenfilename()
# tkinter.filedialog.askopenfile()
# tkinter.filedialog.askdirectory()
# tkinter.filedialog.askopenfilenames()
# tkinter.filedialog.askopenfiles()

## remember:
# command=functools.partial(...)

import tkinter as tk
from tkinter import filedialog
import functools

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Universal Transcript Converter')
        self.configure(bg='#1D243A')
        self.geometry('580x580+40+40')
        self.resizable(True, True)
        
class App(tk.Frame):
    def __init__(self, root):
        super().__init__(bg='#1D243A', bd=0, relief=tk.GROOVE, padx=10, pady=10)
        self.path, self.outpath, self.episodeNr, self.source    = tk.StringVar(self, 'C:/'), tk.StringVar(self, 'C:/'), tk.StringVar(self, 0), tk.StringVar(self, '')
        self.service, self.speaker, self.length, self.error     = tk.StringVar(self, ''), tk.StringVar(self, 'Eric Weinstein'), tk.StringVar(self, '00:00:00'), tk.StringVar(self, '')
        self.filepath, self.filename = '', ''

        self.pack(side="top", fill="both", expand=True)
        
        # last line:
        self.drawGUI()

    def drawGUI(self):
        ##########
        ## FILE ##
        framefile = tk.Frame(self)
        framefile.columnconfigure(1, weight=1)
        framefile.pack(side=tk.TOP, fill=tk.X)
        #LabelFile
        tk.Label(framefile, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='Location of transcript file'
                 ).grid(columnspan=5, sticky='NEWS')
        #EntryFile
        tk.Label(framefile, bg='#1D243A', bd=0, padx=4).grid(column=0, row=1, sticky='NEWS') #padding
        tk.Entry(framefile, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, 
                 highlightthickness=0, 
                 textvariable=self.path
                 ).grid(column=1, row=1, sticky='NEWS')
        #ButtonFile
        tk.Label(framefile, bg='#1D243A', bd=0, padx=4).grid(column=2, row=1, sticky='NEWS') #padding
        tk.Button(framefile, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.openfile, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Open...', width=9
                  ).grid(column=3, row=1, sticky='EW')
        tk.Label(framefile, bg='#1D243A', bd=0, padx=4).grid(column=4, row=1, sticky='NEWS') #padding
        tk.Label(framefile, bg='#1D243A', bd=0, pady=0).grid(columnspan=5, row=2, sticky='NEWS') #padding

        #############
        ## EPISODE ##
        frameepisode = tk.Frame(self)
        frameepisode.columnconfigure(2, weight=1)
        frameepisode.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(frameepisode, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='Which Episode is this from? (optional)'
                 ).grid(columnspan=5, sticky='NEWS')
        #EntryEpisode
        tk.Label(frameepisode, bg='#1D243A', bd=0, padx=4).grid(column=0, row=1, sticky='NEWS') #padding
        tk.Entry(frameepisode, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=4,
                 highlightthickness=0, 
                 textvariable=self.episodeNr
                 ).grid(column=1, row=1, sticky='NEWS')
        tk.Label(frameepisode, bg='#1D243A', bd=0, padx=4).grid(column=2, row=1, sticky='NEWS') #padding
        tk.Button(frameepisode, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.episode_fill, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Fill in', width=9
                  ).grid(column=3, row=1, sticky='EW')
        tk.Label(frameepisode, bg='#1D243A', bd=0, padx=4).grid(column=4, row=1, sticky='NEWS') #padding
        tk.Label(frameepisode, bg='#1D243A', bd=0, pady=0).grid(columnspan=5, row=2, sticky='NEWS') #padding

        ############
        ## OUTPUT ##
        frameoutput = tk.Frame(self)
        frameoutput.columnconfigure(1, weight=1)
        frameoutput.pack(side=tk.TOP, fill=tk.X)
        #LabelOutput
        tk.Label(frameoutput, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='Where should the output go? (optional)'
                 ).grid(columnspan=5, sticky='NEWS')
        #EntryOutput
        tk.Label(frameoutput, bg='#1D243A', bd=0, padx=4).grid(column=0, row=1, sticky='NEWS') #padding
        tk.Entry(frameoutput, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, 
                 highlightthickness=0,
                 textvariable=self.outpath
                 ).grid(column=1, row=1, sticky='NEWS')
        tk.Label(frameoutput, bg='#1D243A', bd=0, padx=4).grid(column=2, row=1, sticky='NEWS') #padding
        #ButtonOutput
        tk.Button(frameoutput, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.getsaveplace, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Choose...', width=9
                  ).grid(column=3, row=1, sticky='EW')
        tk.Label(frameoutput, bg='#1D243A', bd=0, padx=4).grid(column=4, row=1, sticky='NEWS') #padding
        tk.Label(frameoutput, bg='#1D243A', bd=0, pady=0).grid(columnspan=5, row=2, sticky='NEWS') #padding

        #############
        ## SERVICE ##
        frameservice = tk.Frame(self)
        columns = 5
        for i in range(columns):
            frameservice.columnconfigure(i, weight=1)
        frameservice.pack(side=tk.TOP, fill=tk.X)
        #LabelService
        tk.Label(frameservice, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='From where did you export the transcript? (optional for .vtt)'
                 ).grid(columnspan=columns, sticky='NEWS')
        self.service.set('Descript')
        #RadioDescript
        tk.Radiobutton(frameservice, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=8, justify=tk.LEFT, width=13,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='Descript', var=self.service, value='Descript'
                       ).grid(row=1, column=0, sticky='NEWS')
        tk.Radiobutton(frameservice, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=0, justify=tk.LEFT,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='Otter.ai', var=self.service, value='Otter'
                       ).grid(row=1, column=1, sticky='NEWS')
        tk.Label(frameservice, bg='#1D243A', bd=0, pady=0).grid(column=2, columnspan=columns-2, row=1, sticky='NEWS') #padding
        tk.Label(frameservice, bg='#1D243A', bd=0, pady=0).grid(columnspan=columns, row=2, sticky='NEWS') #padding

        ############
        ## SOURCE ##
        framesource = tk.Frame(self)
        for i in range(columns):
            framesource.columnconfigure(i, weight=1)
        framesource.pack(side=tk.TOP, fill=tk.X)
        #LabelSource
        tk.Label(framesource, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='From where did you download the audio?'
                 ).grid(columnspan=columns, sticky='EW')
        self.source.set('art19')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=8, justify=tk.LEFT, width=13,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='Art19/Podcast Feed', var=self.source, value='art19'
                       ).grid(row=1, column=0, sticky='NEWS')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=0, justify=tk.LEFT,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='YouTube', var=self.source, value='yt'
                       ).grid(row=1, column=1, sticky='NEWS')
        tk.Label(framesource, bg='#1D243A', bd=0, pady=0).grid(column=2, columnspan=columns-2, row=1, sticky='NEWS') #padding
        tk.Label(framesource, bg='#1D243A', bd=0, pady=1).grid(columnspan=columns, row=2, sticky='NEWS') #padding

        #############
        ## SPEAKER ##
        framespeaker = tk.Frame(self)
        framespeaker.columnconfigure(1, weight=1)
        framespeaker.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(framespeaker, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='Who are the Speakers? (separate by comma)'
                 ).grid(columnspan=3, sticky='NEWS')
        #EntryEpisode
        tk.Label(framespeaker, bg='#1D243A', bd=0, padx=4).grid(column=0, row=1, sticky='NEWS') #padding
        tk.Entry(framespeaker, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=40,
                 highlightthickness=0, 
                 textvariable=self.speaker
                 ).grid(column=1, row=1, sticky='NEWS')
        tk.Label(framespeaker, bg='#1D243A', bd=0, padx=4).grid(column=2, row=1, sticky='NEWS') #padding
        tk.Label(framespeaker, bg='#1D243A', bd=0, pady=0).grid(columnspan=3, row=2, sticky='NEWS') #padding

        #############
        ## LENGTH ##
        framelength = tk.Frame(self)
        framelength.columnconfigure(2, weight=1)
        framelength.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(framelength, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, pady=8, padx=8,
                 text='Length of the Episode? (optional, first 30 are known to program)'
                 ).grid(columnspan=3, sticky='NEWS')
        #EntryEpisode
        tk.Label(framelength, bg='#1D243A', bd=0, padx=4).grid(column=0, row=1, sticky='NEWS') #padding
        tk.Entry(framelength, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=8,
                 highlightthickness=0, 
                 textvariable=self.length
                 ).grid(column=1, row=1, sticky='NEWS')
        tk.Label(framelength, bg='#1D243A', bd=0, padx=4).grid(column=2, row=1, sticky='NEWS') #padding
        tk.Label(framelength, bg='#1D243A', bd=0, pady=0).grid(columnspan=3, row=2, sticky='NEWS') #padding

        ############
        ## SUBMIT ##
        #ButtonSubmit
        tk.Label(self, bg='#1D243A', bd=0, padx=4).pack(side=tk.RIGHT)
        tk.Button(self, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.convert, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Convert', width=9
                  ).pack(side=tk.RIGHT)
        tk.Label(self, bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', padx=8, textvariable=self.error).pack(side=tk.RIGHT)

    def episode_fill(self):
        self.error.set('')
        try:
            e = int(self.episodeNr.get())
            self.length.set(LENGTHS[int(e)])
            self.speaker.set(', '.join(SPEAKER[int(e)]))
        except:
            self.error.set('Episode Number must be Number')
    def openfile(self):
        self.error.set('')
        self.path.set(filedialog.askopenfilename())
        if '/' in self.path.get():
            self.filepath, self.filename = tuple(self.path.get().rsplit('/', 1))
            for e in EPISODES:
                if e in self.filename:
                    self.episodeNr.set(e)
                    self.length.set(LENGTHS[int(e)])
                    self.speaker.set(', '.join(SPEAKER[int(e)]))
                    break
            if self.outpath.get() == 'C:/' or self.outpath.get() == '':
                self.outpath.set(self.filepath)
    def getsaveplace(self):
        self.error.set('')
        self.outpath.set(filedialog.askdirectory())
    def convert(self):
        if '/' in self.path.get():
            self.filepath, self.filename = tuple(self.path.get().rsplit('/', 1))
        else:
            self.error.set('Please specify a valid input path and file')
        if '00:00:00' in self.length.get():
            length = None
        elif len(self.length.get()) < 7:
            length = None
        else:
            length = self.length.get()
        if not (length is None or len(length.split(':')) == 3):
            self.error.set('delete or correct the Length field')
            return
        if not ('.txt' in self.filename[-5:] or '.vtt' in self.filename[-5:]):
            self.error.set('Wrong type of file, expected .txt or .vtt')
            return
        if '.vtt' in self.filename[-5:]:
            vtt = True
        try:
            int(self.episodeNr.get())
        except:
            self.error.set('Episode Number must be Number')
            return
        if not int(self.episodeNr.get()) >= 0:
            self.error.set('Episode Number must be positive')
            return
        if not vtt and not len(self.speaker.get()) > 1:
            self.error.set('No speakers were given, please write at least Eric Weinstein in')
            return
        MainProgram(self.filepath, self.filename,
                    self.episodeNr.get(), self.source.get(),
                    self.service.get(), self.speaker.get(),
                    length, self.outpath.get())
        self.error.set('Success!')    
    
class MainProgram():
    def __init__(self, filepath, filename, episodeNr, source, service, speaker, length=None, output=None):
        self.filepath, self.filename, self.source, self.service, self.length, self.output = filepath, filename, source, service, length, output
        try:
            self.episodeNr = int(episodeNr) # I checked above, but you never know...
        except:
            self.episodeNr = 0
        if self.output is None or self.output == '':
            self.output = self.filepath
        if self.episodeNr <= CURRENT and self.episodeNr > 0:
            if len(speaker) < len(SPEAKER[self.episodeNr]):
                speaker = SPEAKER[self.episodeNr]
            self.length = LENGTHS[self.episodeNr]

        with open('/'.join((filepath, filename)), 'r') as file:
            rawlines = [line for line in file]
        rawtext = ''.join(rawlines)
        self.speaker = []
        for s in speaker:
            if ' ' in s:
                self.speaker.append(s.rsplit(' ', 1)[1])
        tokens = []

        if('vtt' in filename.rsplit('.', 1)):
            tokens = self.parse_vtt(rawtext)
        elif('descript' in service.lower()):
            title, cleanedtext = (lambda x: (x[0], x[1:]))(rawtext.split('[', 1))
            tokens = self.parse_descript(cleanedtext, self.speaker)
        elif('otter' in service.lower()):
            tokens = self.parse_otter(rawtext, self.speaker)
        else:
            assert False, 'Wrong source, please choose art19 or youtube or wiki.'

        self.save_as_srt(tokens)
        self.save_as_vtt(tokens)
        self.save_as_wiki(tokens)
        
    def parse_vtt(self, rawtext):
        tokens = []
        time = ''
        currentspeaker = ''
        content = ''

        rawtext = rawtext.split('WEBVTT', 1)[1].strip() # remove everything above the first actual line 
        for block in rawtext.split('\n\n'): # specification says two newline between each block. very handy!
            note = False
            content = ''
            for line in block.split('\n'):
                if 'NOTE' in line: # found a comment
                    note = True
                    continue
                if not note and '-->' in line: # we are expecting a timestamp here, always contains -->
                    time = line.strip() # there might be whitespace, meaning a wrench in my functions. gets rid of it
                    continue # no additional content here
                content = ''.join((content, line)) # additional spoken words for the current timestamp
            if note: # it's a comment/NOTE
                tokens.append(list((0, '', '', content))) # 0 means NOTE, will be decoded in the save_as_vtte method
            else: # not a NOTE, actual cue
                if '<v' in content[:3]: # already tagged
                    content = content.strip()
                    content = content[3:]
                    currentspeaker, content = tuple(content.split('>', 1))
                    tokens.append(list((1, currentspeaker, time, content)))
                else: # old format
                    if ':' in content[:32]:
                        currentspeaker, content = tuple(content.split(':', 1))
                    tokens.append(list((2, currentspeaker, time, content)))
        return tokens

    def parse_descript(self, text, people):
        tokens = [] #initialize
        for line in text[0].split('['): # brackets contain timestamp
            splittext = line.split(']')
            if len(splittext)==1: # shouldn't occur
                print('WARNING', line)
                continue
            splittext[1] = splittext[1].strip() # remove trailing whitespace and the newline at the end
            if splittext[1] == '': # two timestamps following each other without content
                continue # ...with the next timestamp
            tokens.append(splittext) # token contains time and text

        tokengen1 = (t for t in tokens)
        prevtoken = next(tokengen1) 
        newtokens = [] 
        for token in tokengen1: # calculate 'start -> end' from two neighbouring tokens timestamps
            newtokens.append([''.join((prevtoken[0], '.000', ' --> ', token[0], '.000')), prevtoken[1]])
            prevtoken = token
        try: # I saved most episode lengths in a list below
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTHS[self.episodeNr], '.000')), prevtoken[2]])
        except: # default
            try:
                newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', self.length, '.000')), prevtoken[2]])
            except:
                newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', '9:00:00', '.000')), prevtoken[2]])
        
        tokengen2 = (token for token in newtokens)
        finaltokens = []
        currentspeaker = next(tokengen2)[1] # always starts with Eric
        Speaker = [s+':' for s in people] # format the folks to fit the file

        for token in tokengen2:
            found = False
            for sp in Speaker:
                if sp in token[1]:
                    currentspeaker = token[1]
                    found = True
                    break
            if not found:
                finaltokens.append([currentspeaker, token[0], token[1]])
        return finaltokens

    def parse_otter(self, rawtext, people):
        tokens = []
        found = False
        currentspeaker = 'Weinstein'
        linegen = (x for x in rawtext.split('\n')) # makes a 'generator' out of the list
        # so that I can call next() on it from within the loop. very helpful here
        for line in linegen:
            if len(line) == 0:
                continue
            found = False
            for i in range(len(people)):
                if people[i] in line:
                    currentspeaker = self.speaker[i]
                    time = line.split('  ')[1]
                    found = True
            if not found:
                break
            ## end parsing line
            if len(time) < 7: ## e.g. 10:35 instead of 00:10:35
                if len(time) == 4:
                    time = ''.join(('00:0', time)) # for the first 10 seconds, e.g. 0:01
                else:
                    time = ''.join(('00:', time))
            elif len(time) == 7:
                time = ''.join(('0', time)) # for 1:20:41 , makes it 01:20:41
            
            tokens.append(list((currentspeaker, time, next(linegen))))
        # edit timestamps to be usable in vtt
        prevtoken = []
        newtokens = []
        first = True
        for token in tokens:
            if first:
                prevtoken = token
                first = False
                continue
            # I take the timestamp from the previous token and assume that the sentence ended at the beginning of the current one.
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', token[1], '.000')), prevtoken[2]])
            prevtoken = token
        # there is now only the last token left, that's where the LENGTH of the episode comes into play
        try: # I saved most episode lengths in a list below
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTHS[self.episodeNr], '.000')), prevtoken[2]])
        except: # default
            try:
                newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', self.length, '.000')), prevtoken[2]])
            except:
                newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', '9:00:00', '.000')), prevtoken[2]])
        return newtokens
    
    ######################################################################################################################################################
    ## vtt file, specification-compliant
    def save_as_vtt(self, tokens):
        if self.episodeNr != 0:
            if self.source is not None:
                filename = ''.join(('Ep_', str(self.episodeNr), '_', self.source.lower(), '.vtt'))
            else:
                filename = ''.join(('Ep_', str(self.episodeNr), '.vtt'))
        else:
            if self.source is not None:
                filename = ''.join((self.filename, '_', self.source.lower(), '.vtt'))
            else:
                filename = ''.join((self.filename, '.vtt'))
        with open('/'.join((self.output, filename)), 'w') as file:
            file.write('\nWEBVTT\n\n')
            vtt = False
            if len(tokens[0]) == 4:
                vtt = True
            if not vtt:
                for token in tokens:
                    file.write(f'{token[2]}\n<v {token[1]}>{token[3]}\n\n')
            else:
                try:
                    
                    for token in tokens:
                        if token[0] == 0:
                            file.write(f'NOTE\n{token[3]}\n\n')
                        else:
                            file.write(f'{token[2]}\n<v {token[1]}>{token[3]}\n\n')
                except IndexError:
                    print('ERRORERROR')
                    print(len(token))
                    print(token)
            
    ## srt file, specification-compliant
    def save_as_srt(self, tokens):
        if self.episodeNr != 0:
            if self.source is not None:
                filename = ''.join(('Ep_', str(self.episodeNr), '_', self.source.lower(), '.srt'))
            else:
                filename = ''.join(('Ep_', str(self.episodeNr), '.srt'))
        else:
            if self.source is not None:
                filename = ''.join((self.filename, '_', self.source.lower(), '.srt'))
            else:
                filename = ''.join((self.filename, '.srt'))
        with open('/'.join((self.output, filename)), 'w') as file:
            i = 0
            currentspeaker = ''
            vtt = False
            if len(tokens[0]) == 4:
                vtt = True
            for token in tokens:
                if vtt:
                    if token[0] == 0:
                        continue
                    if token[0] == currentspeaker: # still the same speaker? 
                        preamble = ''
                    else: # only print speaker name if it changed since last sentence
                        currentspeaker = token[1]
                        preamble = f'{currentspeaker}: '
                    i += 1
                    file.write(f'{i}\n{token[2]}\n{preamble}{token[3]}\n\n')
                else:
                    if token[0] == currentspeaker: # still the same speaker? 
                        preamble = ''
                    else: # only print speaker name if it changed since last sentence
                        currentspeaker = token[0]
                        preamble = f'{currentspeaker}: '
                    i += 1
                    file.write(f'{i}\n{token[1]}\n{preamble}{token[2]}\n\n')

    ## wiki markup
    def save_as_wiki(self, tokens):
        if self.episodeNr != 0:
            filename = ''.join(('Ep_', str(self.episodeNr), '_', 'wiki', '.txt'))
        else:
            filename = ''.join((self.filename, '_', 'wiki', '.txt'))
        with open('/'.join((self.output, filename)), 'w') as file:
            currentspeaker = ''
            vtt = False
            if len(tokens[0]) == 4:
                vtt = True
            for token in tokens:
                if vtt:
                    if token[0] == 0:
                        continue
                    token.pop(0)
                if 'STARTAD' in token[2][:10]:
                    file.write('\n\n\'\'\'AD\'\'\'')
                    token[2] = token[2].split('ENDAD', 1)[1]
                    currentspeaker = ''
                    if len(token[2]) <4:
                        continue
                time = token[1].split(' --> ')[0][:-4]
                if token[0] == currentspeaker: # same speaker? no new headline
                    preamble = ''
                else: # only print speaker name if it changed since last sentence, \' escapes the ' for wiki markup
                    currentspeaker = token[0]
                    preamble = f'\n\n\'\'\'[{time}] {currentspeaker}:\'\'\' '
                file.write(preamble) # speaker or empty
                #format: <span title="timstamp here">text here</span>
                file.write(f'<span title=\"{time}\">{token[2]}</span>')
###############################################################################################################################################################################################
## all episode lengths up to EP30
CURRENT = 30
EPISODES= [str(e).zfill(2) for e in range(0,CURRENT+1)]; EPISODES.pop(19)
LENGTHS = ['0:01:34', '02:52:35', '00:28:33', '01:21:31', '02:45:48', '01:51:21', '02:01:59', '02:01:16', '01:08:49', '02:19:36', '01:43:27', '02:38:59', '01:35:46', '01:38:20', '01:06:39', '01:50:54', '02:18:17', '02:20:04', '01:07:58', '02:18:33', '02:23:04', '01:52:50', '01:10:39', '02:11:03', '01:55:20', '01:09:33', '02:29:56', '03:38:06', '02:05:43', '02:03:49', '02:37:03']
SPEAKER = [['Eric Weinstein'], #0
           ['Eric Weinstein', 'Peter Thiel'],
           ['Eric Weinstein'],
           ['Eric Weinstein', 'Werner Herzog'],
           ['Eric Weinstein', 'Timur Kuran'],
           ['Eric Weinstein', 'Rabbi Wolpe'],
           ['Eric Weinstein', 'Jocko Willink'],
           ['Eric Weinstein', 'Bret Easton Ellis'],
           ['Eric Weinstein', 'Andrew Yang'],
           ['Eric Weinstein', 'Bryan Callen'],
           ['Eric Weinstein', 'Julie Lindendahl'], #10
           ['Eric Weinstein', 'Sam Harris'],
           ['Eric Weinstein', 'Vitalik Buterin'],
           ['Eric Weinstein', 'Garry Gasparov'],
           ['Eric Weinstein', 'London Tsai'],
           ['Eric Weinstein', 'Garrett Lisi'],
           ['Eric Weinstein', 'Tyler Cowen'],
           ['Eric Weinstein', 'Anna Khachiyan'],
           ['Eric Weinstein'],
           ['Eric Weinstein', 'Bret Weinstein'],
           ['Eric Weinstein', 'Sir Roger Penrose'], #20
           ['Eric Weinstein', 'Ashley Mathews'],
           ['Eric Weinstein', 'Ben Greenfield'],
           ['Eric Weinstein', 'Agnes Collard'],
           ['Eric Weinstein', 'Kai Lenny'],
           ['Eric Weinstein'],
           ['Eric Weinstein', 'James O\'Keefe'],
           ['Eric Weinstein', 'Daniel Schmachtenberger'],
           ['Eric Weinstein', 'Eric Lewis'],
           ['Eric Weinstein', 'Jamie Metzl'],
           ['Eric Weinstein', 'Ross Douthat'] #30
           ]

def main():
    root = Root()
    app = App(root)
    app.mainloop()

if __name__ == '__main__':
    main()
