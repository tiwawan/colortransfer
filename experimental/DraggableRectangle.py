import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DraggableRectangle:
    def __init__(self, ax, x, y, size, parent=None):
        self.centerpos = [x,y]
        self.size = size
        self.parent = parent
        self.rect = patches.Rectangle((x-size/2.0,y-size/2.0), size, size, fill=True)
        ax.add_patch(self.rect)
        self.press = None
        self.connect()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return

        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
        xc0, yc0 = self.centerpos
        self.press = x0, y0, xc0, yc0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xc0, yc0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)
        self.centerpos = [xc0+dx, yc0+dy]

        self.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

    def getCenterPos(self):
        return self.centerpos

    def draw(self):
        if self.parent != None:
            self.parent.draw()
        self.rect.figure.canvas.draw()
        

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(221)

    DraggableRectangle(ax, 0.1, 0.1, 0.1)

    plt.show()
