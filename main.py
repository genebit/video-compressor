import os
import time
import math


GREEN = '\033[92m'
RESET = '\033[0m'
YELLOW = '\033[93m'

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
        # set the char[i] to this if char == to '\', '(', ')' otherwise, just leave as it is
        character[i] = '\\ 'if (character[i] == ' ') and character[i-1] != '\\' else character[i]
        character[i] = '\(' if character[i] == '(' else character[i]
        character[i] = '\)' if character[i] == ')' else character[i]
            
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

    # Set default values for crf fps and vcodec
    CRF = 26 if crf == '' else crf
    FPS = 25 if fps == '' else fps
    VCODEC_OPT = '1' if vcodec_opt == '' else vcodec_opt

    videocodec = ['libx264', 'libx265']

    for i in range(0, len(videos)):
        start = time.time()
        os.system(f'ffmpeg -i {checkforspace(videos[i])} -vcodec {videocodec[int(VCODEC_OPT)]} -r {FPS} -crf {CRF} {checkforspace(destdirs[i])}')
        end = time.time()
        time_elapsed = (end - start)
        totaltime.append(time_elapsed)


def createoutputdir(videopath):
    outputfile = f'{videopath}/../Output'
    if not os.path.isdir(outputfile):
        os.system(f'mkdir {checkforspace(videopath)}/../Output')


def main():
    logo = '''
    ▀█░█▀ ░▀░ █▀▀▄ █▀▀ █▀▀█ 　 █▀▀ █▀▀█ █▀▄▀█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀█ █▀▀█ 
    ░█▄█░ ▀█▀ █░░█ █▀▀ █░░█ 　 █░░ █░░█ █░▀░█ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ █░░█ █▄▄▀ 
    ░░▀░░ ▀▀▀ ▀▀▀░ ▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀
    '''
    print(logo)
    videopath = input(f'{GREEN}[PROCESS] Video Path:{RESET}\n> ')
    crf = input(f'{GREEN}[PROCESS] Compression Rate [0-51] (Default: 26):{RESET}\n> ')
    fps = input(f'{GREEN}[PROCESS] Frames Per Second (Default: 25):{RESET}\n> ')
    videocodec = input(f'{GREEN}[PROCESS] Video Codec (H264/H265) [0/1] (Default: 1):{RESET}\n> ')

    print(f'{GREEN}------------START COMPRESSION---------------{RESET}')

    loader(videopath)
    createoutputdir(videopath)
    multiplefilecompression(crf, fps, videocodec)

    print(f'{GREEN}----------------FINISHED!-------------------{RESET}')
    print('LOGS:')
    uncompressed_files = open('videofiles.txt', 'r').read().splitlines()
    compressed_files = open("outputfiles.txt", "r").read().splitlines()

    for i in range(0, len(uncompressed_files)):
        original_filesize = converttomb(os.path.getsize(uncompressed_files[i]))
        compressed_filesize = converttomb(os.path.getsize(compressed_files[i]))

        print(
            f'{GREEN}🗀  {uncompressed_files[i]}{RESET}',
            f'\n↳{GREEN} 🗀  {compressed_files[i]}{RESET}',
            f'\n{YELLOW}From {original_filesize} to {compressed_filesize}{RESET}',
            f'\n{GREEN}Process Time: {round(totaltime[i]/60, 1)}min\n{RESET}')

if __name__ == '__main__':
    # TODO: Solution for not using ../ for a cleaner log
    main()
