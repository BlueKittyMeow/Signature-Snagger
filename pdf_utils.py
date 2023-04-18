## pdf_utils.py - Functions for handling PDFs - overlay sig and convert pdf to img

# Import necessary utilities
import img2pdf
import pdfrw
from pdf2image import convert_from_path

# Convert signature image to PDF
def convert_signature_image_to_pdf(signature_image_path, signature_pdf_path):
    with open(signature_pdf_path, "wb") as f:
        f.write(img2pdf.convert(signature_image_path))

# Overlay signature PDF onto the agreement PDF
def overlay_pdf(agreement_pdf_path, signature_pdf_path, output_pdf_path, x_position, y_position):
    agreement_pdf = pdfrw.PdfReader(agreement_pdf_path)
    signature_pdf = pdfrw.PdfReader(signature_pdf_path)

    signature_page = signature_pdf.pages[0]
    signature_page.MediaBox = agreement_pdf.pages[0].MediaBox

    # Add signature to each page of the agreement PDF at the specified position
    for page in agreement_pdf.pages:
        pdfrw.PageMerge(page).add(signature_page, x=x_position, y=y_position).render()

    # Save the output PDF
    pdfrw.PdfWriter().write(output_pdf_path, agreement_pdf)

# Convert PDF to image
def pdf_to_image(pdf_path, image_path):
    images = convert_from_path(pdf_path)
    images[0].save(image_path, 'JPEG')

#get most recent file in a folder

def get_most_recent_file(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return None
    return os.path.join(folder_path, max(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x))))


