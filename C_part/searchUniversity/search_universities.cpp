
#include <map>
#include <vector>
#include <string>
#include <cstdlib>
#include <algorithm>
#include <iostream>

extern "C" {

    struct University {
        const char* id;
        const char* name;
        const char* region;
    };

    char** search_universities(University* universities, int size, const char* query) {
        if (!query || size <= 0) {
            return nullptr;
        }

        std::vector<University> university_vec(universities, universities + size);
        std::vector<std::string> matching_ids;

        for (const auto& uni : university_vec) {
            std::string name(uni.name);
            std::string search_query(query);

            if (name.find(search_query) != std::string::npos) {
                matching_ids.push_back(uni.id);
            }
        }

        char** result = (char**)malloc((matching_ids.size() + 1) * sizeof(char*));
        if (!result) return nullptr;

        for (size_t i = 0; i < matching_ids.size(); ++i) {
            const std::string& str = matching_ids[i];
            result[i] = (char*)malloc((str.size() + 1) * sizeof(char));
            if (result[i]) {
                std::copy(str.begin(), str.end(), result[i]);
                result[i][str.size()] = '\0';
            }
        }

        result[matching_ids.size()] = nullptr; 
        return result;
    }


    // Функція для звільнення пам'яті
    void free_string_array(char** array, int size) {
        if (!array) return;
        for (int i = 0; i < size; ++i) {
            if (array[i]) free(array[i]);
        }
        free(array);
    }
}
