from PIL import Image
import easyocr
import requests
from discord_webhook import DiscordWebhook,DiscordEmbed
import time
import pyautogui
import json
import os.path

def postMessageDiscord(embed):
    webhook = DiscordWebhook(url=config['discordWebhook'])
    with open("./cropped.png", "rb") as f:
        webhook.add_file(file=f.read(), filename=f"{currValueEuro}_{config['fiat']}.png")
    embed.set_image(url=f"attachment://{currValueEuro}_{config['fiat']}.png")
    webhook.add_embed(embed)
    webhook.execute()

def getBalance():
    isFloatable = False
    while isFloatable == False:
        # Create reader object for English language
        reader = easyocr.Reader(['en'],verbose=False)
        # Load the image from file
        image_path = './screen.png'
        pyautogui.screenshot().save('screen.png')
        image = Image.open(image_path)
        width, height = image.size
        # Define the coordinates of the top right corner
        x_left, y_top, x_right, y_bottom = width-200, 27, width, 58
        # Crop the image to the specified coordinates
        cropped_image = image.crop((x_left, y_top, x_right, y_bottom))
        cropped_image.save("cropped.png")
        # Perform OCR on the cropped image using easyocr
        results = reader.readtext("./cropped.png")
        # Extracting text from the results
        ocr_text = " ".join([result[1] for result in results])
        tmpTxt = ocr_text.strip().replace("ETCPOW Balance: ","")
        try:
            tmpTxt = float(tmpTxt)
            isFloatable = True
        except Exception as e:
            print(e)
            time.sleep(10)
    return tmpTxt

def convertToEuro(balance):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids=etcpow&vs_currencies={config['fiat']}"
        response = requests.get(url)
        eurValue = float(response.json()["etcpow"][config['fiat']])
    except:
        eurValue = coursActuel
    return round(balance*eurValue,3),eurValue

if __name__ == "__main__":
    if os.path.isfile("./config.json") :
        with open("./config.json","r") as f:
            config = json.load(f)
    else:
        availableFiat = ["usd","aud","brl","cad","chf","clp","cny","eur","gbp"]
        config = {}
        currFiat = "none"
        while currFiat not in availableFiat:
            print("Please enter the name of the fiat you want the price to be converted")
            currFiat = input(f"Available fiats {availableFiat} :")
        config["fiat"] = currFiat
        config["discordWebhook"] = input("Enter the link of discord webhook : ")
        currDelay = 0
        while currDelay == 0 :
            try:
                tmpDelay = input("Please enter the refresh time in minutes : ")
                currDelay = float(tmpDelay)*60
            except Exception as e:
                print(e)
        config["delay"] = currDelay
        with open("./config.json", "w") as fp:
            json.dump(config,fp,indent=4)
    while True:
        currBalanceETC = getBalance()
        currValueEuro,coursActuel = convertToEuro(currBalanceETC)
        if float(currBalanceETC) >= 100:
            embed = DiscordEmbed(title="YOU CAN WITHDRAW", description=f"**{currValueEuro}€**\r\nActual price : {coursActuel}  {config['fiat']} / ETCPOW")
        else:
            embed = DiscordEmbed(title=f"**{currValueEuro} {config['fiat']}**", description=f"Actual Price : {coursActuel}  {config['fiat']} / ETCPOW")
        postMessageDiscord(embed)
        time.sleep(config["delay"])
