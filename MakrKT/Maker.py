# other versions of python may need to import tkinter (lowercase) instead
# these are all standard python modules, no pip install needed
from Tkinter import *
import subprocess
import tempfile
import os
import sys
Popen = subprocess.Popen
PIPE = subprocess.PIPE

# eeprom module deps, just in case pyinstaller doesn't find them
from intelhex import IntelHex
from datetime import date
from struct import pack
from math import modf
import crcmod
from getopt import getopt, GetoptError
import eeprom_module

def resource_path(relative_path):
  if getattr(sys, 'frozen', False):
    if hasattr(sys, "_MEIPASS"):
      # we are running in a |PyInstaller| bundle
      basedir = sys._MEIPASS
    elif os.environ.get('_MEIPASS2'):
      # we are running in a |PyInstaller| bundle
      basedir = os.environ.get('_MEIPASS2')
  else:
    # we are running in a normal Python environment
    basedir = os.path.dirname(__file__)

  # return 'real' path to file
  return os.path.join(basedir, relative_path)

# get os path of our scripts we wanna use later
pr_hex_path = resource_path('pr.hex')
hero_pic_path = resource_path('pic.gif')

# method to run eeprom module and get the temporary file back
def build_hex():
  make_eeprom = eeprom_module.get_hex(e1.get())
  flash_hex(make_eeprom)

# run avrdude with prior built temporary hex file
def flash_hex(make_tempfile):
  # chain together the avr dude command with flags
  avrdude_cmd = 'avrdude -qq -P usb -c %s -p attiny45 -b 15 -e -U flash:w:%s:i -U eeprom:w:%s:i' % (e2.get(), pr_hex_path, make_tempfile.name)
  print avrdude_cmd
  # open subprocess to run avrdude
  avrdude = Popen(avrdude_cmd, stderr=PIPE, shell=True)
  avrdude_err = avrdude.communicate()[1]
  
  # output log of what happened (log_string is the var that is bound to the status label at the bottom of the GUI)
  if (avrdude_err == ''):   
    log_string.set('\nHooray, your radio was successfully flashed with frequency %s!\n' % e1.get())
  else:
    log_string.set('\nLog:\n\n' + avrdude_err + '\n')

  # cool so we can delete this file now
  os.remove(make_tempfile.name)

# set up GUI
master = Tk()
# window title bar text
master.title('Public Radio Programmer')
# it only accepts GIFs and other weird formats haha
hero = PhotoImage(file=hero_pic_path)
bold_font = ('sans', 14, 'bold')
normal_font = ('sans', 14)
small_font = ('sans', 12)

# the rest of this file is just me committing GUI design blasphemy I am so sorry
# Just think html tables and you're on the right track of how tkinter interfaces work

# hero image to make it friendlier
Label(master, image=hero).grid(row=0, column=0, rowspan=4, sticky=N, padx=10, pady=10)

# hello message
Label(master, font=bold_font, text='Hi from Public Radio!', wraplength=300, justify=LEFT).grid(row=0, column=1, columnspan=2, sticky=W, pady=0, padx=10)
Label(master, font=normal_font, text='So you\'re ready to flash that radio of yours? Awesome, let\'s do it!', wraplength=300, justify=LEFT).grid(row=1, column=1, columnspan=2, sticky=W+N, pady=0, padx=10)

# inout labels
Label(master, font=normal_font, text='Radio Frequency', justify=RIGHT).grid(row=2, column=1, pady=0, padx=10, sticky=N+E)
Label(master, font=normal_font, text='Programmer', justify=RIGHT).grid(row=3, column=1, pady=0, padx=10, sticky=N+E)

# two input fields
e1 = Entry(master)
e2 = Entry(master)

# a digital frontier
# https://www.youtube.com/watch?v=tFXYuw96d0c
e1.grid(row=2, column=2, pady=0, padx=10, sticky=N)
e2.grid(row=3, column=2, pady=0, padx=10, sticky=N)

# put defaults in the inputs
e1.insert(10, '97.1')
e2.insert(10, 'usbtiny')

# Flash button setup, runs the build_hex method on click
Button(master, font=normal_font, text='Flash my Radio', command=build_hex).grid(row=4, column=2, sticky=E+N, padx=10)
#Button(master, text='Quit', command=master.quit).grid(row=3, column=2, sticky=W, pady=4)

# the avrdude status message stuff
log_string = StringVar()
log_label = Label(master, font=small_font, justify=LEFT, textvariable=log_string).grid(row=5, column=0, columnspan=3, sticky=W, pady=0, padx=10)

# run TK loop
mainloop()
