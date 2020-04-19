###############################################################################################################################################################################################
##
## This script parses VTT and Descript/Otter txt files
## into machine-readable vtt, srt and markup files.
## Please set the parameters in the section at the top to suit your needs.
##
###############################################################################################################################################################################################

FILEPATH = 'C:\\podcasts\\EP01\\'
FILENAME = '01_Peter_Thiel.vtt'
EPISODE = 1
SPEAKER = ['Eric Weinstein', 'Peter Thiel']
LENGTH = '1:03:54' # without milliseconds, please

## Info: '#' means ignore this line
## Choose one:
SOURCE = 'art19'
#SOURCE = 'youtube'

## Choose one:
SERVICE = 'Descript'
#SERVICE = 'Otter'

###############################################################################################################################################################################################
##
## Now save the script
## and double-click it in the file explorer or use the terminal
## (Python 3.x has to be installed on the system)
## see Python.org/downloads for latest release
##
###############################################################################################################################################################################################






def main():
    with open(FILEPATH+FILENAME, 'r') as file:
        rawlines = [line for line in file]
    rawtext = ''.join(rawlines)
    speaker = [(name.rsplit(' ', 1))[1] for name in SPEAKER]
    tokens = []
    tokenlist = []

    if True:
        if('vtt' in FILENAME.rsplit('.', 1)):
            tokens = parse_vtt(rawtext, speaker)
        elif('descript' in SERVICE.lower()):
            title, cleanedtext = (lambda x: (x[0], x[1:]))(rawtext.split('[', 1))
            tokens = parse_descript(cleanedtext, speaker)
        elif('otter' in SERVICE.lower()):
            tokens = parse_otter(rawtext, speaker)
        else:
            assert False, 'Wrong source, please choose art19 or youtube or wiki.'
            
    save_as_srt(tokens)
    save_as_vtt(tokens)
    save_as_wiki(tokens)

###############################################################################################################################################################################################
def parse_vtt(rawtext, speaker):
    tokens = []
    time = ''
    currentspeaker = ''
    content = ''
    skip = False
    
    for block in rawtext.split('\n\n'):
        skip = False
        content = ''
        for line in block.split('\n'):
            if len(line) == 0:
                skip = True
                continue # next line
            if 'NOTE' in line:
                skip = True
                break # next block
            if 'WEBVTT' in line:
                skip =  True
                break # next block
            if ':' in line:
                skip = False
                if '-->' in line: # found a timestamp
                    time = line # save it
                    continue # theres nothing else here
                if speaker[0] in line: # found a name
                    currentspeaker = SPEAKER[0] # save the name
                    splitline = line.split(': ')
                    if len(splitline)>1:
                        content = splitline[1]+' ' # and the spoken word
                elif speaker[1] in line:
                    currentspeaker = SPEAKER[1]
                    splitline = line.split(': ')
                    if len(splitline)>1:
                        content = splitline[1]+' '
            else:
                content = ''.join((content, line)) # additional spoken words for the current timestamp
        if not skip:
            tokens.append(list((currentspeaker, time, content)))
    return tokens

def parse_descript(text, people):
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
        newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTHS[EPISODE], '.000')), prevtoken[2]])
    except: # default
        try:
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTH, '.000')), prevtoken[2]])
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

def parse_otter(rawtext, speaker):
    tokens = []
    currentspeaker = 'Weinstein'
    linegen = (x for x in rawtext.split('\n')) # makes a 'generator' out of the list
    # so that I can call next() on it from within the loop. very helpful here
    for line in linegen:
        if len(line) == 0:
            continue
        if speaker[0] in line:
            currentspeaker = SPEAKER[0]
            time = line.split('  ')[1]
        elif speaker[1] in line:
            currentspeaker = SPEAKER[1]
            time = line.split('  ')[1]
        else:
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
        newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTHS[EPISODE], '.000')), prevtoken[2]])
    except: # default
        try:
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', LENGTH, '.000')), prevtoken[2]])
        except:
            newtokens.append([prevtoken[0], ''.join((prevtoken[1], '.000', ' --> ', '9:00:00', '.000')), prevtoken[2]])
    return newtokens

###############################################################################################################################################################################################
## vtt file, specification-compliant
def save_as_vtt(tokens):
    filename = ''.join(('Ep_', str(EPISODE), '_', SOURCE.lower(), '.vtt'))
    with open(FILEPATH+filename, 'w') as file:
        file.write('\nWEBVTT\n\n')
        for token in tokens:
            file.write(f'{token[1]}\n<v {token[0]}>{token[2]}\n\n')
        
## srt file, specification-compliant
def save_as_srt(tokens, source=None):
    filename = ''.join(('Ep_', str(EPISODE), '_', SOURCE.lower(), '.srt'))
    with open(FILEPATH+filename, 'w') as file:
        i = 0
        currentspeaker = ''
        for token in tokens:
            if token[0] == currentspeaker: # still the same speaker? 
                preamble = ''
            else: # only print speaker name if it changed since last sentence
                currentspeaker = token[0]
                preamble = f'{currentspeaker}: '
            i += 1
            file.write(f'{i}\n{token[1]}\n{preamble}{token[2]}\n\n')

## wiki markup
def save_as_wiki(tokens):
    with open(''.join((FILEPATH, 'Ep_', str(EPISODE), '_', SOURCE.lower(), '_wiki', '.txt')), 'w') as file:
        currentspeaker = ''
        for token in tokens:
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

############################################################################################################################################################################
def Check_the_first_few_lines_and_assign_everything_a_value_please():
    assert FILEPATH
    assert FILENAME
    assert EPISODE
    assert SPEAKER
    try:
        SOURCE
    except:
        SOURCE = 'art19'
    try:
        SERVICE
    except:
        SERVICE = 'vtt'

## all episode lengths up to EP30
LENGTHS = ['0:01:34', '02:52:35', '00:28:33', '01:21:31', '02:45:48', '01:51:21', '02:01:59', '02:01:16', '01:08:49', '02:19:36', '01:43:27', '02:38:59', '01:35:46', '01:38:20', '01:06:39', '01:50:54', '02:18:17', '02:20:04', '01:07:58', '02:18:33', '02:23:04', '01:52:50', '01:10:39', '02:11:03', '01:55:20', '01:09:33', '02:29:56', '03:38:06', '02:05:43', '02:03:49', '02:37:03']

if __name__ == '__main__':
    # named that way because it shows up in the error message
    # since I couldn't figure out how to check if a variable exists...
    Check_the_first_few_lines_and_assign_everything_a_value_please()
    
    main()
