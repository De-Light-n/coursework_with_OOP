import ctypes
from ctypes import POINTER, Structure, c_char_p, c_int
import os
import json


class Bridge:
    class University(Structure):
        _fields_ = [
            ("id", c_char_p),
            ("name", c_char_p),
            ("region", c_char_p),
        ]

    def __init__(self):
        os.add_dll_directory(r"C:\\msys64\\ucrt64\\bin")
        self.lib_sort = ctypes.CDLL('./get_sorted_universities.dll')
        self.lib_search = ctypes.CDLL('./search_universities.dll')

        self.lib_sort.sort_universities.argtypes = [POINTER(self.University), c_int, c_int]
        self.lib_sort.sort_universities.restype = POINTER(ctypes.POINTER(ctypes.c_char))

        self.lib_sort.free_string_array.argtypes = [POINTER(ctypes.POINTER(ctypes.c_char)), c_int]

        self.lib_search.search_universities.argtypes = [POINTER(self.University), c_int, c_char_p]
        self.lib_search.search_universities.restype = POINTER(ctypes.POINTER(ctypes.c_char))

        self.lib_search.free_string_array.argtypes = [POINTER(ctypes.POINTER(ctypes.c_char)), c_int]
        
    def bridge_sort_universities(self, data, sort_type):
        university_array = (self.University * len(data))(
            *[
                self.University(
                    id=univ["university_id"].encode('utf-8'),
                    name=univ["university_name"].encode('utf-8'),
                    region=univ["region_name_u"].encode('utf-8'),
                )
                for univ in data
            ]
        )

        result = self.lib_sort.sort_universities(university_array, len(data), sort_type)

        sorted_ids = [
            ctypes.string_at(result[i]).decode('utf-8') for i in range(len(data))
        ]

        self.lib_sort.free_string_array(result, len(data))
        
        return sorted_ids
    
    def bridge_search_universities(self, data, query):
        university_array = (self.University * len(data))(
            *[
                self.University(
                    id=univ["university_id"].encode('utf-8'),
                    name=univ["university_name"].encode('utf-8'),
                    region=univ["region_name_u"].encode('utf-8'),
                )
                for univ in data
            ]
        )

        result = self.lib_search.search_universities(university_array, len(data), query.encode('utf-8'))

        matched_ids = []
        i = 0
        while result[i]:
            matched_ids.append(ctypes.string_at(result[i]).decode('utf-8'))
            i += 1

        self.lib_search.free_string_array(result, len(matched_ids))

        return matched_ids
    
    def sort_universities(self, sort_type):
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
        
        sorted_list = self.bridge_sort_universities(university_list, sort_type)
        return sorted_list
    

    def search_universities(self, query):
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
        
        result = self.bridge_search_universities(university_list, query)
        return result

    def search_specialities(self, query):
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
        
        result = self.bridge_search_universities(university_list, query)
        return result

    def sort_specialities(self, sort_type):
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
        
        sorted_list = self.bridge_sort_universities(university_list, sort_type)
        return sorted_list
        

if __name__=="__main__":
    bridge = Bridge()
    print("Результат: ", bridge.search_specialities("омп"))