import sys,struct,wave,math,pyaudio,re,os,imp,signal,win32api,ctypes,thread
from matplotlib.mlab import find
import numpy as np
#dependancies = numpy, pyaudio, win32api
start_byte='01111111110110'
end_byte='01111111110010'
pad='00000000000000'
start_byte_pad=(start_byte+pad)*15
end_byte_pad=(end_byte+pad)*15


# Load the DLL manually to ensure its handler gets
# set before our handler.
#basepath = imp.find_module('numpy')[1]
#ctypes.CDLL(os.path.join(basepath, 'core', 'libmmd.dll'))
#ctypes.CDLL(os.path.join(basepath, 'core', 'libifcoremd.dll'))

# Now set our handler for CTRL_C_EVENT. Other control event 
# types will chain to the next handler.
'''
def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
    if dwCtrlType == 0: # CTRL_C_EVENT
        hook_sigint()
        return 1 # don't chain to the next handler
    return 0 # chain to the next handler
'''
def signal_handler(signum, frame):
    print 'Connection Forcefully Terminated By Host!'
    sys.exit()

#win32api.SetConsoleCtrlHandler(handler, 1)
signal.signal(signal.SIGINT, signal_handler)

def Pitch(signal,RATE):
    signal = np.fromstring(signal, 'Int16');
    crossing = [math.copysign(1.0, s) for s in signal]
    index = find(np.diff(crossing));
    f0=round(len(index) *RATE /(2*np.prod(len(signal))))
    return f0;

def convert_text_to_binary(text):
    global start_byte_pad,end_byte_pad,pad
    Alphabet2code ={"A" : "0000000","B" : "0000001","C" : "0000010","D" : "0000011","E" : "0000100","F" : "0000101","G" : "0000110","H" : "0000111",
    "I" : "0001000","J" : "0001001","K" : "0001010","L" : "0001011","M" : "0001100","N" : "0001101","O" : "0001110","P" : "0001111","Q" : "0010000",
    "R" : "0010001","S" : "0010010","T" : "0010011","U" : "0010100","V" : "0010101","W" : "0010110","X" : "0010111","Y" : "0011000","Z" : "0011001",
    "a" : "0011010","b" : "0011011","c" : "0011100","d" : "0011101","e" : "0011110","f" : "0011111","g" : "0100000","h" : "0100001","i" : "0100010",
    "j" : "0100011","k" : "0100100","l" : "0100101","m" : "0100110","n" : "0100111","o" : "0101000","p" : "0101001","q" : "0101010","r" : "0101011",
    "s" : "0101100","t" : "0101101","u" : "0101110","v" : "0101111","w" : "0110000","x" : "0110001","y" : "0110010","z" : "0110011","0" : "0110100",
    "1" : "0110101","2" : "0110110","3" : "0110111","4" : "0111000","5" : "0111001","6" : "0111010","7" : "0111011","8" : "0111100","9" : "0111101",
    "+" : "0111110","/" : "0111111"}
    return_text = ''
    for charecter in text:
        try:
            return_text=return_text+Alphabet2code[charecter]
            #print Alphabet2code[charecter], charecter
        except:
            pass
    return_text = list(pad+start_byte_pad+return_text+end_byte_pad+pad)
    #print return_text
    for digit in range(0,len(return_text)):
        return_text[digit]=int(return_text[digit])
    #print return_text
    return return_text

def convert_binary_to_text(text):
    #text = '01010010101001010000001010101001010'
    text=text.replace('\n','')
    #print text
    code2Alphabet ={"0000000":"A" ,"0000001":"B","0000010":"C","0000011":"D","0000100":"E","0000101":"F","0000110":"G","0000111":"H","0001000":"I",
    "0001001":"J","0001010":"K","0001011":"L","0001100":"M","0001101":"N","0001110":"O","0001111":"P","0010000":"Q","0010001":"R","0010010":"S",
    "0010011":"T","0010100":"U","0010101":"V","0010110":"W","0010111":"X","0011000":"Y","0011001":"Z","0011010":"a","0011011":"b","0011100":"c",
    "0011101":"d","0011110":"e","0011111":"f","0100000":"g","0100001":"h","0100010":"i","0100011":"j","0100100":"k","0100101":"l","0100110":"m",
    "0100111":"n","0101000":"o","0101001":"p","0101010":"q","0101011":"r","0101100":"s","0101101":"t","0101110":"u","0101111":"v","0110000":"w",
    "0110001":"x","0110010":"y","0110011":"z","0110100":"0","0110101":"1","0110110":"2","0110111":"3","0111000":"4","0111001":"5","0111010":"6",
    "0111011":"7","0111100":"8","0111101":"9","0111110":"+","0111111":"/"}
    return_text= ''
    for i in range(0,len(text),7):
        #print text[i:i+7],
        #try:
        #    print code2Alphabet[text[i:i+7]]
        #except:
        #    print '~'

        try:
            return_text=return_text+code2Alphabet[text[i:i+7]]
        except:
            return_text=return_text+'~'
    return return_text

def write_data_digital(data, freq_carry, bitrate, freq_division, destination_file):
    #if destination_file is blank output to speaker
    N =len(data)       #how many bits to send
    Fc =  freq_carry      #simulate a carrier frequency of 1kHz
    Fbit =   bitrate   #simulated bitrate of data, lower = bits last longer
    Fdev = freq_division      #frequency deviation, make higher than bitrate
    A = 1           #transmitted signal amplitude
    Fs = 10000      #sampling frequency for the simulator, must be higher than twice the carrier frequency
    print 'Chunk size is:',Fs/Fbit
    def write2wav(list1):
        data_size = 30495 #15*N
        fname = destination_file
        frate = 44100.0  # framerate as a float
        amp = 64000.0     # multiplier for amplitude
        wav_file = wave.open(fname, "w")
        nchannels = 1
        sampwidth = 2
        framerate = int(frate)
        nframes = data_size
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, framerate, nframes,comptype, compname))
        count=0.0
        bufferer=1.0
        for s in list1: # write the audio frames to file
            percentage=round((count/float(len(list1)))*100,0)
            if percentage>bufferer: #after a change of 1.0% update screen
                bufferer=percentage+1.0 #after a change of 1.0% update screen
                print 'Sending Data To Unknown Client...',str(percentage)+'%\r',
            count+=1.0
            wav_file.writeframes(struct.pack('h', int((s)*amp/2)))
        wav_file.close()
    data_in = data[0:N]
    def write2stream(list1):
        data_size = 30495 #15*N
        frate = 44100.0  # framerate as a float
        amp = 64000.0     # multiplier for amplitude
        nchannels = 1
        sampwidth = 2
        framerate = int(frate)
        nframes = data_size
        comptype = "NONE"
        compname = "not compressed"
        p = pyaudio.PyAudio() # open stream
        stream = p.open(format = p.get_format_from_width(sampwidth),channels = nchannels,rate = framerate,output = True)
        count=0.0
        bufferer=1.0
        for s in list1: # write the audio frames to file
            percentage=round((count/float(len(list1)))*100,0)
            if percentage>bufferer: #after a change of 1.0% update screen
                bufferer=percentage+1.0 #after a change of 1.0% update screen
                print 'Sending Data To Unknown Client...',str(percentage)+'%\r',
            count+=1.0
            stream.write(struct.pack('h', int((s)*amp/2)))
        stream.close()
        p.terminate()

    #VCO
    t=[]
    count=0
    for i in range(0,int((float(N)/float(Fbit))/(1/float(Fs)))):
        t.append(count)
        count+=0.0001
    m=[] #extend the data_in to account for the bitrate and convert 0/1 to frequency
    count=0.0
    bufferer=1.0
    for bit in data_in:
        percentage=round((count/float(len(data_in)))*100,0)
        if percentage>bufferer:
            bufferer=percentage+1.0 #after a change of 1.0% update screen
            print 'Processing Data...',str(percentage)+'%\r',
        count+=1.0
        if bit == 0:
            for i in range(0,Fs/Fbit): 
                m.append(Fc+Fdev)
        else:
            for i in range(0,Fs/Fbit): 
                m.append(Fc-Fdev)
    if len(m)>len(t):
        t.append(count)
    print 'Processing Data... 100.0%  \nData Succesfully Processed\nSending Data To Unknown Client...\r',
    y=[] #calculate the output of the VCO
    def multiply_arrays(A,B):
        print len(A),len(B)
        temp_array=[]
        for i in range(0,len(A)):
          temp_array.append(A[i]*B[i])
        return temp_array
    def multiply_array_by_x(A,X):
        temp_array=[]
        for i in range(0,len(A)):
          temp_array.append(A[i]*X)
        return temp_array

    def multiply_array_by_cos(A):
        temp_array=[]
        for i in range(0,len(A)):
          temp_array.append(math.cos(A[i]))
        return temp_array

    y=multiply_array_by_cos(multiply_array_by_x(multiply_arrays(m,t),2*math.pi))

    if destination_file=='':
        write2stream(y)
    else:
        write2wav(y)   
    print 'Sending Data To Unknown Client... 100.0%\nConnection Terminated Normally!'


def read_data_digital(source_file, chunk, zero_max_freq, zero_min_freq, one_max_freq, one_min_freq, write_stream,visual,input_index): 
    global start_byte
    #if source_file is blank read from mic, input_index selects mic or windows
    # play stream and find the frequency of each chunk
    binary_data='' #to store the data
    max_buffer_size=8192
    revieve_message_printed=False
    
    p = pyaudio.PyAudio() # open strea
    if source_file=='':
        swidth = 2
        RATE = 44100
        CHANNEL_COUNT = 1 
        input_stream = p.open(format=pyaudio.paInt16, channels=CHANNEL_COUNT, rate=RATE, input=True, frames_per_buffer=chunk,input_device_index=input_index)
        data = input_stream.read(chunk)

    else:
        wf = wave.open(source_file, 'rb') # open up a wave
        swidth = wf.getsampwidth()
        RATE = wf.getframerate()
        CHANNEL_COUNT = wf.getnchannels()       
        data = wf.readframes(chunk)

    stream = p.open(format = p.get_format_from_width(swidth),channels = CHANNEL_COUNT,rate = RATE,output = True)
    #window = np.blackman(chunk) # use a Blackman window
    filtered_binary_start=-1
    filtered_binary_end=-1
    filtered_binary_locations_blacklist=[]
    byte_count=0 #allows for live printing
    print 'Listening for data...'
    while len(data) == chunk*swidth:
        if revieve_message_printed: byte_count+=1
        if write_stream: stream.write(data) # write data out to the audio stream
        #indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data))*window # unpack the data and times by the hamming window
        
            # find the frequency and output it
        thefreq=Pitch(data,RATE)
        freq_percentage = int(round((thefreq/10000)*40))
        if freq_percentage<0: freq_percentage=0
        if freq_percentage>80: freq_percentage=80
        if visual==1:
            print ('#'*freq_percentage)+(' '*(80-freq_percentage)),80-freq_percentage,freq_percentage,'\r',
        else:
            if visual!=2: print "The freq is %f Hz." % (thefreq),
        out_file=open('out.txt','r')
        file_data = out_file.read().split(',')
        out_file.close()
        out_file=open('out.txt','w')
        out_file.write(','.join(file_data[-999:])+','+str(freq_percentage))
        out_file.close()
        if zero_max_freq>thefreq>zero_min_freq:
            if visual==0: print 0
            binary_data=binary_data+'0'
        elif one_min_freq<thefreq<one_max_freq:
            if visual==0: print 1
            binary_data=binary_data+'1'
        else:
            if visual==0: print '~',binary_data[-1:]
            #binary_data=binary_data+binary_data[-1:]

        if len(binary_data)>max_buffer_size and filtered_binary_start==-1: #if buffer size exceeded, and we are not gathering data,erase binary text
            binary_data = binary_data[-len(start_byte):]
            #print 'buffer purged'
         
        if source_file=='':
            try:
                data = input_stream.read(chunk)
            except IOError:
                input_stream = p.open(format=pyaudio.paInt16, channels=CHANNEL_COUNT, rate=RATE, input=True, frames_per_buffer=chunk,input_device_index=input_index)
        else:
            data = wf.readframes(chunk)

        if byte_count==7:
            byte_count=0
            sys.stdout.write(convert_binary_to_text(binary_data[-7:]))
            sys.stdout.flush()

        if binary_data[-len(start_byte):]==start_byte:
            if len(binary_data)-len(start_byte) not in filtered_binary_locations_blacklist: #skip if in blacklist
                filtered_binary_start = len(binary_data)-len(start_byte)
                filtered_binary_locations_blacklist.append(len(binary_data)-len(start_byte))

        elif binary_data[-len(end_byte):]==end_byte:
            if len(binary_data)-len(end_byte) not in filtered_binary_locations_blacklist: #skip if in blacklist
                filtered_binary_end = len(binary_data)-len(end_byte)
                filtered_binary_locations_blacklist.append(len(binary_data)-len(end_byte))

        if filtered_binary_end!=-1:
            #print filtered_binary_locations
            revieve_message_printed=False
            raw_data = '0'+binary_data[filtered_binary_start+len(start_byte)+1:filtered_binary_end]
            print '\n'+('='*90)
            print 'Connection Terminated Normally!'
            binary_data='' #clear buffer after data recieved
            filtered_binary_locations=-1
            filtered_binary_locations_blacklist=[]
            byte_count=0
            return raw_data[14:]

        elif filtered_binary_start!=-1 and not revieve_message_printed: #prevent this from running more than once if sync byte found
            print 'Recieving Data From Unknown Client'
            print '='*90
            revieve_message_printed=True

    stream.close()
    p.terminate()
    print binary_data


if len(sys.argv)>=2:
    if sys.argv[1]=='w':
        data = convert_text_to_binary('On December 10, 2016, about 1215 eastern standard time, a privately owned and operated experimental amateur-built Lightning, N59JL, was substantially damaged when it impacted terrain while maneuvering in the traffic pattern at Franklin Municipal-John Beverly Rose Airport, Franklin, Virginia. The commercial pilot sustained minor injuries and the passenger sustained a serious injury. The airplane was operated under the provisions of 14 Code of Federal Regulations Part 91 as a personal, local flight. Visual meteorological conditions prevailed at the time and no flight plan was filed for the flight which was originating at the time of the accident.'.replace(' ','~'))

        write_data_digital(data,1000,60,500,'')
    
    elif sys.argv[1]=='r':
    
        raw_binary=read_data_digital('', 166, 8000, 4000, 3999, 1000,False,2,0)
    
        print convert_binary_to_text(raw_binary)





#no analog, output check before processing write
