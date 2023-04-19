## main.py - Code for running GUI

# Import necessary utilities
import threading
import tkinter as tk
from PIL import Image, ImageTk
import shutil
from pdf_utils import overlay_pdf, pdf_to_image, convert_signature_image_to_pdf, get_most_recent_file
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import os

# Constants
AGREEMENTS_FOLDER = 'agreements'
SIGNATURES_FOLDER = 'signatures'
SIGNED_PDFS_FOLDER = 'signed_pdfs'
IMAGE_PREVIEW_FOLDER = 'image_previews'

# Function to confirm the signature on the agreement PDF
def confirm_signature():
    # Get the paths of the agreement PDF and signature image
    agreement_path = get_most_recent_file(AGREEMENTS_FOLDER)
    signature_image_path = get_most_recent_file(SIGNATURES_FOLDER)

    # Convert signature image to PDF
    signature_pdf_path = os.path.join(SIGNATURES_FOLDER, 'temp_signature.pdf')
    convert_signature_image_to_pdf(signature_image_path, signature_pdf_path)

    # Overlay signature PDF onto the agreement PDF
    output_pdf_path = os.path.join(SIGNED_PDFS_FOLDER, 'signed_agreement.pdf')
    overlay_pdf(agreement_path, signature_pdf_path, output_pdf_path, x_position, y_position)

    # Remove the processed agreement and signature files (if required)
    os.remove(agreement_path)
    os.remove(signature_image_path)

    # Update the image previews in the GUI
    update_image_previews(root)

# Function to cancel the signature process and load the next agreement
def cancel():
    # Remove the current agreement and signature files (if required)
    os.remove(agreement_path)
    os.remove(signature_image_path)

    # Update the image previews in the GUI
    update_image_previews(root)

# Function to resize large pdfs to fit the screen
def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = float(width) / float(height)
    
    if width > max_width:
        width = max_width
        height = int(width / aspect_ratio)
    
    if height > max_height:
        height = max_height
        width = int(height * aspect_ratio)
    
    return image.resize((width, height), Image.LANCZOS)

# Function to update the image previews in the GUI
def update_image_previews():
    global agreement_image, signature_image_label, root

    # Get the most recent agreement and signature image paths
    agreement_path = get_most_recent_file(AGREEMENTS_FOLDER)
    signature_image_path = get_most_recent_file(SIGNATURES_FOLDER)

    # Update the agreement image in the GUI
    if agreement_path:
        agreement_img_path = os.path.join(IMAGE_PREVIEW_FOLDER, "agreement_preview.jpg")
        pdf_to_image(agreement_path, agreement_img_path)
        agreement_img = Image.open(agreement_img_path)
        # Adjust the values 800, 800 to your desired max width and height
        resized_agreement_img = resize_image(agreement_img, 800, 800)  
        agreement_img_tk = ImageTk.PhotoImage(resized_agreement_img)
        agreement_image.config(image=agreement_img_tk)
        agreement_image.image = agreement_img_tk

    # Update the signature image in the GUI
    if signature_image_path:
        # Load the signature image and resize it to a thumbnail
        signature_img = Image.open(signature_image_path)
        signature_img.thumbnail((150, 150))

        # Convert the signature image to a PhotoImage and display it in the signature_image_label
        signature_img_tk = ImageTk.PhotoImage(signature_img)
        signature_image_label.configure(image=signature_img_tk)
        signature_image_label.image = signature_img_tk

    # Refresh the image previews every 3 seconds
    root.after(3000, update_image_previews)



def create_folders():
    os.makedirs(AGREEMENTS_FOLDER, exist_ok=True)
    os.makedirs(SIGNATURES_FOLDER, exist_ok=True)
    os.makedirs(SIGNED_PDFS_FOLDER, exist_ok=True)
    os.makedirs(IMAGE_PREVIEW_FOLDER, exist_ok=True)

class FolderChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        update_image_previews()

def run():
    global agreement_image, signature_image_label, root
    create_folders()

    # Create the GUI
    root = tk.Tk()
    root.title("Signature Overlay")

    # Display the agreement image in the GUI
    agreement_image = tk.Label(root)
    agreement_image.pack(pady=10)

    # Create a new label for the signature image and display it in the GUI
    signature_image_label = tk.Label(root)
    signature_image_label.pack(pady=10)

    confirm_button = tk.Button(root, text="Confirm", command=confirm_signature)
    confirm_button.pack(pady=10)

    cancel_button = tk.Button(root, text="Cancel", command=cancel)
    cancel_button.pack(pady=10)

    instructions = tk.Text(root, wrap=tk.WORD, width=60, height=10)
    instructions.insert(tk.END, "1. Place agreement PDFs in the 'agreements' folder.\n"
                              "2. Place signature image files (PNG format) in the 'signatures' folder.\n"
                              "3. Signed PDFs will be saved in the 'signed_pdfs' folder.\n"
                              "4. Use the 'Confirm' button to confirm and save the signature on the agreement PDF.\n"
                              "5. Use the 'Cancel' button to skip the current agreement and load the next one.")
    instructions.config(state=tk.DISABLED)
    instructions.pack(pady=10)

    # Update the image previews initially and set the interval for refresh
    update_image_previews()

    # Set up folder monitoring
    event_handler = FolderChangeHandler()
    observer = Observer()

    observer.schedule(event_handler, AGREEMENTS_FOLDER, recursive=False)
    observer.schedule(event_handler, SIGNATURES_FOLDER, recursive=False)

    observer.start()

    # Start the GUI event loop
    try: 
        root.mainloop()
    finally:
    # Stop the observer when the GUI is closed
        observer.stop()
    
    observer.join()

if __name__ == '__main__':
    run()