import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import random
import re
from urllib.request import urlretrieve
import os
import subprocess as sp
import ctypes
import configparser
w_list = []
path_w = sp.getoutput("powershell.exe $HOME") + "\Pictures\\"
if os.path.exists(f"{path_w}config_wallapers.ini") == False:
    config_text_size = "#Choose your size:\n#240x320, 240x400, 320x240, 320x480, 360x640\n#480x800, 480x854, 540x960, 720x1280, 800x600\n#800x1280, 960x544, 1024x600, 1080x1920, 2160x3840\n#1366x768, 1440x2560, 800x1200, 800x1420, 938x1668\n#1280x1280, 1350x2400, 2780x2780, 3415x3415, 1024x768\n#1152x864, 1280x960, 1400x1050, 1600x1200, 1280x1024\n#1280x720, 1280x800, 1440x900, 1680x1050, 1920x1200\n#2560x1600, 1600x900, 2560x1440, 1920x1080, 2048x1152\n#2560x1024, 2560x1080"
    config_text_category = "#Choose your category:\n#3d, abstraction, anime, art, vector, cities\n#food, animals, space, love, macro, cars\n#minimalism, motorcycles, music, holidays, nature, miscellaneous\n#words, smilies, sport, textures, dark, technology\n#fantasy, flowers, black"
    config = open(f"{path_w}config_wallapers.ini","w")
    config.write(f"{config_text_size}\n\n{config_text_category}\n\n[Config]\nsize = 1440x900\ncategory = nature")
    config.close()
config_parser = configparser.ConfigParser()
config_parser.read(f"{path_w}config_wallapers.ini")
size = config_parser["Config"]["size"]
category = config_parser["Config"]["category"]
def wallapers_parser():
    #site_number_pars
    URL_p = f"https://wallpaperscraft.ru/catalog/{category}/page1"
    r_p = requests.get(URL_p)
    soup_p = bs(r_p.text, "html.parser")
    vacancies_names_p = soup_p.find('li', class_='pager__item pager__item_last-page').find_all('a', class_='pager__link')
    for name_p in vacancies_names_p:
        p_href_nohttps = name_p.get('href')
        p1_href_nohttps = re.sub(f"/catalog/{category}/page","",p_href_nohttps)
        #print(p1_href_nohttps)    
    site_number = random.randint(1, int(p1_href_nohttps))
    #print(site_number)
    #wallaper_pars
    URL_w = f"https://wallpaperscraft.ru/catalog/{category}/page{site_number}"
    r_w = requests.get(URL_w)
    soup_w = bs(r_w.text, "html.parser")
    vacancies_names_w = soup_w.find_all('a', class_='wallpapers__link')
    for name_w in vacancies_names_w:
        w_href_nohttps = name_w.get('href')
        w1_href_nohttps = re.sub("wallpaper/","",w_href_nohttps)
        w_href_https = "https://images.wallpaperscraft.ru/image/single" + w1_href_nohttps + f"_{size}.jpg"
        w_list.append(w_href_https)
        #print(w_href_https)
    w_list_r = random.choice(w_list)
    urlretrieve(f"{w_list_r}", f"{path_w}wallaper.png")
    #print(w_list_r)
    def set_wallpaper(path):
        cs = ctypes.c_buffer(path.encode())
        SPI_SETDESKWALLPAPER = 0x14
        ctypes.windll.user32.SystemParametersInfoA(20, 0, cs, 3)
    set_wallpaper(f"{path_w}wallaper.png")
wallapers_parser()
