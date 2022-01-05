## Video Compressor
### About
- A script that uses ffmpeg to compress videos for free
- It uses Python as a terminal interface for inputing options

### Prerequisites
- Make sure to install the followings:

    **Linux:**
    - `sudo apt install ffmpeg`
    - `sudo apt install python3`
    - `sudo apt install sox`
    <br>

    **Windows:**
    - Download [ffmpeg here](https://www.ffmpeg.org/)
    - Set ffmpeg to `$PATH`

### Instruction    
**For Multiple File Compression:**

- Create a directory for the uncompressed files
- _Be inside of this directory and_ run `python3 main.py` or run `make` in terminal
- Answer the prompt amd wait for the files to finished _(For default settings just hit `ENTER`)_
- Once finished, the compressed files are found in the `output` folder next to your `main` path

**Sample Prompts**
    
    ▀█░█▀ ░▀░ █▀▀▄ █▀▀ █▀▀█ 　 █▀▀ █▀▀█ █▀▄▀█ █▀▀█ █▀▀█ █▀▀ █▀▀ █▀▀ █▀▀█ █▀▀█ 
    ░█▄█░ ▀█▀ █░░█ █▀▀ █░░█ 　 █░░ █░░█ █░▀░█ █░░█ █▄▄▀ █▀▀ ▀▀█ ▀▀█ █░░█ █▄▄▀ 
    ░░▀░░ ▀▀▀ ▀▀▀░ ▀▀▀ ▀▀▀▀ 　 ▀▀▀ ▀▀▀▀ ▀░░░▀ █▀▀▀ ▀░▀▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░▀▀

    [PROCESS] Video Path:
    > /home/genebit/Downloads/main
    [PROCESS] Compression Rate [0-51] (Default: 26):
    > 26
    [PROCESS] Frames Per Second (Default: 25):
    > 25
    [PROCESS] Video Codec (H264/H265) [0/1] (Default: 1):
    > 0
    ------------START COMPRESSION---------------
    
    - where /home/genebit/Downloads/main is the uncompressed videos
    
    - where compression rate is the rate of compression to be processed,
      low setting will have a higher quality and less compression and high 
      means it will have a higher compression but will have worse quality.
    
    - the output folder automatically generated and is found on 
      /home/genebit/Downloads/output

### Notes
- Make sure to have a faster cpu to increase faster compression time
- Tested on a Quad Core CPU where each process can take from 4-5min depending on the footage size and the filesize. 
 Best to be run on a Quad Core CPUs and above since on Dual Core CPUs it runs slow af running at 30min per compression...
