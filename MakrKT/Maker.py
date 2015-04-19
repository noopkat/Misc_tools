# other versions of python may need to import tkinter (lowercase) instead
# these are all standard python modules, no pip install needed
from Tkinter import *
import subprocess
import tempfile
import os
import sys
Popen = subprocess.Popen
PIPE = subprocess.PIPE

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

# get current directory we're in
current_dir = os.getcwd()
# get os path of our scripts we wanna use later
eeprom_script_path = resource_path('eeprom.py')
pr_hex_path = resource_path('pr.hex')
hero_pic_path = resource_path(os.path.join('.', 'pic.gif'))

# method to run eeprom.py and write to a temporary file
def build_hex():
  # set tempfile to not delete upon close() because we gotta close it to pass it in to avrdude
  make_tempfile = tempfile.NamedTemporaryFile(prefix='eeprom.', suffix='.hex', delete=False)
  # run eeprom.py using the entered frequency of choice
  make_eeprom = subprocess.check_output(eeprom_script_path + ' -f %s' % e1.get(), shell=True)
  # pipe the output of eeprom.py into the tempfile
  make_tempfile.write(make_eeprom)
  # for debug
  log_string.set(make_eeprom)
  # we're done with the file
  make_tempfile.close()
  flash_hex(make_tempfile)

# run avrdude with prior built temporary hex file
def flash_hex(make_tempfile):
  # chain together the avr dude command with flags
  avrdude_cmd = 'avrdude -q -P usb -c %s -p attiny45 -b 15 -e -U flash:w:%s -U eeprom:w:%s' % (e2.get(), pr_hex_path, make_tempfile.name)
  print avrdude_cmd
  # open subprocess to run avrdude
  avrdude = Popen(avrdude_cmd, stderr=PIPE, shell=True)
  avrdude_err = avrdude.communicate()[1]
  
  # log_string is the var that is bound to the status label at the bottom of the GUI
  log_string.set(avrdude_err)
  # cool so we can delete this file now
  os.remove(make_tempfile.name)

# set up GUI
master = Tk()
# window title bar text
master.title('Public Radio Programmer')
# it only accepts GIFs and other weird formats haha
hero = PhotoImage(file=hero_pic_path)

# the rest of this file is just me committing GUI design blasphemy I am so sorry
# Just think html tables and you're on the right track of how tkinter interfaces work
Label(master, image=hero).grid(row=0, column=0, rowspan=4, sticky=N, padx=10, pady=10)
Label(master, text='Hi - So you\'re ready to flash that radio of yours? Awesome, let\'s do it!', wraplength=300, justify=LEFT, font='bold').grid(row=0, column=1, columnspan=2, sticky=W, pady=10, padx=10)
Label(master, text='Radio Frequency', justify=RIGHT).grid(row=1, column=1, pady=10, padx=10, sticky=E)
Label(master, text='Programmer', justify=RIGHT).grid(row=2, column=1, pady=10, padx=10, sticky=E)

# the avrdude status message stuff
log_string = StringVar()
log_label = Message(master, justify=LEFT, textvariable=log_string).grid(row=4, column=1, columnspan=2, pady=10, padx=10)

# two input fields
e1 = Entry(master)
e2 = Entry(master)

# a digital frontier
# https://www.youtube.com/watch?v=tFXYuw96d0c
e1.grid(row=1, column=2, pady=10, padx=10)
e2.grid(row=2, column=2, pady=10, padx=10)

# put defaults in the inputs
e1.insert(10, '97.1')
e2.insert(10, 'usbtiny')

# Flash button setup, runs the build_hex method on click
Button(master, text='Flash', command=build_hex).grid(row=3, column=2, sticky=E+N, padx=10, pady=10)
#Button(master, text='Quit', command=master.quit).grid(row=3, column=2, sticky=W, pady=4)

# run TK loop
mainloop()
