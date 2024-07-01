import sys
from PyQt5.QtWidgets import *
from login import Ui_MainWindow
from lib_gui import lib_gui_MainWindow
import psycopg2
from psycopg2 import Error

class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.login)


    def connect_bd(self, username, password):
        try:
            conn = psycopg2.connect(
                dbname='veterinary_clinic',
                user=username,
                password=password,
                host='localhost'
            )

            return conn
        except psycopg2.Error:
            QMessageBox.warning(self, 'Ошибка!', 'Не удалось подключится к БД.')
            return None

    def aut_user(self, conn, username):
        if conn is None:
            return None

        values = ('man1', 'cl1', 'vet1', 'adm1')

        cursor = conn.cursor()
        for value in values:
            cursor.execute(
                f"SELECT rolname FROM pg_roles WHERE pg_has_role(rolname, '{value}', 'member') and rolname = '{username}';")
            result = cursor.fetchone()
            if result is not None:
                role = value
                break
        cursor.close()
        return role

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        conn = self.connect_bd(username, password)
        role = self.aut_user(conn, username)
        if conn is not None:
            if role == 'man1' or role == 'vet1' or role == 'cl1' or role == 'adm1':
                self.act_win = lib_gui_Window(conn, self)
                self.act_win.show()
                self.hide()
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Такой роли не существует.')
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Неверный логин или пароль.')

class lib_gui_Window(QMainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.lib_gui_ui = lib_gui_MainWindow()
        self.lib_gui_ui.setupUi(self)

        self.conn = conn

        self.lib_gui_ui.comboBox.textActivated.connect(self.onActivated)
        self.setCombo()

        self.Button_and_or = ([self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                               self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                               self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                               self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9])

        self.lib_gui_ui.pushButton_and_or_2.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_2))
        self.lib_gui_ui.pushButton_and_or_3.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_3))
        self.lib_gui_ui.pushButton_and_or_4.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_4))
        self.lib_gui_ui.pushButton_and_or_5.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_5))
        self.lib_gui_ui.pushButton_and_or_6.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_6))
        self.lib_gui_ui.pushButton_and_or_7.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_7))
        self.lib_gui_ui.pushButton_and_or_8.clicked.connect( lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_8))
        self.lib_gui_ui.pushButton_and_or_9.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_9))

        self.textEdit = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8,
                              self.lib_gui_ui.textEdit_9]


        self.textBrowser = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7, self.lib_gui_ui.textBrowser_8,
                                 self.lib_gui_ui.textBrowser_9]

        self.lib_gui_ui.pushButton_filter.clicked.connect(self.filter_table)
        self.lib_gui_ui.pushButton_add.clicked.connect(self.add_table)
        self.lib_gui_ui.pushButton_delete.clicked.connect(self.delete_table)
        self.lib_gui_ui.pushButton_update.clicked.connect(self.update_table)

    def change_button(self, button):
        if button.text() == "AND":
            button.setText("OR")
        elif button.text() == "OR":
            button.setText("")
        else:
            button.setText("AND")

    def do_show(self, element):
        element.show()

    def do_hide(self, element):
        element.hide()

    def setCombo(self):
        self.lib_gui_ui.comboBox.addItems(["Вид животного", "Клиент",
                                          "Работник", "Посещение", "Препарат",
                                          "Питомец", "Должность", "Поставщик",
                                          "Закупка", "Услуга", "Использовано"])

    def onActivated(self):
        text = self.lib_gui_ui.comboBox.currentText()
        if text == "Вид животного":
            self.table = "anim_type"
        elif text == "Порода":
            self.table = "breed"
        elif text == "Клиент":
            self.table = "client"
        elif text == "Работник":
            self.table = "employee"
        elif text == "Посещение":
            self.table = "log_of_visits"
        elif text == "Препарат":
            self.table = "medicine"
        elif text == "Питомец":
            self.table = "pet"
        elif text == "Должность":
            self.table = "post"
        elif text == "Поставщик":
            self.table = "provider"
        elif text == "Закупка":
            self.table = "purchase"
        elif text == "Услуга":
            self.table = "service"
        elif text == "Использовано":
            self.table = "the_medicine_used"

        self.lib_gui_ui.tableWidget.setSortingEnabled(False)
        self.show_table()
        self.lib_gui_ui.tableWidget.setSortingEnabled(True)

    def show_table(self):
        try:
            cursor = self.conn.cursor()
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            if self.table in "anim_type":
                row_labels = ["id", "Вид животного"]
            elif self.table in "client":
                row_labels = ["id", "Фамилия", "Имя", "Отчество", "Адресс", "Телефон", "Электронная почта", "Дополнительная информация"]
            elif self.table in "employee":
                row_labels = ["id", "Фамилия", "Имя", "Отчество", "Телефон", "Электронная почта", "Должность","Дополнительная информация", "Дата рождения"]
            elif self.table in "log_of_visits":
                row_labels = ["id", "Дата", "Животное", "Ветеринар", "Услуга", "Было использовано", "Время приема", "Статус приема"]
            elif self.table in "medicine":
                row_labels = ["id", "Наименования", "Описание"]
            elif self.table in "pet":
                row_labels = ["id", "Хозяин", "Вид животного", "Название породы", "Кличка", "Пол", "Дата рождения", "Дополнительная информация"]
            elif self.table in "post":
                row_labels = ["id", "Название"]
            elif self.table in "provider":
                row_labels = ["id", "Название", "Электронная почта", "Телефон"]
            elif self.table in "purchase":
                row_labels = ["id", "Дата", "Наименования", "Поставщик", "Стоимость"]
            elif self.table in "service":
                row_labels = ["id", "Наименование", "Стоимость"]
            elif self.table in "the_medicine_used":
                row_labels = ["id", "Визит", "Колличество", "Наименование"]

            for i in range(len(row_labels)):
                self.textBrowser[i].setText(row_labels[i])

            self.lib_gui_ui.tableWidget.setColumnCount(len(colum_name))
            self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

            for i in range(len(self.Button_and_or)):
                self.do_hide(self.Button_and_or[i])
            for i in range(len(colum_name) - 1):
                self.do_show(self.Button_and_or[i])

            for i in range(len(self.textEdit)):
               self.do_hide(self.textEdit[i])
            for i in range(len(colum_name)):
                self.do_show(self.textEdit[i])

            for i in range(len(self.textBrowser)):
                self.do_hide(self.textBrowser[i])
            for i in range(len(colum_name)):
                self.do_show(self.textBrowser[i])

            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")

            cursor.execute(f"select * from current_user")
            username = cursor.fetchall()
            if  str(username)[3:5] == 'cl' and (self.table == 'log_of_visits' or self.table == 'client' or self.table == 'pet'):
                cursor.execute(f"SELECT * FROM " + self.table + " where client_id = '" + str(username)[5:-4] + "'")
            else:
                cursor.execute(f"SELECT * FROM " + self.table)
            bib = cursor.fetchall()

            self.lib_gui_ui.tableWidget.setRowCount(len(bib))
            for i in range(len(bib)):
                for j in range(len(colum_name)):
                    self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

            self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def filter_table(self):
        try:
            cursor = self.conn.cursor()
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"SELECT * FROM " + self.table + " WHERE (")
            for i in range(len(colum_name)):
                if self.textEdit[i].toPlainText():
                    if self.Button_and_or[i - 1].text() != '':
                        sql = sql + " " + self.Button_and_or[i - 1].text() + " "
                    sql = sql + colum_name[i][0] + " = '" + str(self.textEdit[i].toPlainText()) + "'"

            sql = sql.replace(';', '')
            sql = sql + ");"

            cursor.execute(f"SAVEPOINT SP1")
            cursor.execute(sql)
            filter_result = cursor.fetchall()

            self.lib_gui_ui.tableWidget.setRowCount(len(filter_result))
            for i in range(len(filter_result)):
                for j in range(len(colum_name)):
                    self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(filter_result[i][j])))
            self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def add_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SAVEPOINT SP1")
            sql = (f"INSERT INTO  " + self.table + " VALUES ('")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + self.lib_gui_ui.textEdit_1.toPlainText()
            if self.lib_gui_ui.textEdit_2.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_2.toPlainText()
            if self.lib_gui_ui.textEdit_3.isVisible() and self.lib_gui_ui.textEdit_3.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_3.toPlainText()
            if self.lib_gui_ui.textEdit_4.isVisible() and self.lib_gui_ui.textEdit_4.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_4.toPlainText()
            if self.lib_gui_ui.textEdit_5.isVisible() and self.lib_gui_ui.textEdit_5.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_5.toPlainText()
            if self.lib_gui_ui.textEdit_6.isVisible() and self.lib_gui_ui.textEdit_6.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_6.toPlainText()
            if self.lib_gui_ui.textEdit_7.isVisible() and self.lib_gui_ui.textEdit_7.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_7.toPlainText()
            if self.lib_gui_ui.textEdit_8.isVisible() and self.lib_gui_ui.textEdit_8.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_8.toPlainText()
            if self.lib_gui_ui.textEdit_9.isVisible() and self.lib_gui_ui.textEdit_9.toPlainText():
                sql = sql + "', '" + self.lib_gui_ui.textEdit_9.toPlainText()

            sql = sql.replace(';', '')
            sql = sql + "');"
            print('sql', sql)

            cursor.execute(f"SAVEPOINT SP1")
            cursor.execute(sql)
            self.conn.commit()

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def delete_table(self):
        try:
            cursor = self.conn.cursor()
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"DELETE FROM " + self.table + " WHERE (")
            for i in range(len(colum_name)):
                if self.textEdit[i].toPlainText():
                    if self.Button_and_or[i - 1].text() != '':
                        sql = sql + " " + self.Button_and_or[i - 1].text() + " "
                    sql = sql + colum_name[i][0] + " = '" + str(self.textEdit[i].toPlainText()) + "'"

            sql = sql.replace(';', '')
            sql = sql + ");"

            cursor.execute(f"SAVEPOINT SP1")
            cursor.execute(sql)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

    def update_table(self):
        try:
            cursor = self.conn.cursor()
            sql_colum_name = (
                f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table}' ORDER BY ordinal_position;")
            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"UPDATE " + self.table + " SET ")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql + " WHERE (" + str(colum_name[0])[2:-3] + " = '" + (
                self.lib_gui_ui.tableWidget.item(self.lib_gui_ui.tableWidget.currentRow(), 0).text())

            sql = sql.replace(';', '')
            sql = sql + "');"

            cursor.execute(f"SAVEPOINT SP1")
            cursor.execute(sql)

            cursor.execute(f"RELEASE SAVEPOINT SP1")

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))
            cursor.execute(f"ROLLBACK TO SAVEPOINT SP1")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
