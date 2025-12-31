# PNG-and-BMP-conversion

这个仓库包含两个用于格式转换的脚本和一个图形界面程序：

- `bmp_to_png.py`：原始的批量 BMP → PNG 转换脚本（会删除原文件）。
- `png_to_bmp.py`：原始的批量 PNG → BMP 转换脚本（会删除原文件）。
- `converter_gui.py`：新的图形界面程序，支持拖放文件夹、选择文件夹、BMP ↔ PNG 双向批量转换，支持保留或删除原文件。

## 使用 GUI

需要先安装依赖，然后运行：

```bash
pip install -r requirements.txt
python3 converter_gui.py
```

在打开的窗口中：
1. 拖放一个文件夹到窗口或点击"选择文件夹"按钮选择待转换的文件夹
2. 选择转换方向：BMP → PNG 或 PNG → BMP
3. 可选：勾选"删除原文件"以删除转换后的原文件
4. 点击"开始转换"开始批量转换

转换日志会实时显示在窗口底部。

## 构建为独立可执行文件

### 依赖

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Windows

```bash
pyinstaller --onefile --windowed --name png_bmp_converter converter_gui.py
```

生成的可执行文件位于 `dist/png_bmp_converter.exe`。

### macOS

为了避免启动时打开终端窗口，使用 `.app` bundle 格式：

```bash
pyinstaller --windowed --name png_bmp_converter converter_gui.py

生成的可执行程序位于 `dist/png_bmp_converter.app`。

## 下载和运行预编译版本

访问 [GitHub Releases](https://github.com/xieyusi9/PNG-and-BMP-conversion/releases) 下载最新版本：

- **Windows**: 下载 `.exe` 文件，直接双击运行
- **macOS**: 下载 `.zip` 文件，解压后双击 `png_bmp_converter.app` 运行
	- 首次运行时，如果 macOS 提示"无法打开"，请右击应用 → 选择"打开" → 点击"打开"确认即可
	- 或在终端运行：`open -a /path/to/png_bmp_converter.app`

## 关于 macOS 代码签名

应用已通过自签名证书进行签名，允许在任何 macOS 系统上运行，无需 Apple Developer ID。
如果仍遇到 Gatekeeper 警告，可在"系统设置" → "安全性与隐私" → "仍然打开"，或直接在终端中运行该应用。
```

生成的应用包位于 `dist/png_bmp_converter.app`。

**注意**：GitHub Actions 自动为 Apple Silicon（ARM64）构建 `.app` bundle 并在 Releases 中发布。

### 自定义图标

添加 `--icon` 选项指定自定义图标：

- Windows: `pyinstaller --onefile --windowed --icon=youricon.ico --name png_bmp_converter converter_gui.py`
- macOS: `pyinstaller --windowed --icon=youricon.icns --name png_bmp_converter converter_gui.py`

## CI/CD 构建

此仓库使用 GitHub Actions 自动构建 Windows `.exe` 和 macOS `.app` 两个平台的可执行文件，并发布为 Release。详见 `.github/workflows/build.yml`。
