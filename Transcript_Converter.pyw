## Tour guide:
## first, the GUI
## then, the parser area
## then saving the generated tokens
## lastly, the archives of all episode data for the program to draw from.
## Enjoy your stay!
__author__ = 'Buhlean'

import tkinter as tk
from tkinter import filedialog

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Universal Transcript Converter')
        self.configure(bg='#1D243A')
        self.geometry('580x580+40+40')
        self.resizable(True, True)
        self.app = App(self)
        self.bind('<Return>',   self.app.convert)
        self.bind('<Escape>',   (lambda s: self.destroy()) ) # destroy takes 1 argument (self), this lambda deletes the second (event). kind of a hack, not bad enough for me to care...
        self.bind('<Control-o>',  self.app.openfile)
        self.bind('<Control-KeyPress-f>',  self.app.episode_fill)
      
class App(tk.Frame):
    def __init__(self, root):
        super().__init__(bg='#1D243A', bd=0, relief=tk.GROOVE, padx=20, pady=20)
        self.path, self.outpath, self.episodeNr, self.source    = tk.StringVar(self, 'C:/'), tk.StringVar(self, 'C:/'), tk.StringVar(self, 0), tk.StringVar(self, '')
        self.service, self.speaker, self.length, self.error     = tk.StringVar(self, ''), tk.StringVar(self, 'Eric Weinstein'), tk.StringVar(self, '00:00:00'), tk.StringVar(self, '')
        self.special                                            = tk.StringVar(self, '')
        self.filepath, self.filename = '', ''

        self.pack(side="top", fill="both", expand=True)
        
        # last line:
        self.drawGUI()

    def drawGUI(self):
        self.padding = 6
        self.columns = 6
        self.drawfile()
        self.drawepisode()
        self.drawoutput()
        self.drawservice()
        self.drawsource()
        self.drawspeaker()
        self.drawlength()
        self.drawother()

    def drawfile(self):    
        framefile = tk.Frame(self)
        framefile.configure(pady=self.padding, bg='#1D243A')
        framefile.columnconfigure(1, weight=1)
        framefile.pack(side=tk.TOP, fill=tk.X)
        #LabelFile
        tk.Label(framefile, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff',
                 justify=tk.LEFT, text='Location of transcript file'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryFile
        tk.Entry(framefile, bg='#111111', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT,
                 highlightthickness=0, textvariable=self.path
                 ).grid(column=1, row=1, sticky='NEWS')
        #ButtonFile
        tk.Button(framefile, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e', command=self.openfile, fg='#ffffff',
                  font=("Helvetica", "13"), padx=0, pady=0, highlightcolor='#eaff68', relief=tk.RAISED, text='Open...', width=9
                  ).grid(column=3, row=1, sticky='EW')
    def drawepisode(self):
        frameepisode = tk.Frame(self)
        frameepisode.configure(pady=self.padding, bg='#1D243A')
        frameepisode.columnconfigure(3, weight=1)
        frameepisode.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(frameepisode, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff',
                 justify=tk.LEFT, text='Which Episode is this from? (optional)'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(frameepisode, bg='#111111', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT,
                 width=4, highlightthickness=0, textvariable=self.episodeNr
                 ).grid(column=1, row=1, sticky='NEWS') # episode
        tk.Label(frameepisode, anchor='s', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff',
                 justify=tk.CENTER, text='or', padx=12, pady=4,
                 ).grid(column=2, row=1, sticky='NEWS', pady=(3,0)) # or
        self.special.set('choose Special Episode')
        choice=tk.Menubutton(frameepisode, activebackground='#7a7e8f', activeforeground='#111111', bd=1, bg='#111111', justify=tk.LEFT, anchor='w',
                             fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0, highlightcolor='#eaff68', relief=tk.RAISED, textvariable=self.special)
        choice.grid(column=3, row=1, sticky='EW', padx=(0,8), ipady=4) # special episode
        choice.menu = tk.Menu(choice, tearoff=0, activebackground='#7a7e8f', activeforeground='#eaff68', bd=0, bg='#1D243A', fg='#ffffff', font=("Helvetica", "13"))
        choice['menu'] = choice.menu
        for ex in EXTERNAL.keys():
            choice.menu.add_radiobutton(label=ex, variable=self.special, value=ex, command=self.external)
        tk.Button(frameepisode, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e', command=self.episode_fill,
                  fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0, highlightcolor='#eaff68', relief=tk.RAISED, text='Fill in', width=9
                  ).grid(column=4, row=1, sticky='EW')
    def drawoutput(self):
        frameoutput = tk.Frame(self)
        frameoutput.configure(pady=self.padding, bg='#1D243A')
        frameoutput.columnconfigure(1, weight=1)
        frameoutput.pack(side=tk.TOP, fill=tk.X)
        #LabelOutput
        tk.Label(frameoutput, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff',
                 justify=tk.LEFT, text='Where should the output go? (optional)'
                 ).grid(columnspan=5, sticky='NEWS', pady=(0,8))
        #EntryOutput
        tk.Entry(frameoutput, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, 
                 highlightthickness=0,
                 textvariable=self.outpath
                 ).grid(column=1, row=1, sticky='NEWS')
        #ButtonOutput
        tk.Button(frameoutput, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e', command=self.getsaveplace,
                  fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0, highlightcolor='#eaff68', relief=tk.RAISED, text='Choose...', width=9
                  ).grid(column=3, row=1, sticky='EW')
    def drawservice(self):
        frameservice = tk.Frame(self)
        frameservice.configure(pady=self.padding, bg='#1D243A')
        for i in range(self.columns):
            frameservice.columnconfigure(i, weight=4)
        frameservice.pack(side=tk.TOP, fill=tk.X)
        #LabelService
        tk.Label(frameservice, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='From where did you export the transcript? (optional for .vtt)'
                 ).grid(columnspan=self.columns, sticky='NEWS', pady=(0,8))
        self.service.set('Descript')
        #RadioDescript
        tk.Radiobutton(frameservice, anchor='nw', font=("Helvetica", "13"), bd=0, pady=0, padx=0, justify=tk.LEFT, width=13,  bg='#1D243A', fg='#ffffff',
                       selectcolor='#1D243A', activebackground='#1D243A', activeforeground='#7a7e8f', text='Descript', var=self.service, value='Descript'
                       ).grid(row=1, column=0, sticky='NEWS')
        tk.Radiobutton(frameservice, anchor='nw', font=("Helvetica", "13"), bd=0, pady=0, padx=0, justify=tk.LEFT, bg='#1D243A', fg='#ffffff',
                       selectcolor='#1D243A', activebackground='#1D243A', activeforeground='#7a7e8f', text='Otter.ai', var=self.service, value='Otter'
                       ).grid(row=1, column=1, sticky='NEWS')
    def drawsource(self):
        framesource = tk.Frame(self)
        framesource.configure(pady=self.padding, bg='#1D243A')
        for i in range(self.columns):
            framesource.columnconfigure(i, weight=4)
        framesource.pack(side=tk.TOP, fill=tk.X)
        #LabelSource
        tk.Label(framesource, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='From where did you download the audio?'
                 ).grid(columnspan=self.columns, sticky='EW', pady=(0,8))
        self.source.set('art19')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), bd=0, pady=0, padx=0, justify=tk.LEFT, width=13, bg='#1D243A', fg='#ffffff',
                       selectcolor='#1D243A', activebackground='#1D243A', activeforeground='#7a7e8f', text='Art19/Podcast Feed', var=self.source, value='art19'
                       ).grid(row=1, column=0, sticky='NEWS')
        tk.Radiobutton(framesource, anchor='nw', font=("Helvetica", "13"), 
                       bd=0, pady=0, padx=4, justify=tk.LEFT,
                       bg='#1D243A', fg='#ffffff', selectcolor='#1D243A',
                       activebackground='#1D243A', activeforeground='#7a7e8f',
                       text='YouTube', var=self.source, value='yt'
                       ).grid(row=1, column=1, sticky='NEWS')
    def drawspeaker(self):
        framespeaker = tk.Frame(self)
        framespeaker.configure(pady=self.padding, bg='#1D243A')
        framespeaker.columnconfigure(1, weight=1)
        framespeaker.pack(side=tk.TOP, fill=tk.X)
        #LabelEpisode
        tk.Label(framespeaker, anchor='nw', bg='#1D243A', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT,
                 text='Who are the Speakers? (separate by comma)'
                 ).grid(columnspan=3, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(framespeaker, bg='#111111', font=("Helvetica", "13"), bd=0, fg='#ffffff', justify=tk.LEFT, width=40, highlightthickness=0,
                 textvariable=self.speaker
                 ).grid(columnspan=2, row=1, sticky='NEWS', ipady=4)
        tk.Label(framespeaker, bg='#1D243A', bd=0, width=12).grid(column=2, row=1, sticky='NEWS') # emulates button
    def drawlength(self):
        framelength = tk.Frame(self)
        framelength.configure(pady=self.padding, bg='#1D243A')
        framelength.columnconfigure(2, weight=1)
        framelength.pack(side=tk.TOP, pady=(0,4), fill=tk.X)
        #LabelEpisode
        tk.Label(framelength, anchor='nw', bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT,
                 text=f'Length of the Episode? (optional, first {CURRENT-1} are known to program)'
                 ).grid(columnspan=3, sticky='NEWS', pady=(0,8))
        #EntryEpisode
        tk.Entry(framelength, bg='#111111', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', justify=tk.LEFT, width=8,
                 highlightthickness=0, 
                 textvariable=self.length
                 ).grid(column=1, row=1, sticky='NEWS', ipady=4)
    def drawother(self):
        tk.Button(self, activebackground='#7a7e8f', activeforeground='#eaff68', bd=1, bg='#3b3f4e',
                  command=self.convert, fg='#ffffff', font=("Helvetica", "13"), padx=0, pady=0,
                  highlightcolor='#eaff68', relief=tk.RAISED, text='Convert', width=9
                  ).pack(side=tk.RIGHT) #ButtonSubmit
        tk.Label(self, bg='#1D243A', font=("Helvetica", "13"),
                 bd=0, fg='#ffffff', padx=8, textvariable=self.error).pack(side=tk.RIGHT)

    def episode_fill(self, e=None): # e is for events, makes it callable with key shortcuts (kind of a hack?)
        self.error.set('')
        self.special.set('choose Special Episode')
        try:
            int(self.episodeNr.get())
        except:
            self.error.set('Episode Number must be Number')
            return
        try:
            s, l = INTERNAL[str(self.episodeNr.get()).zfill(2)] # I have saved all of this information at the end of the file for convenience...
            self.length.set(l)
            self.speaker.set(', '.join(s))
        except:
            self.length.set('')
            self.speaker.set('Eric Weinstein')
            self.error.set('Not found, provide information manually, please')
    def openfile(self, e=None):
        self.error.set('')
        self.path.set(filedialog.askopenfilename())
        if '/' in self.path.get():
            self.filepath, self.filename = tuple(self.path.get().rsplit('/', 1))
            for e in EPISODES:
                if e in self.filename or str(int(e)) in self.filename:
                    self.episodeNr.set(e)
                    s, l = INTERNAL[str(self.episodeNr.get()).zfill(2)] # see above in episode_fill
                    self.length.set(l)
                    self.speaker.set(', '.join(s))
                    break
            if self.outpath.get() == 'C:/' or self.outpath.get() == '':
                self.outpath.set(self.filepath)
    def getsaveplace(self, e=None):
        self.error.set('')
        self.outpath.set(filedialog.askdirectory())
    def external(self):
        self.error.set('')
        self.episodeNr.set('')
        s, l = EXTERNAL[self.special.get()] # again, I have saved all of this, too
        self.length.set(l)
        self.speaker.set(', '.join(s))
    def convert(self, e=None):
        vtt=False
        if '/' in self.path.get():
            self.filepath, self.filename = tuple(self.path.get().rsplit('/', 1))
        else:
            self.error.set('Please specify a valid input path and file')
        if '00:00:00' in self.length.get():
            length = None
        elif len(self.length.get()) < 4:
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
        if 'choose' in self.special.get():
            try:
                int(self.episodeNr.get())
            except:
                self.error.set('Episode Number must be Number')
                return
            if not int(self.episodeNr.get()) >= 0:
                self.error.set('Episode Number must be positive')
                return
        else:
            self.episodeNr.set('-1')
        if not vtt and not 'Otter' in self.service.get() and not len(self.speaker.get()) > 1:
            self.error.set('No speakers were given, please write at least Eric Weinstein in')
            return
        MainProgram(self.filepath, self.filename,
                    self.episodeNr.get(), self.source.get(),
                    self.service.get(), self.speaker.get(),
                    self.special.get(), length, self.outpath.get())
        self.error.set('Success!')    

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
class MainProgram():
    def __init__(self, filepath, filename, episodeNr, source, service, speaker, special, length=None, output=None):
        self.filepath, self.filename, self.source   = filepath, filename, source
        self.service, self.length, self.output      = service, length, output
        self.speaker, self.special                  = speaker, special

        try:
            self.episodeNr = int(episodeNr) # I checked above, but you never know...
        except:
            self.episodeNr = 0
            
        if self.output is None or self.output == '':
            self.output = self.filepath

        if self.episodeNr == -1:
            self.filename = '_'.join(self.special.split(' '))
        if self.episodeNr <= CURRENT and self.episodeNr > 0: # fill everything out if it's in the archives
            speakers, length = INTERNAL[str(self.episodeNr).zfill(2)] # I have saved all of this information at the end of the file for convenience...
            if len(speaker) < len(speakers): # not '<=' to give custom names and abbreviations a chance
                self.speaker = speakers
            self.length = length
        if self.length is None:
            self.length = '09:00:00' # emergency value, I would have to guess either way

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
                    tokens.append(list((1, '', '', content))) # 1 means NOTE
            else: # not a NOTE, actual cue
                if '<v' in content[:3]: # already tagged
                    content = content.strip()
                    content = content[3:]
                    currentspeaker, content = tuple(content.split('>', 1))
                else: # old format
                    if ':' in content[:32]:
                        currentspeaker, content = tuple(content.split(': ', 1))
                for S in self.speaker:
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
        newtokens.append([0, prevtoken[1], ''.join((prevtoken[2], '.000', ' --> ', self.length, '.000')), prevtoken[3]])
        return newtokens
    
    ######################################################################################################################################################
    ## vtt file, specification-compliant
    def save_as_vtt(self, tokens):
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr > 0 else self.filename
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
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr > 0 else self.filename
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
        filename = ''.join(('Ep_', str(self.episodeNr))) if self.episodeNr > 0 else self.filename
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
## all episode inforamtion up to EP30
EXTERNAL = {'Geometric Unity':      (['Eric Weinstein'],                                                    '02:48:23'),
            'JRE #1022':            (['Eric Weinstein', 'Joe Rogan'],                                       '02:41:08'),
            'JRE #1203':            (['Eric Weinstein', 'Joe Rogan'],                                       '03:51:47'),
            'JRE #1320':            (['Eric Weinstein', 'Joe Rogan'],                                       '03:28:12'),
            'JRE #1453':            (['Eric Weinstein', 'Joe Rogan'],                                       '03:02:06'),
            'Lex Round 1':          (['Eric Weinstein', 'Lex Friedman'],                                    '01:21:56'),
            'Lex Round 2':          (['Eric Weinstein', 'Lex Friedman'],                                    '02:46:36'),
            'Rubin 2017':           (['Eric Weinstein', 'Dave Rubin'],                                      '01:40:25'),
            'Rubin 2018':           (['Eric Weinstein', 'Dave Rubin'],                                      '02:05:58'),
            'Rubin with Peterson':  (['Eric Weinstein', 'Dave Rubin', 'Jordan Peterson'],                   '02:11:44'),
            'Rubin with Shapiro':   (['Eric Weinstein', 'Dave Rubin', 'Jordan Peterson', 'Ben Shapiro'],    '00:56:33'),
            'Rubin with Bret':      (['Eric Weinstein', 'Dave Rubin', 'Bret Weinstein'],                    '02:47:44'),
            'Tim Ferriss 2016':     (['Eric Weinstein', 'Tim Ferriss'],                                     '01:40:25')
            }
INTERNAL = {'00': (['Eric Weinstein'],                              '00:01:34'),
            '01': (['Eric Weinstein', 'Peter Thiel'],               '02:52:35'),
            '02': (['Eric Weinstein'],                              '00:28:33'),
            '03': (['Eric Weinstein', 'Werner Herzog'],             '01:21:31'),
            '04': (['Eric Weinstein', 'Timur Kuran'],               '02:45:48'),
            '05': (['Eric Weinstein', 'Rabbi Wolpe'],               '01:51:21'),
            '06': (['Eric Weinstein', 'Jocko Willink'],             '02:01:59'),
            '07': (['Eric Weinstein', 'Bret Easton Ellis'],         '02:01:16'),
            '08': (['Eric Weinstein', 'Andrew Yang'],               '01:08:49'),
            '09': (['Eric Weinstein', 'Bryan Callen'],              '02:19:36'),
            '10': (['Eric Weinstein', 'Julie Lindendahl'],          '01:43:27'),
            '11': (['Eric Weinstein', 'Sam Harris'],                '02:38:59'),
            '12': (['Eric Weinstein', 'Vitalik Buterin'],           '01:35:46'),
            '13': (['Eric Weinstein', 'Garry Gasparov'],            '01:38:20'),
            '14': (['Eric Weinstein', 'London Tsai'],               '01:06:39'),
            '15': (['Eric Weinstein', 'Garrett Lisi'],              '01:50:54'),
            '16': (['Eric Weinstein', 'Tyler Cowen'],               '02:18:17'),
            '17': (['Eric Weinstein', 'Anna Khachiyan'],            '02:20:04'),
            '18': (['Eric Weinstein'],                              '01:07:58'),
            '19': (['Eric Weinstein', 'Bret Weinstein'],            '02:18:33'),
            '20': (['Eric Weinstein', 'Sir Roger Penrose'],         '02:23:04'),
            '21': (['Eric Weinstein', 'Ashley Mathews'],            '01:52:50'),
            '22': (['Eric Weinstein', 'Ben Greenfield'],            '01:10:39'),
            '23': (['Eric Weinstein', 'Agnes Collard'],             '02:11:03'),
            '24': (['Eric Weinstein', 'Kai Lenny'],                 '01:55:20'),
            '25': (['Eric Weinstein'],                              '01:09:33'),
            '26': (['Eric Weinstein', "James O'Keefe"],             '02:29:56'),
            '27': (['Eric Weinstein', 'Daniel Schmachtenberger'],   '03:38:06'),
            '28': (['Eric Weinstein', 'Eric Lewis'],                '02:05:43'),
            '29': (['Eric Weinstein', 'Jamie Metzl'],               '02:03:49'),
            '30': (['Eric Weinstein', 'Ross Douthat'],              '02:37:03'),
            '31': (['Eric Weinstein', 'Ryan Holiday'],              '02:26:59'),
            '32': (['Eric Weinstein', 'J. D. Vance'],               '02:18:08')
            }
EPISODES = sorted(INTERNAL.keys())
EPISODES.pop(19) # otherwise it would 'find' all art19 sourced episodes as episode 19...
EPISODES.reverse() # otherwise it would find '1' before '11' and so on
CURRENT = len(INTERNAL)

def main():
    root = Root()
    root.mainloop()

if __name__ == '__main__':
    main()
