(In progress)

Requirements:
Programs:
Python 3 
ffmpeg

Python packages (install using pip install [packagename]):
google-api-python-client
requests
pysrt
progressbar2
six

Windows:
Install autosub + addsub by putting the autosub root folder in %ProgramFiles%, and adding %ProgramFiles%\autosub to your PATH.

To find the location of your %ProgramFiles% folder, open a command prompt and run 'echo %ProgramFiles%'. Then, put the root autosub folder in the folder that was listed, and close the command prompt.

To add %ProgramFiles%\autosub to your PATH, right click on 'This PC' on your desktop, and select 'Properties'. On the left, select 'Advanced System Settings', and then 'Environment Variables'. On the lower panel, 'System variables', scroll down and find the entry for 'Path' or 'PATH'. Select that entry, and click 'Edit...'. On the right, click 'New', and type '%ProgramFiles%\autosub' (note the backslash!). Then click 'OK', 'OK', and 'OK' to exit the settings windows. You're done!


Mac:
Mac is a bit more complex: you need to place the bash files in /usr/bin/local,
take ownership of them with chmod, and make them executable.
(Detailed instructions + bash files coming.)