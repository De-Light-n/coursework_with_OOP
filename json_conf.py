import json
import requests
from bs4 import BeautifulSoup


def getUniversities():
    with open(
        "C:\Projects\curse 2\coursework_with_OOP\educational_institutions.json",
        "r",
        encoding="utf-8",
    ) as f:
        current = json.load(f)

    new_json = {item["university_id"]: item for item in current}

    with open("new_data.json", "w", encoding="utf-8") as f:
        json.dump(new_json, f, ensure_ascii=False, indent=4)


def getSpecialities():
        try:
            response = requests.get("https://abiturients.info/uk/catalog-specialties-new")
            specialities_dict = {}

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                main_container = soup.find("div", attrs={"id": "main"})

                headers = main_container.find_all("h3")
                containers = main_container.find_all("span", attrs={"class": "field-content"})

                # Створюємо список галузей зі значеннями їхніх перших двох цифр
                galuz = []
                for header in headers:
                    galuz_text = header.get_text(strip=True)
                    galuz_id = galuz_text.split()[0]  # Отримуємо перші дві цифри галузі
                    galuz.append((galuz_id, galuz_text))

                # Проходимо по кожній спеціальності
                for container in containers:
                    element = container.find("a")
                    if element:
                        speciality_text = element.get_text(strip=True)
                        speciality_id = speciality_text.split()[0]  # Отримуємо перші три цифри спеціальності

                        # Знаходимо відповідну галузь за першими двома цифрами спеціальності
                        speciality_galuz_id = speciality_id[:2]
                        corresponding_galuz = next((g[1] for g in galuz if g[0] == speciality_galuz_id), "Невідома галузь")

                        # Додаємо спеціальність до словника
                        specialities_dict[speciality_id] = {
                            "id": speciality_id,
                            "speciality": speciality_text,
                            "galuz": corresponding_galuz
                        }

                with open("specialities.json", "w", encoding="utf-8") as f:
                    json.dump(specialities_dict, f, ensure_ascii=False, indent=4)
            else:
                print(f"Request failed with status code {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    getSpecialities()
