import requests
import json
import os


# Конфигурация языков для поиска
target_languages = {
    'spa': 'Испанский',
    'por': 'Португальский', 
    'deu': 'Немецкий'
}

# Минимальная площадь страны в км²
area_threshold = 100000


def fetch_countries_data(language_code):
    """Получает список стран по коду языка через API"""
    api_url = f'https://restcountries.com/v3.1/lang/{language_code}'
    try:
        resp = requests.get(api_url)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as error:
        print(f'Не удалось загрузить данные: {error}')
        return []


def check_area_criteria(countries_list, minimum_area):
    """Фильтрует страны по минимальной площади"""
    filtered_list = []
    for country in countries_list:
        country_area = country.get('area', 0)
        if country_area > minimum_area:
            filtered_list.append(country)
    return filtered_list


def save_flag_image(image_url, country_title, lang_code):
    """Скачивает и сохраняет флаг страны"""
    try:
        image_data = requests.get(image_url)
        image_data.raise_for_status()
        
        # Создаём папку для флагов
        if not os.path.exists('flags'):
            os.makedirs('flags')
        
        # Формируем безопасное имя файла
        clean_name = country_title.replace(' ', '_').replace('/', '_')
        filename = f'flags/{clean_name}_{lang_code}.png'
        
        with open(filename, 'wb') as file:
            file.write(image_data.content)
        
        return filename
    except Exception as err:
        print(f'Ошибка сохранения флага: {err}')
        return None


def parse_country_data(country_obj):
    """Извлекает нужную информацию о стране"""
    country_dict = {}
    
    # Получаем название
    name_data = country_obj.get('name', {})
    country_dict['name'] = name_data.get('common', 'Неизвестно')
    
    # Получаем столицу
    capitals = country_obj.get('capital', [])
    country_dict['capital'] = capitals[0] if capitals else 'Неизвестно'
    
    # Площадь и население
    country_dict['area'] = country_obj.get('area', 0)
    country_dict['population'] = country_obj.get('population', 0)
    
    # URL флага
    flags = country_obj.get('flags', {})
    country_dict['flag_url'] = flags.get('png', '')
    
    return country_dict


def process_language_data():
    """Основная функция обработки данных"""
    results_by_language = {}
    biggest_countries = {}
    
    for code, name in target_languages.items():
        print(f'\n--- Обработка: {name} ---')
        
        # Получаем все страны
        all_countries = fetch_countries_data(code)
        print(f'Найдено стран: {len(all_countries)}')
        
        # Фильтруем по площади
        large_countries = check_area_criteria(all_countries, area_threshold)
        print(f'Подходящих по площади: {len(large_countries)}')
        
        results_by_language[name] = []
        largest_area = 0
        largest_country = None
        
        # Обрабатываем каждую страну
        for country in large_countries:
            country_info = parse_country_data(country)
            results_by_language[name].append(country_info)
            
            # Проверяем максимальную площадь
            current_area = country_info['area']
            if current_area > largest_area:
                largest_area = current_area
                largest_country = country_info
            
            # Скачиваем флаг
            if country_info['flag_url']:
                flag_file = save_flag_image(
                    country_info['flag_url'], 
                    country_info['name'], 
                    code
                )
                if flag_file:
                    print(f'✓ Флаг сохранён: {flag_file}')
        
        # Сохраняем самую большую страну
        if largest_country:
            biggest_countries[name] = largest_country
            print(f'\nСамая большая страна для {name}:')
            print(f'→ {largest_country["name"]}')
            print(f'→ Столица: {largest_country["capital"]}')
            print(f'→ Площадь: {largest_country["area"]:,.0f} км²')
            print(f'→ Население: {largest_country["population"]:,}')
    
    # Сохраняем результаты в JSON
    with open('results.json', 'w', encoding='utf-8') as output_file:
        json.dump(results_by_language, output_file, ensure_ascii=False, indent=2)
    
    print('\n' + '='*60)
    print('СВОДКА ПО САМЫМ БОЛЬШИМ СТРАНАМ:')
    print('='*60)
    for lang, info in biggest_countries.items():
        print(f'{lang}: {info["name"]} - {info["area"]:,.0f} км²')


if __name__ == '__main__':
    process_language_data()
