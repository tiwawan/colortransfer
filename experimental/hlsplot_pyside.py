import sys

import numpy as np
import scipy as sp


import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'
matplotlib.use('Qt4Agg')

import matplotlib.pyplot as plt

import numpy.linalg as linalg
import scipy.misc as misc
import colorsys

# GUI
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide import QtCore, QtGui

from DeformablePolygon import *

x= misc.imread('nuri3fss.png');

def hls_to_ohls(h, l, s):
    return [s*np.cos(h*2*np.pi), s*np.sin(h*2*np.pi), l]

def ohls_to_hls(co, si, l):
    zero_th = 0.0001
    if np.absolute(co) < zero_th and si > 0:
        h = 0.25
    elif np.absolute(co) < zero_th and si < 0:
        h = 0.75
    else:
        h = np.arctan(si/co)/(2*np.pi)
        if co < 0 and si > 0:
            h = h-0.5
        if co < 0 and si < 0:
            h = h+0.5
        
    s = np.sqrt(co*co+si*si)
    return [h, l, s]

def convertRgbToHls(im):
    """im:numpy array, maximum=1"""
    height = im.shape[0]
    width = im.shape[1]
    im_hls = np.zeros([height, width, 3])
    for i in range(0, height):
        for j in range(0, width):
            hls = colorsys.rgb_to_hls(im[i, j, 0], im[i, j, 1], im[i, j, 2]);
            im_hls[i, j, :] = np.array(hls);
    return im_hls

def convertRgbToOhls(im):
    """im:numpy array, maximum=1"""
    height = im.shape[0]
    width = im.shape[1]
    im_ohls = np.zeros([height, width, 3])
    for i in range(0, height):
        for j in range(0, width):
            hls = colorsys.rgb_to_hls(im[i, j, 0], im[i, j, 1], im[i, j, 2]);
            ohls = hls_to_ohls(hls[0], hls[1], hls[2])
            im_ohls[i, j, :] = np.array(ohls);
    return im_ohls

def convertHlsToRgb(im):
    """im:numpy array, maximum=1"""
    height = im.shape[0]
    width = im.shape[1]
    im_rgb = np.zeros([height, width, 3])
    for i in range(0, height):
        for j in range(0, width):
            rgb = colorsys.hls_to_rgb(im[i, j, 0], im[i, j, 1], im[i, j, 2]);
            im_rgb[i, j, :] = np.array(rgb);
    return im_rgb

def convertOhlsToRgb(im):
    """im:numpy array, maximum=1"""
    height = im.shape[0]
    width = im.shape[1]
    im_rgb = np.zeros([height, width, 3])
    for i in range(0, height):
        for j in range(0, width):
            hls = ohls_to_hls(im[i, j, 0], im[i, j, 1], im[i, j, 2])
            rgb = colorsys.hls_to_rgb(hls[0], hls[1], hls[2]);
            im_rgb[i, j, :] = np.array(rgb);
    return im_rgb

def drawHlsCircle(ax):
    num_points = 200
    angles = np.linspace(0, 2*np.pi, num_points);
    circle_x = np.cos(angles);
    circle_y = np.sin(angles);
    for i in range(0, num_points-1):
        c = colorsys.hls_to_rgb(angles[i]/(2*np.pi), 0.5, 1);
        ax.plot(circle_x[i:i+2], circle_y[i:i+2], color=c)
    c = colorsys.hls_to_rgb(angles[num_points-1]/(2*np.pi), 0.5, 1);
    ax.plot([circle_x[num_points-1],circle_x[0]],
         [circle_y[num_points-1],circle_y[0]], color=c)
    ax.plot([0,0],[1,-1],color=(0.5,0.5,0.5))
    ax.plot([1,-1],[0,0],color=(0.5,0.5,0.5))

x_num = x[:,:,0:3]
x_num = x_num/255

height = x.shape[0]
width = x.shape[1]
N = height*width

#x_num = np.reshape(x_num, [x_num.shape[0]*x_num.shape[1], 3])
x_hls = convertRgbToOhls(x_num)
x_ohls = convertRgbToOhls(x_num)

x_ohls1d = np.reshape(x_ohls, [N, 3])
x_ohls1d = np.transpose(x_ohls1d);

x_mean = np.mean(x_ohls1d,axis=1)
x_mean[2] = 0;


x_cov = np.cov(x_ohls1d[0:2, :], rowvar=1, bias=1)
W, V = linalg.eig(x_cov);

x_mean_tiled = np.tile(x_mean, (N,1));
x_mean_tiled = np.transpose(x_mean_tiled);
x_ohls1d_whiten = x_ohls1d-x_mean_tiled;

x_ohls_whiten = np.transpose(x_ohls1d_whiten)
x_ohls_whiten = np.reshape(x_ohls_whiten, [height, width, 3])

x_whiten = convertOhlsToRgb(x_ohls_whiten);


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    fig = plt.figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(221)
    
    drawHlsCircle(ax)
    ax.scatter(x_ohls1d[0,:], x_ohls1d[1,:])
    ax.set_xlim([-1,1]);
    ax.set_ylim([-1,1]);
    ax.plot(x_mean[0], x_mean[1], "rv");
    
    pos = np.array([[0,0],[0,1],[1,1],[1,0]])
    pos = pos*0.7
    DeformablePolygon(ax, pos)

    
    ax = fig.add_subplot(222)
    ax.imshow(x_num);

    ax = fig.add_subplot(223)
    drawHlsCircle(ax)
    ax.scatter(x_ohls1d_whiten[0,:], x_ohls1d_whiten[1,:])
    ax.set_xlim([-1,1]);
    ax.set_ylim([-1,1]);
    ax.plot(0, 0, "rv");
    
    ax = fig.add_subplot(224)
    ax.imshow(x_whiten);

    win = QtGui.QMainWindow()
    # add the plot canvas to a window
    win.setCentralWidget(canvas)

    win.show()

    app.exec_()

