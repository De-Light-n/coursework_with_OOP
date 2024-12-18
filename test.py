import time
from faker import Faker
import random
from bridge import Bridge

# Ініціалізація Faker з українською локалізацією
fake = Faker('uk_UA')

# Функція для створення фейкової бази даних університетів
def generate_fake_universities(num_records):
    universities = []
    for _ in range(num_records):
        universities.append({
            "university_id": str(random.randint(0, 10000)),
            "university_name": fake.company(),
            "region_name_u": fake.region(),
        })
    return universities

# Генерація фейкових даних
num_records = 100000  # Кількість записів
universities = generate_fake_universities(num_records)

# Ініціалізація класу Bridge
bridge = Bridge()

# Тестування сортування
sort_type = 1  
print(f"Тестування сортування для {num_records} записів...")
start_time = time.time()
sorted_ids = bridge.bridge_sort_universities(universities, sort_type)
end_time = time.time()
print(f"Сортування завершено за {end_time - start_time:.2f} секунд.")

# Тестування пошуку
query = fake.company().split()[0]  # Використання частини випадкової назви компанії для пошуку
print(f"Тестування пошуку для {num_records} записів з запитом: {query}")
start_time = time.time()
matched_ids = bridge.bridge_search_universities(universities, query)
end_time = time.time()
print(f"Пошук завершено за {end_time - start_time:.2f} секунд.")

# Друк результатів
print(f"Знайдено {len(matched_ids)} збігів для запиту '{query}'")
