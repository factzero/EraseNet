import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--pngPath', type=str, default='')
parser.add_argument('--jpgPath', type=str, default='')
args = parser.parse_args()

def get_png_files(png_path):
    """
    获取指定目录下所有PNG文件，不包括子目录
    
    Args:
        png_path: PNG图片目录路径
    
    Returns:
        list: PNG文件路径列表
    """
    png_files = []
    
    # 检查目录是否存在
    if not os.path.exists(png_path):
        print(f"目录不存在: {png_path}")
        return png_files
    
    # 遍历目录中的所有文件
    for filename in os.listdir(png_path):
        # 检查是否为PNG文件（不区分大小写）
        if filename.lower().endswith('.png'):
            # 构建完整路径
            full_path = os.path.join(png_path, filename)
            # 确保是文件而不是子目录
            if os.path.isfile(full_path):
                png_files.append(full_path)
    
    return png_files

def convert_single_png_to_jpg(png_file_path, jpg_file_path, bg_color=(255, 255, 255)):
    """
    将单个PNG图片转换为JPG图片
    """
    img = Image.open(png_file_path)
    
    # 处理透明度
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, bg_color)
        if img.mode == 'RGBA' or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
        else:
            background.paste(img)
        img = background
    
    img.save(jpg_file_path, 'JPEG', quality=95)

if __name__ == "__main__":
    os.makedirs(args.jpgPath, exist_ok=True)
    
    # 获取PNG目录下的所有PNG文件
    png_files = get_png_files(args.pngPath)
    
    print(f"找到 {len(png_files)} 个PNG文件")
    
    # 转换每个PNG文件
    for png_file in png_files:
        # 获取文件名（不含路径）
        filename = os.path.basename(png_file)
        # 替换扩展名为.jpg
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        # 构建JPG文件完整路径
        jpg_path = os.path.join(args.jpgPath, jpg_filename)
        
        try:
            convert_single_png_to_jpg(png_file, jpg_path)
            print(f"已转换: {png_file} -> {jpg_path}")
        except Exception as e:
            print(f"转换失败 {png_file}: {str(e)}")