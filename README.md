# Registration Bot for FIU

If you need to register for a full class, this bot will keep trying to enroll you every 6 minutes until your shopping cart is full (or two factor kicks you out).

### Install Instructions

Clone the repository and navigate to its directory.

```bash
git clone https://github.com/kclejeune/RegistrationBot.git
cd RegistrationBot
```

Ensure that Firefox, firefox-geckodriver, Python3, and pip are installed. Use pip to install selenium and typer.

On Debian based distributions (Ubuntu and Pop_OS! tested):

```bash
$ git clone https://github.com/amija004/FIU-RegistrationBot
$ cd FIU-RegistrationBot
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install python3 pip3 firefox firefox-geckodriver
$ pip install selenium typer
$ python3 bot.py
```
For Windows, the simplest method found was to install Ubuntu from the Windows app store, and then use the above instructions. Only Ubuntu was tested, but other Debian based distributions should work.

## Using the Script

**WARNING: YOU MUST MAKE SURE YOUR COMPUTER WILL NOT SLEEP.  PLUG IT IN AND CHECK THE SETTINGS, OR USE A DEDICATED COMPUTER FOR THIS SCRIPT**

It is *highly* recommended that you use a computer that is on 24/7 with SLEEP DISABLED. A raspberry pi or an old laptop should work well.

The script is intended to run until you get your classes or you get logged out.

To test the script in an actual browser window, run:

```bash
$ python3 bot.py --no-headless
```

To run the script, navigate to the RegistrationBot directory and run:

```bash
$ python3 bot.py
```

Follow the instructions to enter your username and password (type carefully, you can't see the prompt for security reasons).
Enter 1 for Spring, 2 for Summer, 3 for Fall. This should only matter if you have shopping carts for each semester.
The system will attempt to use the call function of the 2 Factor Authentication to authenticate. You should receive the call shortly after starting the script.
That's it, good luck!
