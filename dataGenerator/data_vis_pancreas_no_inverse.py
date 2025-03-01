'''
    将两个原始数据加载并打印出来看看
'''

import scipy.io as io
import numpy as np
from pdb import set_trace as stx
import cv2
import imageio.v2 as iio
import os

category = 'pancreas_no_inverse'

raw_path = '/data2/cyh23/NAF_raw_data/pancreas_240x512x512_int16.raw'

'''
    统一把切片通道调整到最后一个维度
    161 作通道 -> 失败
    103 作通道 -> 失败

    切片对不上的一个原因很可能是一开始 reshape 就 reshape 错了 (103, 94, 161) 是错的
    有可能是 reshape 到 (161, 103, 94)
'''

raw_data = np.fromfile(raw_path, dtype='uint16')
# stx()
# raw_data_vis = raw_data.reshape(94, 161, 103)
# raw_data_vis = raw_data.reshape(94, 103, 161)
# raw_data_vis = raw_data.reshape(103, 161, 94)
# raw_data_vis = np.swapaxes(raw_data.reshape(161, 94, 103), 1, 2)
raw_data_vis = raw_data.reshape(512, 512, 240)
# raw_data_vis =  np.swapaxes(np.swapaxes(raw_data.reshape(174, 512, 512), 0, 1), 1, 2)
# raw_data_vis = np.swapaxes(raw_data.reshape(256, 128, 256), 1, 2)
# raw_data_vis = raw_data.reshape(128, 256, 256)
# raw_data_vis = raw_data.reshape(161, 103, 94)
# raw_data_vis = np.swapaxes(np.swapaxes(raw_data.reshape(161, 103, 94), 0, 1), 1, 2)
# raw_data_vis = raw_data.reshape(103, 94, 161)
# raw_data_vis = np.swapaxes(raw_data.reshape(103, 94, 161), 1, 2)
# raw_data_vis = np.swapaxes(np.swapaxes(raw_data.reshape(103, 94, 161), 0, 1), 1, 2)
# raw_data_vis = np.swapaxes(np.swapaxes(raw_data.reshape(93, 341, 341), 0, 1), 1, 2)
# raw_data_vis = raw_data.reshape(341, 93, 341)

data_float = (np.float32(raw_data_vis) - raw_data_vis.min()) / (raw_data_vis.max() - raw_data_vis.min())

data_uint8 = np.uint8(data_float*255)

show_slice = 50
show_step = data_uint8.shape[-1]//show_slice
show_image = data_uint8[...,::show_step]



vis_dir = 'CT_vis/' + category + '/'
os.makedirs(vis_dir, exist_ok=True)

for i in range(show_slice+1):
    iio.imwrite(vis_dir + 'CT_raw_'+str(i) + '.png', show_image[...,i])



stx()

img_data = data_float
dict_data = dict()
dict_data['img'] = img_data
# stx()
save_dir = 'raw_data/' + category + '/'
os.makedirs(save_dir, exist_ok=True)
io.savemat(save_dir+'img.mat', dict_data)

