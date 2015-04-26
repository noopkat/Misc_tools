# How to flash your Public Radio
Oh hi! You're possibly entering the exciting world of hex compilation and firmware flashing for the very first time. If this is the case - welcome! If you're experienced with this stuff, you can skip ahead to the installation instructions for your operating system choice. 


## Installation
We currently support the major operating systems. Find your operating system below to get started.

+ [OSX instructions](#OSX)
+ [Windows instructions](#Windows)
+ [Linux instructions](#Linux)

### OSX

So you're running on a Mac. Nice! We'll need a couple of tools to get started. This will help you compile your custom firmware and get it flashed onto your radio. Follow the steps below to get all set up.

1. Download and install [Crosspack](https://www.obdev.at/products/crosspack/index.html). 
2. Download our Public Radio Maker Kit app, and double click on it to start 'er up.
3. You're installed! Skip to the [next section](#Using-the-Public-Radio-Software) to learn which values to type in for successful flashing of your radio.

### Windows

To get this all going on windows, we need some cool software that communicates with the radio called **avrdude**. You can get this by downloading and installing **WinAVR**. Let's get started!

1. Download and install [WinAVR](http://sourceforge.net/projects/winavr/files/WinAVR/20100110/).
2. If you haven't already, install the drivers for your programmer device. You should have received an installation CD with the programmer. If not, you can probably get it set up by using a port of `libusb`. [The steps are well written up here](http://eliaselectronics.com/using-the-avrispmkii-with-avrdude-on-windows/).
3. Download our Public Radio Maker Kit software, and double click on the exe file.
5. You're installed! Skip to the [next section](#Using-the-Public-Radio-Software) to learn which values to type in for successful flashing of your radio.

### Linux

If you're running a flavour of Linux, you're probably already familar with using the Terminal. If not, you can find the Terminal application already installed on all Linux distros. Fire it up!

1. Install python-tk by running: `sudo apt-get install python-tk`
2. Next, we need to install avrdude, if you don't already have it. The following commands will install the latest verison for you:
`sudo add-apt-repository ppa:pmjdebruijn/avrdude-release`  
`sudo apt-get update`  
`sudo apt-get install avrdude`  
3. Download our Public Radio Maker Kit app
4. You'll need to run our app with admin privileges. The most straightforward way of doing this is to use Terminal to [cd](http://www.linfo.org/cd.html) to the directory where the app is, and run `sudo Maker`
5. You're installed! Skip to the [next section](#Using-the-Public-Radio-Software) to learn which values to type in for successful flashing of your radio.

## Using the Public Radio Software

todo

## Troubleshooting

todo