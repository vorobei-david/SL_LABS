import requests
from bs4 import BeautifulSoup
import csv


jumping_events = {
    'high-jump': 'Прыжок в высоту',
    'pole-vault': 'Прыжок с шестом',
    'long-jump': 'Прыжок в длину',
    'triple-jump': 'Тройной прыжок'
}

categories = ['men', 'women']
target_years = list(range(2001, 2002))


def build_page_url(event_type, category, year_value):
    """Формирует URL для страницы с результатами"""
    base_path = "https://worldathletics.org/records/toplists/jumps"
    full_url = f"{base_path}/{event_type}/all/{category}/senior/{year_value}"
    return full_url


def extract_winner_data(page_url, event_type, category, year_value):
    """Извлекает данные победителя из таблицы результатов"""
    try:
        request_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Обращение к странице: {page_url}")
        page_response = requests.get(page_url, headers=request_headers, timeout=10)
        page_response.raise_for_status()
        
        parser = BeautifulSoup(page_response.content, 'html.parser')
        results_table = parser.find('table')
        
        if not results_table:
            print(f" Таблица отсутствует")
            return None
        
        table_rows = results_table.find_all('tr')
        
        for row in table_rows:
            columns = row.find_all('td')
            
            if len(columns) < 8:
                continue
            
            position = columns[0].get_text(strip=True)
            
            if position != '1':
                continue
            
            performance = columns[1].get_text(strip=True)
            
            athlete_tag = columns[3].find('a')
            athlete_name = athlete_tag.get_text(strip=True) if athlete_tag else columns[3].get_text(strip=True)
            
            nation = columns[5].get_text(strip=True) if len(columns) > 5 else ""
            
            location = columns[-2].get_text(strip=True)
            
            event_date = columns[-1].get_text(strip=True)
            
            record_info = {
                'year': year_value,
                'discipline': jumping_events[event_type],
                'gender': 'Мужчины' if category == 'men' else 'Женщины',
                'athlete': athlete_name,
                'country': nation,
                'result': performance,
                'venue': location,
                'date': event_date
            }
            
            print(f"✓ Получено: {athlete_name} → {performance}")
            return record_info
        
        print(f" Первое место не обнаружено")
        return None
        
    except requests.exceptions.RequestException as error:
        print(f" Ошибка соединения: {error}")
        return None
    except Exception as error:
        print(f" Ошибка парсинга: {error}")
        return None


def collect_all_records():
    """Собирает все рекорды по всем параметрам"""
    collected_data = []
    
    total_pages = len(jumping_events) * len(categories) * len(target_years)
    processed = 0
    
    print(f"═══════════════════════════════════════")
    print(f"Запуск сбора данных ({total_pages} страниц)")
    print(f"═══════════════════════════════════════\n")
    
    for event_key, event_name in jumping_events.items():
        for cat in categories:
            cat_display = "Мужчины" if cat == "men" else "Женщины"
            print(f"\n→ {event_name} | {cat_display}")
            
            for yr in target_years:
                processed += 1
                print(f"  [{processed}/{total_pages}] {yr} год: ", end='')
                
                page_link = build_page_url(event_key, cat, yr)
                winner_data = extract_winner_data(page_link, event_key, cat, yr)
                
                if winner_data:
                    collected_data.append(winner_data)
                
    return collected_data


def write_results_to_csv(data_list, output_filename='top_results.csv'):
    """Сохраняет собранные данные в CSV файл"""
    if not data_list:
        print("\nНет данных для записи!")
        return
    
    csv_headers = ['year', 'discipline', 'gender', 'athlete', 
                   'country', 'result', 'venue', 'date']
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.DictWriter(file, fieldnames=csv_headers)
        csv_writer.writeheader()
        csv_writer.writerows(data_list)
    
    print(f"\n{'='*50}")
    print(f" Файл сохранён: {output_filename}")
    print(f" Записей в файле: {len(data_list)}")
    print(f"{'='*50}")


def run_parser():
    """Главная функция запуска парсера"""
    records = collect_all_records()
    write_results_to_csv(records)


if __name__ == "__main__":
    run_parser()
