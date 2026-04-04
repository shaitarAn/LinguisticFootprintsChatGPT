from PIL import Image
from fpdf import FPDF

def combine_images_into_pdf(image1_path, image2_path, output_pdf_path):
    # Open the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Resize images to the same height if they are different
    if image1.height != image2.height:
        target_height = min(image1.height, image2.height)
        image1 = image1.resize((int(image1.width * target_height / image1.height), target_height), Image.ANTIALIAS)
        image2 = image2.resize((int(image2.width * target_height / image2.height), target_height), Image.ANTIALIAS)
    
    # Calculate the width of the new image (sum of widths of both images)
    total_width = image1.width + image2.width
    
    # Create a new empty image with a white background
    new_image = Image.new('RGB', (total_width, image1.height), 'white')
    
    # Paste the images into the new image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.width, 0))

    # add a black line between the images
    for i in range(0, new_image.height):
        new_image.putpixel((image1.width, i), (0, 0, 0))
    
    # Save the new image to a temporary file
    temp_image_path = 'temp_combined_image.jpg'
    new_image.save(temp_image_path)
    
    # Create a PDF and add the new image
    pdf = FPDF(unit="pt", format=[new_image.width, new_image.height])
    pdf.add_page()
    pdf.image(temp_image_path, 0, 0, new_image.width, new_image.height)
    
    # Output the PDF
    pdf.output(output_pdf_path, 'F')

# Example usage:
combine_images_into_pdf('../../viz/effect_size/cohen_d_english_2403gpt4.png', '../../viz/effect_size/cohen_d_german_2403gpt4.png', '../../viz/effect_size/cohen_d_2403gpt4.pdf')
