import os
import sys
import numpy as np 
import pandas as pd
import json
import librosa
import scipy.io as sio
import scipy.io.wavfile
import glob
import io, struct
import chardet


# file_path = str(sys.argv[1])
file_path = "/Users/seojiwon/Desktop/sushi/new_cat_pw/cat_pow"

def save_answer_json(data):
    with open("file_path/{answer.json}", data) as jp:
        json.dump(data, jp)

def make_answer(file_path):
    pth = glob.glob(f"{file_path}/Q1/*.wav")
    # print(pth)
    return pth

def load_json_file(data_dir):
    with open(data_dir+'/answer.json', encoding= "utf-8") as json_data:
        data = json.load(json_data)
    return data

def get_duration(audio_path): 
    audio=wave.open(audio_path) 
    print(audio)
    frames=audio.getnframes() 
    rate=audio.getframerate() 
    duration=frames/float(rate) 
    return duration

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


# def read_file(path, num):
#     path = path + '/Q' + str(num)
#     file_lists = [path + '/' + item for item in os.listdir(path)]
#     return file_lists

def read_wav(file_list):
    durations = []
    this_chunk_datas = []
    for item in file_list:
        with io.open(item, 'rb') as fh:
            riff, size, fformat = struct.unpack('<4sl4s', fh.read(12)) # wav 파일의 가장 위에서부터 12byte read
            subchunk_offset = fh.tell()  # current pointer

            while subchunk_offset < size:  # 현재 pointer 위치가 파일 전체 크기보다 적을 경우 
                fh.seek(subchunk_offset) # 포인터 이동
                subchunk_id, subchunk_size = struct.unpack('<4sl', fh.read(8))  # 포인터 위치로부터 subchunk id와 크기를 읽어옴 

                if subchunk_id == b'fmt ': # chunk_id가 fmt인 경우
                    aformat, channels, samplerate, byterate, blockalign, bps = struct.unpack('HHIIHH', fh.read(16))
                    bitrate = (samplerate * channels * bps) / 8
                elif subchunk_id == b'data':
                    durations.append((subchunk_size/bitrate, 3)) # 파일 재생시간 계산
                elif subchunk_id == b'THIS':
                    this_data = fh.read(subchunk_size) # this chunk의 데이터 가져오기 
                    data_codec = chardet.detect(this_data)['encoding'] # this chunk의 encode 정보 가져오기 
                    # chardet는 문자열의 인코딩만 detecting 하는 모듈이기 때문에 문자열 외의 데이터는 encoding=None이 뜬다 
                    if data_codec != None: # data가 text인 경우
                        this_data_decoded = this_data.decode(data_codec) # 인코드 된 데이터를 텍스트 데이터로 디코딩 
                        
                    else: # data가 text가 아닌 경우
                        this_data_decoded = round(subchunk_size/bitrate, 3)

                    this_chunk_datas.append((item, this_data_decoded))
                    

                subchunk_offset = subchunk_offset + subchunk_size + 8  # 포인터를 해당 chunk의 가장 끝 부분으로 이동

    return durations, this_chunk_datas

def answer_Q1_1(file_path,data):
    for d , p in zip(data["Q1"], make_answer(file_path)):
        d["duration"]= truncate(get_duration(p), 3)
    return data

def answer_Q1_2(file_path, data):
    file_list = make_anser(file_path)
    durations, chunk_datas = read_wav(file_list)
    count = 0
    for i, d in enumerate(data["Q1"]):
        if "THIS" in d:
            d["THIS"] = chunk_datas[count][1]
            count+=1

def main(file_path):
    data = load_json_file(file_path)
    data = answer_Q1_1(file_path, data)
    data = answer_Q1_2(file_path, data)
    save_answer_json(data)
    
if __name__ == "__main__":
    main()
