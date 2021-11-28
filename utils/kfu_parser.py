from bs4 import BeautifulSoup as BS
import requests
from statistics import median

class VMKtable:
    """Класс который парсит с сайта таблицы и выводит нужные данные по ним."""
    
    def __init__(self):
        self.dictionary = {
            203:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            369:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            559:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            1084:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            166:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            167:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}},
            370:{1:{"id":[],"score":[]}, 2:{"id":[],"score":[]}}
        }
        self.url = lambda spec, type: f"https://abiturient.kpfu.ru/entrant/abit_entrant_originals_list?p_open=&p_typeofstudy=1&p_faculty=9&p_speciality=" + str(spec) + "&p_inst=0&p_category=" + str(type)
        self.parser()
        
    def parser(self):
        for spec, _ in self.dictionary.items():
            for type, _ in self.dictionary[spec].items():
                site = self.url(spec, type)
                r = requests.get(site)
                html = BS(r.content, "html.parser")
                table = html.find("table", {"id":"t_common"})
                if table.find_all("tr"):
                    for row in table.find_all("tr")[2:]:
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]
                        stud = [ele for ele in cols if ele]
                        self.dictionary[spec][type]["id"].append(str(stud[1]))
                        self.dictionary[spec][type]["score"].append(str(stud[6]))
        
    def get_rank(self, id: str, spec: int, budget: bool):
        if budget:
            return self.dictionary[spec][1]["id"].index(str(id)) + 1
        return self.dictionary[spec][2]["id"].index(str(id)) + 1

    def get_score(self, id: str, spec: int, budget: bool):
        idx = self.get_rank(id, spec, budget)
        if budget:
            return self.dictionary[spec][1]["score"][idx - 1]
        return self.dictionary[spec][2]["score"][idx - 1]
    
    def get_median_above(self, id: str, spec: int, budget: bool):
        idx = self.get_rank(id, spec, budget)
        if budget and idx != 1:
            return median([int(x) for x in self.dictionary[spec][1]["score"][:idx-1]])
        elif idx != 1:
            return median([int(x) for x in self.dictionary[spec][2]["score"][:idx-1]])
        else:
            return -1

        