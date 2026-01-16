#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Google Drive Share Link
# @raycast.mode compact
# @raycast.packageName Utils

# Optional parameters:
# @raycast.icon 🔗
# @raycast.alias gsharelink

# Documentation:
# @raycast.author Immanuel-Aristotle
# @raycast.authorURL https://github.com/Immanuel-Aristotle

# @raycast.description Get the sharelink for mounted file in google drive via cloudmounter
#
# @raycast.argument1 { "type": "text", "placeholder": "mounted file path" }


import os
import sys
import subprocess
from pathlib import Path

# ================= CONFIGURATION =================

# 1. 你的 rclone 配置名称 (必须与你 rclone config 里的名称一致)
RCLONE_REMOTE = "Google_Drive"

# 2. CloudMounter 在本地的挂载根目录
#    注意：这个路径必须精确地指向 Google Drive 的根目录。
MOUNT_POINT = "/Users/veritas/Library/CloudStorage/CloudMounter-Google_Drive"

# =================================================

def get_share_link(input_path: str):
    """
    获取 Google Drive 文件的分享链接。
    
    Args:
        input_path: 用户在命令行输入的本地文件路径。
    """
    # 1. 检查输入
    if not input_path:
        print("Usage: python gsharelink.py /path/to/file", file=sys.stderr)
        sys.exit(1)

    try:
        # 使用 pathlib 获取绝对路径并标准化
        full_path = Path(input_path).resolve()
        mount_point = Path(MOUNT_POINT).resolve()
        
    except Exception as e:
        print(f"Error processing path: {e}", file=sys.stderr)
        sys.exit(1)


    # 2. 验证路径是否在挂载点内
    if not str(full_path).startswith(str(mount_point)):
        print(f"Error: File is not inside the specified CloudMounter drive.", file=sys.stderr)
        print(f"File path:   {full_path}", file=sys.stderr)
        print(f"Mount point: {mount_point}", file=sys.stderr)
        sys.exit(1)

    # 3. 提取相对路径
    try:
        # 使用 Path.relative_to() 获取相对路径
        relative_path = full_path.relative_to(mount_point)
        # 将 Path 对象转换为 rclone 需要的 POSIX 字符串
        rclone_path = f"{RCLONE_REMOTE}:/{relative_path.as_posix()}"
    except ValueError as e:
        # 捕捉路径处理的边缘错误
        print(f"Error extracting relative path: {e}", file=sys.stderr)
        sys.exit(1)


    # 4. 调用 rclone link 命令
    print(f"Fetching link for: {relative_path} ...")
    
    try:
        # 使用 subprocess.run 执行命令
        # capture_output=True: 捕获 stdout 和 stderr
        # check=True: 如果命令返回非零退出代码 (失败)，则抛出 CalledProcessError
        result = subprocess.run(
            ['rclone', 'link', rclone_path],
            capture_output=True,
            text=True, # 确保输出是字符串而不是字节
            check=True
        )

        # rclone link 成功，链接在 stdout
        share_link = result.stdout.strip()
        
        print("----------------------------------------")
        print(share_link)
        print("----------------------------------------")

        # 5. 自动复制到剪贴板 (macOS/Linux)
        if sys.platform == "darwin":
            # macOS 使用 pbcopy
            subprocess.run(['pbcopy'], input=share_link, text=True)
            print("(Link copied to clipboard via pbcopy)")
        elif os.environ.get('DISPLAY'):
            # Linux 如果有 X server 运行，尝试 xclip
            subprocess.run(['xclip', '-selection', 'c'], input=share_link, text=True)
            print("(Link copied to clipboard via xclip)")
        # Windows 也可以使用 pyperclip 库，但这里保持依赖最少

    except subprocess.CalledProcessError as e:
        print(f"\nError: rclone failed to retrieve the link.", file=sys.stderr)
        # 打印 rclone 的错误输出
        print(f"rclone Error Output (stderr): {e.stderr.strip()}", file=sys.stderr)
        print(f"Command run: {' '.join(e.cmd)}", file=sys.stderr)
        print("Please check if the file is synced and the rclone config is correct.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'rclone' command not found. Please ensure rclone is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # 从命令行参数中获取文件路径 (sys.argv[0] 是脚本名, sys.argv[1] 是第一个参数)
    file_path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    get_share_link(file_path_arg)
