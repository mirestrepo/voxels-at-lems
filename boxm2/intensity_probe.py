#!/usr/bin/python
"""
Intensity_Probe - given a directory of images and directory of
corresponding cameras, click on a point in the presented image
and have the intensities at that point in other images
plotted to the left (histogrammed and by image number...)
"""
from boxm2_adaptor import *;
from boxm2_scene_adaptor import *;
from vpgl_adaptor import *;
from bbas_adaptor import *;
from vil_adaptor import *;
from boxm2_tools_adaptor import *;
import scene_registry
import random, os, sys;
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt;
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import axes3d
import numpy;
from numpy import arange, sin, pi , cos, arctan2, arccos
if matplotlib.get_backend() is not 'TkAgg': matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import *
from matplotlib.figure import Figure
from  Tkinter import*
import Image,ImageTk, ImageDraw
import glob,math,random
from optparse import OptionParser

#######################################################
# handle inputs                                       #
#scene is given as first arg, figure out paths        #
parser = OptionParser()
parser.add_option("-i", "--im_dir", action="store", type="string", dest="im_dir", default="", help="specify which image or directory to use")
parser.add_option("-c", "--cam_dir", action="store", type="string", dest="cam_dir", default="", help="specify corresponding camera or directory to use")
(options, args) = parser.parse_args()
print options
print args


#################################
# Get list of imgs and cams
train_imgs = options.im_dir + "/*"
train_cams = options.cam_dir + "/*.txt"

if not os.path.isdir(options.im_dir):
   print "Expected image directory doesn't exist. \nPlease place images in: ! ", options.im_dir
   sys.exit(-1)

if not os.path.isdir(options.cam_dir):
   print "Expected camera directory doesn't exist. \nPlease place cameras in: ! ", options.cam_dir
   sys.exit(-1)


imgList = glob.glob(train_imgs)
camList = glob.glob(train_cams)
imgList.sort()
camList.sort()
if len(imgList) != len(camList) :
  print "CAMS NOT ONE TO ONE WITH IMAGES"
  sys.exit();

assert(len(imgList) > 0)




""" ImageFrame
Helper class keeps track of objects associated with an image frame
"""
class ImageFrame:

  def __init__(self, frame=None, label=None, labString=None, currImg=0, row=0, col=0, label_image=None, image=None, tkpi=None):
    self.frame = frame
    self.label = label
    self.labString = labString
    self.label_image = label_image
    self.currImg = currImg
    self.row = row
    self.col = col
    self.image = image
    self.tkpi = tkpi
    self.lastClick = None


""" Application
gui app takes in Tk, imglist and camlist
"""
suntheta= 0.325398;
sunphi  =0.495398;
class App:
    def __init__(self,master,imgList,camList):
        self.master = master;
        self.master.title("3d Point Intensity Tool");

        #store imgs/cams
        self.imgList = imgList
        self.camList = camList

        #Once a 3d point is generated, it is stored here,
        #and all image's UV points stored in allUVs
        self.point3d = None
        self.allUVs = []

        #############################################
        #set up plot frame
        # firstImg = Image.open(imgList[0]);
        firstImg = mpimg.imread(imgList[0]);


        print "Image size: ", firstImg.size
        self.reduceFactor = 1.4; #max(firstImg.size[0]/640.0, firstImg.size[1]/480.0)
        self.ni = int(firstImg.shape[0]/self.reduceFactor + .5)
        self.nj = int(firstImg.shape[1]/self.reduceFactor + .5)
        self.frame = Frame(self.master, height=self.nj, width=self.ni, bg='blue');
        self.frame.grid_propagate(0)
        self.frame.pack();
        self.frame.grid(row=0, column=0)
        # place a graph somewhere here
        self.f = Figure(figsize=(5.0,5.0), dpi=100)
        self.a = self.f.add_subplot(311)
        self.a.set_xlabel("t")
        self.a.set_ylabel("Info")
        self.a.plot([0,1,2,3,4],[0,1,2,3,4])
        self.canvas = FigureCanvasTkAgg(self.f, self.frame)
        self.canvas.show()
        #self.canvas.mpl_connect('button_press_event', self.get_t);
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        #############################################
        #set up button frame
        self.bFrame = Frame(self.master, height=self.nj, width=self.ni)
        self.bFrame.grid_propagate(0)
        self.bFrame.pack()
        self.bFrame.grid(row=1, column=0)
        #place a button to generate 3d point, and grab intensities from each image
        self.genButton = Button(self.bFrame, text="Generate Point", command=self.point_from_rays)
        self.genButton.pack(fill=BOTH, expand=1)
        #button to clear the points
        self.clearButton = Button(self.bFrame, text="Clear Points", command=self.clear_points)
        self.clearButton.pack()
        #label for std dev and mean
        self.stdLabel = StringVar()
        Label(self.bFrame, textvariable=self.stdLabel).pack()
        self.meanLabel = StringVar()
        Label(self.bFrame, textvariable=self.meanLabel).pack()
        #label for 3d point
        self.pointLabel = StringVar()
        Label(self.bFrame, textvariable=self.pointLabel).pack()

        ##############################################
        #set up images frames (should be 4 or so images)
        self.frames = []
        self.numImageFrames = 1
        frCount = 0
        for i in range(1):
          for j in range(1):
            labString = StringVar()
            label = Label(self.master, textvariable=labString)
            frame1 = LabelFrame(self.master, labelwidget=label, height=self.nj, width=self.ni, bg='green')
            frame1.pack();
            frame1.grid_propagate(0)
            frame1.grid(row=i, column=j+1, sticky=NW)

            currFrame = (len(self.imgList) / self.numImageFrames) * frCount
            imageFrame = ImageFrame(frame1, label, labString, currFrame, i, j);
            self.frames.append(imageFrame)
            frCount += 1

        #display the first frame
        for iFrame in self.frames:
          self.displayImage(iFrame)

        #start the gui
        master.mainloop();

    def point_from_rays(self):
      """generate point from frames with clicked pixels"""
      print "generating the 3d point from given clicked points"

      #gather cams and points clicked
      uvs = []
      cams = []
      for iFrame in self.frames:
        if iFrame.lastClick :
          uv = numpy.multiply(iFrame.lastClick,self.reduceFactor)
          uvs.append(uv)
          cam = load_perspective_camera(self.camList[iFrame.currImg])
          cams.append(cam)
      point = get_3d_from_cams(cams, uvs)
      self.point3d = point;
      print "3d Point: " + str(self.point3d);
      self.pointLabel.set("3d Point: " + str(self.point3d))

      # project 3d point into each image, and gather intensities
      values = []
      ims    = []
      for idx, img in enumerate(self.imgList):
        cam = load_perspective_camera(self.camList[idx])
        imgPoint = project_point(cam, point[0], point[1], point[2])
        imgPoint = numpy.divide(imgPoint, self.reduceFactor)
        self.allUVs.append(imgPoint)

        #grab float intensity value at this point
        imgView,ni,nj = load_image(img)
        val = pixel(imgView, imgPoint)
        if val > 0.0:
          values.append(val)
          ims.append(idx)

        #cleanup
        remove_from_db([imgView, cam])

      #now that each image has a corresponding make sure the
      #point is displayed in each image
      #self.clear_points();
      #for iFrame in self.frames:
        #point = self.allUVs[iFrame.currImg];
        #self.drawBox(iFrame)

      #write mean/std of intensities
      self.meanLabel.set("Mean: " + str(numpy.mean(values)) )
      self.stdLabel.set("Std Dev: " + str(numpy.std(values)) )
      #plot the intensities by image number
      self.f.clf();
      self.a = self.f.add_subplot(311)
      self.a.set_xlabel("img #")
      self.a.set_ylabel("intensity")
      self.a.plot(ims, values)
      #plot the histogram of intensities by image number
      pdf, bins, patches = plt.hist(values)
      self.b = self.f.add_subplot(313)
      self.b.set_xlabel("bin val")
      self.b.set_ylabel("freq")
      self.b.hist(values, 15, normed=1, facecolor="green" )
      self.canvas.show();

    def clear_points(self):
      """clear points in each iFrame"""
      print "clearing each frame of selected points"
      self.point_3d = None
      self.allUVs = []
      for iFrame in self.frames:
        iFrame.lastClick = None;
        self.displayImage(iFrame)

    def displayImage(self, iFrame, img=None):
        """given a frame displays the current image """
        if not img:
          imgPath = self.imgList[iFrame.currImg]
          #img = Image.open(imgPath);
          img = mpimg.imread(imgPath);
          # if img.mode == "I;16":
          #   print "16 bit image, converting to 8 bit"
          #   img.mode = 'I'
          #   img = img.point(lambda i:i*(1./256.)).convert("RGB");
          # img = img.resize((self.ni, self.nj))

        #iframe keeps track of its image
        iFrame.image = img

        #if point is generated, gotta draw squares first
        if self.point3d:
          point = self.allUVs[iFrame.currImg];
          self.drawBox(iFrame, point)

        # store photo image (probably not needed in iFrame)
        # iFrame.tkpi = ImageTk.PhotoImage(img)
        iFrame.tkpi = plt.imshow(img)

        #update frames' label
        # iFrame.labString.set("img {0}".format(iFrame.currImg))

        # #create new label image
        # if iFrame.label_image :
        #   iFrame.label_image.destroy()
        # iFrame.label_image = Label(iFrame.frame, image=iFrame.tkpi)
        # iFrame.label_image.image = iFrame.tkpi
        # iFrame.label_image.bind("<Button-1>", lambda event, arg=iFrame: self.runprobe(event, iFrame))
        # iFrame.label_image.bind("<Button-3>", lambda event, arg=iFrame: self.nextImage(event, iFrame))
        # iFrame.label_image.bind("<Button-2>", lambda event, arg=iFrame: self.prevImage(event, iFrame))
        # iFrame.label_image.pack(side = LEFT);

    def nextImage(self, event, iFrame):
        currImg = 1 + iFrame.currImg
        if currImg >= len(self.imgList):
          currImg = 0
        iFrame.currImg = currImg
        print "Displaying next image: ", self.imgList[currImg]
        self.displayImage(iFrame);

    def prevImage(self, event, iFrame):
        currImg = iFrame.currImg - 1
        if currImg < 0 :
          currImg = len(self.imgList)-1
        iFrame.currImg = currImg
        print "Displaying next image: ", self.imgList[currImg]
        self.displayImage(iFrame);

    def runprobe(self,event,iFrame):
        #print "Image clicked on frame ", iFrame.row, iFrame.col
        #print "    at point", event.x, event.y, " = ", iFrame.image.getpixel( (event.x, event.y) )
        #store x,y clicked and draw
        iFrame.lastClick = (event.x, event.y)
        self.drawBox(iFrame, iFrame.lastClick)
        self.displayImage(iFrame, iFrame.image)

    def drawBox(self, iFrame, point):
        draw = ImageDraw.Draw(iFrame.image)
        imSize = iFrame.image.size
        p1 = ( max(point[0]-5,0), max(point[1]-5,0) )
        p2 = ( min(point[0]+5,imSize[0]-1), min(point[1]+5, imSize[1]-1) )
        draw.rectangle([p1, p2],  fill="green")
        del draw

#instantiate Tk root, and make App
root = Tk();
app = App(root, imgList, camList);

