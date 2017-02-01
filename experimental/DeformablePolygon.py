import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np

from DraggableRectangle import *

class DeformablePolygon:
    def __init__(self, ax, pos):
        self.pos = pos
        self.num_verts = pos.shape[0]
        self.verts = [None] * self.num_verts
        for i in range(0,self.num_verts):
            self.verts[i] = DraggableRectangle(ax, pos[i,0], pos[i,1], 0.05, self)
        self.poly = patches.Polygon(self.pos, fill=False)
        ax.add_patch(self.poly)
        
    def draw(self):
        #update pos
        for i in range(0, self.num_verts):
            vcp = self.verts[i].getCenterPos()
            self.pos[i,0] = vcp[0]
            self.pos[i,1] = vcp[1]
        self.poly.set_xy(self.pos)
        
        self.poly.figure.canvas.draw()

    def getPos(self):
        return self.pos
        

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pos = np.array([[0,0],[0,1],[1,1],[1,0]])
    pos = pos*0.7
    DeformablePolygon(ax, pos);

    plt.show()
