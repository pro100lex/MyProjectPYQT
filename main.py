import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel


class First_Window(QMainWindow):  # класс самого первого окна при запуске
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_fir_page.ui', self)
        self.initUI()

    def initUI(self):
        # показываем список фильмов
        self.show_table_begin()

        # создаем объекты классов для дальнейшего их открытия
        self.window_app_film = Window_append_film()
        self.window_favourites = Window_favourites()

        # кнопка для показа избранных фильмов
        self.btn_favourites.clicked.connect(self.show_favourites)

        # кнопка для применения поискового запроса к фильмам
        self.find_btn.clicked.connect(self.finder_film)

        # кнопка для вызова окна, чтобы добавить фильм в избранное
        self.btn_append_film.clicked.connect(self.show_append_film)

        # кнопка для сброса всех фильтров и поисковых запросов
        self.btn_reset.clicked.connect(self.reset_table)

        # кнопка для применения фильтров
        self.btn_apply_filter.clicked.connect(self.apply_filter)

    def show_table_begin(self):  # метод для создания модели, которая будет показывать список фильмов
        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_for_begin()
        self.tableFilms.setModel(self.model)

    def createModel_for_begin(self):  # метод обучения модели для первого запуска
        self.model = QSqlQueryModel(self)
        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "Название")
        self.model.setHeaderData(2, Qt.Horizontal, "Год")
        self.model.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model.setQuery("""SELECT title, year, country, genre, rate FROM films""")
        self.db.close()

    def createModel_for_filter(self, answer):  # метод обучения модели для применения фильтров
        self.model_filter = QSqlQueryModel()
        self.model_filter.setHeaderData(0, Qt.Horizontal, "id")
        self.model_filter.setHeaderData(1, Qt.Horizontal, "Название")
        self.model_filter.setHeaderData(2, Qt.Horizontal, "Год")
        self.model_filter.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model_filter.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model_filter.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model_filter.setQuery(answer)
        self.db.close()

    def createModel_for_finder(self, answer):  # метод обучения модели для применения строки поиска
        self.model_finder = QSqlQueryModel()
        self.model_finder.setHeaderData(0, Qt.Horizontal, "id")
        self.model_finder.setHeaderData(1, Qt.Horizontal, "Название")
        self.model_finder.setHeaderData(2, Qt.Horizontal, "Год")
        self.model_finder.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model_finder.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model_finder.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model_finder.setQuery(answer)
        self.db.close()

    def createModel_for_reset(self, answer):  # метод обучения модели для применения кнопки сброса
        self.model_reset = QSqlQueryModel()
        self.model_reset.setHeaderData(0, Qt.Horizontal, "id")
        self.model_reset.setHeaderData(1, Qt.Horizontal, "Название")
        self.model_reset.setHeaderData(2, Qt.Horizontal, "Год")
        self.model_reset.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model_reset.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model_reset.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model_reset.setQuery(answer)
        self.db.close()

    def createConnection(self):  # метод для подключения базы с фильмами
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data_base.db')
        if not self.db.open():
            QMessageBox.critical(None, ("Cannot open database"),
                                 ("Unable to establish a database connection.\n"
                                  "This example needs SQLite support. Please read "
                                  "the Qt SQL driver documentation for information "
                                  "how to build it.\n\n"
                                  "Click Cancel to exit."),
                                 QMessageBox.Cancel)
            return False

    def finder_film(self):  # метод для показа фильмов похожих на ввод в строке поиска
        # получаем поисковой запрос и формируем его под запрос SQL
        search_query = self.pole_enter_film.text()
        answer = f"""SELECT title, year, country, genre, rate FROM films WHERE title LIKE '{search_query}%' OR title LIKE '%{search_query}' OR title LIKE '%{search_query}%'"""

        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_for_finder(answer)
        self.tableFilms.setModel(self.model_finder)

    def show_append_film(self):  # метод для вызова окна добавления фильма в избранные
        self.window_app_film.show()

    def show_favourites(self):  # метод для вызова окна избранных фильмов
        self.window_favourites.show()

    def reset_table(self):  # метод для показа фильмов со сбросом всех поисковых настроек
        # формируем запрос под SQL
        answer = """SELECT title, year, country, genre, rate FROM films"""

        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_for_reset(answer)
        self.tableFilms.setModel(self.model_reset)

    def apply_filter(self):  # метод для получения фильмов, которые удовлетворяют условиям поиска
        # собираем всю информацию о критериях поиска
        fir_year = self.le_fir_year.text()
        sec_year = self.le_sec_year.text()
        genre = self.le_genre.text()
        country = self.le_country.text()
        fir_rate = self.le_fir_rate.text()
        sec_rate = self.le_sec_rate.text()

        # выполняем поиск фильмов которые подходят по фильтрам
        answer = f"""SELECT title, year, country, genre, rate FROM films WHERE
         year BETWEEN {fir_year} AND {sec_year} 
         AND (genre LIKE '{genre}%' OR genre LIKE '%{genre}%' OR genre LIKE '{genre}%') 
         AND (country LIKE '{country}%' OR country LIKE '%{country}%' OR country LIKE '%{country}')
         AND rate BETWEEN {fir_rate} AND {sec_rate}"""

        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_for_filter(answer)
        self.tableFilms.setModel(self.model_filter)


class Window_append_film(QMainWindow):  # класс окна для добавления фильмов в избранные
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_append_film.ui', self)
        self.initUI()

    def initUI(self):
        # кнопка вызывающая метод для добавления в основную базу данных
        self.btn_append_to_favourite.clicked.connect(self.append_to_fav_films)

    def append_to_fav_films(self):  # метод класса для добавления фильмов в омсновную базу данных
        # получаем всю интересующую нас информацию из полей LineEdit
        film_title = self.le_title.text()

        # подключаем базу данных и вносим туда новый фильм, сохраняем изменения
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()

        info_film = cur.execute(f"""SELECT title, year, country, genre, rate FROM films WHERE title = '{film_title}'""").fetchall()
        cur.execute("""INSERT INTO favourite (title, year, rate, genre, country) 
                    VALUES (?, ?, ?, ?, ?)""", (info_film[0][0], info_film[0][1], info_film[0][4], info_film[0][3], info_film[0][2]))
        self.le_title.setText('')
        con.commit()


class Window_favourites(QMainWindow):  # класс окна для показа избранных фильмов
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_favourites.ui', self)
        self.initUi()

    def initUi(self):
        # получаем объект класса окна для добавления фильма в избранное
        self.window_app_from_fav = Window_appender_from_favourites()
        self.window_del_from_fav = Window_delete_from_favourites()
        self.window_change_from_fav = Window_change_from_favourites1()

        # кнопка вызывающая метод для показа окна для добавления фильмов в избранное
        self.btn_append_film.clicked.connect(self.show_app_from_fav)

        # кнопка для показа окна удаления фильма из избранных
        self.btn_delete.clicked.connect(self.show_del_from_fav)

        # кнопка для обновления данных в таблице
        self.btn_update.clicked.connect(self.update_table)

        # кнопка для очищения избранных фильмов
        self.btn_clear.clicked.connect(self.clear_table)

        # кнопка для вызова окна с изменением данных фильма
        self.btn_change.clicked.connect(self.show_change1)

        # вызов метода показа всех фильмов в базе с избранными фильмами
        self.show_films_from_favourite()

    def show_films_from_favourite(self):  # метод показа всех фильмов в базе с избранными фильмами
        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_for_show_fav()
        self.table_fav_films.setModel(self.model_show_fav)

    def show_app_from_fav(self):  # метод показывающий окно для добавления фильмов в избранное
        self.window_app_from_fav.show()

    def show_change1(self):  # метод показывающий окно для изменения фильма
        self.window_change_from_fav.show()

    def show_del_from_fav(self):  # метод показывающий окно для удаления фильма
        self.window_del_from_fav.show()

    def update_table(self):  # метод для обновления информации таблицы в окне
        # подключаем базу данных и обучаем модель
        self.createConnection()
        self.createModel_update()
        self.table_fav_films.setModel(self.model_update)

    def createConnection(self):  # метод для подключения базы с фильмами
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data_base.db')
        if not self.db.open():
            QMessageBox.critical(None, ("Cannot open database"),
                                 ("Unable to establish a database connection.\n"
                                  "This example needs SQLite support. Please read "
                                  "the Qt SQL driver documentation for information "
                                  "how to build it.\n\n"
                                  "Click Cancel to exit."),
                                 QMessageBox.Cancel)
            return False

    def createModel_for_show_fav(self):  # метод обучения модели для показа всех фильмов из избранных фильмов
        self.model_show_fav = QSqlQueryModel()
        self.model_show_fav.setHeaderData(0, Qt.Horizontal, "id")
        self.model_show_fav.setHeaderData(1, Qt.Horizontal, "Название")
        self.model_show_fav.setHeaderData(2, Qt.Horizontal, "Год")
        self.model_show_fav.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model_show_fav.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model_show_fav.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model_show_fav.setQuery("""SELECT title, year, country, genre, rate FROM favourite""")
        self.db.close()

    def createModel_update(self):  # метод обучения модели для обновления всех фильмов из избранных фильмов
        self.model_update = QSqlQueryModel()
        self.model_update.setHeaderData(0, Qt.Horizontal, "id")
        self.model_update.setHeaderData(1, Qt.Horizontal, "Название")
        self.model_update.setHeaderData(2, Qt.Horizontal, "Год")
        self.model_update.setHeaderData(3, Qt.Horizontal, "Рейтинг")
        self.model_update.setHeaderData(4, Qt.Horizontal, "Жанр")
        self.model_update.setHeaderData(5, Qt.Horizontal, "Страна")
        self.model_update.setQuery("""SELECT title, year, country, genre, rate FROM favourite""")
        self.db.close()

    def clear_table(self):  # метод для очищения всей базы данных с избранными фильмами
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()
        cur.execute("""DELETE FROM favourite""")
        con.commit()


class Window_appender_from_favourites(QMainWindow):  # класс для добавления фильмов во вкладке избранное
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_appender_from_favourite.ui', self)
        self.initUi()

    def initUi(self):
        # кнопка вызывающая окно для добавления фильма
        self.btn_append_to_favourite.clicked.connect(self.app_to_db_favourite)

    def app_to_db_favourite(self):   # метод для добавление в базу данных избранные фильмы
        # получаем всю интересующую нас информацию из полей LineEdit
        title = self.le_title.text()
        year = self.le_year.text()
        country = self.le_country.text()
        genre = self.le_country.text()
        rate = self.le_rate.text()

        # подключаем базу данных и вносим туда новый фильм, сохраняем изменения, увеличиваем значение переменной
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()
        cur.execute("""INSERT INTO favourite (title, year, rate, genre, country) 
                            VALUES (?, ?, ?, ?, ?)""", (title, year, rate, genre, country))
        con.commit()
        self.le_title.setText('')
        self.le_year.setText('')
        self.le_country.setText('')
        self.le_genre.setText('')
        self.le_country.setText('')
        self.le_rate.setText('')


class Window_delete_from_favourites(QMainWindow):  # класс окна для удаления из избранных
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_delete_from_favourite.ui', self)
        self.initUi()

    def initUi(self):
        # кнопка для вызова окна удаления фильма из избранных
        self.btn_delete_from_favourite.clicked.connect(self.del_from_fav)

    def del_from_fav(self):
        # получение название фильма
        title_film = self.le_title.text()

        # подключаем базу данных, удаляем фильм, сохраняем
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()
        cur.execute(f"""DELETE FROM favourite WHERE title = '{title_film}'""")
        self.le_title.setText('')
        con.commit()


class Window_change_from_favourites1(QMainWindow):  # класс окна для получения названия фильма, чтобы потом изменить его
    def __init__(self):
        super().__init__()
        uic.loadUi('style_for_change_from_fvourite.ui', self)
        self.initUi()

    def initUi(self):
        # кнопка для вызова следующего окна с изменением фильма
        self.btn_change_from_favourite.clicked.connect(self.show_change2)

        # название фильма, который нужно изменить
        self.title_change_film = ''

    def show_change2(self):
        # получаем название фильма, который нужно изменить
        self.title_change_film = self.le_title.text()

        # объект класса в который мы передаем название фильма для изменения
        self.window_change_from_fav = Window_change_from_favourites2(self.title_change_film)
        self.window_change_from_fav.show()
        self.le_title.setText('')


class Window_change_from_favourites2(QMainWindow):  # класс окна для изменения фильма
    def __init__(self, title):
        super().__init__()
        uic.loadUi('style_for_change_from_fvourite2.ui', self)
        self.initUi(title)

    def initUi(self, title):
        # название фильма, который нужно изменить
        self.title_film = title

        # подключаем базу данных
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()

        # получаем всю информацию из фильма, который нужно изменить
        info_film = cur.execute(f"""SELECT * FROM favourite WHERE title = '{self.title_film}'""").fetchall()
        print(info_film)

        # вставляем в поля информацию, для большего удобства
        self.le_title.setText(str(info_film[0][1]))
        self.le_year.setText(str(info_film[0][2]))
        self.le_country.setText(str(info_film[0][5]))
        self.le_genre.setText(str(info_film[0][4]))
        self.le_rate.setText(str(info_film[0][3]))

        # кнопка для возова метода с перезаписью поля
        self.btn_change_in_favourite.clicked.connect(self.change_info_film)

    def change_info_film(self):
        # подключаем базу данных и изменяем нужную нам информацию о фильме, сохраняем изменения
        con = sqlite3.connect('data_base.db')
        cur = con.cursor()
        cur.execute(f"""UPDATE favourite 
                SET title = '{self.le_title.text()}', year = '{self.le_year.text()}', country = '{self.le_country.text()}', genre = '{self.le_genre.text()}', rate = '{self.le_rate.text()}' 
                WHERE title = '{self.title_film}'""")
        con.commit()
        self.le_title.setText('')
        self.le_year.setText('')
        self.le_country.setText('')
        self.le_genre.setText('')
        self.le_rate.setText('')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = First_Window()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
