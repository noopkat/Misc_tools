from Tkinter import *
import subprocess
Popen = subprocess.Popen
PIPE = subprocess.PIPE

def build_hex():
  make_tempfile = Popen(['mktemp', '-t eeprom.XXXXXX'], stdout=subprocess.PIPE)
  tempfile = str(make_tempfile.stdout.read()).rstrip()

  f = open(tempfile, 'r+')
  make_eeprom = Popen(['./eeprom.py', '-f %s' % e1.get()], stdout=f)
  make_eeprom.wait()
  f.close()

  avrdude_flags = '-q -q -P usb -c %s -p attiny45 -b 15 -e -U flash:w:pr.hex -U eeprom:w:"%s"' % (e2.get(), tempfile)
  avrdude = Popen(['avrdude', avrdude_flags])

master = Tk()
Label(master, text='Radio Frequency').grid(row=0)
Label(master, text='Programmer').grid(row=1)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

e1.insert(10, '97.1')
e2.insert(10, 'usbtiny')

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Flash', command=build_hex).grid(row=3, column=1, sticky=W, pady=4)

mainloop()