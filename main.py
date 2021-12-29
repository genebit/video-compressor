import os

def converttomb(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6)) # Display only 2 decimal places w/o rounding off

def main():
    # For multiple files
    with open('videofiles.txt', 'r') as ORIGINAL_VIDEOS:
        ORIGINAL_VIDEO = ORIGINAL_VIDEOS.read().splitlines()
        DESTINATION_FILE = open("outputfiles.txt", "r").read().splitlines()
        CRF_VALUE = 28
        FPS_VALUE = 25
        CODEC = ['libx264', 'libx265']

        for i in range(0, len(ORIGINAL_VIDEO)-1):
            # The Default Value
            os.system(f'ffmpeg -i {ORIGINAL_VIDEO[i]} -vcodec {CODEC[1]} -r {FPS_VALUE} -crf {CRF_VALUE} {DESTINATION_FILE[i]}')

            # Size comparison for log
            ORIGINAL_VIDEO_SIZE = converttomb(os.path.getsize(ORIGINAL_VIDEO[i]))
            OUTPUT_VIDEO_SIZE = converttomb(os.path.getsize(DESTINATION_FILE[i]))

            print('------------------------------------------------------------------')
            print(f'Finished Compression!\n From {ORIGINAL_VIDEO_SIZE}MB to {OUTPUT_VIDEO_SIZE}MB')

if __name__ == '__main__':
    # NOTE: LOWER 'CRF' values = higher bitrates, and hence produce higher quality videos.
    # NOTE: HIGHER 'CRF' values = higher compression rate, a good increment shoud be around 4-6 for H265

    # The range of the CRF scale is 0–51, where 0 is lossless, 23 is the default, and 51 is worst quality possible. 
    # A lower value generally leads to higher quality, and a subjectively sane range is 17–28.

    # NOTE: The larger the crf is the more time it takes: around 30min
    main()