#!/usr/bin/env python3
"""
依赖检测脚本 - 检查视频制作所需的工具是否已安装
用法: python check_deps.py [--all | --manim | --hyperframes | --remotion | --tts | --whisper]
不带参数时只检查必须依赖（FFmpeg）
"""
import subprocess
import sys
import shutil
import json


def check_command(cmd, version_flag="--version"):
    """检查命令是否可用，返回 (是否可用, 版本信息)"""
    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True, text=True, timeout=10
        )
        version = (result.stdout or result.stderr).strip().split("\n")[0]
        return True, version
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None


def check_python_package(package, python_cmd="python"):
    """检查 Python 包是否已安装"""
    try:
        result = subprocess.run(
            [python_cmd, "-m", "pip", "show", package],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    return True, line.split(":")[1].strip()
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None


def check_npm_package(package):
    """检查全局 npm 包是否已安装"""
    try:
        result = subprocess.run(
            ["npx", package, "--version"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            return True, version
        return False, None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False, None


def find_python312():
    """查找 Python 3.12 的可执行路径"""
    candidates = ["py -3.12", "python3.12", "python3", "python"]
    for cmd in candidates:
        try:
            parts = cmd.split()
            result = subprocess.run(
                parts + ["--version"],
                capture_output=True, text=True, timeout=5
            )
            version = (result.stdout or result.stderr).strip()
            if "3.12" in version:
                return cmd, version
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None, None


def main():
    args = set(sys.argv[1:])
    check_all = "--all" in args or len(args) == 0

    results = {"required": {}, "optional": {}}
    install_hints = []

    # === 必须依赖 ===
    ok, ver = check_command("ffmpeg", "-version")
    results["required"]["ffmpeg"] = {"installed": ok, "version": ver}
    if not ok:
        install_hints.append(
            "FFmpeg: 从 https://www.gyan.dev/ffmpeg/builds/ 下载（Windows）"
            "或 brew install ffmpeg（Mac）"
        )

    ok, ver = check_command("node", "--version")
    results["required"]["node"] = {"installed": ok, "version": ver}
    if not ok:
        install_hints.append("Node.js: 从 https://nodejs.org/ 下载")

    # === 可选依赖 ===
    if check_all or "--manim" in args:
        py_cmd, py_ver = find_python312()
        results["optional"]["python3.12"] = {
            "installed": py_cmd is not None,
            "version": py_ver,
            "command": py_cmd,
        }
        if py_cmd:
            ok, ver = check_python_package("manim", py_cmd.split()[0])
            results["optional"]["manim"] = {"installed": ok, "version": ver}
            if not ok:
                install_hints.append(f"Manim: {py_cmd} -m pip install manim")
        else:
            results["optional"]["manim"] = {"installed": False, "version": None}
            install_hints.append("Python 3.12: 从 https://www.python.org/downloads/ 下载")
            install_hints.append("Manim: py -3.12 -m pip install manim")

    if check_all or "--hyperframes" in args:
        ok, ver = check_npm_package("hyperframes")
        results["optional"]["hyperframes"] = {"installed": ok, "version": ver}
        if not ok:
            install_hints.append("HyperFrames: npm install -g hyperframes")

    if check_all or "--remotion" in args:
        ok, ver = check_npm_package("remotion")
        results["optional"]["remotion"] = {"installed": ok, "version": ver}
        if not ok:
            install_hints.append("Remotion: npx create-video@latest")

    if check_all or "--tts" in args:
        ok, ver = check_python_package("edge_tts")
        results["optional"]["edge-tts"] = {"installed": ok, "version": ver}
        if not ok:
            install_hints.append("edge-tts: pip install edge-tts")

    if check_all or "--whisper" in args:
        ok, ver = check_python_package("openai-whisper")
        results["optional"]["whisper"] = {"installed": ok, "version": ver}
        if not ok:
            install_hints.append("Whisper: pip install openai-whisper")

    # === 输出 ===
    print("=" * 50)
    print("视频制作依赖检测结果")
    print("=" * 50)

    print("\n【必须依赖】")
    for name, info in results["required"].items():
        status = "✅" if info["installed"] else "❌"
        ver = info.get("version", "") or ""
        print(f"  {status} {name}: {ver}" if info["installed"] else f"  {status} {name}: 未安装")

    if results["optional"]:
        print("\n【可选依赖】")
        for name, info in results["optional"].items():
            status = "✅" if info["installed"] else "⚠️"
            ver = info.get("version", "") or ""
            print(f"  {status} {name}: {ver}" if info["installed"] else f"  {status} {name}: 未安装")

    if install_hints:
        print("\n【安装建议】")
        for hint in install_hints:
            print(f"  → {hint}")

    # 输出 JSON 供 Skill 解析
    print(f"\n__JSON__{json.dumps(results, ensure_ascii=False)}")

    # 必须依赖缺失时返回非零退出码
    missing_required = [k for k, v in results["required"].items() if not v["installed"]]
    sys.exit(1 if missing_required else 0)


if __name__ == "__main__":
    main()
