import os.path
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QScrollArea, QVBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


# 该文件显示多图像的窗口口，直接代码生成，因此没有对应的.ui文件。
class MultiPicturesWindow(QMainWindow):
    def __init__(self, pic_path_list=[], pic_width=160, pic_height=90, rows=20, cols=30,
                 horizon_spacing=20, vertical_spacing=20,
                 window_width=1280, window_height=800, show_default_pics=True,
                 fixed_window_size=False, show_window_title=True):
        super(MultiPicturesWindow, self).__init__()
        self.setWindowTitle('巡视主机屏幕')
        self.setWindowIcon(QIcon('../images/logo2.png'))
        if not show_window_title:
            self.setWindowFlags(Qt.FramelessWindowHint)  # 不显示标题栏
        # pic_width, pic_height = 160, 90
        # rows, cols = 20, 30
        # horizon_spacing, vertical_spacing = 20, 20

        # 宽度 = 各图片的宽度 + 图片间水平空隙的宽度 + 裕量（150）
        # 高度 = 各图片的高度 + 图片间垂直空隙的高度 + 标题栏高度 + 裕量（150)
        # 经过计算，可以自适应显示所有图片，不需要滚动条（但现在由于显示器尺寸可能不足，需要显示滚动条，因此注释掉）
        if fixed_window_size:
            self.setFixedSize(pic_width*cols + horizon_spacing*(cols-1) + 150,
                              pic_height*rows + vertical_spacing*(rows-1) +
                              self.frameGeometry().height()-self.geometry().height() + 150)
        else:
            self.setGeometry(self.x(), self.y(), window_width, window_height)

        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(scroll_area)
        self.centralwidget = QWidget(self)
        self.centralwidget.setLayout(vbox_layout)
        self.setCentralWidget(self.centralwidget)

        self.multi_pics_widget = QWidget(self.centralwidget)  # 放置多张图的控件，使用GridLayout

        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(horizon_spacing)
        grid_layout.setVerticalSpacing(vertical_spacing)
        self.multi_pics_widget.setLayout(grid_layout)

        if not show_default_pics and len(pic_path_list) == 0:
            print('No pics for show')
        else:
            for r in range(rows):
                for c in range(cols):
                    pic_item = QLabel(self.multi_pics_widget)
                    if r*cols+c < len(pic_path_list):
                        # print(r*cols+c)
                        # print(pic_path_list[r*cols+c])
                        if os.path.exists(pic_path_list[r*cols+c]):
                            pic_item.setPixmap(QPixmap(pic_path_list[r*cols+c]).scaled(pic_width, pic_height))
                        else: # 文件找不到，显示一个特殊图像
                            pic_item.setPixmap(QPixmap('../images/splash_title.png').scaled(pic_width, pic_height))
                        grid_layout.addWidget(pic_item, r, c)
                    else:
                        if show_default_pics:
                            pic_item.setPixmap(QPixmap('../images/logo2.png').scaled(pic_width, pic_height))
                            grid_layout.addWidget(pic_item, r, c)

        scroll_area.setWidget(self.multi_pics_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = MultiPicturesWindow()
    my_win.show()
    sys.exit(app.exec_())
