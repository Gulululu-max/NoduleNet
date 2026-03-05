import os
import zipfile
from tqdm import tqdm

def unzip_single_subset(zip_file_path, target_dir):
    """
    解压单个subset压缩包到目标文件夹（断点续传）
    :param zip_file_path: subset9.zip的完整路径（如~/LUNA16/raw/subset9.zip）
    :param target_dir: 已有的combined文件夹路径
    """
    # 确保目标文件夹存在
    os.makedirs(target_dir, exist_ok=True)
    
    if not os.path.exists(zip_file_path):
        print(f"错误：未找到文件 {zip_file_path}")
        return
    
    zip_name = os.path.basename(zip_file_path)
    print(f"开始解压：{zip_name}")
    
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            # 遍历压缩包内文件，带进度条
            for file_info in tqdm(zf.infolist(), desc=f"解压{zip_name}"):
                if file_info.is_dir():
                    continue
                
                # 目标文件路径（合并到combined）
                target_file = os.path.join(target_dir, os.path.basename(file_info.filename))
                
                # 跳过已解压的文件（避免重复）
                if os.path.exists(target_file) and os.path.getsize(target_file) == file_info.file_size:
                    continue
                
                # 解压并修正路径
                zf.extract(file_info, target_dir)
                extracted_file = os.path.join(target_dir, file_info.filename)
                if os.path.exists(extracted_file) and extracted_file != target_file:
                    os.rename(extracted_file, target_file)
                    # 删除空文件夹
                    extracted_dir = os.path.dirname(extracted_file)
                    if not os.listdir(extracted_dir):
                        os.rmdir(extracted_dir)
        
        print(f"\n✅ {zip_name} 已解压合并到：{target_dir}")
        
        # 统计更新后的文件数
        all_files = os.listdir(target_dir)
        mhd_files = [f for f in all_files if f.endswith('.mhd')]
        raw_files = [f for f in all_files if f.endswith('.raw')]
        print(f"📊 更新后：总文件数={len(all_files)}, .mhd={len(mhd_files)}, .raw={len(raw_files)}")
    
    except zipfile.BadZipFile:
        print(f"错误：{zip_name} 是损坏的压缩包，请重新下载！")
    except Exception as e:
        print(f"解压出错：{str(e)}")

if __name__ == "__main__":
    SUBSET9_ZIP_PATH = "/home/ubuntu-user/WMQ/data/subsets/subset9.zip"  # subset9.zip的路径
    COMBINED_DIR = "/home/ubuntu-user/WMQ/data/merged_subsets"  # 已有的combined文件夹路径
    
    unzip_single_subset(SUBSET9_ZIP_PATH, COMBINED_DIR)