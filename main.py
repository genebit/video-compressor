import os
import time
import mimetypes

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

OUTPUT_FOLDER = "compressed"

VIDEO_CODEC = ['None','libx264', 'libx265','mpeg4']

compression_time_dict:dict[str,float] = {}

def get_output_folder(input_file_path):
    output_folder = os.path.join(os.path.dirname(input_file_path),OUTPUT_FOLDER)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

def get_output_path(input_file_path):
    output_path = os.path.join(get_output_folder(input_file_path),os.path.basename(input_file_path))
    return output_path

def get_input_output_list(input_path):
    input_output_dict:dict[str,str] = {}
    if os.path.isfile(input_path):
        if is_video_file(input_path):
            input_output_dict[input_path] = get_output_path(input_path)
    elif os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if not is_video_file(file):
                continue  # Skip non-video files
            input_video_path=os.path.join(input_path, file)
            input_output_dict[input_video_path] = get_output_path(input_video_path)
    else:
        raise FileExistsError(f'{RED} [ERROR] The path does not right. Path: [{input_path}] {RESET}')
        
    return input_output_dict

def convert_to_mb(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6))  # Display only 2 decimal places w/o rounding off


def convert_list_to_string(li):
    temp = ""
    for i in li:
        temp += i
    return temp


def check_for_space(path):
    character = list(path)
    for i in range(0, len(character)):
        # set the char[i] to this if char == to '\', '(', ')' otherwise, just leave as it is
        character[i] = '\\ 'if (character[i] == ' ') and character[i-1] != '\\' else character[i]
        character[i] = '\(' if character[i] == '(' else character[i]
        character[i] = '\)' if character[i] == ')' else character[i]
            
    return convert_list_to_string(character)

def is_video_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('video')

def single_compress_done(input_path:str,output_path:str):
    print(f'{GREEN} {input_path} compressed. {RESET}')
    # duration = 0.1 
    # beeps = [500, 1200, 2000]
    # for i in range(0, 3):
    #     os.system('play -nq -t alsa synth {0} sine {1}'.format(duration, beeps[i]))

def single_compress(input_path,output_path,crf, fps, vcodec_opt):
    # Set default values for crf fps and vcodec
    CRF = 26 if crf == '' else crf
    FPS = 25 if fps == '' else fps
    VCODEC_OPT = '0' if vcodec_opt == '' else vcodec_opt
    
    start = time.time()
    if VCODEC_OPT == '0':
        os.system(f'ffmpeg -i {check_for_space(input_path)} -r {FPS} -crf {CRF} {check_for_space(output_path)}')
    else:
        os.system(f'ffmpeg -i {check_for_space(input_path)} -vcodec {VIDEO_CODEC[int(VCODEC_OPT)]} -r {FPS} -crf {CRF} {check_for_space(output_path)}')
    end = time.time()
    time_elapsed = (end - start)
    compression_time_dict[input_path] = time_elapsed
    single_compress_done(input_path,output_path)


def get_user_params():
    crf = input(f'{GREEN}[PROCESS] Compression Rate [0-51] (Default: 26):{RESET}\n> ')
    fps = input(f'{GREEN}[PROCESS] Frames Per Second (Default: 25):{RESET}\n> ')
    videocodec = input(f'{GREEN}[PROCESS] Video Codec (None/H264/H265/MPEG4) [0-3] (Default: 0):{RESET}\n> ')
    return crf,fps,videocodec

    
def main_compress(path:str):
    input_path = path
    crf, fps, video_format_opt = get_user_params()
    
    print(f'{GREEN}------------START COMPRESSION---------------{RESET}')
    input_output_dict = get_input_output_list(input_path)
    # iterate the input_output_dict and extract the key as iFile, Value as oFile
    for iFile,oFile in input_output_dict.items():
        single_compress(iFile,oFile,crf,fps,video_format_opt)

        
    print(f'{GREEN}----------------FINISHED!-------------------{RESET}')
    print(f'{GREEN}--------------------------------------------{RESET}')
    print(f'{GREEN}------------------LOGS----------------------{RESET}')
    for iFile,oFile in input_output_dict.items():
        original_filesize = convert_to_mb(os.path.getsize(iFile))
        compressed_filesize = convert_to_mb(os.path.getsize(oFile))
        print(
            f'{GREEN}🗀  {iFile}{RESET}',
            f'\n↳{GREEN} 🗀  {oFile}{RESET}',
            f'\n{YELLOW}From {original_filesize} to {compressed_filesize}{RESET}',
            f'\n{GREEN}Process Time: {round(compression_time_dict[iFile]/60, 1)}min\n{RESET}')

def main():
    print(f'{RED}[INFO] If it is a folder, compress all videos in that folder. {RESET}')
    print(f'{RED}[INFO] If it is a single video file, compress that file directly {RESET}')
    user_input = input(f'{GREEN}[PROCESS] Path:{RESET}\n> ').strip().strip('"').strip().strip('"')
    
    if os.path.exists(user_input):
        main_compress(user_input)
    else:
        compression_time_dict.clear()
        print(f'{RED} [ERROR] The path does not right. Path: [{user_input}] {RESET}')
        main()

if __name__ == '__main__':
    main()
