import wx
import os
import sys
import stat

import wx.grid as grid
import wx.lib.inspection
import filecmp

from ttkwidgets import Table
from ttkwidgets import CheckboxTreeview
import tkinter.scrolledtext as tkscrolled

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog


class CompareApp():

    def __init__(self, master, title):
        #super().__init__(master)
        self.master = master
        self.pathList = set([])
        self.fileLists = []
        self.groupFiles = {}
        self.InitUI()

    def InitUI(self):
        self.wholeContainer = tk.Frame(self.master)
        self.wholeContainer.pack()

        button_width = 3  ### (1)
        button_padx = "2m"  ### (2)
        button_pady = "1m"  ### (2)
        buttons_frame_padx = "3m"  ### (3)
        buttons_frame_pady = "2m"  ### (3)
        buttons_frame_ipadx = "3m"  ### (3)
        buttons_frame_ipady = "1m"  ### (3)

        self.buttons_frame = tk.Frame(self.wholeContainer, height=10,
                                      width=980)  ###
        self.buttons_frame.pack(
            side=tk.TOP,  ###
            fill=tk.BOTH,
            expand=tk.YES,
            anchor="w",
            ipadx=buttons_frame_ipadx,
            ipady=buttons_frame_ipady,
            padx=buttons_frame_padx,
            pady=buttons_frame_pady,
        )
        self.button1 = tk.Button(self.buttons_frame, command=self.Add)
        self.button1.configure(text="Add")
        self.button1.focus_force()
        self.button1.configure(
            width=button_width,  ### (1)
            padx=button_padx,  ### (2)
            pady=button_pady  ### (2)
        )
        self.button1.pack(side=tk.LEFT)
        self.button2 = tk.Button(self.buttons_frame, command=self.Remove)
        self.button2.configure(text="Remove")
        self.button2.configure(
            width=6,  ### (1)
            padx=button_padx,  ### (2)
            pady=button_pady  ### (2)
        )
        self.button2.pack(side=tk.LEFT)
        # top frame
        self.top_frame = tk.Frame(self.wholeContainer, relief=tk.RIDGE,
                                  height=250,
                                  width=980, )
        self.top_frame.pack(side=tk.TOP,
                            fill=tk.BOTH,
                            expand=tk.YES,
                            )  ###
        self.selctedFolder = ""

       # self.folderBox.pack(side=tk.LEFT,fill=tk.BOTH,expand=tk.YES,)  ###
        self.boxScroll = tk.Scrollbar(self.top_frame, orient="vertical")
       # self.boxScroll.config(command=self.folderBox.yview)
        self.boxScroll.grid(row=0, column=1, sticky=tk.NW + tk.S)
        self.folderBox = tk.Listbox(self.top_frame, selectmode=tk.MULTIPLE, relief=tk.RIDGE,
                                  height=20,
                                  width=30, yscrollcommand=self.boxScroll.set, )
        self.folderBox.grid(row=0, column=0, sticky=tk.NW + tk.S)
        #self.boxScroll.pack(side="right", fill="y")

        self.checkScroll = tk.Scrollbar(self.top_frame, orient="vertical")
        self.checkScroll.grid(row=0, column=3, sticky=tk.W, columnspan = 1)

        self.checkwithfile = CheckboxTreeview(self.top_frame, height=20, yscrollcommand=self.checkScroll.set)
        self.checkwithfile.grid(row=0, column=2, sticky=tk.NW + tk.S, columnspan=200)
        #self.checkwithfile.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #self.checkScroll.pack(side="right", fill="y")



        self.btnCompare = tk.Button(self.buttons_frame, command=self.compareFiles)
        self.btnCompare.configure(text="Compare Files")
        self.btnCompare.pack(side=tk.LEFT)
        self.btnCompare.bind("<Return>", self.compareFiles)

        self.btnDel = tk.Button(self.buttons_frame, command=self.deleteSelectedFiles)
        self.btnDel.configure(text="Deleted Selected")
        self.btnDel.pack(side=tk.LEFT)
        self.btnCompare.bind("<Return>", self.deleteSelectedFiles)
        # bottom frame
        self.bottom_frame = tk.Frame(self.wholeContainer,
                                     relief=tk.RIDGE,
                                     height=20,
                                     width=970,
                                     )  ###
        self.bottom_frame.pack(side=tk.BOTTOM,
                               fill=tk.BOTH,
                               expand=tk.YES,
                               )  ###


        self.output = tkscrolled.ScrolledText(self.bottom_frame, width=970, height=6, wrap='word')
        self.output.config(state=tk.DISABLED)
        self.output.pack(side=tk.LEFT)



    def Add(self):

        # otherwise ask the user what new file to open
        pathname = filedialog.askdirectory()
        pathname = os.path.abspath(pathname)
        print(pathname)
        if pathname in self.pathList:
            print("folder already exist" + pathname)
            return
        else:
            self.pathList.add(pathname)
            for id, path in enumerate(self.pathList):
                if path == pathname:
                    self.folderBox.insert(id, pathname)
        if os.path.exists(pathname):
            for i in self.checkwithfile.get_children():
                self.checkwithfile.delete(i)
            #self.fileLists = {}
            self.groupFiles = {}
        else:
            print("folder not found:"+pathname)
            return

        allFiles = set(self.fileLists)
        allFiles.update(self.getAllFileListByPath(pathname))
        #print("allFiles:")
        #print(allFiles)
        self.fileLists = list(allFiles)
        #print("converted fileLists:")
        #print(self.fileLists)
        self.renewFileList()

    def renewFileList(self):
        fileList = [0 for i in range(len(self.fileLists))]
        for i in range(len(self.fileLists)):
            if os.path.exists(self.fileLists[i]):
                fileList[i]=(self.fileLists[i], os.path.getsize(self.fileLists[i]))
            else:
                print("remove not exist file:"+self.fileLists[i])
                fileList.pop(i)
        fileList.sort(key=lambda filename: filename[1], reverse=True)
        for i in range(len(fileList)):
            self.fileLists[i] = fileList[i][0]
        print("file list:")
        print(self.fileLists)
        print("file list end")
        self.groupFileListSameSize()
        print("groupFiles:")
        print(self.groupFiles)
        index=0
        for fileSize, fileList in self.groupFiles.items():
            rootIndex = "r_" + str(index)
            sizeCal = str(fileSize)+'b'
            if fileSize > 1024:

                if fileSize > 1024*1024:
                    if fileSize >1024*1024*1024:
                        if fileSize >1024*1024*1024*1024:
                            sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024*1024*1024)) + 'T'
                        else:
                            sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024*1024)) + 'G'
                    else:
                        sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024)) + 'M'
                else:
                    sizeCal = "{:.3f}".format(float(fileSize) / 1024) + 'k'
            fileNum = len(fileList)
            self.checkwithfile.insert('', "end", rootIndex, text=sizeCal+'('+str(fileNum)+')')

            self.checkwithfile.tag_configure("evenrow", background='white', foreground='black')
            self.checkwithfile.tag_configure("oddrow", background='black', foreground='white')
            for i in range(len(fileList)):
                childIndex = "c_"+str(fileSize)+'_i_'+str(i)
                textC = fileList[i]
                print("textC:"+textC)
                self.checkwithfile.insert(rootIndex, "end", childIndex, text=fileList[i])
            index = index+1

    def Remove(self):
        print("selected:")
        for i in self.folderBox.curselection():
            print(i)
            filePath = self.folderBox.get(i)
            print(filePath)
            self.folderBox.delete(i)
            self.pathList.remove(filePath)
        #selected_text_list = [self.folderBox.get(i) for i in self.folderBox.curselection()]
        #print(selected_text_list)
        for i in self.checkwithfile.get_children():
            self.checkwithfile.delete(i)
        # self.fileLists = {}
        self.groupFiles = {}
        if len(self.pathList) > 0:
            allFiles = set([])
            for pathname in self.pathList:
                allFiles.update(self.getAllFileListByPath(pathname))
            self.fileLists = list(allFiles)
            self.renewFileList()

    def getAllFileListByPath(self, pathname):
        fileSet = set([])
        try:
            if os.path.isdir(pathname):
                fileList = os.listdir(pathname)
                print('pathname')
                print(pathname)
                print('filelist:')
                print(fileList)

                for file in fileList:
                    if not file.startswith('.'):
                        fullPath = pathname + os.sep +  file
                        if os.path.exists(fullPath):
                            if os.path.isdir(fullPath):
                                fileSet.update(self.getAllFileListByPath(fullPath))
                            else:
                                fileSet.add(fullPath)
            elif os.path.exists(pathname):
                fileSet.add(pathname)

        except IOError:
            wx.LogError("Cannot open Directoy '%s'." % pathname)
        return fileSet

    def compareFiles(self):
        print("compare")

        for i in self.checkwithfile.get_children():
            self.checkwithfile.delete(i)
        rootIn = 0
        for fileSize, fileList in self.groupFiles.items():
            rootIndex = "r_" + str(rootIn)
            sizeCal = str(fileSize)+'b'
            if fileSize > 1024:

                if fileSize > 1024*1024:
                    if fileSize >1024*1024*1024:
                        if fileSize >1024*1024*1024*1024:
                            sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024*1024*1024)) + 'T'
                        else:
                            sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024*1024)) + 'G'
                    else:
                        sizeCal = "{:.3f}".format(float(fileSize) / (1024*1024)) + 'M'
                else:
                    sizeCal = "{:.3f}".format(float(fileSize) / 1024) + 'k'
            fileNum = len(fileList)
            self.checkwithfile.insert('', "end", rootIndex, text=sizeCal+'('+str(fileNum)+')')


            indexFileGroup = {}
            groupedSameList = self.compareSameSizeFiles(fileList)

            childIn = 0
            for groupIndex in range(len(groupedSameList)):
                #indexFileGroup[child] = fileList[groupIndex]


                textC = fileList[groupIndex]
                print("textC:"+textC)
                self.checkwithfile.tag_configure("evenrow", background='white', foreground='black')
                self.checkwithfile.tag_configure("oddrow", background='black', foreground='white')
                for i in range(len(groupedSameList[groupIndex])):
                    childIndex = "c_" + str(fileSize) + '_i_' + str(childIn)
                    if groupIndex % 2 == 0:
                        self.checkwithfile.insert(rootIndex, "end", childIndex, text=fileList[i], tags=('evenrow',))
                    else:
                        self.checkwithfile.insert(rootIndex, "end", childIndex, text=fileList[i], tags=('oddrow',))
                    if i > 0:
                        self.checkwithfile.change_state(childIndex, 'checked')


                    childIn = childIn + 1

            rootIn = rootIn+1


    def compareSameSizeFiles(self, fileList):
        groupComparedFiles=[]
        groupMap = []
        compareIndex = ""
        groupComparedFiles.append(groupMap)
        for index in range(len(fileList)):
            fileName = fileList[index]
            groupMap = []
            if len(groupComparedFiles) == 1 and len(groupComparedFiles[0]) == 0:
                groupComparedFiles[0].append(fileName)
                continue

            for i in range(len(groupComparedFiles)):
                (groupIndex, fileIndex) = self.getIndexInGroup(groupComparedFiles, fileName)
                if groupIndex == -1:
                    outputStr = "Comparing: " + groupComparedFiles[i][0] + " and " + fileName + "\n"
                    self.output.config(state=tk.NORMAL)
                    self.output.insert("end", outputStr)
                    self.output.see("end")
                    self.output.config(state=tk.DISABLED)
                    if filecmp.cmp(groupComparedFiles[i][0], fileName):
                        groupComparedFiles[i].append(fileName)
                        break
                    else:
                        groupMap.append(fileName)
                        groupComparedFiles.append(groupMap)


        print("groupComparedFiles:")
        print(groupComparedFiles)
        return groupComparedFiles

    def getIndexInGroup(self, groupList, fileName):
        for groupIndex in range(len(groupList)):
            for fileIndex in range(len(groupList[groupIndex])):
                if groupList[groupIndex][fileIndex] == fileName:
                    return (groupIndex, fileIndex)
        return  (-1, -1)

    def groupFileListSameSize(self):

        if (len(self.fileLists)>0):
            fileSize = os.path.getsize(self.fileLists[0])
            groupList = []
            groupList.append(self.fileLists[0])
            for i in range(len(self.fileLists)-1):
                fileNewSize = os.path.getsize(self.fileLists[i+1])
                if(fileSize != fileNewSize):
                    self.groupFiles[fileSize] = groupList
                    fileSize = fileNewSize
                    groupList = []
                groupList.append(self.fileLists[i+1])
            if len(groupList) > 0:
                self.groupFiles[fileSize] = groupList

    def deleteSelectedFiles(self):
        print("enter deleteSelectedFiles")
        for i in self.checkwithfile.get_children():
            orgLen = len(self.checkwithfile.get_children(i))
            newLen = orgLen
            for item in self.checkwithfile.get_children(i):
                if self.checkwithfile.tag_has("checked", item):
                    fileName = self.checkwithfile.item(item)['text']
                    print(fileName)
                    os.chmod(fileName, stat.S_IWUSR)
                    os.remove(fileName)
                    self.checkwithfile.delete(item)
                    newLen -= 1
            if orgLen > newLen:
                text = self.checkwithfile.item(i)['text'].replace("("+str(orgLen)+")", "("+str(newLen)+")")
                self.checkwithfile.item(i, text=text)

class MyGrid(grid.Grid):
    def __init__(self, parent):
        grid.Grid.__init__(self, parent, -1, pos=(10,40), size=(420,95))
        self.Bind(grid.EVT_GRID_SELECT_CELL,self.onCellSelected)
        self.Bind(grid.EVT_GRID_CELL_LEFT_CLICK,self.onMouse)
        self.Bind(grid.EVT_GRID_EDITOR_CREATED, self.onEditorCreated)
        self.CreateGrid(0,3)
        self.RowLabelSize = 0
        #self.ColLabelSize = 20
        self.SetColLabelValue(0, ' ')
        self.SetColLabelValue(1, 'file name')
        self.SetColLabelValue(2, 'file size')
        self.AutoSizeColumn(0, False)
        self.SetColSize(0, 24)
        self.SetColSize(1, 1060)
        self.SetColMinimalWidth(2, 100)

    def setAttribute(self):

        attr = grid.GridCellAttr()
        attr.SetEditor(grid.GridCellBoolEditor())
        attr.SetRenderer(grid.GridCellBoolRenderer())
        self.SetColAttr(0,attr)
        attr = grid.GridCellAttr()
        attr.SetReadOnly(True)
        self.SetColAttr(1, attr)
        self.SetColAttr(2, attr)

        attr = grid.GridCellAttr()
        #attr.SetBackgroundColour("pink")
        self.SetRowAttr(1, attr)

    def addRow(self, rowIndex, filepath, size):
        self.SetCellValue(rowIndex, 1, filepath)
        self.SetCellValue(rowIndex, 2, size)


    def onMouse(self,evt):
        print("mouse event")
        print(evt)
        if evt.Col == 0:
            wx.CallLater(100, self.toggleCheckBox)
        evt.Skip()

    def toggleCheckBox(self):
        print("cb value:"+str(self.cb.Value))
        self.cb.Value = not self.cb.Value
        self.afterCheckBox(self.cb.Value)

    def onCellSelected(self,evt):
        if evt.Col == 0:
            wx.CallAfter(self.EnableCellEditControl)
        evt.Skip()

    def onEditorCreated(self,evt):
        if evt.Col == 0:
            self.cb = evt.Control
            self.cb.WindowStyle |= wx.WANTS_CHARS
            self.cb.Bind(wx.EVT_KEY_DOWN,self.onKeyDown)
            self.cb.Bind(wx.EVT_CHECKBOX,self.onCheckBox)
        evt.Skip()

    def onKeyDown(self,evt):
        if evt.KeyCode == wx.WXK_UP:
            if self.GridCursorRow > 0:
                self.DisableCellEditControl()
                self.MoveCursorUp(False)
        elif evt.KeyCode == wx.WXK_DOWN:
            if self.GridCursorRow < (self.NumberRows-1):
                self.DisableCellEditControl()
                self.MoveCursorDown(False)
        elif evt.KeyCode == wx.WXK_LEFT:
            if self.GridCursorCol > 0:
                self.DisableCellEditControl()
                self.MoveCursorLeft(False)
        elif evt.KeyCode == wx.WXK_RIGHT:
            if self.GridCursorCol < (self.NumberCols-1):
                self.DisableCellEditControl()
                self.MoveCursorRight(False)
        else:
            evt.Skip()

    def onCheckBox(self,evt):
        self.afterCheckBox(evt.IsChecked())

    def afterCheckBox(self,isChecked):
        print('afterCheckBox',self.GridCursorRow,isChecked)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1000x600')
    app = CompareApp(root, "test")
    root.mainloop()