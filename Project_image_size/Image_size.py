from PIL import Image

Img = Image.open('Input.jpg')

Resize = Img.resize((900, 300), resample=Image.Resampling.LANCZOS)

Resize.save('Output.jpg')

print("Image is resized and saved as output.jpg")