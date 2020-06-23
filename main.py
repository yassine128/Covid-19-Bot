import discord
import random
from discord.ext import commands
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
import COVID19Py
import sched, time
import keep_alive
import warnings
warnings.filterwarnings('ignore')


client = discord.Client()
@client.event #event decorator/wrapper
async def on_ready():
    print(f"We have logged in as {client.user}")
    await client.change_presence(activity=discord.Game(name='Type !chelp to see the functions')) 


@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    random_case = random.randint(1,10)
    #PRENDRE LE FICHIER
    coronavirus = pd.read_csv('covid_data.csv')
    #coronavirus.head()


    #TRAITER LE FICHIER ET SUPPRIMER LES (DATA) INUTILES
    #coronavirus['death'] = coronavirus['death'].astype('Int64')
    #coronavirus['age'] = coronavirus['age'].astype('Int64')
    coronavirus = coronavirus[['gender', 'age', 'death', 'symptom']]
    coronavirus = coronavirus[coronavirus['gender'].notna()]
    coronavirus = coronavirus[coronavirus['age'].notna()]
    coronavirus['gender'].replace(['male', 'female'], [0, 1], inplace=True)
    #coronavirus.tail()

    symptom = coronavirus['symptom']
    coronavirus['symptom'] = symptom[symptom != 0] = 1
    symptom.tail()
    coronavirus.tail()

    #REMPLACER TOUTES LES MAUVAISES (DATA) PAR 1
    coronavirus['death'].replace(['2/21/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/21/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/19/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/19/2020'], [1], inplace=True)
    coronavirus['death'].replace(['02/01/20'], [1], inplace=True)
    coronavirus['death'].replace(['2/27/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/25/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/22/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/24/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/23/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/26/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/23/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/23/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/23/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/25/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/27/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/26/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/28/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/13/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/26/2020'], [1], inplace=True)
    coronavirus['death'].replace(['2/14/2020'], [1], inplace=True)

    #Besoin de (sex), (age), (death)
    from sklearn.neighbors import KNeighborsClassifier

    y = coronavirus['death']
    y=y.astype('int')
    X = coronavirus.drop('death', axis=1)
    X=X.astype('int')

    #ENTRAINER LE MODÈLE
    model = KNeighborsClassifier()
    model.fit(X, y)
    model.score(X, y)

    gender = 0 
    age = 0
    if message.content.startswith("cursed is a bitch"):
        await message.channel.send("Shut your bitch ass up. Cursed is the best :relieved:")
    if message.content.startswith("!cnews"):
        covid19 = COVID19Py.COVID19(data_source="jhu")
        latest = covid19.getLatest()
        latest.pop("recovered")
        for x in list(latest)[0:2]:
          data = (" {}: {} ".format(x,  latest[x]))
          await message.channel.send(str(data))
    if message.content.startswith("!creator"):
        await message.channel.send("```Created by Yassine Seddaoui aka Cursedbuddy#3572```")
    #if message.content.startswith("!cnews"):
        #await message.channel.send(f"Updated every day!\n```Total Confirmed: 1,014,673  \nTotal Deaths: 52,973\nTotal Recovered: 210,335```\nData from: https://bit.ly/2IYWbIx")
    if message.content.startswith("!chelp"):
        await message.channel.send("```For news: !cnews \n To make a prediction: !cpredic <gender> <age> <symptoms [yes/no]> \n Contact the creator: !creator```")
    if message.content.startswith("!cupbot"):
        await message.channel.send("The bot is up")
    if message.content.startswith("!cpredic"):
        text = message.content.split()
        #await message.channel.send(text)
        if text[1] == "male" and text[3] == "no":
            gender = 0
            age = text[2]
            symptom = 0
            x = np.array([gender, age, symptom]).reshape(1, 3)
            predic = model.predict(x)
            test = model.predict_proba(x).T
            survive = test.item(0)
            die = test.item(1)
            survive_text = str(survive*100)
            die_text = str(die*100)
            if predic == 0:
                #text0 = "You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying"
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
            if predic == 1:
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
                #await message.channel.send("You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying")
        if text[1] == "male" and text[3] == "yes":
            gender = 0
            age = text[2]
            symptom = 1
            x = np.array([gender, age, symptom]).reshape(1, 3)
            predic = model.predict(x)
            test = model.predict_proba(x).T
            survive = test.item(0)
            die = test.item(1)
            survive_text = str(survive*100-random_case)
            die_text = str(die*100+random_case)
            if predic == 0:
                #text0 = "You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying"
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
            if predic == 1:
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
                #await message.channel.send("You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying") 
        if text[1] == "female" and text[3] == "no":
            gender = 1
            age = text[2]
            symptom = 0
            x = np.array([gender, age, symptom]).reshape(1, 3)
            predic = model.predict(x)
            test = model.predict_proba(x).T
            survive = test.item(0)
            die = test.item(1)
            survive_text = str(survive*100)
            die_text = str(die*100)
            if predic == 0:
                #text0 = "You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying"
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
            if predic == 1:
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
                #await message.channel.send("You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying")
        if text[1] == "female" and text[3] == "yes":
            gender = 1
            age = text[2]
            symptom = 1
            x = np.array([gender, age, symptom]).reshape(1, 3)
            predic = model.predict(x)
            test = model.predict_proba(x).T
            survive = test.item(0)
            die = test.item(1)
            survive_text = str(survive*100-random_case)
            die_text = str(die*100+random_case)
            if predic == 0:
                #text0 = "You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying"
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
            if predic == 1:
                await message.channel.send("<@"+str(message.author.id)+">\n```You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying```")
                #await message.channel.send("You have " + str(survive_text) + " % chance of surviving and " + str(die_text) + " % chance of dying")
keep_alive.keep_alive()
client.run("<your token>")
