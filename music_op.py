##########################音
import numpy as np
from moviepy.editor import *
from scipy.io import wavfile
from del_repeated_video_and_record_time import *
import os

def music_op(pre_video,dele_pic_time,pic_index):
    #wav是无损的
    video = VideoFileClip(pre_video)
    audio = video.audio
    audio.write_audiofile('{}.wav'.format(pre_video.split('.')[0]))
    # audio.write_audiofile('shu.mp3')
    like = wavfile.read('{}.wav'.format(pre_video.split('.')[0]))
    # print (like)
    # 音频结果将返回一个tuple。第一维参数是采样频率，单位为秒；第二维数据是一个ndarray表示歌曲，如果第二维的ndarray只有一个数据表示单声道，两个数据表示立体声。所以，通过控制第二维数据就能对歌曲进行裁剪。
    # 对like这个元组第二维数据进行裁剪，所以是like[1];第二维数据中是对音乐数据切分。 start_s表示你想裁剪音频的起始时间；同理end_s表示你裁剪音频的结束时间。乘44100 是因为每秒需要进行44100次采样
    # 这里表示对该音频的13-48秒进行截取

    a=like[0]
    # print(dele_pic_time0)
    mix=like[1][0:int(dele_pic_time[0][0]*a)]#开始的一段
    for i in  range(len(dele_pic_time)-1):#删除的时间间隔个数减1
        mix_section=like[1][int(dele_pic_time[i][1]*a):int(dele_pic_time[i+1][0]*a)]
        mix=np.concatenate((mix,mix_section))#axis用默认的

    mix_section=like[1][int(a*dele_pic_time[i+1][1]):int(pic_index*a)]
    mix=np.concatenate((mix,mix_section))#最后的一段,pic_index可能不是最后一帧，但是前后相差三帧，无所谓了
    wavfile.write('{}_processed.wav'.format(pre_video.split('.')[0]),a,mix)
    # wavfile.write('test2.wav',44100,like[1][13*44100:48*44100])



#可以单独运行，但是总的流程需要运行video_music_merge.py！！！！！


if __name__ == '__main__':
    pre_video = 'shu.mp4'  # 待处理视频名称
    tuple1 = list(video_op(pre_video))
    # 这是从del_repeated_video_and_record_time.py引用的，处理视频并且返回(dele_pic_time,pic_index)
    # 返回的 删除时间节点和视频总帧数
    music_op(tuple1[0], tuple1[1])






