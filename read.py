import os
import re
import json 
import unidecode
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
from slugify import slugify
import codecs


def save_file(filename, content):
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()


def read_esocial_tabelas(path, url):
    url = 'https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-nt-01-2021-html/index.html/tabelas.html#05'

    r = req.get(url)
    r.encoding = r.apparent_encoding
    html_content = r.text

    soup = BeautifulSoup(html_content, "html.parser")
    li = str(soup.find_all("ul", {"class":"sumario"})[0])
    table_names = BeautifulSoup(li, "html.parser").find_all("li")
    table_names = [tn.get_text() for tn in table_names]
    tables = soup.find_all("table", {"class":"table is-fullwidth is-bordered tabela quebra-anterior"})
    
    for n in range(len(table_names)):
        table_name = table_names[n]
        header = 1
        if re.sub('[^0-9]', '', table_name) in ['11', '12', '22',]:
            header = 2
        table = pd.read_html(str(tables[n]), header=header)[0]
        table.columns = [unidecode.unidecode(c).lower() for c in table.columns]
         
        dictionary = {
            'name': table_name, 
            'content': table.to_dict(orient='records')}


        if not os.path.exists(path):
            os.makedirs(path)
                
        json_object = json.dumps(dictionary, indent = 4, ensure_ascii=False)
        filename = os.path.join(path, '{}.json'.format(slugify(table_name)))
        save_file(filename, json_object)


if __name__ == "__main__":
    eventos = [
        ['v_S_01_00_00', 
         'https://www.gov.br/esocial/pt-br/documentacao-tecnica/leiautes-esocial-nt-01-2021-html/index.html/tabelas.html'],
    ]
    for evt in eventos:
        read_esocial_tabelas(evt[0], evt[1])


