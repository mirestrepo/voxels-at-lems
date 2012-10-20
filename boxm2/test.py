import matplotlib
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button


class PointPicker:
    def __init__(self, points, image, axis):
        self.points = points
        self.xs = list(points.get_xdata())
        self.ys = list(points.get_ydata())
        self.labels = list()
        self.cid = points.figure.canvas.mpl_connect('button_press_event', self)
        self.im = image
        self.ax = axis

    def __call__(self, event):
        print 'click', event
        print 'button=%d, key=%s, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.key, event.x, event.y, event.xdata, event.ydata)
        if event.inaxes!=self.points.axes: return

        #Add point - left click + a
        if event.button==1 and event.key=='a':
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.points.set_data(self.xs, self.ys)
            l= self.ax.annotate(
            str(len(self.xs)),
            xy = (event.xdata, event.ydata), xytext = (-10, 10),
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            fontproperties= matplotlib.font_manager.FontProperties(family='Helvetica', size=8))
            self.labels.append(l)
            self.points.figure.canvas.draw()

        #remove last point - left click + r
        if event.button==1 and event.key=='r':
            self.xs.pop()
            self.ys.pop()
            self.points.set_data(self.xs, self.ys)
            to_remove = self.labels.pop()
            to_remove.remove()
            self.points.figure.canvas.draw()

        #clear all points - left click + c
        if event.button==1 and event.key=='c':
            while len(xs) > 0:
                self.xs.pop()
                self.ys.pop()
                self.points.set_data(self.xs, self.ys)
                to_remove = self.labels.pop()
                to_remove.remove()
            self.points.figure.canvas.draw()





img_file="/data/helicopter_providence_3_12/site_1/imgs/frame001.png"
img=mpimg.imread(img_file)
fig = plt.figure()
ax = fig.add_subplot(121)
plt.hold(True)
image = ax.imshow(img)
ax.set_title('click to pick a point')
points, = ax.plot([], [], "s", color="green" )  # empty line
p1 = PointPicker(points , image, ax)
# bclear = Button(ax, 'Clear')
# bclear.on_clicked(PointPicker.clear_points)

img_file="/data/helicopter_providence_3_12/site_1/imgs/frame002.png"
img2=mpimg.imread(img_file)
ax2 = fig.add_subplot(122)
image2 = ax2.imshow(img2)
ax2.set_title('click to pick a point')
points2, = ax2.plot([], [], "s", color="green" )  # empty line
p2 = PointPicker(points2, image2, ax2)




plt.show()