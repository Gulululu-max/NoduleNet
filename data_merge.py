import os
import zipfile
import glob
from tqdm import tqdm  # 进度条，可选但推荐

def unzip_and_merge(subset_zip_dir, target_dir):
    """
    解压所有subset压缩包并合并到目标文件夹
    :param subset_zip_dir: 存放10个subset.zip的文件夹路径（如~/LUNA16/raw）
    :param target_dir: 合并后的目标文件夹路径（如~/LUNA16/all_data）
    """
    # 1. 创建目标文件夹（不存在则创建）
    os.makedirs(target_dir, exist_ok=True)
    
    # 2. 找到所有subset压缩包（匹配subset0.zip ~ subset9.zip）
    zip_pattern = os.path.join(subset_zip_dir, "subset*.zip")
    zip_files = glob.glob(zip_pattern)
    
    if not zip_files:
        print(f"错误：在 {subset_zip_dir} 中未找到subset*.zip文件！")
        return
    
    # 3. 遍历并解压每个压缩包
    for zip_file in tqdm(zip_files, desc="解压进度"):
        # 获取压缩包名称（如subset0.zip）
        zip_name = os.path.basename(zip_file)
        print(f"\n开始解压：{zip_name}")
        
        try:
            # 打开压缩包（支持大文件）
            with zipfile.ZipFile(zip_file, 'r') as zf:
                # 遍历压缩包内的所有文件
                for file_info in zf.infolist():
                    # 跳过文件夹（避免重复创建）
                    if file_info.is_dir():
                        continue
                    
                    # 目标文件路径（直接合并，不保留subset子文件夹）
                    target_file = os.path.join(target_dir, os.path.basename(file_info.filename))
                    
                    # 跳过已解压的文件（断点续传）
                    if os.path.exists(target_file) and os.path.getsize(target_file) == file_info.file_size:
                        continue
                    
                    # 解压文件到目标文件夹
                    zf.extract(file_info, target_dir)
                    # 修正解压后的路径（移除压缩包内的子文件夹）
                    extracted_file = os.path.join(target_dir, file_info.filename)
                    if os.path.exists(extracted_file) and extracted_file != target_file:
                        os.rename(extracted_file, target_file)
                        # 删除空的子文件夹（可选）
                        extracted_dir = os.path.dirname(extracted_file)
                        if not os.listdir(extracted_dir):
                            os.rmdir(extracted_dir)
            
            print(f"{zip_name} 解压完成！")
        
        except zipfile.BadZipFile:
            print(f"错误：{zip_name} 是损坏的压缩包，请重新下载！")
        except Exception as e:
            print(f"解压 {zip_name} 时出错：{str(e)}")
    
    print(f"\n✅ 所有文件已合并到：{target_dir}")
    # 统计合并后的文件数量
    all_files = glob.glob(os.path.join(target_dir, "*"))
    mhd_files = glob.glob(os.path.join(target_dir, "*.mhd"))
    raw_files = glob.glob(os.path.join(target_dir, "*.raw"))
    print(f"📊 合并结果：总文件数={len(all_files)}, .mhd文件数={len(mhd_files)}, .raw文件数={len(raw_files)}")

if __name__ == "__main__":
    # 1. 存放10个subset.zip的文件夹
    SUBSET_ZIP_DIR = "/home/ubuntu-user/WMQ/data/subsets"
    # 2. 合并后的目标文件夹（自定义，不存在会自动创建）
    TARGET_DIR = "/home/ubuntu-user/WMQ/data/merged_subsets"
    
    # 运行解压合并
    unzip_and_merge(SUBSET_ZIP_DIR, TARGET_DIR)