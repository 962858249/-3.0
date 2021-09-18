""" 从视频读取帧保存为图片"""
import cv2
import numpy as np
import hashlib

from hash_fun import *

def video_op(video):
    #初始视频路径,将python文件与video放在一起
    cap=cv2.VideoCapture(video)
    ret, frame_tem = cap.read()#预知视频的尺寸
    size = (frame_tem.shape[1],frame_tem.shape[0])#保证视频的大小不变
    fps = cap.get(cv2.CAP_PROP_FPS)# fps=10，可以自己设置
    #保存视频
    video = cv2.VideoWriter(video[:-4]+"_processed.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps,size,True)

    pic_index=1#图片的帧序号->计算所在时间  time=float(pic_index/fps)
    dele_pic_time=[[-1,-1]] #被删除的图像所在时间点列表,[-1,-1]只是为了方便操作，没有实际意义
    while(True):
        a1=aHash(frame_tem)

        ret, frame2 = cap.read()
        if ret is False:
            break
        a2=aHash(frame2)

        ret, frame3 = cap.read()
        if ret is False:
            break
        a3 = aHash(frame3)

        ret, frame4 = cap.read()
        if ret is False:
            break
        a4 = aHash(frame4)

        #其实本来一个cmpHash就可以的，但是发现好像有的帧之间夹杂着cmpHash=0，其实不应该删除，就弄了3个比较，这样好一点
        if(cmpHash(a1,a2)>0 or cmpHash(a2,a3)>0 or cmpHash(a3,a4)>0):
            # video.write(frame_tem)没有加入是因为这个其实就是上一个帧组合的frame4，已经加过了
            video.write(frame2)
            video.write(frame3)
            video.write(frame4)
            frame_tem=frame4
        else:
            del_sta=1.000*pic_index/fps  #删除开始时间点
            del_end=1.000*(pic_index+3)/fps  #删除结束时间点
            time_tap=[del_sta,del_end]
            if time_tap[0]==dele_pic_time[-1][1]:#下一个的开始时间就是删除时间
                dele_pic_time[-1][1]=time_tap[1]
            else:
                dele_pic_time.append(time_tap)#[sta_time1,end_time1,sta_time2,end_time2,sta_time3,end_time3,......]

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pic_index+=3  #图像帧+3
    dele_pic_time=dele_pic_time[1:]#去掉第一个[-1,-1],里面的才是真正删除的
    # print(dele_pic_time)#测试一下时间点
    cap.release()
    cv2.destroyAllWindows()

    return (dele_pic_time,pic_index)


#可以单独运行，但是总的流程需要运行video_music_merge.py！！！！！
if __name__ == '__main__':
    video_op('shu.mp4')