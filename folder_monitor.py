## monitors the folder containing pdf agreement forms and signature images

## import necessary utilities
from watchdog.events import FileSystemEventHandler
import os
from pdf_utils import pdf_to_image, convert_signature_image_to_pdf

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            if file_name.endswith('.pdf') and 'agreement' in file_name:
                pdf_to_image(file_path, os.path.join('image_previews', 'agreement_preview.jpg'))

            elif file_name.endswith('.png') and 'signature' in file_name:
                convert_signature_image_to_pdf(file_path, os.path.join('signatures', 'signature.pdf'))
                os.remove(file_path)
