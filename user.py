import json
import os

class User:
    def __init__(self, username, password="", filename="users.json"):
        self.filename = filename
        self.username = username
        self.password = password
        self.name = ""
        self.prizvushce = ""
        self.pobatkovi = ""
        self.burthday = ""
        self.phone = ""
        self.email = ""
        self.ukr_lan_score = 0
        self.math_score = 0
        self.history = 0
        self.forth_subject = [0, 0]
        self.creative_concurse = 0
        self.EFVV_score = 0
        self.photo = ""
        self.favorite_institutions = []

        self.load_or_initialize()

    def load_or_initialize(self):
        """Завантажує дані користувача з JSON або ініціалізує нульовими значеннями."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                users_data = json.load(file)
        else:
            users_data = {}

        if self.username in users_data:
            user_data = users_data[self.username]
            if user_data["password"] != self.password:
                raise ValueError("Користувач вже існує або неправильний пароль.")
            self._load_from_dict(user_data)
        else:
            self._initialize_empty()

    def _load_from_dict(self, data:dict):
        """Заповнює поля об'єкта даними зі словника."""
        self.password = data.get("password", "")
        self.name = data.get("name", "")
        self.prizvushce = data.get("prizvushce", "")
        self.pobatkovi = data.get("pobatkovi", "")
        self.burthday = data.get("burthday", "")
        self.phone = data.get("phone", "")
        self.email = data.get("email", "")
        self.ukr_lan_score = data.get("ukr_lan_score", 0)
        self.math_score = data.get("math_score", 0)
        self.history = data.get("history", 0)
        self.forth_subject = data.get("forth_subject", [0, 0])
        self.creative_concurse = data.get("creative_concurse", 0)
        self.EFVV_score = data.get("EFVV_score", 0)
        self.photo = data.get("photo", "")
        self.favorite_institutions = data.get("favorite_institutions", [])

    def _initialize_empty(self):
        """Ініціалізує поля користувача нульовими значеннями."""
        self.name = ""
        self.prizvushce = ""
        self.pobatkovi = ""
        self.burthday = ""
        self.phone = ""
        self.email = ""
        self.ukr_lan_score = 0
        self.math_score = 0
        self.history = 0
        self.forth_subject = [0, 0]
        self.creative_concurse = 0
        self.EFVV_score = 0
        self.photo = ""
        self.favorite_institutions = []

    def save_data(self):
        """Зберігає дані користувача в JSON."""
        data = {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "prizvushce": self.prizvushce,
            "pobatkovi": self.pobatkovi,
            "burthday": self.burthday,
            "phone": self.phone,
            "email": self.email,
            "ukr_lan_score": self.ukr_lan_score,
            "math_score": self.math_score,
            "history": self.history,
            "forth_subject": self.forth_subject,
            "creative_concurse": self.creative_concurse,
            "EFVV_score": self.EFVV_score,
            "photo": self.photo,
            "favorite_institutions": self.favorite_institutions,
        }

        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                users_data = json.load(file)
        else:
            users_data = {}

        users_data[self.username] = data

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(users_data, file, ensure_ascii=False, indent=4)
