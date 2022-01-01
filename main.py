import os
import time
import math


GREEN = '\033[92m'
RESET = '\033[0m'

totaltime = []


def converttomb(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6))  # Display only 2 decimal places w/o rounding off


def convertlisttostring(li):
    temp = ""
    for i in li:
        temp += i
    return temp


def checkforspace(path):
    character = list(path)
    for i in range(0, len(character)):
        if character[i] == ' ' and character[i-1] != '\\':
            character[i] = '\\ '
    return convertlisttostring(character)

def loader(directory):
    videos = open('videofiles.txt', 'w')
    outputfiles = open('outputfiles.txt', 'w')

    for file in os.listdir(directory):
        absolutepath = os.path.join(directory, file)
        destfilepath = os.path.join(os.path.join(directory, '../Output'), file)
        videos.write(absolutepath + '\n')
        outputfiles.write(destfilepath + '\n')

    videos.close()
    outputfiles.close()
    print('Finished Loading Files!')


def multiplefilecompression(crf, fps, vcodec_opt):
    videos = open('videofiles.txt', 'r').read().splitlines()
    destdirs = open("outputfiles.txt", "r").read().splitlines()

    CRF = '26' if crf == '' else crf
    FPS = '25' if fps == '' else fps
    VCODEC_OPT = '1' if vcodec_opt == '' else vcodec_opt

    videocodec = ['libx264', 'libx265']

    for i in range(0, len(videos)):
        start = time.time()
        os.system(f'ffmpeg -i {checkforspace(videos[i])} -vcodec {videocodec[int(VCODEC_OPT)]} -r {FPS} -crf {CRF} {checkforspace(destdirs[i])}')
        end = time.time()
        time_elapsed = (end - start)
        totaltime.append(time_elapsed)


def main():
    logo = '''
    ▀█░█▀ ░▀░ █▀▀▄ █▀▀ █▀▀█ 　 █▀▀ █▀▀█ █▀▄▀█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀█ █▀▀█ 
    ░█▄█░ ▀█▀ █░░█ █▀▀ █░░█ 　 █░░ █░░█ █░▀░█ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ █░░█ █▄▄▀ 
    ░░▀░░ ▀▀▀ ▀▀▀░ ▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀
    '''
    print(logo)
    videopath = input('[PROCESS] Video Path:\n> ')
    crf = input('[PROCESS] Compression Rate [0-51] (Default: 26):\n> ')
    fps = input('[PROCESS] Frames Per Second (Default: 25):\n> ')
    videocodec = input('[PROCESS] Video Codec (H264/H265) [0/1] (Default: 1):\n> ')

    print(f'{GREEN}------------START COMPRESSION---------------{RESET}')

    loader(videopath)

    outputfile = f'{videopath}/../Output'
    if not os.path.isdir(outputfile):
        os.system(f'mkdir {checkforspace(videopath)}/../Output')
    
    multiplefilecompression(crf, fps, videocodec)

    print(f'{GREEN}----------------FINISHED!-------------------{RESET}')
    print('Logs:')


if __name__ == '__main__':
    main()
