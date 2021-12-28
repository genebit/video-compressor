from tkinter import font, ttk
from tkinter.constants import HORIZONTAL
from ttkthemes import ThemedTk
import tkinter as tk
import math

# Fonts
HEADING_FONT = 'Inter 14'
LABEL_FONT = 'Inter 11'

# Colors
WHITE = '#FFFFFF'

def elements(window):
    # Private values
    video_file_path = tk.StringVar()
    file_input_type = tk.StringVar()
    output_file_path = tk.StringVar()
    codec_value = tk.StringVar()
    fps_value = tk.StringVar()

    crf_value = tk.StringVar()
    crf_value.set('28') # Default value

    # -------------------------
    # ELEMENTS ----------------
    # -------------------------
    heading = ttk.Label(window, background=WHITE, text='Video Compressor', font=HEADING_FONT)
    heading.place(x=47, y=10)

    # -----MAIN VIDEO FILE-----
    ttk.Label(window, background=WHITE, text='Video File', font=LABEL_FONT).place(x=50, y=40)
    ttk.Entry(window, background=WHITE, font=LABEL_FONT, width=35).place(x=50, y=60)

    # -----FILE INPUT TYPE-----
    ttk.Label(window, background=WHITE, text='Choose Input Type', font=LABEL_FONT).place(x=400, y=40)

    file_input_options = ['Single File', 'From Text File']
    file_input = ttk.Combobox(window, background=WHITE, values=file_input_options, width=15, font=LABEL_FONT)
    file_input.set(file_input_options[0])
    file_input.place(x=400, y=60)

    # -----FILE DESTINATION-----
    ttk.Label(window, background=WHITE, text='File Destination', font=LABEL_FONT).place(x=50, y=100)
    ttk.Entry(window, background=WHITE, font=LABEL_FONT, width=35).place(x=50, y=120)

    # -----COMPRESSION OPTIONS-----
    ttk.Label(window, background=WHITE, text='Compression Option', font=HEADING_FONT).place(x=47, y=160)

    # -----CODEC-----
    ttk.Label(window, background=WHITE, text='Codec', font=LABEL_FONT).place(x=50, y=190)

    ttk.Style().configure('TCheckbutton', font=LABEL_FONT, background=WHITE)
    ttk.Checkbutton(window, width=10, style='TCheckbutton', text='H264').place(x=50, y=210)
    ttk.Checkbutton(window, width=10, style='TCheckbutton', text='H265').place(x=50, y=240)

    # -----FPS-----
    ttk.Label(window, background=WHITE, text='Frame Rate', font=LABEL_FONT).place(x=195, y=190)

    fps_options = [25, 30, 60]
    fps_option = ttk.Combobox(window, background=WHITE, values=fps_options, width=17, font=LABEL_FONT)
    fps_option.set(fps_options[0])
    fps_option.place(x=195, y=210)

    # -----CRF-----
    ttk.Style().configure('TScale', background=WHITE)
    ttk.Label(window, background=WHITE, text='Compression Rate', font=LABEL_FONT).place(x=400, y=190)

    s = ttk.Scale(window, length=150, from_=0, to=51, orient=HORIZONTAL, command=lambda s:crf_value.set(math.floor(float(s))))
    s.set(float(crf_value.get()))
    s.place(x=400, y=210)

    ttk.Label(window, background=WHITE, textvariable=crf_value, font=LABEL_FONT).place(x=550, y=208)

    # -----START BUTTON-----
    ttk.Style().configure('TButton', font=LABEL_FONT)
    ttk.Button(window, text='Start Compression!', command=start_compression).place(x=400, y=240)

def start_compression():
    pass

def main():
    GUI = ThemedTk(theme='arc')
    GUI['background'] = WHITE
    elements(GUI)
    GUI.title('Video Compressor by Gene')
    GUI.geometry('600x300')
    GUI.mainloop()
    
if __name__ == '__main__':
    main()
