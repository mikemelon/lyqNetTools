import os
from qt5_utils.multi_pictures_window import MultiPicturesWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_path_list = []
    for n in os.listdir(r'..\images'):
        file_path_list.append(os.path.join(r'..\images', n))
    print(file_path_list)
    win1 = MultiPicturesWindow(pic_path_list=file_path_list, pic_width=200, pic_height=200, rows=3, cols=2,
                               window_width=2000, window_height=1500, show_window_title=True, fixed_window_size=True)
    win1.show()
    sys.exit(app.exec_())