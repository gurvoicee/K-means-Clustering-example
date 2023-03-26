import sys
import sqlite3
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QPushButton, QLineEdit, QLabel, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

path = "indir" ## name of image
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'My App'
        self.left = 50
        self.top = 50
        self.width = 320
        self.height = 400
        self.initUI()

        # Connect DataBase
        self.db = sqlite3.connect('comments.db')
        self.cursor = self.db.cursor()
        self.create_table()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # User sing in
        self.username, ok_pressed = QInputDialog.getText(self, 'Kullanıcı Adı', 'Kullanıcı adınızı girin:')
        if ok_pressed:
            self.setWindowTitle(f"{self.title} - {self.username}")
        else:
            self.setWindowTitle(self.title)

        # Text box
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 60)
        self.textbox.resize(280, 30)

        # Save button
        self.save_button = QPushButton('Kaydet', self)
        self.save_button.move(20, 100)
        self.save_button.resize(280, 30)
        self.save_button.clicked.connect(self.save_comment)

        # Image
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap(path+".png").scaledToWidth(280))
        self.image_label.move(20, 140)
        self.image_label.resize(280, 100)

        # Comment
        self.comments_label = QLabel(self)
        self.comments_label.move(20, 250)
        self.comments_label.resize(280, 120)

        self.show()

    def save_comment(self):
        text = self.textbox.text()
        if text:
            print(f"{self.username} Yorum: ", text)

            # add user, comment and path of image to database
            self.cursor.execute("INSERT INTO comments (image_path, comment, username) VALUES (?, ?, ?)", (path+".png", text, self.username))
            self.db.commit()

            self.textbox.setText("")

        else:
            print("Lütfen bir yorum girin.")

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS comments
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      image_path TEXT,
                      comment TEXT,
                      username TEXT)''')
        self.db.commit()

    def read_comments(self):
        self.cursor.execute("SELECT * FROM comments")
        comments = self.cursor.fetchall()

        layout = QVBoxLayout()
        for comment in comments:
            comment_label = QLabel(f"{comment[3]}: {comment[2]}")
            layout.addWidget(comment_label)

        self.comments_label.setLayout(layout)

    def all(self):
        self.cursor.execute("SELECT * FROM comments")
        comments = self.cursor.fetchall()
        for comment in comments:
            print(comment)

    
    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.read_comments()
    ex.all()
    sys.exit(app.exec_())
