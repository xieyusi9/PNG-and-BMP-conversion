import os
import sys
from pathlib import Path
from PIL import Image

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QComboBox,
    QCheckBox,
)


class ConverterThread(QThread):
    log = Signal(str)

    def __init__(self, folder: str, mode: str, delete_original: bool):
        super().__init__()
        self.folder = Path(folder)
        self.mode = mode
        self.delete_original = delete_original

    def run(self):
        if not self.folder.exists():
            self.log.emit(f"路径不存在: {self.folder}")
            return

        if self.mode == "BMP→PNG":
            exts = (".bmp",)
            target_ext = ".png"
        else:
            exts = (".png",)
            target_ext = ".bmp"

        count = 0
        for root, _, files in os.walk(self.folder):
            for f in files:
                if f.lower().endswith(exts):
                    src = Path(root) / f
                    dst = src.with_suffix(target_ext)
                    try:
                        img = Image.open(src)
                        if img.mode not in ("RGB", "RGBA"):
                            img = img.convert("RGBA")
                        img.save(dst)
                        self.log.emit(f"Converted: {src} -> {dst}")
                        count += 1
                        if self.delete_original:
                            try:
                                src.unlink()
                                self.log.emit(f"Deleted: {src}")
                            except Exception as e:
                                self.log.emit(f"Failed to delete {src}: {e}")
                    except Exception as e:
                        self.log.emit(f"Failed to convert {src}: {e}")

        self.log.emit(f"完成：共转换 {count} 个文件")


class DropLabel(QLabel):
    dropped = Signal(str)

    def __init__(self, text="将文件夹拖到这里或点击选择"):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            "QLabel{border: 2px dashed #666; padding: 20px; font-size:14px;}"
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return
        # 只处理第一个拖入项（通常是文件或文件夹）
        path = urls[0].toLocalFile()
        self.dropped.emit(path)


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量 PNG ↔ BMP 转换器")
        self.resize(700, 420)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.drop = DropLabel()
        self.drop.dropped.connect(self.on_dropped)
        layout.addWidget(self.drop)

        row = QHBoxLayout()
        row.addWidget(QLabel("转换方向:"))
        self.mode = QComboBox()
        self.mode.addItems(["BMP→PNG", "PNG→BMP"])
        row.addWidget(self.mode)

        self.delete_cb = QCheckBox("转换后删除原文件")
        row.addWidget(self.delete_cb)

        choose_btn = QPushButton("选择文件夹")
        choose_btn.clicked.connect(self.choose_folder)
        row.addWidget(choose_btn)

        convert_btn = QPushButton("开始转换")
        convert_btn.clicked.connect(self.start_conversion)
        row.addWidget(convert_btn)

        layout.addLayout(row)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.folder_path = None

    def on_dropped(self, path: str):
        p = Path(path)
        if p.is_dir():
            self.folder_path = str(p)
            self.drop.setText(f"已选择：{self.folder_path}")
            self.log.append(f"已添加文件夹: {self.folder_path}")
        else:
            # 如果拖入的是文件，则使用父目录
            parent = p.parent
            self.folder_path = str(parent)
            self.drop.setText(f"已选择：{self.folder_path}")
            self.log.append(f"已添加文件所属文件夹: {self.folder_path}")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹", os.path.expanduser("~"))
        if folder:
            self.folder_path = folder
            self.drop.setText(f"已选择：{self.folder_path}")
            self.log.append(f"已选择文件夹: {self.folder_path}")

    def start_conversion(self):
        if not self.folder_path:
            self.log.append("请先选择或拖入要转换的文件夹")
            return

        mode = self.mode.currentText()
        delete_original = self.delete_cb.isChecked()
        self.thread = ConverterThread(self.folder_path, mode, delete_original)
        self.thread.log.connect(self.log.append)
        self.thread.finished.connect(lambda: self.log.append("转换线程已结束"))
        self.thread.start()


def main():
    app = QApplication(sys.argv)
    win = ConverterApp()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
