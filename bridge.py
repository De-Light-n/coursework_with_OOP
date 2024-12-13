import ctypes
from ctypes import POINTER, Structure, c_char_p, c_int
import os
import json


# Завантаження бібліотек
os.add_dll_directory(r"C:\msys64\ucrt64\bin")
lib_sort = ctypes.CDLL('./get_sorted_universities.dll')  # або .dll для Windows
lib_search = ctypes.CDLL('./search_universities.dll')  # Заміна на шлях до вашого DLL-файлу

# Структура University
class University(Structure):
    _fields_ = [
        ("id", c_char_p),
        ("name", c_char_p),
        ("region", c_char_p),
    ]

# Налаштування функцій
lib_sort.sort_universities.argtypes = [POINTER(University), c_int, c_int]
lib_sort.sort_universities.restype = POINTER(ctypes.POINTER(ctypes.c_char))

lib_sort.free_string_array.argtypes = [POINTER(ctypes.POINTER(ctypes.c_char)), c_int]



def bridge_sort_universities(data, sort_type):
    university_array = (University * len(data))(
        *[
            University(
                id=univ["university_id"].encode('utf-8'),
                name=univ["university_name"].encode('utf-8'),
                region=univ["region_name_u"].encode('utf-8'),
            )
            for univ in data
        ]
    )

    # Виклик функції C++
    result = lib_sort.sort_universities(university_array, len(data), sort_type)

    # Отримання результатів
    sorted_ids = [
        ctypes.string_at(result[i]).decode('utf-8') for i in range(len(data))
    ]

    # Звільнення пам'яті
    lib_sort.free_string_array(result, len(data))
    
    return sorted_ids


def sort_universities(sort_type):
    with open("universities.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    university_list = [
        {
            "university_id": value["university_id"],
            "university_name": value["university_name"],
            "region_name_u": value["region_name_u"],
        }
        for key, value in json_data.items()
    ]
    
    sorted_list = bridge_sort_universities(university_list, sort_type)
    return sorted_list

# Налаштування функцій
lib_search.search_universities.argtypes = [POINTER(University), c_int, c_char_p]
lib_search.search_universities.restype = POINTER(ctypes.POINTER(ctypes.c_char))

lib_search.free_string_array.argtypes = [POINTER(ctypes.POINTER(ctypes.c_char)), c_int]

def bridge_search_universities(data, query):
    university_array = (University * len(data))(
        *[
            University(
                id=univ["university_id"].encode('utf-8'),
                name=univ["university_name"].encode('utf-8'),
                region=univ["region_name_u"].encode('utf-8'),
            )
            for univ in data
        ]
    )

    # Виклик функції C++
    result = lib_search.search_universities(university_array, len(data), query.encode('utf-8'))

    # Отримання результатів
    matched_ids = []
    i = 0
    while result[i]:
        matched_ids.append(ctypes.string_at(result[i]).decode('utf-8'))
        i += 1

    # Звільнення пам'яті
    lib_search.free_string_array(result, len(matched_ids))

    return matched_ids

def search_universities(query):
    with open("universities.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    university_list = [
        {
            "university_id": value["university_id"],
            "university_name": value["university_name"],
            "region_name_u": value["region_name_u"],
        }
        for key, value in json_data.items()
    ]
    
    result = bridge_search_universities(university_list, query)
    return result

def search_specialities(query):
    with open("specialities.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    university_list = [
        {
            "university_id": value["id"],
            "university_name": value["speciality"],
            "region_name_u": value["galuz"],
        }
        for key, value in json_data.items()
    ]
    
    result = bridge_search_universities(university_list, query)
    return result

def sort_specialities(sort_type):
    with open("specialities.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    university_list = [
        {
            "university_id": value["id"],
            "university_name": value["speciality"],
            "region_name_u": value["galuz"],
        }
        for key, value in json_data.items()
    ]
    
    sorted_list = bridge_sort_universities(university_list, sort_type)
    return sorted_list

if __name__=="__main__":
    print("Результат: ", search_universities("олітехніка"))