# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 13:47:50 2016

@author: aboulch
"""

from struct import *
import numpy as np
import glob, os

# level 0
objects_dict_l0 = {}
objects_dict_l0[0] = ["misc",[0],[0.0,0.0,0.0]]
objects_dict_l0[1] = ["man-made-terrain",[1],[0.75,0.75,0.75]]
objects_dict_l0[2] = ["natural-terrain",[2],[0.0,1.0,0.0]]
objects_dict_l0[3] = ["high-vegetation", [3] , [0.15,0.84,0.25]]
objects_dict_l0[4] = ["low-vegetation",[4],[0.97,0.97,0.0]]
objects_dict_l0[5] = ["building",[5],[0.99,0.01,0.0]]
objects_dict_l0[6] = ["hard-scape",[6],[0.48,0.0,1.0]]
objects_dict_l0[7] = ["scanning-artefacts",[7],[0.0,1.0,1.0]]
objects_dict_l0[8] = ["cars",[8],[0.99,0.43,0.81]]
# objects_dict_l0[0] = ["misc",[0],[0.0,0.0,0.0]]
# objects_dict_l0[1] = ["man-made-terrain",[1],[0.62,0.32,0.176]]
# objects_dict_l0[2] = ["natural-terrain",[2],[1.0,1.0,1.0]]
# objects_dict_l0[3] = ["high-vegetation", [3] , [1.0,0.62,0.0]]
# objects_dict_l0[4] = ["low-vegetation",[4],[0.0,1.0,0.0]]
# objects_dict_l0[5] = ["building",[5],[0.0,0.0,0.5]]
# objects_dict_l0[6] = ["hard-scape",[6],[0.0,1.0,0.5]]
# objects_dict_l0[7] = ["scanning-artefacts",[7],[0.0,1.0,1.0]]
# objects_dict_l0[8] = ["cars",[8],[0.7,0.0,0.7]]

# level 1
objects_dict_l1 = {}
objects_dict_l1[40] = ["misc. veg.",[40]]
objects_dict_l1[41] = ["low-vegetation",[41]]
objects_dict_l1[42] = ["shrub",[42]]
objects_dict_l1[50] = ["misc.",[50]]
objects_dict_l1[51] = ["roof",[51]]
objects_dict_l1[52] = ["facade", [52]]
objects_dict_l1[60] = ["misc. hardscape",[60]]
objects_dict_l1[61] = ["power-line",[61]]
objects_dict_l1[62] = ["fences",[62]]

# level 2
objects_dict_l2 = {}
objects_dict_l2[520] = ["misc.",[520]]
objects_dict_l2[521] = ["wall",[521]]
objects_dict_l2[522] = ["window",[522]]
objects_dict_l2[523] = ["door",[523]]
objects_dict_l2[524] = ["crack", [524]]

class PointCloud:

    def __init__(self, name="default"):
        self.name = name
        self.points = None
        self.normals = None
        self.colors = None
        self.category = None
        self.safe = None

    def set_points(self, points):
        self.points = points

    def set_normals(self, normals):
        self.normals = normals

    def set_colors(self, colors):
        self.colors = colors

    def extract_category_from_name(self):
        spl_name = self.name.split("_")


        self.l0_cat = 0
        self.l1_cat = None
        self.l2_cat = None

        # level 0
        if(len(spl_name) == 0):
            print("Error, extract_category_from_name")
            return None
        l0_name = spl_name[0]
        for key, value in objects_dict_l0.items():
            if(l0_name == value[0]):
                self.l0_cat = key

        #level 1
        if(len(spl_name) > 1):
            l1_name = spl_name[1]
            self.l1_cat = self.l0_cat*10
            for key, value in objects_dict_l1.items():
                if(l1_name == value[0]):
                    self.l1_cat = key

            # level 2
            if(len(spl_name) > 2):
                l2_name = spl_name[2]
                self.l2_cat = self.l1_cat*10
                for key, value in objects_dict_l2.items():
                    if(l2_name == value[0]):
                        self.l2_cat = key

        if spl_name[-1] == "safe":
            self.safe = True
        if spl_name[-1] == "rubble":
            self.safe = False


def load_pc_from_directory(source_directory):
    print("load pc from directory")
    pc = []
    os.chdir(source_directory)
    for file in glob.glob("*.asc"):
        filename = os.path.join(source_directory,file)
        print(filename)

        # read the name of the object
        f = open(filename, 'r')
        obj_name = f.readline().split("//")[1].split("\n")[0]
        print("  "+obj_name)
        f.close()

        # read the data
        data = np.loadtxt(filename, comments="//")

        # create point clouds instance
        pc_obj = PointCloud(obj_name)
        pc_obj.set_points(data[:,:3])
        pc_obj.set_colors(data[:,3:])
        data = None

        pc_obj.extract_category_from_name()

        #add it to the global point cloud
        pc.append(pc_obj)
    return pc


def export_to_obj(output_directory,output_name, pc):
    """
    Export to obj format
    Args:
        output_directory   directory
        output_name        filename
        pc:                point cloud
    """

    filename = os.path.join(output_directory,output_name)

    print("Export to obj ")
    # MTL file
    ofs = open(filename+".mtl", 'w')
    for key,value  in objects_dict_l0.items():
        ofs.write("newmtl "+str(value[0])+"\n")
        ofs.write("Ka "+str(value[2][0])+" "+str(value[2][1])+" "+str(value[2][2])+"  \n")
        ofs.write("Kd "+str(value[2][0])+" "+str(value[2][1])+" "+str(value[2][2])+"  \n")
        ofs.write("Ks 0.000 0.000 0.000 \n")
    ofs.close()

    # OBJ file
    ofs = open(filename+".obj", 'w')
    ofs.write('mtllib '+output_name+".mtl"+" \n")
    for obj in pc:
        ofs.write("o "+obj.name+" \n")
        ofs.write("usemtl "+objects_dict_l0[obj.l0_cat][0]+"\n")
        for pt_id in range(obj.points.shape[0]):
            ofs.write("v "+str(obj.points[pt_id,0]))
            ofs.write(" "+str(obj.points[pt_id,1]))
            ofs.write(" "+str(obj.points[pt_id,2]))
            ofs.write(" \n")
        ofs.flush()
    ofs.close()
    
    
def export_to_semantic3d(output_directory, output_name, pc):
    """
    Export to semantic 3d format
    Args:
        output_directory   directory
        output_name        filename
        pc:                point cloud
    """
    #.labels
    #.txt  {x, y, z, intensity, r, g, b}
    filename = os.path.join(output_directory,output_name)
    print("export to semantic 3D format")
    ofs_points = open(filename+".txt", 'w')
    ofs_labels = open(filename+".labels", 'w')
    for obj in pc:
        obj_label = objects_dict_l0[obj.l0_cat][0]
        for pt_id in range(obj.points.shape[0]):
            
            ofs_points.write(str(obj.points[pt_id,0])+" ")
            ofs_points.write(str(obj.points[pt_id,1])+" ")
            ofs_points.write(str(obj.points[pt_id,2])+" ")
            ofs_points.write("0 ")
            ofs_points.write(str(int(obj.colors[pt_id,0]))+" ")
            ofs_points.write(str(int(obj.colors[pt_id,1]))+" ")
            ofs_points.write(str(int(obj.colors[pt_id,2]))+" ")
            ofs_points.write(" \n")
            
            ofs_labels.write(str(obj_label))
            ofs_labels.write(" \n")
        ofs_labels.flush()
        ofs_points.flush()
        
    ofs_points.close()
    ofs_labels.close()

def export_to_ply(output_directory, output_name, pc, use_label_color=False):
    """
    Export to ply format
    Args:
        output_directory   directory
        output_name        filename
        pc:                point cloud
        use_labels_color:  use the point cloud colors or the label colors
    """
    filename = os.path.join(output_directory,output_name)
    print("export to ply")
    ofs = open(filename+".ply", 'w')

    # number of points
    pts_nbr = 0
    for obj in pc:
        pts_nbr += obj.points.shape[0]
    
    #write header
    ofs.write("ply \n")
    ofs.write("format ascii 1.0 \n")
    ofs.write("element vertex "+str(pts_nbr)+" \n")
    ofs.write("property float x \n")
    ofs.write("property float y \n")
    ofs.write("property float z \n")
    ofs.write("property uchar red \n")
    ofs.write("property uchar green \n")
    ofs.write("property uchar blue \n")
    ofs.write("end_header \n")
    
    for obj in pc:
        obj_color = objects_dict_l0[obj.l0_cat][2]
        obj_color = [int(obj_color[i]*255) for i in range(len(obj_color))]
        for pt_id in range(obj.points.shape[0]):
            
            ofs.write(str(obj.points[pt_id,0])+" ")
            ofs.write(str(obj.points[pt_id,1])+" ")
            ofs.write(str(obj.points[pt_id,2])+" ")
            
            if(use_label_color):
                ofs.write(str(obj_color[0])+" ")
                ofs.write(str(obj_color[1])+" ")
                ofs.write(str(obj_color[2])+" ")
            else:
                ofs.write(str(int(obj.colors[pt_id,0]))+" ")
                ofs.write(str(int(obj.colors[pt_id,1]))+" ")
                ofs.write(str(int(obj.colors[pt_id,2]))+" ")
            
            ofs.write(" \n")
        ofs.flush()

    ofs.close()

def export_rubble_to_ply(output_directory, output_name, pc):
    """
    Export point-cloud to ply format with rubble/safe/nothing color info
    Args:
        output_directory   directory
        output_name        filename
        pc:                point cloud
    """



    filename = os.path.join(output_directory,output_name)
    print("export to ply")
    ofs = open(filename+"_rubble.ply", 'w')

    # number of points
    pts_nbr = 0
    for obj in pc:
        pts_nbr += obj.points.shape[0]
    
    #write header
    ofs.write("ply \n")
    ofs.write("format ascii 1.0 \n")
    ofs.write("element vertex "+str(pts_nbr)+" \n")
    ofs.write("property float x \n")
    ofs.write("property float y \n")
    ofs.write("property float z \n")
    ofs.write("property uchar red \n")
    ofs.write("property uchar green \n")
    ofs.write("property uchar blue \n")
    ofs.write("end_header \n")
    
    ## (green for safe, red for rubble,black for none)
    color_rubble = [255,0,0]
    color_safe = [0,255,0]
    color_none = [0,0,0]

    for obj in pc:
#        obj_color = objects_dict_l0[obj.l0_cat][2]
#        obj_color = [int(obj_color[i]*255) for i in range(len(obj_color))]
        obj_color = color_none
        if obj.safe == True:
            obj_color = color_safe
        elif obj.safe == False:
            obj_color = color_rubble

        for pt_id in range(obj.points.shape[0]):
            
            ofs.write(str(obj.points[pt_id,0])+" ")
            ofs.write(str(obj.points[pt_id,1])+" ")
            ofs.write(str(obj.points[pt_id,2])+" ")
            
            ofs.write(str(obj_color[0])+" "+str(obj_color[1])+" "+str(obj_color[2]))
            """
            if(use_label_color):
                ofs.write(str(obj_color[0])+" ")
                ofs.write(str(obj_color[1])+" ")
                ofs.write(str(obj_color[2])+" ")
            else:
                ofs.write(str(int(obj.colors[pt_id,0]))+" ")
                ofs.write(str(int(obj.colors[pt_id,1]))+" ")
                ofs.write(str(int(obj.colors[pt_id,2]))+" ")
            """

            ofs.write(" \n")
        ofs.flush()

    ofs.close()




# define locations
# source_directory = "/media/aboulch/data/inachus/Mirabello/test"
# source_directory = "/c8/FP7.INACHUS/data/AlteSpinnerei/AlteSpinnerei_segmentedAsc/"
source_directory = "/c8/FP7.INACHUS/data/Mirabello/Mirabello_segmented_BLSAsc/"
# output_directory = "/media/aboulch/data/inachus/"
output_directory = "/tmp/"
# output_name = "AlteSpinnerei_segmented"
output_name = "Mirabello_segmented"

# create the point cloud
pc = load_pc_from_directory(source_directory)


#export_to_obj(output_directory,output_name,pc)
export_to_semantic3d(output_directory,output_name,pc)
export_to_ply(output_directory,output_name,pc)
export_to_ply(output_directory,output_name+"_color_label",pc, use_label_color=True)

export_rubble_to_ply(output_directory,output_name,pc)
