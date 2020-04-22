
import tkinter as tk
from tkinter import filedialog

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Universal Transcript Converter')
        self.configure(bg='#1D243A')
        self.geometry('580x580+40+40')
        self.resizable(True, True)
        
class App(tk.Frame):
    def __init__(self, root):
        super().__init__(bg='#1D243A', bd=0, relief=tk.GROOVE, padx=20, pady=20)
        self.path, self.outpath, self.episodeNr, self.source    = tk.StringVar(self, 'C:/'), tk.StringVar(self, 'C:/'), tk.StringVar(self, 0), tk.StringVar(self, '')
        self.service, self.speaker, self.length, self.error     = tk.StringVar(self, ''), tk.StringVar(self, 'Eric Weinstein'), tk.StringVar(self, '00:00:00'), tk.StringVar(self, '')
        self.filepath, self.filename = '', ''

        self.pack(side="top", fill="both", expand=True)
        
        # last line:
        self.drawGUI()

    def drawGUI(self):
        padding = 6
        ##########
        ## FILE ##
        framefile = tk.Frame(self)
        framefile.configure(pady=padding, bg='#1D243A')
        framefile.columnconfigure(1, weight=1)
        framefile.pack(side=tk.TOP, fill=tk.X)
        #LabelFile
        tk.Label(framefile, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Location of transcript file'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryFile
        tk.Entry(framefile, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, 
                 highlightthickness=0, 
                 textvariable=self.path
                 ).grid(column=1, row=1, sticky='NEWS')
        #ButtonFile
        tk.Button(framefile, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.openfile, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Open...', width=9
                  ).grid(column=3, row=1, sticky='EW')

        #############
        ## EPISODE ##
        frameepisode = tk.Frame(self)
        frameepisode.configure(pady=padding, bg='#1D243A')
        frameepisode.columnconfigure(2, weight=1)
        frameepisode.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(frameepisode, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Which Episode is this from? (optional)'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(frameepisode, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=4,
                 highlightthickness=0, 
                 textvariable=self.episodeNr
                 ).grid(column=1, row=1, sticky='NEWS')
        tk.Button(frameepisode, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.episode_fill, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Fill in', width=9
                  ).grid(column=3, row=1, sticky='EW')

        ############
        ## OUTPUT ##
        frameoutput = tk.Frame(self)
        frameoutput.configure(pady=padding, bg='#1D243A')
        frameoutput.columnconfigure(1, weight=1)
        frameoutput.pack(side=tk.TOP, fill=tk.X)
        #LabelOutput
        tk.Label(frameoutput, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Where should the output go? (optional)'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryOutput
        tk.Entry(frameoutput, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, 
                 highlightthickness=0,
                 textvariable=self.outpath
                 ).grid(column=1, row=1, sticky='NEWS')
        #ButtonOutput
        tk.Button(frameoutput, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.getsaveplace, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Choose...', width=9
                  ).grid(column=3, row=1, sticky='EW')

        #############
        ## SERVICE ##
        frameservice = tk.Frame(self)
        frameservice.configure(pady=padding, bg='#1D243A')
        columns = 6
        for i in range(columns):
            frameservice.columnconfigure(i, weight=4)
        frameservice.pack(side=tk.TOP, fill=tk.X)
        #LabelService
        tk.Label(frameservice, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='From where did you export the transcript? (optional for .vtt)'
                 ).grid(columnspan=columns, sticky='NEWS', pady=(0,8))
        self.service.set('Descript')
        #RadioDescript
        tk.Radiobutton(frameservice, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=0, justify=tk.LEFT, width=13,
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

        ############
        ## SOURCE ##
        framesource = tk.Frame(self)
        framesource.configure(pady=padding, bg='#1D243A')
        for i in range(columns):
            framesource.columnconfigure(i, weight=4)
        framesource.pack(side=tk.TOP, fill=tk.X)
        #LabelSource
        tk.Label(framesource, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='From where did you download the audio?'
                 ).grid(columnspan=columns, sticky='EW', pady=(0,8))
        self.source.set('art19')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=0, justify=tk.LEFT, width=13,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='Art19/Podcast Feed', var=self.source, value='art19'
                       ).grid(row=1, column=0, sticky='NEWS')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=4, justify=tk.LEFT,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='YouTube', var=self.source, value='yt'
                       ).grid(row=1, column=1, sticky='NEWS')

        #############
        ## SPEAKER ##
        framespeaker = tk.Frame(self)
        framespeaker.configure(pady=padding, bg='#1D243A')
        framespeaker.columnconfigure(1, weight=1)
        framespeaker.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(framespeaker, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Who are the Speakers? (separate by comma)'
                 ).grid(columnspan=3, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(framespeaker, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=40,
                 highlightthickness=0, 
                 textvariable=self.speaker
                 ).grid(columnspan=2, row=1, sticky='NEWS', ipady=4)
        tk.Label(framespeaker, bg='#1D243A', bd=0, width=12).grid(column=2, row=1, sticky='NEWS')

        #############
        ## LENGTH ##
        framelength = tk.Frame(self)
        framelength.configure(pady=padding, bg='#1D243A')
        framelength.columnconfigure(2, weight=1)
        framelength.pack(side=tk.TOP, pady=(0,4), fill=tk.X)
        #LabelEpisode
        tk.Label(framelength, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Length of the Episode? (optional, first 30 are known to program)'
                 ).grid(columnspan=3, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(framelength, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=8,
                 highlightthickness=0, 
                 textvariable=self.length
                 ).grid(column=1, row=1, sticky='NEWS', ipady=4)

        ############
        ## SUBMIT ##
        #ButtonSubmit
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
            for e in reversed(EPISODES):
                if e in self.filename or str(int(e)) in self.filename:
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
        vtt=False
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
        if '.vtt' in self.filename[-9:]:
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

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
class MainProgram():
    def __init__(self, filepath, filename, episodeNr, source, service, speaker, length=None, output=None):
        self.filepath, self.filename, self.source   = filepath, filename, source
        self.service, self.length, self.output      = service, length, output
        self.speaker                                = speaker

        try:
            self.episodeNr = int(episodeNr) # I checked above, but you never know...
        except:
            self.episodeNr = 0
            
        if self.output is None or self.output == '':
            self.output = self.filepath
            
        if self.episodeNr <= CURRENT and self.episodeNr > 0: # fill everything out if it's in the archives
            if len(speaker) < len(SPEAKER[self.episodeNr]): # not '<=' to give custom names and abbreviations a chance
                self.speaker = SPEAKER[self.episodeNr]
            self.length = LENGTHS[self.episodeNr]

        with open('/'.join((filepath, filename)), 'r') as file:
            rawlines = [line for line in file]
        rawtext = ''.join(rawlines)
        rawlines= []
                
        tokens = []
        if('vtt' in filename.rsplit('.', 1)):
            tokens = self.parse_vtt(rawtext)
        elif('descript' in service.lower()):
            tokens = self.parse_descript((rawtext.split('[', 1))[1:], self.speaker)
        elif('otter' in service.lower()):
            tokens = self.parse_otter(rawtext.rsplit('Transcribed by https://otter.ai',1)[0])
        else:
            assert False, 'Wrong source, please choose art19 or youtube.'
        rawtext = ''
        
        #self.save_as_srt(tokens)
        self.save_as_vtt(tokens)
        self.save_as_wiki(tokens)
        
    def parse_vtt(self, rawtext):
        tokens = []
        time, currentspeaker, content = '', '', ''

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
                if len(content) > 1:
                    content = ' '.join((content, line.strip())) # additional spoken words for the current timestamp
                else:
                    content = ''.join((content, line.strip()))
            if note: # it's a comment/NOTE
                if not 'www.descript.com' in content:
                    tokens.append(list((1, '', '', content))) # 0 means NOTE, will be decoded in the save_as_vtte method
            else: # not a NOTE, actual cue
                if '<v' in content[:3]: # already tagged
                    content = content.strip()
                    content = content[3:]
                    currentspeaker, content = tuple(content.split('>', 1))
                else: # old format
                    if ':' in content[:32]:
                        currentspeaker, content = tuple(content.split(': ', 1))
                for S in SPEAKER[self.episodeNr]:
                    if currentspeaker in S:
                        currentspeaker = S
                tokens.append(list((0, currentspeaker, time, content)))
        return tokens

    ## TODO: cleanup, verify this
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
            tokens.append(0, splittext) # token contains time and text

        newtokens = self.make_timestamps(tokens)
        
        tokengen2 = (token for token in newtokens)
        finaltokens = []
        currentspeaker = next(tokengen2)[2] # always starts with Eric
        Speaker = [s+':' for s in people] # format the folks to fit the file

        for token in tokengen2:
            found = False
            for sp in Speaker:
                if sp in token[2]:
                    currentspeaker = token[2]
                    found = True
                    break
            if not found:
                finaltokens.append([0,currentspeaker, token[1], token[2]])
        return finaltokens

    def parse_otter(self, rawtext):
        tokens = []
        currentspeaker = ''
        blockgen = (x for x in rawtext.split('\n\n')) # makes a 'generator' out of the list
        for block in blockgen:
            lines = block.split('\n',1)
            lines[0] = lines[0].strip()
            if len(lines[0]) < 4:
                break
            currentspeaker, time = lines[0].split('  ')
            if len(time) < 7: ## e.g. 10:35 instead of 00:10:35
                if len(time) == 4:
                    time = ''.join(('00:0', time)) # for the first 10 seconds, e.g. 0:01
                else:
                    time = ''.join(('00:', time))
            elif len(time) == 7:
                time     = ''.join(('0', time)) # for 1:20:41 , makes it 01:20:41
            
            tokens.append(list((0, currentspeaker, time, lines[1])))
        return self.make_timestamps(tokens)
    
    def make_timestamps(self, tokens):
        tokengen = (t for t in tokens)
        prevtoken = next(tokengen)
        newtokens = []
        for token in tokengen:
            newtokens.append(    [0, prevtoken[1], ''.join((prevtoken[2], '.000', ' --> ', token[2], '.000')), prevtoken[3]])
            prevtoken = token
        # there is now only the last token left, that's where the LENGTH of the episode comes into play
        try: # I saved most episode lengths in a list below
            newtokens.append(    [0, prevtoken[1], ''.join((prevtoken[2], '.000', ' --> ', LENGTHS[self.episodeNr], '.000')), prevtoken[3]])
        except: # default
            try:
                newtokens.append([0, prevtoken[1], ''.join((prevtoken[2], '.000', ' --> ', self.length, '.000')), prevtoken[3]])
            except:
                newtokens.append([0, prevtoken[1], ''.join((prevtoken[2], '.000', ' --> ', '9:00:00', '.000')), prevtoken[3]])
        return newtokens
    
    ######################################################################################################################################################

    ## vtt file, specification-compliant
    def save_as_vtt(self, tokens):
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr != 0 else self.filename
        filename = ''.join((filename, '_', self.source.lower())) if self.source is not None else filename
        if self.filename[:-4] == filename:
            ''.join((filename, '(1)'))
        with open(''.join((self.output, '/', filename, '.vtt')), 'w') as file:
            file.write('WEBVTT\n\n')
            for token in tokens:
                if token[0] == 1:
                    file.write(f'NOTE\n{token[3]}\n\n')
                else:
                    file.write(f'{token[2]}\n<v {token[1]}>{token[3]}\n\n')
                
    ## srt file, specification-compliant
    def save_as_srt(self, tokens):
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr != 0 else self.filename
        filename = ''.join((filename, '_', self.source.lower())) if self.source is not None else filename
        if self.filename[:-4] == filename:
            ''.join((filename, '(1)'))
        with open(''.join((self.output, '/', filename, '.srt')), 'w') as file:
            i = 0
            currentspeaker = ''
            for token in tokens:
                if token[0] == 1:
                    continue
                preamble = ''
                if not token[1] == currentspeaker: # different speaker? new headline
                    preamble = f'{currentspeaker}: '
                i += 1
                file.write(f'{i}\n{token[2]}\n{preamble}{token[3]}\n\n')

    ## wiki markup
    def save_as_wiki(self, tokens):
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr != 0 else self.filename
        with open(''.join((self.output, '/', filename, '_wiki.txt')), 'w') as file:
            currentspeaker = ''
            for token in tokens:
                if token[0] == 1:
                    continue
                if 'STARTAD' in token[3][:10]:
                    file.write('\n\n\'\'\'AD\'\'\'')
                    token[3] = token[3].split('ENDAD', 1)[1]
                    currentspeaker = ''
                    if len(token[2]) <4:
                        continue
                time = token[2].split(' --> ')[0][:-4]
                if not token[0] == currentspeaker: # different speaker? new headline
                    file.write(f'\n\'\'\'[{time}] {token[1]}:\'\'\' ')
                file.write(f'<span title=\"{time}\">{token[3]}</span>')
                
###############################################################################################################################################################################################
## all episode lengths up to EP30
CURRENT = 30
EPISODES= [str(e).zfill(2) for e in range(0,CURRENT+1)]; EPISODES.pop(19)
LENGTHS = ['0:01:34', #0
	'02:52:35', 
	'00:28:33', 
	'01:21:31', 
	'02:45:48', 
	'01:51:21', 
	'02:01:59', 
	'02:01:16', 
	'01:08:49', 
	'02:19:36', 
	'01:43:27', #10
	'02:38:59', 
	'01:35:46', 
	'01:38:20', 
	'01:06:39', 
	'01:50:54', 
	'02:18:17', 
	'02:20:04', 
	'01:07:58', 
	'02:18:33', 
	'02:23:04', #20
	'01:52:50', 
	'01:10:39', 
	'02:11:03', 
	'01:55:20', 
	'01:09:33', 
	'02:29:56', 
	'03:38:06', 
	'02:05:43', 
	'02:03:49', 
	'02:37:03'  #30
	]
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
