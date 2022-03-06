import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from discord.ext import commands
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
from datetime import date
import smtplib, ssl
import html
import datetime


DnT = datetime.datetime.now()
current_date_time = DnT.strftime("%Y-%m-%d %H:%M:%S")
smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = ""
receiver_email = ""
password = ""

# Create a secure SSL context
context = ssl.create_default_context()


proxy = {

}

productSKUs_monitored = {
    # "314102018604":"https://www.footlocker.sg/en/p/jordan-1-retro-high-og-men-shoes-81697?v=314102018604", #smokegreys
    # # "315345819502":"https://www.footlocker.sg/en/p/jordan-1-retro-high-og-women-shoes-80785?v=315345819502", #snakeskin
    # "314101980804":["https://www.footlocker.sg/en/p/jordan-1-retro-high-og-men-shoes-81697?v=314101980804",[]], #biohacks
    # "315345835102":["https://www.footlocker.sg/en/p/jordan-1-mid-women-shoes-78632?v=315345835102",[]],
    # "314102456804":"https://www.footlocker.sg/en/p/jordan-1-retro-high-og-co-jp-men-shoes-107141?v=314102456804", #co.japan
    # "314101533504":"https://www.footlocker.sg/en/p/jordan-1-retro-high-og-men-shoes-68433?v=314101533504", #royaltoe
    # "315550548002":"https://www.footlocker.sg/en/p/adidas-yeezy-slide-women-flip-flops-and-sandals-107304?v=315550548002" #yeezyslides
    # "315345835102":["https://www.footlocker.sg/en/p/jordan-1-mid-women-shoes-78632?v=315345835102",[]] #test product 1
    # "314207796104":["https://www.footlocker.sg/en/p/adidas-yeezy-boost-350-v2-eu36-47-men-shoes-100974?v=314207796104",[]],
    # "315240803502":["https://www.footlocker.sg/en/p/adidas-nite-jogger-x-ivy-park-women-shoes-109988?v=315240803502",[]],
    # "314108444804":["https://www.footlocker.sg/en/p/jordan-1-retro-high-og-men-shoes-81697?v=314108444804",[]]
    "314208908104":["https://www.footlocker.sg/en/p/adidas-ultraboost-22-heat-rdy-men-shoes-128478?v=314208908104",[]]
    # "314101197904":["https://www.footlocker.sg/en/p/nike-kobe-v-protro-men-shoes-88424?v=314101197904",[]], #kobe big stage
    # "314101048404":"https://www.footlocker.sg/en/p/nike-kobe-protro-5-men-shoes-83017?v=314101048404", #kobe lakers
    # "315345834402":"https://www.footlocker.sg/en/p/jordan-1-mid-women-shoes-78632?v=315345834402" #test prodcut 2
    # "314100492504":["https://www.footlocker.sg/en/p/jordan-1-retro-high-og-men-shoes-65494?v=314100492504",[]], #bloodline
    # "314100493304":["https://www.footlocker.sg/en/p/jordan-1-mid-men-shoes-49357?v=314100493304",[]], #mid smoke greys
    # "316701094704":["https://www.footlocker.sg/en/p/jordan-1-retro-high-grade-school-shoes-83023?v=316701094704",[]], #pinegreen gs
    # "314108304404":["https://www.footlocker.sg/en/p/jordan-1-low-men-shoes-4102?v=314108304404",[]], #aj1 low smoke grey
    # "316702039104":["https://www.footlocker.sg/en/p/jordan-1-low-grade-school-shoes-49733?v=316702039104",[]]
}



while True:
    print("Sleeping for 60s...")
    sleep(5)


    try:
        #loops through every SKU, if SKU has stock,send webhook and email,if not, continue looping until all SKU is finished. Once finished, restart whole loop from first SKU again.
        for sku in productSKUs_monitored:

            print(sku)
            productURL = productSKUs_monitored[sku][0]
            productData = requests.get(productURL)
            print(productData)
            soup2 = BeautifulSoup(productData.content, 'html.parser')
            product_name = soup2.find('span', itemprop='name')
            price = soup2.find("meta", itemprop="price")


            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
                "referer": "%s" % productSKUs_monitored[sku][0]
            }

            inventory_data = requests.get("https://www.footlocker.sg/INTERSHOP/web/FLE/FootlockerAsiaPacific-Footlocker_SG-Site/en_GB/-/SGD/ViewProduct-ProductVariationSelect?BaseSKU=" + sku + "&InventoryServerity=ProductDetail",headers=headers)
            data = inventory_data.json()

            data2 = (data['content'])
            print(data2)


            soup = BeautifulSoup(data2, "html.parser")
            productsizeData = soup.find('div', {'data-ajaxcontent': 'product-variation-%s'% sku})
            stockData = productsizeData.get("data-product-variation-info-json")
            stockDatajson = json.loads(stockData)
            stockDataList = productSKUs_monitored[sku][1]

            sizeList = []
            newStockList = []
            for x in stockDatajson:
                newStockList.append(stockDatajson[x]['inventoryLevel'])
                sizeList.append(stockDatajson[x]['sizeValue'])

            print(stockDataList)
            print("Showing new stock list")
            print(newStockList)

            if newStockList != stockDataList:
                for x in stockDatajson:
                    stockDataList.append(stockDatajson[x]['inventoryLevel'])



                try:
                    webhook = DiscordWebhook(url='')
                    embed = DiscordEmbed(title="%s" % product_name.text,
                                         description="*Product stock **UPDATED***",
                                         url="%s" % productSKUs_monitored[sku][0],
                                         color=65280)
                    embed.set_author(name="AdenAIO Monitors", icon_url="https://i.imgur.com/VjQYSHz.png")

                    embed.add_embed_field(name="SKU: ",
                                          value="%s" % sku, inline=False)
                    try:
                        embed.add_embed_field(name="Price: ",
                                              value="%s" % price.text, inline=True)


                    except AttributeError:
                        embed.add_embed_field(name="Price: ",
                                              value="NOT AVAILABLE", inline=True)

                    embed.add_embed_field(name="**Available Sizes**",
                                          value="** **", inline=False)
                    for _,stockcolor in zip((range(len(sizeList))),newStockList):
                        if stockcolor == "GREEN":
                            embed.add_embed_field(name="** **", value=":green_square: -- US " + "%s" % sizeList[_], inline=False)
                        elif stockcolor == "YELLOW":
                            embed.add_embed_field(name="** **", value=":yellow_square: -- US " + "%s" % sizeList[_], inline=False)
                        elif stockcolor == "RED":
                            embed.add_embed_field(name="** **", value=":red_square: -- US " + "%s" % sizeList[_], inline=False)

                    embed.set_thumbnail(url="https://images.footlocker.com/is/image/FLEU/" + sku + "?wid=232&hei=232")

                    embed.set_footer(text="AdenAIO Monitors • %s" % current_date_time)

                    webhook.add_embed(embed)

                    webhook.execute()
                    print("Webhook sent successfully.")

                except Exception:
                    print(Exception)





    except Exception:
        webhook = DiscordWebhook(url='')
        embed = DiscordEmbed(title="Footlocker SG Monitor",
                             description="*Unable to get sizes. Retrying again in 60s...*",
                             color=65280)
        webhook.add_embed(embed)

        webhook.execute()

