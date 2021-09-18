import subprocess
import os
from del_repeated_video_and_record_time import video_op
from music_op import music_op
from moviepy.editor import VideoFileClip

def video_add_mp4(file_name, mp4_file):
    outfile_name = file_name.split('.')[0] + '-new.mkv'  # 注意，修改成mp4会报错！之后自己修改一下后缀格式改变一下就行
    outfile_name2 = file_name.split('.')[0] + '-new.mp4'
    cmd = f'ffmpeg -i {mp4_file} -i {file_name} -acodec copy -vcodec copy {outfile_name}'
    cmd2 = f"ffmpeg -i {outfile_name} -c:v copy -c:a aac -vcodec libx264 {outfile_name2}"  #x264格式
    # 因为直接转成mp4不行，所以就中间加了过渡的视频格式mkv，之后再删除就可以了
    subprocess.call(cmd, shell=True)
    subprocess.call(cmd2, shell=True)


# #将其他格式实现转换为x264的mp4格式-------------不需要了，直接转换了
# def preprocesse(pre_video):
#     outfile=pre_video[:-4]+'.mp4'
#     if pre_video.endswith('.mp4'):
#         pass
#     else:
#         cmd = f"ffmpeg -i {pre_video} -c:v copy -c:a aac -vcodec libx264 {outfile}"  #x264格式
#         subprocess.call(cmd, shell=True)
# # 总的流程在此，运行即可！！！！！


def merge_two(pre_video):

    # preprocesse(pre_video)  # 将不是mp4的提前转换为mp4格式

    tuple1 = list(video_op(pre_video))
    # 这是从del_repeated_video_and_record_time.py引用的，处理视频并且返回(dele_pic_time,pic_index)
    # 返回的 删除时间节点和视频总帧数
    music_op(pre_video,tuple1[0], tuple1[1])

    video_a = pre_video[:-4] + '_processed.mp4'  # 视频
    music_b = pre_video[:-4] + '_processed.wav'  # mp4格式的音频
    video_add_mp4(video_a, music_b)

    # 关键步骤(bitrate可以自己调节，视频内存的关键修改)
    output_video = video_a.split('.')[0] + '-new.mp4'
    a = VideoFileClip(output_video)
    a.write_videofile(pre_video[:-4] + '_200k.mp4', bitrate='200k')  # 最终的视频生成结果
    a.close()


    os.remove(video_a.split('.')[0] + '-new.mkv')
    os.remove(pre_video[:-4] + '.wav')
    os.remove(video_a)
    os.remove(music_b)
    os.remove(output_video)


