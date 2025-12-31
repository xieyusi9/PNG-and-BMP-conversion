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
# 为 macOS 生成一个 `.app` 应用包（这样从 Finder 启动不会打开终端窗口）
如果你使用的是 Apple Silicon（M1/M2 等），为了兼容 Intel 与 Apple Silicon，我们在 CI 中构建了一个 universal `.app`（包含 arm64 与 x86_64 架构）。

在本地生成 universal `.app` 的示例命令（需要在一台 macOS 机器上分别生成两个架构的构建并用 `lipo` 合并）：

```bash
# 1) 原生 ARM 构建（在 Apple Silicon 上运行）：
python3 -m pip install -r requirements.txt pyinstaller
pyinstaller --windowed --name png_bmp_converter converter_gui.py
mv dist/png_bmp_converter.app dist/png_bmp_converter-arm.app

# 2) 在 Rosetta 下做 x86_64 构建（Apple Silicon 上同样可以使用 Rosetta）：
softwareupdate --install-rosetta --agree-to-license
arch -x86_64 python3 -m pip install -r requirements.txt pyinstaller
arch -x86_64 pyinstaller --windowed --name png_bmp_converter converter_gui.py
mv dist/png_bmp_converter.app dist/png_bmp_converter-x86.app

# 3) 合并为 universal .app
cp -R dist/png_bmp_converter-arm.app dist/png_bmp_converter.app
lipo -create -output dist/png_bmp_converter.app/Contents/MacOS/png_bmp_converter \
	dist/png_bmp_converter-arm.app/Contents/MacOS/png_bmp_converter \
	dist/png_bmp_converter-x86.app/Contents/MacOS/png_bmp_converter
chmod +x dist/png_bmp_converter.app/Contents/MacOS/png_bmp_converter
```
```

说明：
- 打包后会在 `dist/` 目录里生成可执行文件：Windows 为 `dist/png_bmp_converter.exe`，macOS 为应用包 `dist/png_bmp_converter.app`（macOS 可能需要 codesign 以及允许运行的权限设置）。
- 若要使用自定义图标，请添加 `--icon=youricon.ico`（Windows）或 `--icon=youricon.icns`（macOS）。

依赖请参见 `requirements.txt`。

示例：将一个文件夹拖到窗口中，选择“BMP→PNG”或“PNG→BMP”，点击“开始转换”。
# PNG-and-BMP-conversion