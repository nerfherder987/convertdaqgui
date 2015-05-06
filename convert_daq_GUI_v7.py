### GUI for DAQ processing program, Ainsley Mitchum (10/25/2014)
# Tested under Python 2.7 (64-bt) on Windows 7
# 1. Checks to indicate which data streams will be extracted
#       Take checked items as a single list and add them as the 
#       variable that tells the DAQ script what to grab
# 2. Browse for the input and output directories
# 3. User specify the experiment name, so which part of the file 
#    the glob command looks for in the source directory.
# 4. User specify whether the files should be renamed at output
#       If output files are to be renamed, specify rename pattern
#
# NOTE: Only includes the option to convert the DAQs to .mat files
# 
# Got basic info from: http://www.tutorialspoint.com/python/python_gui_programming.htm
# Framework for gui class from: http://sebsauvage.net/python/gui/#our_project
#
# Exe instructions: http://logix4u.net/component/content/article/27-tutorials/
# 44-how-to-create-windows-executable-exe-from-python-script
#
# DAQ-related functions borrowed from U of Iowa supplied: convert_DAQ.py
############################################################################

from Tkinter import * # equivalent to import Tkinter, but now don't need to 
# have "Tkinter" in front of Tkinter function calls
from tkFileDialog import askdirectory # browse for file
from tkMessageBox import askokcancel  # dialog boxes
#import ttk # for progress bar / not used in this version

# Instead of importing whole modules, only import the functions
# the program uses
from os import path,listdir
from glob import glob
from re import search

# Copied from U of Iowa convert_daq.py script
from struct import unpack
from copy import copy
from numpy import array
from scipy.io import savemat
#from scipy import io as sio

## Trying out putting the GUI in a class
class conv_daq_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    ## Keep all of the button and check box initializing in this method
    def initialize(self):
        self.grid()
        
        ###############
        ## ENTRY BOX ##
        ###############
        # This is for text entry, which I may not want
        # Could use it for the user to specify the file name pattern
        # but make sure to have a default action if nothing is specified (doesn't now)
        self.entryVariable = StringVar()
        self.entry = Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0, row=0, sticky="EW")
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter experiment name.")
        
        #################
        ## CHECK BOXES ##
        #################
        ## Variables related to check boxes
        ## Default value of list if no selections are made
        self.elemlist = ["VDS_Chassis_CG_Position","VDS_Veh_Speed","CFS_Brake_Pedal_Force",\
        "SCC_LogStreams","SCC_Collision_Count"]
        
        self.CheckVar1 = IntVar()
        self.CheckVar2 = IntVar()
        self.CheckVar3 = IntVar()
        self.CheckVar4 = IntVar()
        self.CheckVar5 = IntVar()
        self.CheckVar6 = IntVar()
        self.CheckVar7 = IntVar()
        self.CheckVar8 = IntVar()
        self.CheckVar9 = IntVar()
        self.CheckVar10 = IntVar()
        self.CheckVar11 = IntVar()
        self.CheckVar12 = IntVar()
        self.CheckVar13 = IntVar()
        self.CheckVar14 = IntVar()
        self.CheckVar15 = IntVar()
        
        C1 = Checkbutton(self.parent, text = "Participant Position", variable = self.CheckVar1, \
                         onvalue = 1, offvalue = 0, height=2, \
                         width = 20)
        C2 = Checkbutton(self.parent, text = "Participant Speed", variable = self.CheckVar2, \
                         onvalue = 2, offvalue = 0, height=2, \
                         width = 20)
        C3 = Checkbutton(self.parent, text = "Brake Force", variable = self.CheckVar3, \
                         onvalue = 3, offvalue = 0, height=2, \
                         width = 20)
        C4 = Checkbutton(self.parent, text = "Log Streams", variable = self.CheckVar4, \
                         onvalue = 4, offvalue = 0, height=2, \
                         width = 20)
        C5 = Checkbutton(self.parent, text = "Collision Count", variable = self.CheckVar5, \
                         onvalue = 5, offvalue = 0, height=2, \
                         width = 20)
        C6 = Checkbutton(self.parent, text = "Object Position", variable = self.CheckVar6, \
                         onvalue = 6, offvalue = 0, height=2, \
                         width = 20)
        C7 = Checkbutton(self.parent, text = "Object Name", variable = self.CheckVar7, \
                         onvalue = 7, offvalue = 0, height=2, \
                         width = 20)
        C8 = Checkbutton(self.parent, text = "Traffic Light State", variable = self.CheckVar8, \
                         onvalue = 8, offvalue = 0, height=2, \
                         width = 20)
        C9 = Checkbutton(self.parent, text = "Traffic Light ID", variable = self.CheckVar9, \
                         onvalue = 9, offvalue = 0, height=2, \
                         width = 20)
        C10 = Checkbutton(self.parent, text = "Steering Wheel Angle", variable = self.CheckVar10, \
                         onvalue = 10, offvalue = 0, height=2, \
                         width = 20)
        C11 = Checkbutton(self.parent, text = "Steering Angle Rate", variable = self.CheckVar11, \
                         onvalue = 11, offvalue = 0, height=2, \
                         width = 20)
        C12 = Checkbutton(self.parent, text = "Auxiliary Buttons", variable = self.CheckVar12, \
                         onvalue = 12, offvalue = 0, height=2, \
                         width = 20)
        C13 = Checkbutton(self.parent, text = "Object Heading", variable = self.CheckVar13, \
                         onvalue = 13, offvalue = 0, height=2, \
                         width = 20)
        C14 = Checkbutton(self.parent, text = "Veh to Lead Distance", variable = self.CheckVar14, \
                         onvalue = 14, offvalue = 0, height=2, \
                         width = 20)
        C15 = Checkbutton(self.parent, text = "Lane Deviation", variable = self.CheckVar15, \
                         onvalue = 15, offvalue = 0, height=2, \
                         width = 20)

        C1.grid(row=2,column=0,sticky="EW")
        C2.grid(row=2,column=1,sticky="EW")
        C3.grid(row=2,column=2,sticky="EW")
        C4.grid(row=2,column=3,sticky="EW")
        C5.grid(row=2,column=4,sticky="EW")
        C6.grid(row=3,column=0,sticky="EW")
        C7.grid(row=3,column=1,sticky="EW")
        C8.grid(row=3,column=2,sticky="EW")
        C9.grid(row=3,column=3,sticky="EW")
        C10.grid(row=3,column=4,sticky="EW")
        C11.grid(row=4,column=0,sticky="EW")
        C12.grid(row=4,column=1,sticky="EW")
        C13.grid(row=4,column=2,sticky="EW")
        C14.grid(row=4,column=3,sticky="EW")
        C15.grid(row=4,column=4,sticky="EW")
        
        #############
        ## BUTTONS ##
        #############
        # Variables that go with these buttons
        # Select directory example: http://tkinter.unpythonic.net/wiki/tkFileDialog
        # See: https://docs.python.org/2/library/tkinter.html?highlight=tkinter
        self.inputDirVar = StringVar()
        self.outputDirVar = StringVar()
        
        button1 = Button(self,text=u"Input Directory",
                                command=self.SelectInDir)
        button1.grid(column=3,row=0)
        
        button2 = Button(self,text=u"Output Directory",
                                 command=self.SelectOutDir)
        button2.grid(column=4,row=0)
        
        button3 = Button(self,text=u"Accept Selection",
                                command=self.AcceptChoices)
        button3.grid(column=1,row=5)
        
        button4 = Button(self,text=u"Process DAQs!",
                                command=self.youSureBoutThat)
        button4.grid(column=3,row=5)
        # Need prompt if no variable selection is made
        # Set default variable selection to all available
        
        ############
        ## LABELS ##
        ############
        # I don't really need this label variable, but I could recycle it to
        # display the selected directory
        self.labelVariable = StringVar()
        label = Label(self,textvariable=self.labelVariable,
                              anchor="w", fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky="EW")
        self.labelVariable.set(u"Enter experiment name")
        
        label2 = Label(self,text="Press <ENTER> to accept experiment name",
                        anchor="w", fg="red")
        label2.grid(column=1,row=0,columnspan=2,sticky="EW")
        
        #################
        ## OTHER STUFF ##
        #################
        ## I think this chunk of stuff refers to the whole GUI
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False) # resize x,y
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        
        #############
        ## OPTIONS ##
        #############
        ## Options for the "select directory" dialog boxes
        ## This is borrowed from: http://tkinter.unpythonic.net/wiki/tkFileDialog
        ## Their code has parent as root, here it needs to be self.parent
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = self.parent # not having self in front crashed app
        options['title'] = 'Select directory'
     
    #####################################
    ## General functions, not handlers ##
    #####################################
    # Needed to add "self" as an argument for this to work
    # I think Cary wrote the original function
    # def get_part_num(self,part_dir):
        # part_num = "NA"
        # match = search("(\d+)", part_dir)
        # part_num = match.group(0)
        # return(part_num)
    
    # Updated version of get_part_num that gets 3 or 4 digit 
    # subject numbers, should work the same as the older version
    # of the function and works with "clean_empty_paths" function
    # I could probably rewrite so that these two functions aren't
    # dependent on one another
    def get_part_num(self,part_dir):
        part_num = "NA"
        match = search("(\d{3,4})", part_dir)
        while True:
            try:
                part_num = match.group(0)
                return(part_num)
            except AttributeError:
                part_num = "NoNum"
                return(part_num)
    
    # Gets rid of junk paths: Not a folder, empty folders, or folders that
    # do not have a number in the path name
    def clean_empty_paths(self,part_list):
        for item in reversed(part_list):
            # Delete stuff that isn't a folder
            if path.isdir(item) == False or listdir(item) == []\
            or self.get_part_num(item) == "NoNum":
                del(part_list[part_list.index(item)])
    
    # Add in necessary functions from process DAQ here
    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    # Added self as an argument to all of these and updated function calls
    def daq_meta(self,fid):
        daq={}
        daq['magic'] = fid.read(4).encode('hex')
        daq['title'] = fid.read(120).split('\x00')[0]
        daq['date'] = fid.read(27).split('\x00')[0]
        daq['subject'] = fid.read(128).split('\x00')[0]
        daq['run'] = fid.read(128).split('\x00')[0]
        daq['runinst'] = fid.read(129).split('\x00')[0]
        daq['numentries'] = unpack('i',fid.read(4))[0]
        daq['frequency'] = unpack('i',fid.read(4))[0]
        return daq

    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    def init_header(self):
        header={}
        header['id']=[]
        header['numvalues']=[]
        header['name']=[]
        header['units']=[]
        header['rate']=[]
        header['type']=[]
        header['varrateflag']=[]
        header['bytes']=[]
        return header
        
    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    def init_frame(self):
        frame={}
        frame['code']=[]
        frame['frame']=[]
        frame['count']=[]
        return frame
        
    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    # I don't know if I need the elemlist argument
    def init_data(self, header, elemlist = []):
        data={}
        if elemlist:
            for name in header['name']:
                if name in elemlist:
                    data[name]=[]
        else:
            for name in header['name']:
                data[name]=[]
        return data
        
    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    def append_header(self, fid, header):
        if not header['id']:
            header['id']=[0]
        else:
            header['id'].append(header['id'][-1]+1)
        numvalues=unpack('i',fid.read(4))[0]
        header['numvalues'].append(numvalues)
        header['name'].append(fid.read(36).split('\x00')[0])
        header['units'].append(fid.read(16).split('\x00')[0])
        rate=unpack('h',fid.read(2))[0]
        if rate == 65535:
            rate=-1
        header['rate'].append(rate)
        dummy=fid.read(2)
        type=chr(unpack('i', fid.read(4))[0])
        header['type'].append(type)
        header['varrateflag'].append(unpack('B', fid.read(1))[0])
        post1=fid.read(3)
    
    # FROM convert_daq_REV.py (modified ver of U of Iowa script
    # Used in read_file function
    # ADDED "self" AS FIRST ARGUMENT TO ALL OF THE DAQ FUNCTIONS
    # Removed elemlist = [] as last argument and changed to varlist
    # having an element list was optional in original script, but now
    # an element list (list of variables) must be specified
    def append_data(self, fid, header, frame, data, varlist):
        id = unpack('i', fid.read(4))[0]
        if header['varrateflag'][id]==1:
            numitems = unpack('i', fid.read(4))[0]
        else:
            numitems = header['numvalues'][id]
        type = header['type'][id]
        if type == 'i' or type == 'f':
            size = 4
        elif type == 's':
            type = 'h'
            size = 2
        elif type == 'c': # Changing to anything but 1 makes this not run
            size = 1
        elif type == 'd':
            size = 8
        #bytes = numitems*size
        name = header['name'][id]
        dataframe=[unpack(type, fid.read(size))[0] for i in range(numitems)]
    #    if 'ET_filtered_gaze_object_name' in name:
    #        pdb.set_trace()
        if not varlist or name in varlist:
            if not data[name]:
                data[name]=map(copy, [[]]*numitems)
            for i in range(numitems):
                data[name][i].append(dataframe[i])
            if header['rate'][id]==-1:
                try:
                    data[name+'_Frames'].append(frame['frame'][-1])
                except:
                    data[name+'_Frames']=[frame['frame'][-1]]
                    
    # FROM convert_daq_REV.py (modified ver of U of Iowa script 
    # Used in convert_daq function
    def read_file(self,filename):
        # Don't need this, also removed elemfile = '' as last argument
        # if elemfile:
            # elemlist = read_elemlist(elemfile)
        # else:
            # elemlist = ["CFS_Brake_Pedal_Force","SCC_Collision_Count","SCC_DynObj_Name",\
            # "SCC_DynObj_Pos","SCC_LogStreams","VDS_Chassis_CG_Position","VDS_Veh_Speed"]
            # Instead of having the elemlist passed to the read_file function, the variable
            # is just accessed directly (hopefully)
        with open(filename,'rb') as f:
            daqdata={}
            daq=self.daq_meta(f)
            header = self.init_header()
            for i in range(daq['numentries']):
                self.append_header(f,header)
            frame = self.init_frame()
            data = self.init_data(header, self.elemlist)
            while True:
                try:
                    frame['code'].append(unpack('i',f.read(4))[0])
                except Exception, err:
                    break;
                if frame['code'][-1]==-2:
                    break
                frame['frame'].append(unpack('i',f.read(4))[0])
                frame['count'].append(unpack('i',f.read(4))[0])
                for j in range(frame['count'][-1]):
                    try:
                        self.append_data(f, header, frame, data, self.elemlist)
                    except Exception, err:
                        break;
            data['Frames'] = frame['frame']
            daqdata['daqInfo']=daq
            daqdata['elemInfo']=header
            daqdata['elemFrames']=frame
            daqdata['elemData']=data
            return daqdata
    
    # FROM convert_daq_REV.py (modified ver of U of Iowa script 
    # Used in convert_daq function
    # added self argument
    def convert_file(self,daqdata, filename):
        for cell in daqdata['elemData']:
            daqdata['elemData'][cell]=array(daqdata['elemData'][cell],order='F').transpose()
        savemat(filename,daqdata,long_field_names=True,oned_as='column')
    
    # FROM convert_daq_REV.py (modified ver of U of Iowa script 
    # Used in ProcessDAQs function
    # Deleted third argument (elemfile='')
    def convert_daq(self, filename, outname='', outpath=''):
        print "reading " + filename
        daqdata=self.read_file(filename)
        if not outname:
            outname = path.splitext(filename)[0]+'.mat'
        if outpath:
            outname = path.join(outpath,outname)
        self.convert_file(daqdata,outname)
        print "file saved as " + outname
        return daqdata
    
    ####################
    ## EVENT HANDLERS ##
    ####################
    # These are where to specify what happens when a button or check is clicked
    # use command for buttons and bind for the text entry. 
    def SelectInDir(self):
        #return tkFileDialog.askdirectory(**self.dir_opt)
        ## The is needs to return the directory, not really set variable (I think)
        # Old way that makes it local to this method
        #inputDir = tkFileDialog.askdirectory(**self.dir_opt)
        self.inputDirVar.set(askdirectory(**self.dir_opt))
        print self.inputDirVar.get()
        # return self.inputDirVar.get()
        
    def SelectOutDir(self):
        self.outputDirVar.set(askdirectory(**self.dir_opt))
        print self.outputDirVar.get()
        # return self.outputDirVar.get()
        
    ### New handler for other buttons or check boxes
    # NEEDS TO CHECK WHICH VARIABLES HAVE CHANGED FROM THEIR DEFAULT VALUES 
    # AND CONSTRUCT A LIST THAT CONSISTS OF ONLY THOSE
    # elemlist = ["VDS_Chassis_CG_Position","VDS_Veh_Speed","CFS_Brake_Pedal_Force",\
    # "SCC_LogStreams","SCC_Collision_Count","SCC_DynObj_Pos","SCC_DynObj_Name",\
    # "SCC_TrafLight_State","SCC_TrafLight_Id","CFS_Steering_Wheel_Angle","CIS_Auxiliary_Buttons",
    # "CFS_Accelerator_Pedal_Position","CFS_Brake_Pedal_Position","SCC_OwnVehToLeadObjDist",
    # "SCC_Lane_Deviation"]
    def AcceptChoices(self):
        elemDict = {0:"No_Selection",1:"VDS_Chassis_CG_Position",2:"VDS_Veh_Speed",
                    3:"CFS_Brake_Pedal_Force",4:"SCC_LogStreams",5:"SCC_Collision_Count",
                    6:"SCC_DynObj_Pos",7:"SCC_DynObj_Name",8:"SCC_TrafLight_State",
                    9:"SCC_TrafLight_Id",10:"CFS_Steering_Wheel_Angle",11:"CFS_Steering_Wheel_Angle_Rate",
                    12:"CIS_Auxiliary_Buttons",13:"SCC_DynObj_Heading",
                    14:"SCC_OwnVehToLeadObjDist",15:"SCC_Lane_Deviation"}
                    
        self.elemlist = [elemDict[self.CheckVar1.get()],elemDict[self.CheckVar2.get()],
                         elemDict[self.CheckVar3.get()],elemDict[self.CheckVar4.get()],
                         elemDict[self.CheckVar5.get()],elemDict[self.CheckVar6.get()],
                         elemDict[self.CheckVar7.get()],elemDict[self.CheckVar8.get()],
                         elemDict[self.CheckVar9.get()],elemDict[self.CheckVar10.get()],
                         elemDict[self.CheckVar11.get()],elemDict[self.CheckVar12.get()],
                         elemDict[self.CheckVar13.get()],elemDict[self.CheckVar14.get()],
                         elemDict[self.CheckVar15.get()]]
                         
        # Only keeps elements in list that are not "No_Selection"
        self.elemlist[:] = [x for x in self.elemlist if x != "No_Selection"]
        print self.elemlist # just for debugging
        return self.elemlist # I don't know if I need a return
        
    # Press enter to accept the experiment name
    # This is the part of the file name the glob command
    # should look for
    def OnPressEnter(self,event):
        self.labelVariable.set(self.entryVariable.get() )
        self.entry.focus_set()
        self.entry.selection_range(0, END)
        return self.labelVariable
        
    def youSureBoutThat(self):
       result = askokcancel("You sure?","Process DAQ files now?")
       if result is True:
          self.ProcessDAQs()
       else:
          pass
        
        
    ## This is the part of the script that runs after you click "Process DAQs"
    ## It is adapted from the "main" loop of the convert_daq.py script
    ## EDIT SO THAT THE "Process DAQ" BUTTON FIRST CALLS AN "ARE YOU SURE?" BOX
    def ProcessDAQs(self):
        import argparse
        # See: https://docs.python.org/3/library/argparse.html
        # I think part_list can just be local
        # Get list of participants from input directory
        ## SET A DEFAULT OPTION HERE, ALSO CHECK OUTPUT DIRECTORY AND SET
        ## A DEFAULT
        part_list = glob(self.inputDirVar.get() + "\*")
        
        # Get rid of junk paths
        self.clean_empty_paths(part_list)
        
        print part_list # Just for debugging
        # To check if everything in the list is a directory: os.path.isdir()
        # Don't currently have that clean up step implemented
        # Get rid of folders: listname = [x for x in f_list if os.path.isdir(x) == FALSE]
        
        for part in part_list:
            part_num = self.get_part_num(part)
            print(part_num)
            
            if len(glob(part + "\\" + self.labelVariable.get() + "*.daq")) != 0:
                parser = argparse.ArgumentParser()
                parser.add_argument("-f", "--file", \
                    help="The name of the daq file")
                parser.add_argument("-e", "--elements", \
                    help="The name of a txt file with a sublist of elements")
                parser.add_argument("-o","--outname", \
                    help="The desired name of the output file")
                parser.add_argument("-p","--outpath", \
                    help="The path in which to save the output file")
                    #help="C:\Users\minisim\Documents\test\2021\output")
                args = parser.parse_args()
                # daq file name for run; labelVariable tells part of file name that
                # uniquely identifies the current experiment
                filename = glob(part + "\\" + self.labelVariable.get() + "*.daq")[0]
                ## I don't think I need this elemfile stuff (elemfile + the if statements)
                ## I really don't think I need the argparse either.
                elemfile = ''
                outname = part_num
                outpath = self.outputDirVar.get()
                if args.file:
                    filename = args.file
                if args.elements:
                    elemfile = args.elements
                if args.outname:
                    outname = args.outname
                if args.outpath:
                    outpath = args.outpath
                # Removed argument "elemfile", was second
                d = self.convert_daq(filename,outname,outpath)
                # FINAL_Crosswalk_Study_C_20140307093117.daq
                # filename = '20120601154617.daq' # default test file
                #from timeit import Timer
                #t = Timer("convert_daq('20120212145024')","from __main__ import test")
                #print t.timeit(1)
                #import cProfile
                #cProfile.run("test('20120212145024')")
                #d=convert_daq('HFCV_DriveB_main_20120611140939','elemListJoel.txt')
            else:
                print "DAQ file missing for participant " + part_num
                continue

###############
## MAIN LOOP ##
###############
if __name__ == "__main__":
    app = conv_daq_tk(None)
    app.title('Process DAQ Files')
    app.mainloop()
    
"""
Version 2:
1. Added confirmation dialog box before starting process DAQ function
2. Cleaned up module imports

Didn't figure out how to do a progress bar. Requires multithreading

Version 3:
1. Added more simulator variables:
CIS_Auxiliary_Buttons, CIS_Auxiliary_Buttons,
CFS_Accelerator_Pedal_Position,CFS_Brake_Pedal_Position,SCC_OwnVehToLeadObjDist,
and SCC_Lane_Deviation
2. Moved buttons 3 and 4 down to row 5 to make room for an additional
row of variables.

Version 7:
Replaced Vehicle Velocity with Object Heading
"""