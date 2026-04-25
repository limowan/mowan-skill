#!/usr/bin/env python3
"""
视频合成辅助脚本 - 将多个视频片段+音频合成为最终视频
用法: python merge_video.py --clips-dir <clips_dir> --output <output_path> [--bgm <bgm_path>] [--srt <srt_path>]
"""
import argparse
import subprocess
import sys
import os
import json


def get_duration(filepath):
    """获取媒体文件时长（秒）"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", filepath],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def merge_segment(video_path, audio_path, output_path, max_duration=None):
    """合并单段视频和音频，视频不够长时用最后一帧填充"""
    if max_duration is None:
        max_duration = get_duration(audio_path) + 2

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-filter_complex",
        f"[0:v]scale=1920:1080,fps=30,tpad=stop=-1:stop_mode=clone:stop_duration={int(max_duration)}[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-shortest",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    return output_path


def concat_segments(segment_paths, output_path):
    """拼接多个视频段落"""
    n = len(segment_paths)
    inputs = []
    for p in segment_paths:
        inputs.extend(["-i", p])

    filter_parts = []
    concat_inputs = []
    for i in range(n):
        filter_parts.append(f"[{i}:v][{i}:a]")
        concat_inputs.append(f"[{i}:v][{i}:a]")

    filter_str = f"{''.join(concat_inputs)}concat=n={n}:v=1:a=1[vout][aout]"

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    return output_path


def add_bgm(video_path, bgm_path, output_path, bgm_volume=0.12):
    """混入背景音乐"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", bgm_path,
        "-filter_complex",
        f"[1:a]volume={bgm_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    return output_path


def burn_subtitles(video_path, srt_path, output_path):
    """烧录字幕"""
    srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_escaped}:force_style='FontSize=22,FontName=Microsoft YaHei'",
        "-c:v", "libx264", "-crf", "18",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="视频合成辅助脚本")
    parser.add_argument("--clips-dir", required=True, help="片段目录（含 seg_*.mp4）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--bgm", help="BGM 文件路径（可选）")
    parser.add_argument("--bgm-volume", type=float, default=0.12, help="BGM 音量（默认 0.12）")
    parser.add_argument("--srt", help="SRT 字幕文件路径（可选）")
    args = parser.parse_args()

    clips_dir = args.clips_dir
    segment_files = sorted([
        os.path.join(clips_dir, f)
        for f in os.listdir(clips_dir)
        if f.startswith("seg_") and f.endswith(".mp4")
    ])

    if not segment_files:
        print("错误：未找到 seg_*.mp4 文件")
        sys.exit(1)

    print(f"找到 {len(segment_files)} 个片段，开始合成...")

    # 拼接
    temp_output = args.output.replace(".mp4", "_temp.mp4")
    current = concat_segments(segment_files, temp_output)
    print(f"拼接完成: {get_duration(current):.1f}s")

    # 加 BGM
    if args.bgm:
        bgm_output = args.output.replace(".mp4", "_bgm.mp4")
        current = add_bgm(current, args.bgm, bgm_output, args.bgm_volume)
        print("BGM 混入完成")

    # 烧字幕
    if args.srt:
        sub_output = args.output.replace(".mp4", "_sub.mp4")
        current = burn_subtitles(current, args.srt, sub_output)
        print("字幕烧录完成")

    # 最终输出
    if current != args.output:
        os.rename(current, args.output)

    # 清理临时文件
    for f in [temp_output,
              args.output.replace(".mp4", "_bgm.mp4"),
              args.output.replace(".mp4", "_sub.mp4")]:
        if os.path.exists(f) and f != args.output:
            os.remove(f)

    duration = get_duration(args.output)
    size_mb = os.path.getsize(args.output) / (1024 * 1024)
    print(f"\n合成完成: {args.output}")
    print(f"时长: {int(duration//60)}分{int(duration%60)}秒 | 大小: {size_mb:.1f}MB")


if __name__ == "__main__":
    main()
