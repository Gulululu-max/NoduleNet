import os

def check_non_mhd_raw_files(folder_path):
    """
    遍历文件夹，统计非.raw/.mhd后缀的文件数量
    :param folder_path: 目标文件夹路径（如merged_subsets）
    :return: 非目标后缀的文件数量、文件列表
    """
    # 初始化统计变量
    non_target_count = 0
    non_target_files = []
    
    # 遍历文件夹中所有文件（不递归子文件夹，适配你的合并场景）
    for file_name in os.listdir(folder_path):
        # 拼接完整文件路径
        file_path = os.path.join(folder_path, file_name)
        
        # 跳过文件夹（只检查文件）
        if os.path.isdir(file_path):
            continue
        
        # 获取文件后缀（转小写，避免大小写问题）
        file_suffix = os.path.splitext(file_name)[1].lower()
        
        # 检查是否不是.raw或.mhd
        if file_suffix not in ['.raw', '.mhd']:
            non_target_count += 1
            non_target_files.append(file_name)
    
    # 输出结果
    print("="*50)
    print(f"检查文件夹：{folder_path}")
    print(f"非.raw/.mhd后缀的文件总数：{non_target_count}")
    print("="*50)
    
    # 如果有异常文件，列出具体名称
    if non_target_count > 0:
        print("异常文件列表：")
        for idx, file in enumerate(non_target_files, 1):
            print(f"{idx}. {file}")
    else:
        print("✅ 所有文件均为.raw或.mhd格式！")
    
    return non_target_count, non_target_files

if __name__ == "__main__":
    # ==================== 修改为实际路径 ====================
    MERGED_FOLDER = "/home/ubuntu-user/WMQ/data/merged_subsets"  # merged_subsets路径
    # ===========================================================
    
    # 执行检查
    check_non_mhd_raw_files(MERGED_FOLDER)