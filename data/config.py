BOT_TOKEN = '2139729122:AAF5KFfdWDB_EYDkgekPTZjifDWA3UWouCY'
NOTIFICATION_WAIT = 60*60   # 1 час
PARSER_WAIT = 60*10   # 5 минут

faculty_encode = {
    "faculty": {
        "ивмиит": 9
    },
    "speciality": {
        "би": 203,
        "иб": 369,
        "пи": 1084,
        "пми": 166,
        "фиит": 167,
        "ист": 370,
        "пм": 559
    },
    "inst": {
        "кфу": 0 
    },
    "category":{
        'бюджет':1,
        'внебюджет':0
    }
}

snils_pattern = r'^\d{3}-\d{3}-\d{3}-\d{2}$'
kfu_id_patter = r'^\d{6}$'