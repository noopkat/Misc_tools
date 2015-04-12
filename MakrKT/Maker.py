from Tkinter import *
import subprocess
import tempfile
import os
Popen = subprocess.Popen
PIPE = subprocess.PIPE

current_dir = os.getcwd()
eeprom_script = os.path.join(current_dir, 'eeprom.py')
pr_hex = os.path.join(current_dir, 'pr.hex');

# run eeprom.py and write to a temporary file
def build_hex():
  make_tempfile = tempfile.NamedTemporaryFile(prefix='eeprom.', suffix='.hex', delete=False)

  make_eeprom = Popen([eeprom_script, '-f %s' % e1.get()], stdout=PIPE)
  eeprom_output = make_eeprom.stdout.read()
  make_eeprom.wait()
  make_tempfile.write(eeprom_output)
  make_tempfile.close()

  #print 'temp file: ' + make_tempfile.name
  flash_hex(make_tempfile)

# run avrdude with prior built temporary hex file
def flash_hex(make_tempfile):
  avrdude_cmd = 'avrdude -q -P usb -c %s -p attiny45 -b 15 -e -U flash:w:%s -U eeprom:w:%s' % (e2.get(), pr_hex, make_tempfile.name)
  avrdude = Popen(avrdude_cmd.split(), stdout=PIPE, stderr=PIPE)
  avrdude_err = avrdude.stderr.read()

  #print avrdude_cmd

  if (avrdude_err != 0):
    log_string.set('Oh no! There was an error:\n\n' + avrdude_err)
  else:
    log_string.set('Yay!\nYour radio was successfully reprogrammed!')

  os.remove(make_tempfile.name)

# set up GUI
master = Tk()
master.title('Public Radio Programmer')

Label(master, text='Hi - So you\'re ready to flash that radio of yours? \nAwesome, let\'s do it!', justify=LEFT).grid(row=0, columnspan=2, sticky=W, pady=10, padx=10)
Label(master, text='Radio Frequency', justify=RIGHT).grid(row=1, pady=10, padx=10)
Label(master, text='Programmer', justify=RIGHT).grid(row=2, pady=10, padx=10)

log_string = StringVar()
log_label = Label(master, justify=LEFT, textvariable=log_string).grid(row=4, columnspan=2, pady=10, padx=10)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=1, column=1, pady=10, padx=10)
e2.grid(row=2, column=1, pady=10, padx=10)

e1.insert(10, '97.1')
e2.insert(10, 'usbtiny')

Button(master, text='Flash', command=build_hex, relief=RAISED).grid(row=3, column=1, sticky=E+N, padx=10, pady=10)
#Button(master, text='Quit', command=master.quit).grid(row=3, column=2, sticky=W, pady=4)

# run TK loop
mainloop()