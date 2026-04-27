# GPU 检测与 FFmpeg 编码参数

## GPU 渲染能力检测

运行：

```bash
python tools/check_deps.py --gpu
```

根据检测结果选择输出链路：

| 环境 | 默认链路 | 说明 |
|------|----------|------|
| Windows + NVIDIA + `h264_nvenc` 可用 | Remotion 生成画面 → FFmpeg `h264_nvenc` 编码最终 MP4 | Windows 下 Remotion 内置 `--hardware-acceleration` 不支持 H.264 GPU 编码 |
| MacBook / macOS | Remotion `--hardware-acceleration=if-possible` | macOS 由 Remotion 调用 Apple VideoToolbox |
| 其他环境 | CPU `libx264 -crf 18` | 稳定回退，不阻塞出片 |

## GPU 渲染总原则

- 默认画质优先：上传平台前的源片要清晰，文件大小适中即可
- 不追求 GPU 版和 CPU 版完全同码率：`libx264` 同码率压缩效率通常更好，GPU 版强行压到同码率更容易糊
- 禁止二次压缩：不要把已经压好的最终 MP4 再转 GPU；应从高质量中间产物或帧序列直接生成最终 GPU 版 MP4
- 如果字幕、细线、图片边缘发糊，优先把 `-cq` 调到 `17`，不要优先压低文件大小

## FFmpeg 编码参数

### Windows NVIDIA 默认参数

```
h264_nvenc -preset p6 -tune hq -rc vbr -cq 18 -b:v 4M -maxrate 8M -bufsize 16M -pix_fmt yuv420p
```

### CPU 回退参数

```
libx264 -preset medium -crf 18 -pix_fmt yuv420p
```

## 合成命令模板

### 逐段合并视频+音频

视频不够长时用最后一帧填充（不是黑屏）：

```bash
# Windows + NVIDIA
ffmpeg -y -i {video}.mp4 -i {audio}.mp3 \
  -filter_complex "[0:v]scale=1920:1080,fps=30,tpad=stop=-1:stop_mode=clone:stop_duration={max_dur}[v]" \
  -map "[v]" -map 1:a \
  -c:v h264_nvenc -preset p6 -tune hq -rc vbr -cq 18 -b:v 4M -maxrate 8M -bufsize 16M -pix_fmt yuv420p \
  -c:a aac -shortest \
  {output_segment}.mp4

# CPU fallback
ffmpeg -y -i {video}.mp4 -i {audio}.mp3 \
  -filter_complex "[0:v]scale=1920:1080,fps=30,tpad=stop=-1:stop_mode=clone:stop_duration={max_dur}[v]" \
  -map "[v]" -map 1:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -shortest \
  {output_segment}.mp4
```

### 拼接所有段落

```bash
ffmpeg -y \
  -i seg_01.mp4 -i seg_02.mp4 ... \
  -filter_complex "[0:v][0:a][1:v][1:a]...concat=n=N:v=1:a=1[vout][aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v {编码器参数} \
  -c:a aac -b:a 192k \
  {final_output}.mp4
```

也可以直接使用 `tools/merge_video.py` 一步完成：

```bash
python tools/merge_video.py --clips-dir 产物/视频片段 --output 产物/最终视频/终版.mp4 [--bgm bgm.mp3] [--srt 字幕.srt]
```

### 混入 BGM

```bash
# BGM 音量压低到 10-15%，不抢配音
ffmpeg -y -i {video_with_voice}.mp4 -i {bgm}.mp3 \
  -filter_complex "[1:a]volume=0.12[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac \
  {final_with_bgm}.mp4
```

### 烧录字幕

```bash
ffmpeg -y -i {video}.mp4 -vf "subtitles={srt_file}:force_style='FontSize=22,FontName=Microsoft YaHei'" \
  -c:v {编码器参数} \
  -c:a copy {final_with_subs}.mp4
```

## 免版权 BGM 来源

- [Pixabay Music](https://pixabay.com/music/) — CC0 协议，国内可直接访问
- [FreePD.com](https://freepd.com/) — 公共领域，零限制
- [爱给网](https://www.aigei.com/) — 有免费可商用音乐区
- [淘声网](https://www.tosound.com/) — 免费音效和音乐
- [YouTube Audio Library](https://studio.youtube.com/channel/audio) — 完全免费，需科学上网
