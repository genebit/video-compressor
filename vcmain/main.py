import os
import re
import subprocess
import sys
import time
import mimetypes

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

OUTPUT_FOLDER = "compressed"

VIDEO_CODEC = ['None','libx264', 'libx265','mpeg4']


FFMPEG_PATH = None
compression_time_dict:dict[str,float] = {}


def find_ffmpeg():
    # If ffmpeg is not in system PATH, try to find it in the script's directory
    script_dir =os.path.dirname(sys.argv[0])
    ffmpeg_path = os.path.join(script_dir, "ffmpeg.exe")
    # print(ffmpeg_path)
    
    if os.path.isfile(ffmpeg_path):
        print(f'{GREEN}[INFO] Successfully found FFMPEG in application directory.{RESET}')
        print(f'{GREEN}\t--> FFMPEG path: {ffmpeg_path}.{RESET}')
        return ffmpeg_path
    
    try:
        # Try to run ffmpeg from the system PATH
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if result.returncode == 0:
            print(f'{GREEN}[INFO] Successfully found FFMPEG in SYSTEM PATH.{RESET}')
            return "ffmpeg"
    except FileNotFoundError:
        pass

    print(f'{RED}[INFO] Unable to find FFMPEG.{RESET}')
    return None  # ffmpeg not found



def get_output_folder(input_file_path):
    """
    Get the output folder path based on the input file path.

    Args:
    - input_file_path (str): The path of the input file.

    Returns:
    str: The path of the output folder.
    """
    # Combine the directory of the input file with the specified output folder name
    output_folder = os.path.join(os.path.dirname(input_file_path), OUTPUT_FOLDER)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return output_folder


def get_output_path(input_file_path):
    """
    Get the output file path based on the input file path.

    Args:
    - input_file_path (str): The path of the input file.

    Returns:
    str: The path of the output file.
    """
    # Combine the output folder path with the base name of the input file
    output_path = os.path.join(get_output_folder(input_file_path), os.path.basename(input_file_path))
    return output_path


def get_input_output_list(input_path):
    """
    Generate a dictionary mapping input video paths to corresponding output paths.

    Args:
    - input_path (str): The input path, which can be a file or a directory.

    Returns:
    dict: A dictionary where keys are input video paths and values are corresponding output paths.
    """
    input_output_dict:dict[str,str] = {}

    if os.path.isfile(input_path):
        # If the input is a file and a video, add it to the dictionary
        if is_video_file(input_path):
            input_output_dict[input_path] = get_output_path(input_path)
    elif os.path.isdir(input_path):
        # If the input is a directory, iterate through files and add video files to the dictionary
        for file in os.listdir(input_path):
            if not is_video_file(file):
                continue  # Skip non-video files
            input_video_path = os.path.join(input_path, file)
            input_output_dict[input_video_path] = get_output_path(input_video_path)
    else:
        # Raise an exception if the input path is invalid
        raise FileExistsError(f'{RED}[ERROR] The path is not correct. Path: [{input_path}] {RESET}')

    return input_output_dict


def process_input_paths(paths:str|list[str]):
    """
    Process a single file path or a list of file paths.

    Args:
    - paths (str or list): A file path or a list of file paths to process.

    Returns:
    dict: A dictionary containing input-output pairs for all processed files.
    """
    input_output_dict: dict[str, str] = {}

    def process_single_path(single_path):
        """
        Process a single file path and update the input-output dictionary.

        Args:
        - single_path (str): A single file path to process.
        """
        if os.path.isfile(single_path) or os.path.isdir(single_path):
            input_output_dict.update(get_input_output_list(single_path))
        else:
            # Handle the case when the path is neither a file nor a directory
            raise FileNotFoundError(f'{RED} [ERROR] The path does not exist. Path: [{single_path}] {RESET}')

    if isinstance(paths, str):
        # If a single path is provided, process it
        process_single_path(paths)
    elif isinstance(paths, list):
        # If a list of paths is provided, process each path
        for path in paths:
            process_single_path(path)
    else:
        # Raise an exception if the input type is not supported
        raise TypeError(f'{RED} [ERROR] Unsupported input type. Type: [{type(paths)}] {RESET}')

    return input_output_dict


def convert_to_mb(size):
    # Where size is the byte value
    # size to KB (1e+6 means 1×10^6 which also means)
    # So, to put it simply, it is 1 with 6 zeros: 1,000,000
    return float('{0:.2f}'.format(size / 1e+6))  # Display only 2 decimal places w/o rounding off

def check_for_space(path: str):
    special_chars = {' ': '\\ ', '(': '\(', ')': '\)'}

    def escape_special_characters(path: str, special_chars: dict) -> str:
        """
        Replace special characters in the given path with their corresponding escape sequences.

        :param path: The input path string.
        :param special_chars: A dictionary mapping special characters to their escape sequences.
        :return: The escaped path string.
        """
        if not isinstance(path, str):
            raise TypeError("The provided 'path' argument must be a string.")

        escaped_chars = {re.escape(char): escape for char, escape in special_chars.items()}
        pattern = re.compile("|".join(escaped_chars.keys()))

        def replace(match):
            return escaped_chars[re.escape(match.group())]

        return pattern.sub(replace, path)

    return escape_special_characters(path,special_chars)

def is_video_file(file_path:str):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('video')

def single_compress_done(input_path:str,output_path:str):
    print(f'{GREEN}[INFO] {input_path} compressed.{RESET}')
    # duration = 0.1 
    # beeps = [500, 1200, 2000]
    # for i in range(0, 3):
    #     os.system('play -nq -t alsa synth {0} sine {1}'.format(duration, beeps[i]))

def single_compress(input_path:str,output_path:str,crf, fps, vcodec_opt):
    # Set default values for crf fps and vcodec
    CRF = 26 if crf == '' else crf
    FPS = 25 if fps == '' else fps
    VCODEC_OPT = '0' if vcodec_opt == '' else vcodec_opt
    
    start = time.time()
    if VCODEC_OPT == '0':
        os.system(f'{FFMPEG_PATH} -i {check_for_space(input_path)} -r {FPS} -crf {CRF} {check_for_space(output_path)}')
    else:
        os.system(f'{FFMPEG_PATH} -i {check_for_space(input_path)} -vcodec {VIDEO_CODEC[int(VCODEC_OPT)]} -r {FPS} -crf {CRF} {check_for_space(output_path)}')
    end = time.time()
    time_elapsed = (end - start)
    compression_time_dict[input_path] = time_elapsed
    single_compress_done(input_path,output_path)

def get_user_params():
    crf = input(f'{GREEN}[PROCESS] Compression Rate [0-51] (Default: 26):{RESET}\n> ')
    fps = input(f'{GREEN}[PROCESS] Frames Per Second (Default: 25):{RESET}\n> ')
    videocodec = input(f'{GREEN}[PROCESS] Video Codec (None/H264/H265/MPEG4) [0-3] (Default: 0):{RESET}\n> ')
    return crf,fps,videocodec

def main_compress(path:str|list[str]):
    input_output_dict = process_input_paths(path)
    
    for i, (key, value) in enumerate(input_output_dict.items(), start=1):
        print(f'{i}. {key}')
        print(f'\t-> {value}')
        print()
    
    crf, fps, video_format_opt = get_user_params()
    print(f'{GREEN}------------START COMPRESSION---------------{RESET}')

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
            f'{GREEN}🗀  Input: {iFile}{RESET}',
            f'\n↳{GREEN} 🗀  Output: {oFile}{RESET}',
            f'\n{YELLOW}From {original_filesize} MB to {compressed_filesize}{RESET} MB',
            f'\n{GREEN}Process Time: {round(compression_time_dict[iFile]/60, 1)}min\n{RESET}')

def process_dragon_files(file_paths:list[str]):
    main_compress(file_paths)

def process_user_input_files():
    print(f'{RED}[INFO] If it is a folder, compress all videos in that folder. {RESET}')
    print(f'{RED}[INFO] If it is a single video file, compress that file directly {RESET}')
    user_input = input(f'{GREEN}[PROCESS] Target Path:{RESET}\n> ').strip().strip('"').strip().strip('"')
    
    if os.path.exists(user_input):
        main_compress(user_input)
    else:
        compression_time_dict.clear()
        print(f'{RED}[ERROR] The path does not right. Path: [{user_input}] {RESET}')

def main():
    global FFMPEG_PATH
    handled_drag_files = False
    while(True):
        try:
            FFMPEG_PATH = find_ffmpeg()
            if FFMPEG_PATH:
                if len(sys.argv) > 1 and not handled_drag_files:
                    # 如果有命令行参数，说明是通过拖拽文件或文件夹启动的
                    file_paths = sys.argv[1:]
                    process_dragon_files(file_paths)
                    handled_drag_files = True
                else:
                    # 否则，可能是通过其他方式启动的，可以在这里添加你的程序逻辑
                    process_user_input_files()
            else:
                raise FileNotFoundError(f'ffmpeg cannot found in system PATH or current directory {os.path.dirname(os.path.abspath(__file__))}')
            print("Press any key to continue...")
            input()  # This line will wait for the user to press Enter
            
        except KeyboardInterrupt:
            print(f'{YELLOW}[WARN] Terminated by user (Ctrl+C), do you want to exit [Y/N] ?{RESET}')
            user_choice = input('> ').upper()
            if user_choice == 'Y' or user_choice == 'YES':
                sys.exit(0)
                
        except Exception as e:
            print(f'{RED}[ERROR] An error occurred:\n{e}{RESET}')
            handled_drag_files = True
            print("Press any key to continue...")
            input()  # This line will wait for the user to press Enter
            

if __name__ == '__main__':
    main()


