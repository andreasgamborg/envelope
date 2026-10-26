# Envelope

Nothing fancy, just a python script that can make fold-it-yourself envelopes on A4 paper.

## Usage

Show the help with

 ```sh
  python envelope.py -h
```

![help](resources/help.png)

Example:  
Make all the addresses in *wedding.txt* into envelopes and place them in the directory **wedding_envelopes/**. Print the return address from *my_address.txt* on all of them. Include the "Please, do not bend" stamp and use ink save mode.

 ```sh
  python envelope.py -i wedding.txt -o wedding_envelopes -r my_address.txt -b -s
```

Take a look at **examples/** for how to write input and address files.

## "Install"

Make a *envelope.bat* file with the following two lines. Replace [path] with the path to *envelope.py* on your machine

```bat
@echo off
python [path]\envelope.py %*
```

'%\*' will pass any argument given to the bat script onto the python script. Place the *envelope.bat* file anywhere in your PATH.

Then you can call the script e.g.

```sh
  envelope -i addresses.txt
```

from anywhere
  
## Folding instructions

![envelope_fold_instructions](resources/envelope_fold_instructions.png)
