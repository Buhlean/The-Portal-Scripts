###############################################################################################################################################################################################
## Change these to the desired values and Run the script.
## FILEPATH is relative to the script or absolute, your choice.
###############################################################################################################################################################################################

FILEPATH = 'C:\\Users\\Alex\\Documents\\Python Projects\\PORTAL\EP21\\'
FILENAME = 'Ep_21_art19.vtt'

## Format: 'hh:mm:ss --> hh:mm:ss' (as many times a s needed, seperated by comma)
## Example: AD_OCCURRENCES = ['00:00:00 --> 00:05:00', '01:55:00 --> 01:57:36']
AD_OCCURRENCES = ['00:00:00 --> 00:05:00', '01:55:00 --> 01:57:36']

## Choose one:
ACTION = 'REMOVE'
#ACTION = 'INSERT'

###############################################################################################################################################################################################
def parse_vtt(rawtext, ad_times):
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
        if len(time) > 20:
            its_an_ad, time = adjust_time(time, ad_times)
            if its_an_ad:
                note = True
                content = ';'.join((time, content))
        if note: # it's a comment/NOTE
            tokens.append(list((0, '', '', content))) # 0 means NOTE, will be decoded in the save_as_vtte method
        else: # not a NOTE, actual cue
            if '<v' in content[:3]: # already tagged
                tokens.append(list((1, currentspeaker, time, content)))
            else: # old format
                tokens.append(list((2, currentspeaker, time, content)))
    return tokens

###############################################################################################################################################################################################
## vtt file, specification-compliant
def save_as_vtt(tokens):
    name, ext = tuple(FILENAME.rsplit('.', 1)) # seperate extension from name with 'split at dot from the right once'
    if ACTION == 'REMOVE':
        filename = ''.join((name, '_without_ads.', ext))
    if ACTION == 'INSERT':
        filename = ''.join((name, '_added_ads.', ext))
    with open(FILEPATH+filename, 'w') as file:
        file.write('\nWEBVTT\n\n')
        for token in tokens:
            if token[0] == 0:
                file.write(f'NOTE\n{token[3]}\n\n')
            if token[0] == 1:
                file.write(f'{token[2]}\n{token[1]}{token[3]}\n\n')
            if token[0] == 2:
                file.write(f'{token[2]}\n<v {token[1]}>{token[3]}\n\n')
                
def adjust_time(time, ad_times):
    found_an_ad = False
    stamps = time.split(' --> ')
    start = deconstruct_and_convert(stamps[0])
    end   = deconstruct_and_convert(stamps[1])
    for ad_start, ad_end, duration in ad_times: # given as parameter calculated from the user defined constant at the top of the file
        if ACTION == 'REMOVE':
            if start >= ad_start and end <= ad_end: # it's an ad, send emssage to rem it out
                found_an_ad = True
                break
            elif start >= ad_end: # we are after an ad, we need to now substract/add time
                start -= duration # for each ad,
                end -= duration # we shift the time
        if ACTION == 'INSERT':
            if start >= ad_start: # if we start after an ad - any ad - add its duration
                start += duration
                end += duration
    return ( found_an_ad, ' --> '.join((to_time(start),  to_time(end))) ) #pack it into a neat timestamp again
    
def to_milliseconds(time):
    return ((( int(time[0]) ) *60 +int(time[1]) ) *60 +int(time[2]) ) *1000 +int(time[3])
def to_time(milliseconds):
    milli   = milliseconds  % 1000
    seconds = milliseconds // 1000
    return '.'.join((':'.join((str(seconds//3600).zfill(2), str((seconds%3600)//60).zfill(2), str( (seconds%3600)%60 ).zfill(2) )), str(milli) ))
def deconstruct_and_convert(stamp):
    partial_split = stamp.split(':')
    four_components = partial_split[:2]
    four_components.extend((partial_split[2]).split('.'))
    return to_milliseconds(four_components)
###############################################################################################################################################################################################

def main():
    ad_timings = []
    for ad in AD_OCCURRENCES:
        both = ad.split(' --> ')
        both = ['.'.join((b, '000')) for b in both if len(b) < 9]
        start = deconstruct_and_convert(both[0])
        end   = deconstruct_and_convert(both[1])
        diff = end-start
        ad_timings.append([start, end, diff])
    with open(FILEPATH+FILENAME, 'r') as file:
        rawlines = [line for line in file]
    rawtext = ''.join(rawlines)
    save_as_vtt(parse_vtt(rawtext, ad_timings))

assert FILENAME[-4:] == '.vtt', 'Only VTT files allowed in here!'
if __name__ == '__main__':
    main()


