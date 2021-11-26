import sqlite3 as sql

class Database:
    def __init__(self, db_file: str):
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS base (
                    id STRING,
                    tgid INTEGER,
                    speciality STRING,
                    sub_status BOOl
                    )""")
        self.connection.commit()
    
    # добавить пользователя в базу 
    def add_user(self, tgid: id, id: str, speciality: int):
        with self.connection:
            return self.cursor.execute("INSERT INTO base VALUES (?, ?, ?, ?)", (id, tgid, speciality, False, ))

    # проверить есть ли пользователь в базе
    def user_exists(self, tgid: int) -> bool:
        result = self.cursor.execute("SELECT tgid FROM base WHERE tgid = ?", (tgid,))
        return bool(len(result.fetchall()))

    # получить все строчку с подпиской
    def get_subsriptions(self, status: bool = True) -> list:
        with self.connection:
            return self.cursor.execute("SELECT * FROM base WHERE sub_status = ?", (status,)).fetchall()
    
    # обновить поле подписки для пользователя
    def update_sub(self, tgid: int, status: bool = True):
        with self.connection:
            return self.cursor.execute("UPDATE base SET sub_status = ? WHERE tgid = ?", (status, tgid,))
    
    # получить все строчки нужного пользователя
    def get_info(self, tgid: int) -> list:
        result = self.cursor.execute("SELECT * FROM base WHERE tgid = ?", (tgid,))
        return result.fetchall()

    # удалить строчку с определенной специальностью 
    def delete_spec(self, tgid: int, spec: str):
        with self.connection:
            return self.cursor.execute("DELETE FROM base WHERE (tgid, speciality) = (?,?)", (tgid, spec,))

    def close(self):
        self.connection.close()