from urllib.request import urlopen
from bs4 import BeautifulSoup
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
    AdaptiveETA, FileTransferSpeed, FormatLabel, Percentage, \
    ProgressBar, ReverseBar, RotatingMarker, \
    SimpleProgress, Timer, UnknownLength
import re
import random
import os
from sys import platform



symbols_identifications = {
    "%27": "'",
    "%26": "&",
    "%C3": "",
    "%A8": "e",
    "%AD": "i",
    "%A1": "a",
    "%BC": "u",
    "%C2": "^",
    "%BE": "3/4",
    "%A9": "e",
    "%C5": "",
    "%8D": "o",
    "%AB": "e"
}



class Book():
    """Структура книги БЕЗ:
    Кода - ее порядковый номер
    Номера стелажа - рандомное число"""
    def __init__(self):
        self.title = "Title"
        self.author = "Author"
        self.year = 0



def get_html():

    wiki_link = "https://en.wikipedia.org/wiki/The_Big_Read"

    # Проверка интернет соединения
    internet_connection = True
    try:
        html = urlopen(wiki_link, timeout=5).read().decode("utf-8") # Чтение "https://en.wikipedia.org/wiki/The_Big_Read"
    except:
        internet_connection = False

    if internet_connection:
        soup = BeautifulSoup(html, "html.parser")        # Суп
        html_links = ""                                  # Строка хранения строк с ссылками
        for a in soup.find_all("ol"):                    # Выбор таблиц в стринг
           html_links += str(a)
        soup = BeautifulSoup(html_links, "html.parser")  # Суп из элементов таблиц

        # Суп ссылок и удаление соавторства
        data_links = soup.find_all("a", href=True)
        data_links.pop(186*2+2)
        data_links.pop(172*2+1)
        data_links.pop(68*2)

        return data_links, internet_connection

    else:
        return None, internet_connection



def fill_structure(links):

    n = int(input("Enter the number of books> "))

    if n > 200:
        n = 200

    book_list = []
    for i in range(n):
        new_unit = Book()
        book_list.append(new_unit)

    print("\n")
    progress_bar = ProgressBar().start()

    if (platform == "win32"):
        os.system("cls")                   # Очистка консоли для красивого вывода
        os.system("color 02")              # Зеленый цвет вывода в консоли windows

    elif (platform == "linux"):
        os.system("clear")



    i = 0
    while ((i < 2*n) and (i < 2*200)):
        # Каждая 2 ссылка {0, 2, 4...} - на книгу

        num = i//2 # Порядковый номер книги
        if (i%2 == 0):
            book_link = "https://en.wikipedia.org" + links[i]["href"]  # Локальная ссылка на книгу

            book_list[num].title = book_link[30:]

            while (book_list[num].title.find("%") != -1):                    # Вырез percent'а
                percent = book_list[num].title.find("%")
                book_list[num].title = (book_list[num].title[:percent] + 
                                        symbols_identifications[book_list[num].title[percent:(percent + 3)]] + 
                                        book_list[num].title[(percent + 3):])

            # Cразу вывод даты
            html = urlopen(book_link).read().decode("utf-8")
            infobox = html.find('<table class="infobox')    # Поиск инфобокса
            start = html.find(">Author<", infobox)          # Автор всегда первый. Поиск будет с начала
            date = re.search(r"\d{4}", html[start:])         # Первая дата чего-то


            if date is None:  # Если автора нет
                start = html.find("<p>")
                date = re.search(r"\d{4}", html[start:])
                
            while ((date.group(0) < "1800") or (date.group(0) > "2004")):
                start = html.find(date.group(0), start + 4) + 4
                date = re.search(r"\d{4}", html[(start):])
                if date is None:  # Если автора нет
                    start = html.find("<p>")
                    date = re.search(r"\d{4}", html[start:])

            book_list[num].year = date.group(0)  # Дата / груп убирает лишнее, оставляя значение

    
        else:
        # {1, 3, 5...} ссылки на авторов
            author_link = "https://en.wikipedia.org" + links[i]["href"]  # Локальная ссылка на автора
            author_name = author_link[30:]

            # Мусор в ссылке
            if author_name.find(",") != -1:
                not_a_symbol = author_name.find(",")
                author_name = author_name[:not_a_symbol]
            if author_name.find("(") != -1:
                not_a_symbol = author_name.find("_(")
                author_name = author_name[:not_a_symbol]

            # Постановка фамилии впереди имени
            n_ = author_name.rfind("_")                                    # Позиция последней черточки
            author_name = author_name[(n_ + 1):] + "_" + author_name[:n_]  # Замена местами

            # Замена ID символов на символы
            while (author_name.find("%") != -1):
                percent = author_name.find("%")
                author_name = author_name[:percent] + symbols_identifications[author_name[percent:(percent + 3)]] + author_name[(percent + 3):]
            

            book_list[num].author = author_name

            # Обновление прогресс-бара
            progress_bar.update((i+1)/2/n*100)

        i += 1

    if (platform == "win32"):
        os.system("cls")
        os.system("color 07") # Кончилась красота
    elif (platform == "linux"):
        os.system("clear")

    return book_list



def write_to_file(book_list):
    n = len(book_list)
    file = open('data.txt', 'w')
    file.write(str(n) + "\n")
    for i in range(n):
        file.write(str(i+1) + " " + 
                    book_list[i].author + " " + 
                    book_list[i].title + " " + 
                    str(book_list[i].year) + " " + 
                    str(random.randint(1, 3)) + '\n')
    file.close()



def main():
    (links, internet_connection) = get_html() 

    if internet_connection:
        book_list = fill_structure(links)
        write_to_file(book_list)
    else:
        print("\n\n========================HAVE NOT INTERNET CONNECTION!!!!!!!!!!!!!!\n")
        write_to_file([Book()])



if __name__ == '__main__':
    main()