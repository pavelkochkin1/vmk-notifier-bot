from bs4 import BeautifulSoup as BS
import requests
from statistics import median

class VMKtable:
    """Класс который парсит с сайта таблицы и выводит нужные данные по ним."""
    
    def __init__(self):
        self.dictionary = {
            203:{"id":[],"score":[]},
            369:{"id":[],"score":[]},
            559:{"id":[],"score":[]},
            1084:{"id":[],"score":[]},
            166:{"id":[],"score":[]},
            #1508:{"id":[],"score":[]},
            #370:{"id":[],"score":[]}
        }

        self.url = lambda spec: f"https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_faculty=9&p_speciality={spec}&p_inst=0&p_typeofstudy=1"
        self.parser()
        
    def parser(self):
        for spec in self.dictionary.keys():
            site = self.url(spec)
            r = requests.get(site)
            html = BS(r.content, "html.parser")
            table = html.find(id="t_all")
            table = table.find(id="t_common").find_all("tr")
            for row in table[2:]:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                stud = [ele for ele in cols if ele]
                self.dictionary[spec]["id"].append(stud[1])
                self.dictionary[spec]["score"].append(stud[6])
        
    def get_rank(self, id: str, spec: int):
        return self.dictionary[spec]["id"].index(id) + 1

    def get_score(self, id: str, spec: int):
        idx = self.get_rank(id, spec)
        return self.dictionary[spec]["score"][idx - 1]
    
    def get_median_above(self, id: str, spec: int):
        idx = self.get_rank(id, spec)
        return median([int(x) for x in self.dictionary[spec]["score"][:idx-1]])

        