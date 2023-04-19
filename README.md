# Signature-Snagger
Utility to capture a signature from a signature pad and to add it to a PDF. 


Requires setuptools to generate the code on my end (pip install setuptools)
Requires Pillow for the GUI (pip install pillow)

To package the app, run in terminal: 
python setup.py sdist

This creates a source distro in a folder named "dist"

To install app on another machine: 
Copy the "dist" folder to target machine then run following command inside 'dist' folder: 
pip install signature_overlay-0.1.tar.gz

also must run pip install -r requirements.txt

After installation, run the program by executing the following: 
signature_overlay


Note to self: 
Error checking/testing - next steps (as of 4/19/23 at 5:47 PM) - these are up for tomorrow: 

Okay awesome thank you, I changed that. So it looks like outstanding issues are the following: 

1. The error message at the end of the traceback (PIL.UnidentifiedImageError: cannot identify image file 'signatures/temp_signature.pdf') you said indicates that the program is trying to open a PDF instead of an image. Here is what I have in that signatures folder after attempting to run the program once: samplesignature001.png (the test signature file I added) and a new file temp_signature.pdf that I presume was created by the program. What should the files here look like and what would the expected behavior be? What should I do? 

2. defining the x and y coordinates - I want to come back to this after we address the first issue