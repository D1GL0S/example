import csv
import json
import requests
from bs4 import BeautifulSoup

# Функция для загрузки HTML кода страницы
def get_html(url, page_number):
    params = {'page': page_number}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

# Функция для извлечения данных из HTML
def extract_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_list = []

    for article in soup.find_all('article', class_='product-card'):
        book_data = {}
        book_data['Title'] = article['data-chg-product-name']
        book_data['Author'] = article.find('div', class_='product-title__author').text.strip()

        # Добавим проверку на наличие рейтинга перед его извлечением
        rating_elem = article.find('span', itemprop='ratingValue')
        book_data['Rating'] = rating_elem.text.strip() if rating_elem else ''

        review_elem = article.find('span', itemprop='reviewCount')
        book_data['ReviewCount'] = review_elem.text.strip()[1:-1] if review_elem else ''

        prices_elem = article.find('div', class_='product-price')
        if prices_elem:
            prices = prices_elem.find_all('div', class_='product-price__value')
            book_data['OldPrice'] = prices[0].text.strip()

            if len(prices) > 1:
                book_data['NewPrice'] = prices[1].text.strip()
            else:
                book_data['NewPrice'] = ''
        else:
            book_data['OldPrice'] = ''
            book_data['NewPrice'] = ''

        book_data['Publisher'] = article['data-chg-product-brand']
        book_data['ISBN'] = article.find('a', class_='product-card__title')['href'].split('-')[-1]
        book_data['ImageURL'] = article.find('img', class_='product-picture__img')['data-src']
        book_data['Description'] = article.find('div', class_='product-card__text').text.strip()

        book_list.append(book_data)

    return book_list

# Сохранение данных в CSV
def save_to_csv(data_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data_list[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

# Сохранение данных в JSON
def save_to_json(data_list, filename):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data_list, jsonfile, ensure_ascii=False, indent=2)

# Вывод данных в консоль на русском
def print_book_data(book_data_list):
    for book_data in book_data_list:
        print("Название книги -", book_data['Title'])
        print("Автор -", book_data['Author'])
        print("Рейтинг -", book_data['Rating'])
        print("Количество отзывов -", book_data['ReviewCount'])
        print("Старая цена -", book_data['OldPrice'])
        print("Новая цена -", book_data['NewPrice'])
        print("Издательство -", book_data['Publisher'])
        print("ISBN -", book_data['ISBN'])
        print("Ссылка на обложку книги -", book_data['ImageURL'])
        print("Описание книги -", book_data['Description'])
        print("-----------------------------------------------------------")

# Основная функция для выполнения программы
def main():
    url = 'https://www.chitai-gorod.ru/collections/o-druzhbe-lyudey-i-zhivotnyh-265'
    total_pages = 3  # Здесь указываем общее количество страниц

    all_book_data_list = []  # Список для хранения данных о всех книгах

    for page_number in range(1, total_pages + 1):
        html_code = get_html(url, page_number)
        book_data_list = extract_data_from_html(html_code)
        all_book_data_list.extend(book_data_list)

    # Сохраняем данные в CSV и JSON
    save_to_csv(all_book_data_list, 'books_data.csv')
    save_to_json(all_book_data_list, 'books_data.json')

    # Выводим данные в консоль на русском
    print_book_data(all_book_data_list)

if __name__ == '__main__':
    main()
