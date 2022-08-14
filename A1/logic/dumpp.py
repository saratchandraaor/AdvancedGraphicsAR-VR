from PIL import Image,ImageDraw,ImageFont

image = Image.new("RGBA", (600,150), (255,255,255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", 12)

draw.text((10, 0), "Hello", (0,0,0), font=font)
img_resized = image.resize((188,45), Image.ANTIALIAS)