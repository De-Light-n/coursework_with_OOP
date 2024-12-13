cmake_minimum_required(VERSION 3.10)
project(SortedUniversities LANGUAGES CXX)

# Встановити стандарт C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Налаштування бібліотеки
add_library(search_universities SHARED search_universities.cpp)

# Оптимізації та видимість
if(CMAKE_SYSTEM_NAME STREQUAL "Linux" OR CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    target_compile_options(search_universities PRIVATE -fvisibility=hidden)
endif()

# Установлення специфічних флагів для MSVC або інших компіляторів
if(MSVC)
    target_compile_options(search_universities PRIVATE /W4)
else()
    target_compile_options(search_universities PRIVATE -Wall -Wextra -pedantic)
endif()

# Додаткові налаштування для Windows
if(WIN32)
    set_target_properties(search_universities PROPERTIES PREFIX "")
    set_target_properties(search_universities PROPERTIES SUFFIX ".dll")
endif()

# Додаткові налаштування для Linux/MacOS
if(UNIX AND NOT WIN32)
    set_target_properties(search_universities PROPERTIES PREFIX "lib")
    set_target_properties(search_universities PROPERTIES SUFFIX ".so")
endif()

# Інсталяція бібліотеки
install(TARGETS search_universities DESTINATION lib)

