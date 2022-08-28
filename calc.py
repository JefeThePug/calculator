import sys
import math
import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from functools import partial

# COLORS
C_BG = "black"
C_FRAME = "black"
C_DISP = "darkslategrey"
C_DISP_TXT = "yellowgreen"
C_BUT_NUM = "mistyrose"
C_BUT_OP = "darkseagreen"
C_BUT_FUNC = "palevioletred"

class Win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caculator")
        self.setGeometry(200, 200, 550, 600)
        self.setStyleSheet(f"background-color:{C_BG};")
        # FRAME
        self.fr_calc = QtWidgets.QFrame(self)
        self.fr_calc.setGeometry(QtCore.QRect(10, 10, 530, 580))
        self.fr_calc.setStyleSheet(f"background-color:{C_FRAME};")
        # DISPLAY
        self.lcd = QtWidgets.QLCDNumber(self.fr_calc)
        self.lcd.setGeometry(QtCore.QRect(15, 15, 500, 70))
        self.lcd.setStyleSheet(f"background-color:{C_DISP};color:{C_DISP_TXT};")
        self.lcd.setSmallDecimalPoint(True)
        self.lcd.setDigitCount(12)
        self.txt_mem = QtWidgets.QLabel(self.fr_calc)
        self.txt_mem.setGeometry(QtCore.QRect(17, 16, 16, 16))
        self.txt_mem.setStyleSheet(f"background-color:0;color:{C_DISP_TXT};")
        # ROWS
        self.rows = []
        for num in range(5):
            r = QtWidgets.QSplitter(self.fr_calc)
            r.setGeometry(QtCore.QRect(15, 90 * num + 120, 498, 80))
            r.setStyleSheet("QSplitter::handle{image:none;}")
            self.rows.append(r)
        # BUTTONS
        self.buttons = []
        self.fill_buttons()
        # MEMORY
        self.clear_mem()
        self.clear()

    def fill_buttons(self):
        style = [f"background-color:{x};" for x in [C_BUT_OP, C_BUT_NUM, C_BUT_FUNC]]
        text = [
            "AC", "MR", "MC", "M+", "CE",
             "7",  "8",  "9",  "±",  "√",
             "4",  "5",  "6",  "%",  "÷",
             "1",  "2",  "3",  "×",  "-",
             "0", "00",  ".",  "+",  "=",
        ]
        for row in range(5):
            for x in range(5):
                i = row * 5 + x
                txt = text[i]
                self.buttons.append(QtWidgets.QPushButton(self.rows[row]))
                self.buttons[i].setText(txt)
                self.buttons[i].setMaximumSize(QtCore.QSize(94, 80))
                s = (txt[0] in "00123456789.AMC") + (txt[0] in ".AMC")
                self.buttons[i].setStyleSheet(f"font:bold 26px;text-align:center;{style[s]}")
                self.buttons[i].clicked.connect(partial(self.clicked_button, txt))

    def clear(self, mem=False):
        self.eval_str = ""
        self.num_str = ""
        self.finished_num = False
        self.finished_eval = False
        self.sq_push = False
        if mem:
            self.clear_mem()

    def clear_mem(self):
        self.memory = "0"
        self.txt_mem.setText("")

    def append_to_number(self, txt):
        if txt == "." and "." in self.num_str:
            return

        if self.finished_num or self.sq_push:
            self.finished_num = False
            self.num_str = ""
        if self.finished_eval:
            self.finished_eval = False
            self.eval_str = ""

        self.num_str += txt
        if (r := re.match(r"(0{1,2})(\d.*)", self.num_str)) :
            self.num_str = r.group(2)

    def add_operator(self, txt):
        txt = txt.replace("×", "*").replace("÷", "/")
        self.finished_eval = False
        self.sq_push = False

        if self.num_str:
            if not self.finished_num:
                self.eval_str += self.num_str
            if re.match(r"[\d.]+[-+*/][\d.]+", self.eval_str):
                self.eval_str = f"{eval(self.eval_str)}"
                self.num_str = self.eval_str
            self.eval_str += txt
        else:
            self.eval_str = self.eval_str[:-1] + txt

        self.finished_num = True

    def totaling(self, txt):
        if txt == "%":
            self.num_str = f"{float(self.num_str)/100}"

        if not (
            (s := self.eval_str + self.num_str).count(".") <= 1
            and not re.findall(r"[-+*/]", s)
        ):
            self.eval_str = s
        try:
            n = eval(self.eval_str)
        except ZeroDivisionError:
            n = "E"
        self.eval_str = f"{n}"
        self.num_str = f"{n}"
        self.finished_num = True
        self.finished_eval = True

    def check_clicked(self, txt):
        if txt.isnumeric() or txt == ".":
            self.append_to_number(txt)
        elif txt in "+-×÷":
            self.add_operator(txt)
        elif txt in "=%":
            self.totaling(txt)
        elif txt == "√":
            self.sq_push = True
            if "-" in self.num_str:
                self.num_str = "E"
            else:
                self.num_str = f"{math.sqrt(float(self.num_str))}"
                # self.finished_num = True
        elif txt == "±":
            n = float(self.num_str) if "." in self.num_str else int(self.num_str)
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
        if "E" not in self.num_str or txt == "AC":
            self.check_clicked(txt)
            if "E" in self.num_str:
                self.lcd_out.display("ERROR")
                return
            self.lcd.display(float(self.num_str) if self.num_str else "0")
        else:
            self.lcd.display("ERROR")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Win()
    MainWindow.show()
    sys.exit(app.exec_())
