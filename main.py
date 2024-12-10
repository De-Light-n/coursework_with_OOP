import sys
import os
import PySide2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from qt_material import *

from interface import *
from user import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Забирання рамки
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Тінs
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # Іконка і заголовок застосунку
        self.setWindowIcon(
            QtGui.QIcon(
                ":/icons/icons/account_balance_24dp_FFFFFF_FILL0_wght400_GRAD0_opsz24 – копія.svg"
            )
        )
        self.setWindowTitle("Довідник Абітурієнта")

        QSizeGrip(self.ui.size_grip)

        # Кнопки дій над вікном
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        self.ui.close_window_button.clicked.connect(self.handle_close)
        self.ui.restor_window_button.clicked.connect(lambda: self.restore_window())

        # Кнопки дій для меню
        self.ui.institution_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.institutions_page)
        )
        self.ui.specialty_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.specialty_page)
        )
        self.ui.account_menu_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.account_page)
        )
        self.ui.account_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.account_page)
        )
        self.ui.calculation_button.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.calculator_page)
        )
        self.ui.menu_button.clicked.connect(lambda: self.left_menu_slide())
        
        
        self.ui.log_out_button.clicked.connect(self.handle_logout)
        self.ui.login_pushButton.clicked.connect(self.handle_login)

        # Перетягування вікна
        self.ui.header_frame.mouseMoveEvent = self.moveWindow
        self.ui.central_frame.mouseMoveEvent = self.moveWindow

        # Події до кнопок калькулятора
        self.ui.calculate_button.clicked.connect(
            lambda: self.calculate_and_create_piechart()
        )

        self.current_user = None
        self.ui.login_pushButton.clicked.connect(self.handle_login)
        self.ui.main_body_account_stackedWidget.setCurrentWidget(self.ui.main_body_account_stackedWidgetPage2)
        
        
        self.show()

    def moveWindow(self, event):
        if not self.isMaximized():
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_window(self):
        """Змінює повноекранний режим"""
        if self.isMaximized():
            self.showNormal()
            self.ui.restor_window_button.setIcon(
                QtGui.QIcon(":/icons/icons/open_in_full_24dp_000000.png")
            )
        else:
            self.showMaximized()
            self.ui.restor_window_button.setIcon(
                QtGui.QIcon(":/icons/icons/close_fullscreen_24dp_000000.png")
            )

    def left_menu_slide(self):
        width = self.ui.left_munu_cont_frame.width()
        if width == 37:
            new_width = 190
        else:
            new_width = 37

        self.animation = QPropertyAnimation(
            self.ui.left_munu_cont_frame, b"minimumWidth"
        )
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def calculate_and_create_piechart(self):
        """Збирає значення з полів калькулятора, обраховує конкурсний бал і виводить результат з графіком"""
        coefficients = [
            self.ui.coef_1_lineEdit.text(),
            self.ui.coef_2_lineEdit.text(),
            self.ui.coef_3_lineEdit.text(),
            self.ui.coef_4_lineEdit.text(),
            self.ui.coef_cc_lineEdit.text(),
            self.ui.coef_EFVV_lineEdit.text(),
            self.ui.coef_industry_lineEdit.text(),
            self.ui.coef_region_lineEdit.text(),
        ]
        scores = [
            ("1-й предмет", self.ui.score_1_lineEdit.text()),
            ("2-й предмет", self.ui.score_2_lineEdit.text()),
            ("3-й предмет", self.ui.score_3_lineEdit.text()),
            ("4-й предмет", self.ui.score_4_lineEdit.text()),
            ("Творчий конкурс", self.ui.score_cc_lineEdit.text()),
            ("ЄФВВ", self.ui.score_EFVV_lineEdit.text()),
        ]
        series = QPieSeries()

        results = []

        for score, coef in zip(scores, coefficients):
            try:
                grade = float(score[1])
                coef = float(coef)
                if coef < 0 or grade < 0:
                    raise ValueError()
                result_per_subject = grade * coef
                results.append((result_per_subject, coef))
                slice = series.append(
                    f"{score[0]}: {result_per_subject:.2f}", result_per_subject
                )
                slice.setLabelVisible(False)
                slice.setExploded(False)
                QTimer.singleShot(
                    0,
                    lambda s=slice: s.hovered.connect(
                        lambda hovered, s=s: self.on_slice_hovered(s, hovered)
                    ),
                )
            except ValueError:
                continue

        overall_score = sum(r[0] for r in results)
        coef_sum = sum(r[1] for r in results)
        if coef_sum > 0:
            overall_score /= coef_sum

        try:
            reg_coef = float(coefficients[-2]) if coefficients[-2] else 1.0
        except ValueError:
            reg_coef = 1.0

        try:
            indust_coef = float(coefficients[-1]) if coefficients[-1] else 1.0
        except ValueError:
            indust_coef = 1.0

        overall_score *= reg_coef * indust_coef

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Результати обчислень")

        self.ui.calculator_result_label.setText(
            f"Загальний результат: {overall_score:.2f}"
        )

        if hasattr(self, "current_chart_view") and self.current_chart_view is not None:
            self.ui.horizontalLayout_16.removeWidget(self.current_chart_view)
            self.current_chart_view.deleteLater()
            self.current_chart_view = None

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setMinimumSize(150, 150)
        self.ui.horizontalLayout_16.addWidget(chart_view)

        self.current_chart_view = chart_view

    def on_slice_hovered(self, slice, hovered):
        """
        Обробляє подію наведення на слайс.
        """
        if hovered:
            slice.setExploded(True)
            slice.setLabelVisible(True)
        else:
            slice.setExploded(False)
            slice.setLabelVisible(False)

    def handle_login(self):
        """Обробка авторизації користувача."""
        username = self.ui.name_lineEdit.text().strip()
        password = self.ui.password_lineEdit.text().strip()

        if not username or not password:
            self.ui.advice_pass_ac_label.setText("Введіть ім'я користувача та пароль.")
            return

        try:
            user = User(username=username, password=password)
            self.current_user = user
            self.ui.advice_pass_ac_label.setText("Авторизація успішна.")
            
            self.ui.user_name_lineEdit.setText(str(self.current_user.name))
            self.ui.user_prizvushce_lineEdit.setText(str(self.current_user.prizvushce))
            self.ui.user_pobatkovilineEdit.setText(str(self.current_user.pobatkovi))
            self.ui.user_burthday_lineEdit.setText(str(self.current_user.burthday))
            self.ui.user_phone_lineEdit.setText(str(self.current_user.phone))
            self.ui.user_email_lineEdit.setText(str(self.current_user.email))
            self.ui.ukr_lang_lineEdit.setText(str(self.current_user.ukr_lan_score))
            self.ui.math_lineEdit.setText(str(self.current_user.math_score))
            self.ui.history_lineEdit.setText(str(self.current_user.history))
            self.ui.forth_subject_comboBox.setCurrentIndex(self.current_user.forth_subject[0])
            self.ui.four_sub_lineEdit.setText(str(self.current_user.forth_subject[1]))
            self.ui.creative_lineEdit.setText(str(self.current_user.creative_concurse))
            self.ui.EFVV_lineEdit.setText(str(self.current_user.EFVV_score))
            
            
            self.ui.account_button.setText(self.current_user.username)
            self.create_user_score_chart()
            
            self.switch_to_account_page()
        except ValueError as e:
            self.ui.advice_pass_ac_label.setText(str(e))

    def save_user_data(self):
        self.current_user.name = self.ui.user_name_lineEdit.text()
        self.current_user.prizvushce = self.ui.user_prizvushce_lineEdit.text()
        self.current_user.pobatkovi = self.ui.user_pobatkovilineEdit.text()
        self.current_user.burthday = self.ui.user_burthday_lineEdit.text()
        self.current_user.phone = self.ui.user_phone_lineEdit.text()
        self.current_user.email = self.ui.user_email_lineEdit.text()
        self.current_user.ukr_lan_score = self.ui.ukr_lang_lineEdit.text()
        self.current_user.math_score = self.ui.math_lineEdit.text()
        self.current_user.history = self.ui.history_lineEdit.text()
        self.current_user.forth_subject[0] = self.ui.forth_subject_comboBox.currentIndex()
        self.current_user.forth_subject[1] = self.ui.four_sub_lineEdit.text()
        self.current_user.creative_concurse = self.ui.creative_lineEdit.text()
        self.current_user.EFVV_score = self.ui.EFVV_lineEdit.text()
        
        self.current_user.save_data()
        
    def handle_close(self):
        """Закриття програми з збереженням даних."""
        if self.current_user:
            self.save_user_data()
        self.close()

    def handle_logout(self):
        """Розлогінення користувача."""
        if self.current_user:
            self.save_user_data()
        self.ui.account_button.setText("Гість")
        self.current_user = None
        self.ui.advice_pass_ac_label.setText("Ви вийшли з облікового запису.")
        self.ui.main_body_account_stackedWidget.setCurrentWidget(self.ui.main_body_account_stackedWidgetPage2)

    def switch_to_account_page(self):
        """Перемикання на головну сторінку після успішного входу."""
        self.ui.main_body_account_stackedWidget.setCurrentWidget(self.ui.main_body_account_stackedWidgetPage1)

    def create_user_score_chart(self):
        """Створення бар-графіку оцінок користувача."""
        if not self.current_user:
            return 
        
        subjects = [
            "Українська мова",
            "Математика",
            "Історія України",
            "4-й предмет",
            "Творчий конкурс",
            "ЄФВВ"
        ]
        scores = [
            float(self.current_user.ukr_lan_score or 0),
            float(self.current_user.math_score or 0),
            float(self.current_user.history or 0),
            float(self.current_user.forth_subject[1] or 0),
            float(self.current_user.creative_concurse or 0),
            float(self.current_user.EFVV_score or 0),
        ]

        bar_set = QBarSet("Оцінки")
        bar_set.append(scores)

        bar_series = QBarSeries()
        bar_series.append(bar_set)

        chart = QChart()
        chart.addSeries(bar_series)
        chart.setTitle("Оцінки за предметами")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        axis_x = QBarCategoryAxis()
        axis_x.append(subjects)
        chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
        bar_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, 200)
        chart.addAxis(axis_y, QtCore.Qt.AlignLeft)
        bar_series.attachAxis(axis_y)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        
        for i in reversed(range(self.ui.account_graph_verticalLayout.count())):
            widget = self.ui.account_graph_verticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.ui.account_graph_verticalLayout.addWidget(chart_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
