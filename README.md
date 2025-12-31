# PNG-and-BMP-conversion

这个仓库包含两个用于格式转换的脚本和一个图形界面程序：

- `bmp_to_png.py`：原始的批量 BMP -> PNG 转换（会删除原文件）。
- `png_to_bmp.py`：原始的批量 PNG -> BMP 转换（会删除原文件）。
- `converter_gui.py`：新的图形界面程序，支持拖放文件夹、选择文件夹、BMP↔PNG 双向批量转换，支持保留或删除原文件。

运行 GUI（需要安装依赖）：

```bash
python3 converter_gui.py
```

构建为独立可执行文件（使用 `pyinstaller`）：

- Windows (在 Windows 上运行)：

```bash
pyinstaller --onefile --windowed --name png_bmp_converter converter_gui.py
```

- macOS (在 macOS 上运行)：

```bash
pyinstaller --onefile --windowed --name png_bmp_converter converter_gui.py
```

说明：
- 打包后会在 `dist/` 目录里生成可执行文件，Windows 为 `.exe`，macOS 为可执行二进制（macOS 可能需要 codesign 以及允许运行的权限设置）。
- 若要使用自定义图标，请添加 `--icon=youricon.ico`（Windows）或 `.icns`（macOS）。

依赖请参见 `requirements.txt`。

示例：将一个文件夹拖到窗口中，选择“BMP→PNG”或“PNG→BMP”，点击“开始转换”。
# PNG-and-BMP-conversion