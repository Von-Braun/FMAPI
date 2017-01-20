# What FMAPI Does
This program allows data to be transfered from one computer to another via:

* The audio jack

* A wav file

One computer listens while the other transmits data.

# File Descriptions

* example.py = an example of importing and using the library.

* FMAPI_lib.py = contains all the functons.

# Example Output

* listening

>Listening for data...

>Recieving Data From Unknown Client

>==============================================================-
OnDecember102016about1215easternstandardtimeaprivatelyownedandoperatedexperimentalamateurbuiltLightningN59JLwassubstantiallydamagedwhenitimpactedterrainwhilemaneuveringinthetrafficpatternatFranklinMunicipalJohnBeverlyRoseAirportFranklinVirginiaThecommercialpilotsustainedminorinjuriesandthepassengersustainedaseriousinjuryTheairplanewasoperatedundertheprovisionsof14CodeofFederalRegulationsPart91asapersonallocalflightVisualmeteorologicalconditionsprevailedatthetimeandnoflightplanwasfiledfortheflightwhichwasoriginatingatthetimeoftheaccident
================================================================-

>Connection Terminated Normally!

* transmitting

>Chunk size is: 166

>Processing Data... 100.0%

>Data Succesfully Processed

>Sending Data To Unknown Client... 100.0%

>Connection Terminated Normally!

# How To Use It

There are currently two main functions: write_data_digital and read_data_digital.

**write_data_digital(data, freq_carry, bitrate, freq_division, destination_file):**

* data = an array of intigers, either of 1's and 0's 

* freq_carry = the carrier frequency

* bitrate = bits transfered per second, higher = less time per bit, lower = more time per bit

* freq_division = added or subtracted to the carrier frequency to encode a 1 or a 0

* destination_file = if destination_file is blank output to speaker, else output to wav file named destination_file

**read_data_digital(source_file, chunk, zero_max_freq, zero_min_freq, one_max_freq, one_min_freq, write_stream,visual,input_index):**

* source_file = wav file or if source_file is blank read from mic

* chunk = chunk size

* zero_max_freq = max acceptable zero frequency

* zero_min_freq = min acceptable zero frequency

* one_max_freq = max acceptable one frequency

* one_min_freq = min acceptable one frequency

* write_stream = output detected frequency to speaker

* visual = format of outputing data. [0]print binary, [1]print graph, [2]print frequency, [3]print text

* input_index = selects mic(1) or windows(0)

**Other Functions**

* convert_text_to_binary = convert a string to a list of 1s and 0s.

* convert_binary_to_text =  convert a list of 1s and 0s to a string.

* Pitch = used in determining frequency

* signal_handler = handle a control C event


