import os

def converttomb(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6)) # Display only 2 decimal places w/o rounding off

GREEN = '\033[92m'
RESET = '\033[0m'

def loader(directory, destdir):
    videos = open('videofiles.txt', 'w')
    outputfiles = open('outputfiles.txt', 'w')

    for file in os.listdir(directory):
        absolutepath = os.path.join(directory, file)
        destfilepath = os.path.join(destdir, file)
        videos.write(absolutepath + '\n')
        outputfiles.write(destfilepath + '\n')

    videos.close()
    outputfiles.close()
    print('Finished Loading Files!')

def multiplefilecompression(crf, fps, vcodec):
    videos = open('videofiles.txt', 'r').read().splitlines()
    destdirs = open("outputfiles.txt", "r").read().splitlines()

    videocodec = [ 'libx264', 'libx265' ]

    for i in range(0, len(videos)):
        os.system(f'ffmpeg -i {videos[i]} -vcodec {videocodec[int(vcodec)]} -r {fps} -crf {crf} {destdirs[i]}')

        originalfilesize = converttomb(os.path.getsize(videos[i]))
        compressedfilesize = converttomb(os.path.getsize(destdirs[i]))

        print(f'\nFinished Compression!\n {GREEN}From {originalfilesize}MB to {compressedfilesize}MB{RESET}')

def singlefilecompression(video, destdir, crf, fps, vcodec):
    path, file = os.path.split(video)

    videocodec = [ 'libx264', 'libx265' ]

    os.system(f'ffmpeg -i {os.path.join(path, file)} -vcodec {videocodec[int(vcodec)]} -r {fps} -crf {crf} {os.path.join(destdir, file)}')

    originalfilesize = converttomb(os.path.getsize(video))
    compressedfilesize = converttomb(os.path.getsize(os.path.join(destdir, file)))

    print(f'\nFinished Compression!\n {GREEN}From {originalfilesize}MB to {compressedfilesize}MB{RESET}')

def main():
    s_logo = '''
    ▀█░█▀ ░▀░ █▀▀▄ █▀▀ █▀▀█ 　 █▀▀ █▀▀█ █▀▄▀█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀█ █▀▀█ 
    ░█▄█░ ▀█▀ █░░█ █▀▀ █░░█ 　 █░░ █░░█ █░▀░█ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ █░░█ █▄▄▀ 
    ░░▀░░ ▀▀▀ ▀▀▀░ ▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀
    
    [INSTRUCTION]
    SINGLE FILE COMPRESSION:
        - Reference the file's full path
        - Reference only the output folder
        - Answer the prompt
    '''

    m_logo = '''
    ▀█░█▀ ░▀░ █▀▀▄ █▀▀ █▀▀█ 　 █▀▀ █▀▀█ █▀▄▀█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀█ █▀▀█ 
    ░█▄█░ ▀█▀ █░░█ █▀▀ █░░█ 　 █░░ █░░█ █░▀░█ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ █░░█ █▄▄▀ 
    ░░▀░░ ▀▀▀ ▀▀▀░ ▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀

    [INSTRUCTION]
    MULTIPLE FILE COMPRESSION:
        - Create a folder, move the videos within and reference the folder in the prompt
        - Create an output folder for the compressed videos
        - Answer the prompt
    '''

    compress_singlefile = True if input('[PROCESS] Compress Single File? (y/n)\n> ') == 'y' else False

    if compress_singlefile:
        print(s_logo)
        videopath = input('[PROCESS] Video Path:\n> ')
        destdir = input('[PROCESS] Output Path:\n> ')
        crf = input('[PROCESS] Compression Percentage [0-51]: (Low Percentage will have higher Quality, High will have worse Quality)\n> ')
        fps = input('[PROCESS] Frames Per Second:\n> ')
        videocodec = input('[PROCESS] Video Codec (H264/H265) [0/1]:\n> ')

        print('--------------------------------------------\n------------START COMPRESSION---------------\n--------------------------------------------')
        singlefilecompression(videopath, destdir, crf, fps, videocodec)
    else:
        print(m_logo)
        videopath = input('[PROCESS] Video Path:\n> ')
        destdir = input('[PROCESS] Output Path:\n> ')
        crf = input('[PROCESS] Compression Rate [0-51]: (Low rate = Higher Quality, High rate = Worse Quality)\n> ')
        fps = input('[PROCESS] Frames Per Second:\n> ')
        videocodec = input('[PROCESS] Video Codec (H264/H265) [0/1]:\n> ')

        print('--------------------------------------------\n------------START COMPRESSION---------------\n--------------------------------------------')

        loader(videopath, destdir)
        multiplefilecompression(crf, fps, videocodec)

if __name__ == '__main__':
    # Requirements:
    #   ffmpeg
    #   python3
    main()