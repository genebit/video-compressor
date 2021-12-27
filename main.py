import os

def convert_size(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6)) # Display only 2 decimal places w/o rounding off

def main():
    # Path
    ORIGINAL_VIDEO = 'videos/original.MP4'
    DESTINATION_FILE = 'testdirdest/output.mp4'

    # Default Value
    os.system('ffmpeg -i {0} -vcodec libx265 -crf 28 {1}'.format(ORIGINAL_VIDEO, DESTINATION_FILE))

    # Size comparison for log
    ORIGINAL_VIDEO_SIZE = convert_size(os.path.getsize(ORIGINAL_VIDEO))
    OUTPUT_VIDEO_SIZE = convert_size(os.path.getsize(DESTINATION_FILE))

    print('-----------------------------------------')
    print('Finished!\n From {0}MB to {1}MB'.format(ORIGINAL_VIDEO_SIZE, OUTPUT_VIDEO_SIZE))

if __name__ == '__main__':
    # NOTE: LOWER 'CRF' values = higher bitrates, and hence produce higher quality videos.
    # NOTE: HIGHER 'CRF' values = higher compression rate, a good increment shoud be around 4-6 for H265

    # The range of the CRF scale is 0–51, where 0 is lossless, 23 is the default, and 51 is worst quality possible. 
    # A lower value generally leads to higher quality, and a subjectively sane range is 17–28.

    # NOTE: The larger the crf is the more time it takes: around 30min
    main()