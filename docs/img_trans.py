from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

img = r'C:\Users\mstyx\Anchor\development_management_platform\docs\mountain-landscape-first-person-illustration-vector.jpg'

img = Image.open(img)
font_pth = r'C:\Windows\Fonts\calibri.ttf'
font = ImageFont.truetype(font_pth,80)

img_draw = ImageDraw.Draw(img)

img_draw.text((0,0),'Development Manager',(8, 31, 46),font)
img.save(r'C:\Users\mstyx\Anchor\development_management_platform\docs\dmp_head.jpg')