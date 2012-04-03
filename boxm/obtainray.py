from  Tkinter import*
import Image, ImageTk, ImageDraw
import boxm_batch

import matplotlib.pyplot as plt
class dbvalue:
 def __init__(self, index, type):
   self.id = index # unsigned integer
   self.type = type # string
boxm_batch.register_processes();
boxm_batch.register_datatypes();

scene_path="/Users/isa/Experiments/tests/ocl_scene/scene.xml"
camera_path="/Volumes/vision/video/dec/capitol_sfm_rotated/cameras_KRT/camera_00040.txt";
image_path = "/Volumes/vision/video/dec/CapitolSiteHigh/video/frame_00040.png";
int_image_path = "/Volumes/vision/video/dec/CapitolSiteHigh/video_grey/frame_00040.png";


# scene_path = "F:/visdt/sceneocl/scene.xml";
# image_path ="f:/visdt/cd/_00113.png";
# int_image_path ="F:/visdt/imgs/gray00113.png";
# camera_path="f:/visdt/cameras_KRT/camera_00113.txt"

print("Load Initial camera ");
boxm_batch.init_process("vpglLoadPerspectiveCameraProcess");
boxm_batch.set_input_string(0,camera_path);
boxm_batch.run_process();
(id,type) = boxm_batch.commit_output(0);
cam = dbvalue(id,type);

print("initializing ray tracing");
boxm_batch.init_process("boxmOclInitRenderProbeProcess");
boxm_batch.set_input_string(0, scene_path);
boxm_batch.set_input_from_db(1, cam);
boxm_batch.set_input_unsigned(2, 200);
boxm_batch.set_input_unsigned(3, 200);
boxm_batch.run_process();
(scene_id, scene_type) = boxm_batch.commit_output(0);
scene_mgr = dbvalue(scene_id, scene_type);

image2 = Image.open(int_image_path)



def subone(y): return 1-y
def mult(x,y): return x*y
def callback(event):
  print "clicked at", event.x, event.y;
  posx=event.x;
  posy=event.y;
  print runprobe(event.x,event.y);
	
def runprobe(event):
  posx=event.x;
  posy=event.y;
  array2d=list();

  plt.figure(1);
  plt.clf();
  print("Run ray tracing");
  boxm_batch.init_process("boxmOclRunRenderProbeProcess");
  boxm_batch.set_input_from_db(0, scene_mgr);
  boxm_batch.set_input_from_db(1, cam);
  boxm_batch.set_input_unsigned(2, posx);
  boxm_batch.set_input_unsigned(3, posy);
  boxm_batch.set_input_float(4,(image2.getpixel((posx,posy)))/255.0);
  boxm_batch.run_process();

  for i in range(0,10):
    (scene_id, scene_type) = boxm_batch.commit_output(i);
    array_1d = dbvalue(scene_id, scene_type);
    vallist = boxm_batch.get_bbas_1d_array_float(scene_id);
    array2d.append(vallist);

  for i in [1,2,3,5]:
    plt.plot(array2d[0],array2d[i]);
  #plt.plot(array2d[0],array2d[7]);
  plt.legend(('Omega','Mean0','Alpha','Mean1'),loc='upper left');
  print (image2.getpixel((posx,posy)))/255.0;
  plt.show();

def neighborchange(event):
  posx=event.x;
  posy=event.y;
  array2d=list();

  vallist=list();
  plt.figure(1);
  plt.clf();
  for i in (-1, 0):
      for j in (-1, 0):
        print("Run ray tracing");
        boxm_batch.init_process("boxmOclRunRenderProbeProcess");
        boxm_batch.set_input_from_db(0, scene_mgr);
        boxm_batch.set_input_from_db(1, cam);
        boxm_batch.set_input_unsigned(2, posx+i);
        boxm_batch.set_input_unsigned(3, posy+j);
        boxm_batch.set_input_float(4, (image2.getpixel((posx,posy)))/255.0);
        boxm_batch.run_process();
        (scene_id, scene_type) = boxm_batch.commit_output(10);
        x = boxm_batch.get_input_float(scene_id);
        vallist.append(x);
  print vallist;
def zoomin(event):
	print "zoom"
	tkpi.zoom(self,2);





root = Tk()
root.bind("<Button-1>", runprobe);
root.bind("<Double-Button-1>", zoomin);
root.title("Probe")
image1 = Image.open(image_path)
root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
tkpi = ImageTk.PhotoImage(image1)
label_image = Label(root, image=tkpi)
label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
root.mainloop()

print("Finish ray tracing");
boxm_batch.init_process("boxmOclFinishRenderProbeProcess");
boxm_batch.set_input_from_db(0, scene_mgr);
boxm_batch.run_process();