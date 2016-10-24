
"""
This is an example to show how to build cross-GUI applications using
matplotlib event handling to interact with objects on the canvas

"""
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from matplotlib.mlab import dist_point_to_segment


class DeformableMesh(object):

    showverts = True
    epsilon = 10  # max pixel distance to count as a vertex hit

    def __init__(self, ax):
        self.ax = ax
        canvas = plt.gcf().canvas
        self.num_points = 4

        self.points = np.array([[0.0,0.0],[0.0,1.0],[1.0,1.0],[1.0,0.0]]);
        
        self.markers = [0] * self.num_points

        for i in range(0, self.num_points):
            self.markers[i] = Line2D([self.points[i,0]],[ self.points[i,1]], marker='o', markerfacecolor='r', animated=True)
            self.ax.add_line(self.markers[i])

        self._ind = None  # the active vert

        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas

    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        for x in self.markers:
            self.ax.draw_artist(x)
        self.canvas.blit(self.ax.bbox)

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'

        # display coords
        xyt = self.markers[0].get_transform().transform(self.points)
        xt, yt = xyt[:, 0], xyt[:, 1]
        d = np.sqrt((xt - event.x)**2 + (yt - event.y)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]

        if d[ind] >= self.epsilon:
            ind = None

        return ind

    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)
        print(str(self.points))

    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts:
            return
        if event.button != 1:
            return
        self._ind = None

    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return

        ex, ey = event.xdata, event.ydata
        x,y = self.markers[0].get_transform().inverted().transform([ex,ey]);
        
        self.points[self._ind, 0] = ex
        self.points[self._ind, 1] = ey
        self.markers[self._ind].set_data([ex],[ey])

        self.canvas.restore_region(self.background)
        for x in self.markers:
            self.ax.draw_artist(x)
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon

    fig, ax = plt.subplots()
    p = DeformableMesh(ax)

    #ax.add_line(p.line)
    ax.set_title('Click and drag a point to move it')
    ax.set_xlim((-2, 2))
    ax.set_ylim((-2, 2))
    plt.show()
