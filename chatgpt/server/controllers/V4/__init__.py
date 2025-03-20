# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys

def run_command(cmd, work_dir=".", shell=False):
    # Run command in subprocess
    # 执行子进程中的命令
    p = subprocess.Popen(cmd, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    retcode = p.returncode

    return retcode, out, err

def extract_commit_messages(log):
    # Extract commit messages from git log
    # 从git日志中提取提交消息
    commit_messages = re.findall(r"commit\s[a-z0-9]{40}\n(Author:\s.*\n)?Date:.*\n\n(.*(\n|$))", log, re.MULTILINE)
    messages = [msg[1].strip() for msg in commit_messages]
    return messages

def check_git_repo(path):
    # Check if the given path is a git repository
    # 检查给定的路径是否为git仓库
    retcode, out, err = run_command(["git", "rev-parse", "--is-inside-work-tree"], work_dir=path)
    if retcode != 0:
        return False
    return True

def get_git_log(path, from_commit=None, to_commit="HEAD"):
    # Get git log from the given path
    # 从给定路径获取git日志
    cmd = ["git", "log", "--pretty=full"]
    if from_commit:
        cmd.append(f"{from_commit}..{to_commit}")

    retcode, out, err = run_command(cmd, work_dir=path)
    if retcode != 0:
        print(f"Error getting git log: {err.decode()}")
        return None

    return out.decode()

def main():
    # Main function
    # 主函数
    repo_path = "."  # Current directory as default
    from_commit = None

    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
        if not os.path.exists(repo_path):
            print(f"Error: Path '{repo_path}' does not exist.")
            return

    if len(sys.argv) > 2:
        from_commit = sys.argv[2]

    if not check_git_repo(repo_path):
        print(f"Error: '{repo_path}' is not a git repository.")
        return

    log = get_git_log(repo_path, from_commit)
    if not log:
        return

    commit_messages = extract_commit_messages(log)

    print("Commit Messages:")
    for message in commit_messages:
        print(f"- {message}\n")

if __name__ == "__main__":
    main()
