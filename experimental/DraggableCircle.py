import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DraggableCircle:
    def __init__(self, ax, x, y, r):
        self.pos = [x,y]
        self.circle = patches.Circle((x,y), r, fill=True)
        ax.add_patch(self.circle)
        self.press = None
        self.connect()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.circle.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.circle.axes: return

        contains, attrd = self.circle.contains(event)
        if not contains: return
        print('event contains', self.circle.xy)
        x0, y0 = self.pos
        self.press = x0, y0, event.xdata, event.ydata

    def on_motion(self, event):
        'on motion we will move the circle if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.circle.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.circle.set_x(x0+dx)
        self.circle.set_y(y0+dy)
        self.pos = x0+dx
        self.circle.figure.canvas.draw()


    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circle.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

    def getPos(self):
        return self.pos
        

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)

    DraggableCircle(ax, 0.5, 0.5, 0.1)

    plt.show()
