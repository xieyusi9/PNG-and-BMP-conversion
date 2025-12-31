import os
from PIL import Image

# 设置要转换的文件夹路径
folder_path = r"Z:\Downloads\屠龙\bmp"  # 替换为您的文件夹路径

# 遍历文件夹下的所有文件
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".bmp"):  # 仅处理 BMP 文件
        input_path  = os.path.join(folder_path, filename)
        output_path = os.path.join(
            folder_path,
            os.path.splitext(filename)[0] + ".png"
        )

        # 打开 BMP 图片并转换为 PNG 格式
        image = Image.open(input_path)

        # 如果原图是 “RGB” 模式或 “RGBA” 模式，保存为 PNG 通常没问题；
        # BMP 文件如果有透明通道（RGBA），Pillow 保存 BMP 时可能不能写入 RGBA 模式（见后文）；
        # 但这里我们是从 BMP 到 PNG，PNG 支持透明，所以可以保留 RGBA。
        # 为保险起见，如果模式不是 “RGB” 或 “RGBA”，转成 “RGBA” 或 “RGB”：
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA")

        image.save(output_path)
        print(f"Converted: {filename} -> {os.path.basename(output_path)}")

        # 删除原始 BMP 文件
        os.remove(input_path)
        print(f"Deleted original file: {filename}")

print("批量转换和删除完成！")