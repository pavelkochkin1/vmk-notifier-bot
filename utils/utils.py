from data.config import faculty_encode
from loader import Table, BotDB
from data.config import snils_pattern, kfu_id_patter
import re

# проверить является ли входной id СНИЛСом или id с сайта КФУ
def is_valid_id(user_id: str) -> bool:
    return re.match(snils_pattern, user_id) or re.match(kfu_id_patter, user_id)

# проверить есть ли уже входные данные регистрации в базе
def is_full_match(input_info: list, info_db: list, tgid: int) -> bool:
    for row in info_db:
        if input_info[1] == row[0] and faculty_encode['speciality'][input_info[2]] == row[2] and tgid == row[1] and faculty_encode['category'][input_info[3]] == row[4]:
            return True
    return False

# раскодировать специальность
def decode_spec(d: dict, value: int) -> str:
    for k, v in d.items():
        if v == value:
            return k

# выводит информацию для пользователя по всем направлениям
def info_message(tgid: int) -> int:
    answer = "📤 Вы в списках:\n"
    res = BotDB.get_info(tgid)
    for row in res:
        id = row[0]
        spec = row[2]
        budget = row[4]
        try:
            rank = Table.get_rank(id, spec, budget)
            median = Table.get_median_above(id, spec, budget)
            answer += f"На направлении {decode_spec(faculty_encode['speciality'], spec)}({decode_spec(faculty_encode['category'], budget)}) вы на {rank} месте.\n"
            answer += f"Средний балл среди поступающих выше вас по списку: {median}\n\n"
        except:
            answer += f"Извините, не смогли найти вас в списках {decode_spec(faculty_encode['speciality'], spec)}({decode_spec(faculty_encode['category'], budget)})\n"
    return answer