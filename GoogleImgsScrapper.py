import discord
from discord.ext import commands
#parser
import requests
from bs4 import BeautifulSoup
# to work with apikeys.txt
import os
import time

print("Created by Lalo'fik: discord: Lalo'fik#0443, telegram: Sam_lutiv, GitHub: SememN")
print("Welcome to Google images scrapper!\nДобро пожаловать в парсер гугл картинок!")
TOKEN = input("Input your discord token: \nВведите свой токен: ")
print("The bot command structure is .find <tag>, so just print it in your discord channel and enjoy!\nКоманда для запуска бота в дискорде: .find <тэг_для_поска>, удачи в использовании!")
print("I'm sorry to Google for creating tis script, but it won't use in commercial purposes!\nПрошу прощения у Google за создания и использования этого скрипта! Он не будет ипользоваться в коммерческих целях!")


#this func used in get_all_links 
def get_links(objectToParse):
    #list to save link for download
    pageLinks = []

    #searching for img's links to download
    imgs = objectToParse.find_all("img")
    for img in imgs:
        try:
            pageLinks.append(img["data-src"])
        except KeyError:
            pass

    return pageLinks

#getting all imgs from current search
def get_all_imgs(*args):
        links = []
        result = requests.get("https://www.google.com/search?q=" + args[0] + "&client=opera-gx&hs=t8v&sxsrf=ALeKk01_A8bqk0jm8coIYEsG5Vk3SKGq9Q:1592479790298&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjzitnBoYvqAhVGxKYKHVnoB44Q_AUoAXoECBkQAw&biw=1879&bih=939&sfr=vfe&safe=images")
        parseObj = BeautifulSoup(result.text, "html.parser")
        pageLinks = get_links(parseObj)
        for link in pageLinks:
            links.append(link)

        return links

def save_img(tag, linksList):
    cwd = os.getcwd()
    os.mkdir(tag)
    count = 0

    for link in linksList:
        print("making request...")
        response = requests.get(link)
        print("downloading...")
        file = open(cwd + "\\" + tag + "\\" + str(count) +".jpg", "wb")
        file.write(response.content)
        file.close()
        print("succesfully downloaded!")
        count += 1

    print("end")

#creating bot
bot = commands.Bot(command_prefix=".", self_bot=True)

#Main bot command. Manipulating the whole script
@bot.command()
async def find(ctx, *args):
    allLinks = get_all_imgs(*args)
    save_img(args[0], allLinks)
    await ctx.send("You could send next request after 10 sec!")
    time.sleep(10)
    await ctx.send("New request is available!")
    
bot.run(TOKEN, bot=False)