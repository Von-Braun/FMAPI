import FMAPI_lib,sys

if len(sys.argv)>=2:
    
    if sys.argv[1]=='w':
        data = FMAPI_lib.convert_text_to_binary('On December 10, 2016, about 1215 eastern standard time, a privately owned and operated experimental amateur-built Lightning, N59JL, was substantially damaged when it impacted terrain while maneuvering in the traffic pattern at Franklin Municipal-John Beverly Rose Airport, Franklin, Virginia. The commercial pilot sustained minor injuries and the passenger sustained a serious injury. The airplane was operated under the provisions of 14 Code of Federal Regulations Part 91 as a personal, local flight. Visual meteorological conditions prevailed at the time and no flight plan was filed for the flight which was originating at the time of the accident.'.replace(' ','~'))
        FMAPI_lib.write_data_digital(data,1000,60,500,'test.wav')
    
    elif sys.argv[1]=='r':
        raw_binary=FMAPI_lib.read_data_digital('test.wav', 166, 8000, 4000, 3999, 1000,False,3,0)
        print FMAPI_lib.convert_binary_to_text(raw_binary)