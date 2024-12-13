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

    // Таблиця порядку символів українського алфавіту
    std::map<char, int> create_ukrainian_order() {
        std::string alphabet = "абвгґдеєжзийіїклмнопрстуфхцчшщьюя";
        std::map<char, int> order;
        for (int i = 0; i < alphabet.size(); ++i) {
            order[alphabet[i]] = i;
            order[std::toupper(alphabet[i])] = i; // Для підтримки великих літер
        }
        return order;
    }

    bool compare_ukrainian(const std::string& a, const std::string& b, const std::map<char, int>& order) {
        size_t len = std::min(a.size(), b.size());
        for (size_t i = 0; i < len; ++i) {
            char char_a = a[i];
            char char_b = b[i];
            if (order.count(char_a) && order.count(char_b)) {
                if (order.at(char_a) != order.at(char_b)) {
                    return order.at(char_a) < order.at(char_b);
                }
            } else {
                return char_a < char_b; // Порівняння за замовчуванням, якщо символи поза алфавітом
            }
        }
        return a.size() < b.size(); // Якщо всі символи рівні, коротший рядок йде першим
    }

    // Головна функція
    char** sort_universities(University* universities, int size, int sort_type) {
        if (sort_type < 1 || sort_type > 3) {
            return nullptr; // Перевірка валідності типу сортування
        }

        // Перетворюємо масив у std::vector для зручності
        std::vector<University> university_vec(universities, universities + size);

        // Створюємо таблицю порядку символів
        auto uk_order = create_ukrainian_order();

        // Сортування залежно від типу
        if (sort_type == 1) {
            std::sort(university_vec.begin(), university_vec.end(), [](const University& a, const University& b) {
                return std::stoi(a.id) < std::stoi(b.id);
            });
        } else if (sort_type == 2) {
            std::sort(university_vec.begin(), university_vec.end(), [&uk_order](const University& a, const University& b) {
                return compare_ukrainian(a.name, b.name, uk_order);
            });
        } else if (sort_type == 3) {
            std::sort(university_vec.begin(), university_vec.end(), [&uk_order](const University& a, const University& b) {
                return compare_ukrainian(a.region, b.region, uk_order);
            });
        }

        // Створюємо масив рядків для результату
        char** result = (char**)malloc(size * sizeof(char*));
        if (!result) return nullptr; // Перевірка на успішне виділення пам'яті

        for (int i = 0; i < size; ++i) {
            const std::string& str = university_vec[i].id;
            result[i] = (char*)malloc((str.size() + 1) * sizeof(char));
            if (result[i]) {
                std::copy(str.begin(), str.end(), result[i]);
                result[i][str.size()] = '\0'; // Додаємо термінуючий нуль
            }
        }

        return result;
    }

    // Функція для звільнення пам'яті
    void free_string_array(char** array, int size) {
        if (!array) return;
        for (int i = 0; i < size; ++i) {
            free(array[i]);
        }
        free(array);
    }
}
