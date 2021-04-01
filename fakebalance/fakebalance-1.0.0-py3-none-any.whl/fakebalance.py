"""
    Типа TO-DO:
        - Разбиение баланса на условные 2 639,22, при вводимых 2639.22 
        - Сука разобраться в этом ебанном ООП
        - Сделать время 
        - Сделать последние 4 цифры карты 
        - Наконец-то прочитать PEP 8 )0))

    > Начало: 31.03.2021    

"""
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


class Balance:

    def __init__(
            self, balance="", filename="fake_balance.jpg",
            time=datetime.strftime(datetime.now(), "%H:%M"), # current time
            card="", show=False, currency="RUB") -> str:
        
        self.balance = balance
        self.filename = filename
        self.time = time
        self.card = card
        self.show = show
        self.currency = currency


    def sberbank(self):  
        # Opening a template drawing
        image = Image.open("templates/sber.jpg")

        # fonts
        font = ImageFont.truetype(r"fonts/sf-ui-display-medium.ttf", 27) 
        font_card = ImageFont.truetype(r"fonts/sf-ui-display-medium.ttf", 18) 
        font_time = ImageFont.truetype(r"fonts/Roboto-Light.ttf", 18) 
        
        # drawing
        d = ImageDraw.Draw(image)
        d.text((89,475), text = self.balance + " ₽", font=font, fill=(252,252,252,128))
        d.text((26,10), text = self.time, font=font_time, fill=(252,252,252,128))
        d.text((438,448), text = self.card, font=font_card, fill=(114,114,114,128))

        if self.show == True:
            image.show()

        image.save(self.filename)


    def qiwi(self):
        image =  Image.open("templates/qiwi.jpg")

        font = ImageFont.truetype(r"fonts/Roboto-Bold.ttf", 85)
        font_time = ImageFont.truetype(r"fonts/Roboto-Light.ttf", 34)

        d = ImageDraw.Draw(image)
        d.text((280,290), text = self.balance + " ₽", font=font, fill=(255,252,252,128)) 
        d.text((45,15), text = self.time, font=font_time, fill=(252,252,252,128)) 
        
        if self.show == True:
            image.show()

        image.save(self.filename)
 

       