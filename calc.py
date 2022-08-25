import sys
import math
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial


class Win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 550, 600)
        self.setWindowTitle("Caculator")
        self.setStyleSheet("background-color: black;")

        # FRAME
        self.fr_calc = QtWidgets.QFrame(self)
        self.fr_calc.setGeometry(QtCore.QRect(10, 10, 530, 580))
        self.fr_calc.setStyleSheet("background-color: black;")
        self.fr_calc.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.fr_calc.setFrameShadow(QtWidgets.QFrame.Raised)
        # DISPLAY
        self.lcd_out = QtWidgets.QLCDNumber(self.fr_calc)
        self.lcd_out.setGeometry(QtCore.QRect(15, 15, 500, 70))
        self.lcd_out.setFont(QtGui.QFont())
        self.lcd_out.setStyleSheet(
            "background-color: darkslategrey;color: yellowgreen;"
        )
        self.lcd_out.setSmallDecimalPoint(True)
        self.lcd_out.setDigitCount(12)
        self.lcd_out.setProperty("value", 0.0)
        self.txt_mem = QtWidgets.QLabel(self.fr_calc)
        self.txt_mem.setGeometry(QtCore.QRect(17, 16, 16, 16))
        self.txt_mem.setStyleSheet("background-color: 0;color: yellowgreen;")
        # ROWS
        self.rows = []
        for num in range(5):
            r = QtWidgets.QSplitter(self.fr_calc)
            r.setStyleSheet("QSplitter::handle { image: none; }")
            r.setGeometry(QtCore.QRect(15, 90 * num + 120, 498, 80))
            self.rows.append(r)
        # BUTTONS
        self.but_ac = QtWidgets.QPushButton(self.rows[0])
        self.but_mr = QtWidgets.QPushButton(self.rows[0])
        self.but_mmin = QtWidgets.QPushButton(self.rows[0])
        self.but_mplu = QtWidgets.QPushButton(self.rows[0])
        self.but_ce = QtWidgets.QPushButton(self.rows[0])
        self.but_7 = QtWidgets.QPushButton(self.rows[1])
        self.but_8 = QtWidgets.QPushButton(self.rows[1])
        self.but_9 = QtWidgets.QPushButton(self.rows[1])
        self.but_plumin = QtWidgets.QPushButton(self.rows[1])
        self.but_sqrt = QtWidgets.QPushButton(self.rows[1])
        self.but_4 = QtWidgets.QPushButton(self.rows[2])
        self.but_5 = QtWidgets.QPushButton(self.rows[2])
        self.but_6 = QtWidgets.QPushButton(self.rows[2])
        self.but_per = QtWidgets.QPushButton(self.rows[2])
        self.but_div = QtWidgets.QPushButton(self.rows[2])
        self.but_1 = QtWidgets.QPushButton(self.rows[3])
        self.but_2 = QtWidgets.QPushButton(self.rows[3])
        self.but_3 = QtWidgets.QPushButton(self.rows[3])
        self.but_mul = QtWidgets.QPushButton(self.rows[3])
        self.but_sub = QtWidgets.QPushButton(self.rows[3])
        self.but_0 = QtWidgets.QPushButton(self.rows[4])
        self.but_00 = QtWidgets.QPushButton(self.rows[4])
        self.but_dec = QtWidgets.QPushButton(self.rows[4])
        self.but_add = QtWidgets.QPushButton(self.rows[4])
        self.but_eq = QtWidgets.QPushButton(self.rows[4])
        self.fill_buttons()
        self.clear_mem()
        self.clear()

    def fill_buttons(self):
        styles = [
            "background-color: darkseagreen;",
            "background-color: mistyrose;",
            "background-color: palevioletred;",
        ]
        d = {
            self.but_ac: "AC",
            self.but_mr: "MR",
            self.but_mmin: "MC",
            self.but_mplu: "M+",
            self.but_ce: "CE",
            self.but_7: "7",
            self.but_8: "8",
            self.but_9: "9",
            self.but_plumin: "±",
            self.but_sqrt: "√",
            self.but_4: "4",
            self.but_5: "5",
            self.but_6: "6",
            self.but_per: "%",
            self.but_div: "÷",
            self.but_1: "1",
            self.but_2: "2",
            self.but_3: "3",
            self.but_mul: "×",
            self.but_sub: "-",
            self.but_0: "0",
            self.but_00: "00",
            self.but_dec: ".",
            self.but_add: "+",
            self.but_eq: "=",
        }
        for button, txt in d.items():
            button.setText(txt)
            button.setMinimumSize(QtCore.QSize(94, 80))
            button.setMaximumSize(QtCore.QSize(94, 80))
            style = (txt[0] in "00123456789.AMC") + (txt[0] in ".AMC")
            button.setStyleSheet(
                "padding: 15px 20px;font: bold 26px;text-align: center;" + styles[style]
            )
            button.clicked.connect(partial(self.clicked_button, txt))

    def clear(self, mem=False):
        self.eval_str = ""
        self.num_str = ""
        self.finished_num = False
        if mem:
            self.clear_mem()

    def clear_mem(self):
        self.memory = 0
        self.txt_mem.setText("")

    def check_clicked(self, txt):
        if txt.isnumeric() or txt == ".":
            if self.finished_num:
                self.finished_num = False
                self.num_str = ""
            if txt == "." and "." in self.num_str:
                txt = ""
            self.num_str += txt
            if self.num_str[0] == "0" and len(self.num_str) > 1:
                self.num_str = self.num_str[1:]
        elif txt in "+-×÷":
            txt = txt.replace("×", "*").replace("÷", "/")
            if self.num_str:
                if self.num_str == "E":
                    return
                if not self.finished_num:
                    self.eval_str += self.num_str
                if re.match(r"[\d.]+[-+*/][\d.]+", self.eval_str):
                    self.eval_str = f"{eval(self.eval_str)}"
                    self.num_str = self.eval_str
                    self.finished_num = True
                self.eval_str += txt
            else:
                self.eval_str = self.eval_str[:-1] + txt
            self.finished_num = True
        elif txt in "=%":
            if txt == "%":
                self.num_str = f"{float(self.num_str)/100}"
            self.eval_str += self.num_str
            try:
                n = eval(self.eval_str)
            except ZeroDivisionError:
                n = "E"
            self.eval_str = f"{n}"
            self.num_str = f"{n}"
            self.finished_num = True
        elif txt == "√":
            self.num_str = f"{math.sqrt(float(self.num_str))}"
            self.finished_num = True
        elif txt == "±":
            if "." in self.num_str:
                n = float(self.num_str)
            else:
                n = int(self.num_str)
            self.num_str = f"{-n}"
        elif txt == "CE":
            self.num_str = ""
        elif txt == "AC":
            self.clear(True)
        elif txt == "MR":
            self.num_str = self.memory
            self.finished_num = True
        elif txt == "M+":
            self.memory = self.num_str
            self.finished_num = True
            self.txt_mem.setText("M")
        elif txt == "MC":
            self.clear_mem()

    def clicked_button(self, txt):
        self.check_clicked(txt)
        if self.num_str == "E":
            self.lcd_out.display("ERROR")
        else:
            self.lcd_out.display(float(self.num_str) if self.num_str else "0")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Win()
    MainWindow.show()
    sys.exit(app.exec_())
