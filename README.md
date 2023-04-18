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


