# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 15:22:41 2020

@author: brian
functions are from: https://www.thepythoncode.com/code/download-web-page-images-python
"""
import datetime
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
    
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(url, img_url)
        # remove URLs like '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    return urls
    
def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)

    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))

    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])

    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))

def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each img, download it
        download(img, path)
    
if __name__ == "__main__":
    import json
    
    source = json.load(open("ix.json",'r', encoding='utf-8'))
    ixp_list = source['data']
    ixp_url_stats_list = []
    ixp_name_list = []
    x = datetime.datetime.now()
    
    ixp_whitelist = [
        'angonix', 
        'ANIX - Albanian Neutral Internet eXchange', 
        'ArmIX', 
        'BALT-IX', 
        'BCIX', 
        'B-IX', 
        'BKNIX', 
        'CAIX', 
        'ChIX', 
        'CIX', 
        'CNX', 
        'DE-CIX Dallas', 
        'DE-CIX Delhi', 
        'DE-CIX Frankfurt',
        'DE-CIX Hamburg', 
        'DE-CIX Istanbul',
        'DE-CIX Kolkata', 
        'DE-CIX Madrid', 
        'DE-CIX Marseille', 
        'DE-CIX Mumbai', 
        'DE-CIX Munich', 
        'DE-CIX New York', 
        'DE-CIX Palermo', 
        'EPIX.Katowice', 
        'EPIX.Warszawa-KIX', 
        'EVIX', 
        'GrenoblIX', 
        'Hopus', 
        'HOUIX', 
        'IIX-Bali', 
        'IIX-Jogja', 
        'IX.br (PTT.br) Belém',
        'IX.br (PTT.br) Belo Horizonte',
        'IX.br (PTT.br) Brasília',
        'IX.br (PTT.br) Campina Grande',
        'IX.br (PTT.br) Campinas',
        'IX.br (PTT.br) Campo Grande',
        'IX.br (PTT.br) Cascavel',
        'IX.br (PTT.br) Caxias do Sul',
        'IX.br (PTT.br) Cuiabá',
        'IX.br (PTT.br) Curitiba',
        'IX.br (PTT.br) Florianópolis',
        'IX.br (PTT.br) Fortaleza',
        'IX.br (PTT.br) Foz do Iguaçu',
        'IX.br (PTT.br) Goiânia',
        'IX.br (PTT.br) João Pessoa',
        'IX.br (PTT.br) Lajeado',
        'IX.br (PTT.br) Londrina',
        'IX.br (PTT.br) Maceió',
        'IX.br (PTT.br) Manaus',
        'IX.br (PTT.br) Maringá',
        'IX.br (PTT.br) Natal',
        'IX.br (PTT.br) Porto Alegre',
        'IX.br (PTT.br) Recife',
        'IX.br (PTT.br) Rio de Janeiro',
        'IX.br (PTT.br) Salvador',
        'IX.br (PTT.br) Santa Maria',
        'IX.br (PTT.br) São José do Rio Preto',
        'IX.br (PTT.br) São José dos Campos',
        'IX.br (PTT.br) São Luís',
        'IX.br (PTT.br) São Paulo',
        'IX.br (PTT.br) Teresina',
        'IX.br (PTT.br) Vitória',
        'IX.LODZ.PL', 
        'IXPN Lagos', 
        'JPIX OSAKA', 
        'JPIX TOKYO', 
        'JPNAP Osaka', 
        'JPNAP Tokyo', 
        'KAZ-GOV-IX', 
        'LONAP', 
        'LyonIX', 
        'MASS-IX', 
        'MICE', 
        'MIX-IT', 
        'MUS-IX', 
        'NetIX', 
        'NYIIX', 
        'NYIIX Los Angeles', 
        'NYIIX Philadelphia', 
        'PhOpenIX-Manila',
        'QIX', 
        'RED-IX', 
        'RIX', 
        'SAIX', 
        'SGIX', 
        'SIX Seattle', 
        'SIX Seattle (Jumbo)', 
        'SIX SI', 
        'STHIX - Gothenburg', 
        'STHIX - Stockholm', 
        'STHIX - Sundsvall', 
        'STHIX - Umeå', 
        'TahoeIX', 
        'TIX Tanzania - Dar es Salaam', 
        'TN-IX', 
        'TorIX', 
        'TPIX Warsaw', 
        'TWIX', 
        'UAE-IX', 
        'UA-IX', 
        'VarnaIX',
        'YAR-IX'
        'YEGIX', 
        'YXEIX', 
        'YYCIX'
        ]
    
    for dict_entry in ixp_list:
        if dict_entry['url_stats'] != '' and is_valid(dict_entry['website']) is not False and dict_entry['name'] in ixp_whitelist:
            try:
                ixp_url_stats_list.append(dict_entry['url_stats'])
                ixp_name_list.append(dict_entry['name'])
                main(dict_entry['url_stats'],  x.strftime("%Y") + '-' + x.strftime("%m") + '-' + x.strftime("%d") + ' ' + dict_entry['name'])
            except:
                pass
            
            
    print("Scraping completed.")
        
        