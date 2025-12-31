import os
from PIL import Image

# 设置要转换的文件夹路径
folder_path = r"Z:\Downloads\红色倚天\Weapon"  # 替换为您的文件夹路径

# 遍历文件夹下的所有文件
for filename in os.listdir(folder_path):
    if filename.lower().endswith(".png"):  # 仅处理PNG文件
        # 构造输入和输出文件路径
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".bmp")
        
        # 打开PNG图片并转换为BMP格式
        image = Image.open(input_path)
        bmp_image = image.convert('RGBA')
        bmp_image.save(output_path)
        print(f"Converted: {filename} -> {output_path}")

        # 删除原始PNG文件
        os.remove(input_path)
        print(f"Deleted original file: {input_path}")

print("批量转换和删除完成！")