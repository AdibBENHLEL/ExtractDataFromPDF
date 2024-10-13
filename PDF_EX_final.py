import fitz  # PyMuPDF
from PIL import Image
import os

def extract_screenshots_combined(pdf_path, output_folder, coordinates):
    """
    Extracts multiple screenshots from specific areas of a PDF page and combines them into a single image.
    Args:
        pdf_path (str): Path to the PDF file.
        output_folder (str): Path to the folder where the combined image will be saved.
        coordinates (list of tuples): List of tuples, each containing (x1, y1, x2, y2) coordinates for areas to capture.
    """
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)  # Load the first page
    pix = page.get_pixmap()

    # Convert Pixmap to PIL Image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # List to store cropped images
    cropped_images = []

    # Crop images based on coordinates
    for (x1, y1, x2, y2) in coordinates:
        cropped_img = img.crop((x1, y1, x2, y2))
        cropped_images.append(cropped_img)

    # Determine the size of the combined image
    total_width = max(cropped_img.width for cropped_img in cropped_images)
    total_height = sum(cropped_img.height for cropped_img in cropped_images)

    # Create a new blank image to combine the cropped images
    combined_img = Image.new('RGB', (total_width, total_height))

    # Paste the cropped images into the combined image
    y_offset = 0
    for cropped_img in cropped_images:
        combined_img.paste(cropped_img, (0, y_offset))
        y_offset += cropped_img.height

    # Generate output filename with page number
    output_filename = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_combined.png"
    output_path = os.path.join(output_folder, output_filename)

    # Save the combined image
    combined_img.save(output_path)

if __name__ == "__main__":
    # Specify folder containing PDFs
    pdf_folder = "C:/Users/SomeTwo/Desktop/exaract data from pdf/files"

    # Specify folder to save combined screenshots
    output_folder = "C:/Users/SomeTwo/Desktop/exaract data from pdf/output"

    # Define coordinates of the areas to capture (replace with your values)
    coordinates = [
        (90, 10, 680, 200),  # Area 1 (top)
        (90, 700, 680, 800)  # Area 2 (bottom)
    ]

    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each PDF in the folder
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            extract_screenshots_combined(pdf_path, output_folder, coordinates)
    print("Combined screenshots extracted successfully!")
