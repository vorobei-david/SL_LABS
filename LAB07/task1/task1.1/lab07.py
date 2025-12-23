# вариант 11 (ну я в списке лаб 11 поэтому выбрал 11 вариант)
import pickle

cities_temp = { 
    "Москва": {"2017": 6.5, "2018": 7.2, "2019": 5.8, "2020": 7.9, "2021": 6.3, 
    "2022": 7.1}, 
    "Сочи": {"2017": 14.8, "2018": 15.2, "2019": 14.1, "2020": 15.6, "2021": 14.9, 
    "2022": 15.4}, 
    "Новосибирск": {"2017": 2.1, "2018": 2.8, "2019": 1.5, "2020": 3.2, "2021": 2.4, 
    "2022": 2.9}, 
    "Минск" : {"2017": 2.9, "2018": 1.7, "2019": 4.8, "2020": 4.9, "2021": 5.1, 
    "2022": 5.3},
    "Гродно" : {"2017": 3, "2018": 3.1, "2019": 5.1, "2020": 4.9, "2021": 5, 
    "2022": 4.9},
    "Брест" : {"2017": 4.1, "2018": 4.3, "2019": 4.8, "2020": 4.9, "2021": 5.6, 
    "2022": 5.1},
}

result = {}

for city, years in cities_temp.items():
    max_temp = 0
    average_temp = 0
    min_temp = 999
    for year, temp in years.items():
        average_temp += temp;
        if max_temp < temp:
            max_temp = temp
        if min_temp > temp:
            min_temp = temp
    average_temp = average_temp / len(years)

    city_data = {
        "Средняя температура" : round(average_temp, 1),
        "Максимальная температура" : max_temp
    }
    if cities_temp[city]["2019"] == min_temp:
        city_data["Примечание"] = "В 2019 году была минимальная температура"
    if cities_temp[city]["2017"] - cities_temp[city]["2018"] >= 1:
        city_data["Примечание 2"] = "2017 теплее 2018 на более 1 градуса"
    result[city] = city_data

with open('data.pickle', 'wb') as file:
    pickle.dump(result, file)