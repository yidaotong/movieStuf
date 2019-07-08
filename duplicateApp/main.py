import wx
import os

import wx.grid as grid
import wx.lib.inspection
import filecmp

from ttkwidgets import Table
from ttkwidgets import CheckboxTreeview

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
        self.fileLists = []
        self.wholeContainer = tk.Frame(self.master)
        self.wholeContainer.pack()

        button_width = 3  ### (1)
        button_padx = "2m"  ### (2)
        button_pady = "1m"  ### (2)
        buttons_frame_padx = "3m"  ### (3)
        buttons_frame_pady = "2m"  ### (3)
        buttons_frame_ipadx = "3m"  ### (3)
        buttons_frame_ipady = "1m"  ### (3)

        self.buttons_frame = tk.Frame(self.wholeContainer,height=80,
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
        self.button1 = tk.Button(self.buttons_frame, command=self.OnOpen)
        self.button1.configure(text="Open")
        self.button1.focus_force()
        self.button1.configure(
            width=button_width,  ### (1)
            padx=button_padx,  ### (2)
            pady=button_pady  ### (2)
        )
        self.button1.pack(side=tk.LEFT)
        # top frame
        self.top_frame = tk.Frame(self.wholeContainer, relief=tk.RIDGE,
                                  height=50,
                                  width=980,)
        self.top_frame.pack(side=tk.TOP,
                            fill=tk.BOTH,
                            expand=tk.YES,
                            anchor="w",
                            )  ###



        self.middle_frame = tk.Frame(self.top_frame, background="white",
                                borderwidth=5, relief=tk.RIDGE,
                                height=500,
                                width=980,
                                )  ###
        self.middle_frame.pack(side=tk.LEFT,
                              fill=tk.BOTH,
                              expand=tk.YES,
                              )  ###

        self.checkwithfile = CheckboxTreeview(self.middle_frame )
        self.checkwithfile.pack()


        # now we add the buttons to the buttons_frame


#        self.left_frame = tk.Frame(self.middle_frame, background="white",
#                                borderwidth=0, relief=tk.RIDGE,
#                                height=500,
#                                width=2,
#                                )  ###
#        self.left_frame.pack(side=tk.LEFT,
#                             fill=tk.BOTH,
#                             expand=tk.YES,
#                             )  ###

        ### right_frame
#        self.right_frame = tk.Frame(self.middle_frame, background="white",
#                                 borderwidth=0, relief=tk.RIDGE,
#                                    height=500,
#                                 width=900,
 #                                )
 #       self.right_frame.pack(side=tk.RIGHT,
 #                             fill=tk.BOTH,
 #                             expand=tk.YES,
 #                             )  ###

 #       isAllSelected=False

 #       self.AllCheckButton = ttk.Checkbutton(self.middle_frame, text="All", variable=isAllSelected)
 #       self.AllCheckButton.grid(sticky=tk.W)
 #       self.checkMap={}

 #       columns = ["File List", "Size"]
 #       self.table = Table(self.right_frame, columns=columns, height=20)
 #       for col in columns:
 #           self.table.heading(col, text=col)

#        self.table.column(columns[0], width=800, stretch=True)
#        self.table.column(columns[1], width=80, stretch=True)
#        sx = tk.Scrollbar(self.middle_frame, orient='horizontal', command=self.table.xview)
 #       sy = tk.Scrollbar(self.middle_frame, orient='vertical', command=self.table.yview)
 #       self.table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        #self.table.pack()
 #       self.table.grid(sticky='ewns')
 #       self.master.update_idletasks()


        # bottom frame
        self.bottom_frame = tk.Frame(self.wholeContainer,
                                  relief=tk.RIDGE,
                                  height=50,
                                  width=980,
                                  )  ###
        self.bottom_frame.pack(side=tk.BOTTOM,
                               fill=tk.BOTH,
                               expand=tk.YES,
                               anchor="w",
                               )  ###

        self.btnCompare = tk.Button(self.bottom_frame, command=self.compareFiles)
        self.btnCompare.configure(text="Compare Files")
        self.btnCompare.pack(side=tk.LEFT)
        self.btnCompare.bind("<Return>", self.compareFiles)

        self.btnDel = tk.Button(self.bottom_frame)
        self.btnDel.configure(text="Deleted Selected")
        self.btnDel.pack(side=tk.LEFT)


        #t = CheckboxTreeview(self.left_frame, show="tree", padding=1)
        #t.pack()
        #t.insert("", 0, "1", text="All")

        #self.checkAll = tk.Checkbutton(self.left_frame, text="All", width=2)
        #self.checkAll.pack(side=tk.LEFT)
        #self.checkAll.grid(row=0, column=0)

        #self.lbFile = tk.Label(self.middle_frame, relief=tk.RIDGE, width=60)
        #self.lbFile["text"] = "File List"
        #self.lbFile.pack(side=tk.LEFT)
        #self.lbFile.grid(row=0, column=1)

        #self.lbSize = tk.Label(self.middle_frame, relief=tk.RIDGE, width=10)
        #self.lbSize["text"] = "Size"
        #self.lbSize.pack(side=tk.LEFT)
        #self.mylist = tk.Listbox(self.middle_frame, yscrollcommand=self.scrollbar.set)
        #for line in range(100):
        #    self.mylist.insert(tk.END, 'This is line number' + str(line))
        #self.mylist.pack(side=tk.LEFT, fill=tk.BOTH)
        #self.scrollbar.config(command=self.mylist.yview)
        #self.lbSize.grid(row=0, column=2)


        #self.button1.bind("<Return>", self.OnOpen)

        #self.btnDel.bind("<Return>", self.compareFiles)
        #self.btnCompare.grid(row=2, column=0, columnspan=20)
        #self.pack(fill=tk.BOTH, expand=1)
        #self.create_widgets()
        #self.InitUI()
        #self.Centre()
        #self.Show()

    def InitUI(self):
        self.openButton = Button(self)
        self.openButton["text"] = "Select Folder"
        self.openButton["command"] = self.OnOpen
        self.openButton.place(x=20, y=20)

        self.frame = tk.Frame(self)
        self.frame.pack()
        #self.pack()
        self.lbFile = tk.Label(self.frame)
        self.lbFile["text"] = "File List"
        #self.lbFile.grid(row=1, column=0, columnspan=20)

        self.lbSize = tk.Label(self.frame)
        self.lbSize["text"] = "Size"
        #self.lbSize.grid(row=1, column=1, columnspan=20)


        self.btnCompare = tk.Button(self)
        self.btnCompare["text"] = "Compare Files"
        self.btnCompare["command"] = self.btnCompare
        self.btnCompare.grid(row=2, column=0, columnspan=20)

        self.btnDel = tk.Button(self)
        self.btnDel["text"] = "Deleted Selected"
        #self.btnDel["command"] = self.btnCompare
        self.btnDel.grid(row=2, column=1, columnspan=20)

        self.btnOk = tk.Button(self)
        self.btnOk["text"] = "Ok"
        #self.btnOk["command"] = self.btnCompare
        self.btnOk.grid(row=2, column=2, columnspan=2)

        self.btnClose = tk.Button(self)
        self.btnClose["text"] = "Close"
        #self.btnOk["command"] = self.btnCompare
        self.btnClose.grid(row=2, column=3, columnspan=2)


    def OnOpen(self):

        # otherwise ask the user what new file to open
        pathname = filedialog.askdirectory()
        print(pathname)

        self.getAllFileListByPath(pathname)
        fileList = [0 for i in range(len(self.fileLists))]
        for i in range(len(self.fileLists)):
            fileList[i]=(self.fileLists[i], os.path.getsize(self.fileLists[i]))
        fileList.sort(key=lambda filename: filename[1], reverse=True)
        for i in range(len(fileList)):
            self.fileLists[i] = fileList[i][0]
        print("file list:")
        print(self.fileLists)
        print("file list end")
        self.groupFileListSameSize()
        index=0
        fileSize=0
        for fileList in self.groupIndex:
            for i in range(len(fileList)):
                print(fileList[i])
                fileSize = os.path.getsize(fileList[i])
                rootIndex = "index_"+str(index)
                childIndex = "s_"+str(fileSize)+str(i)
                if i == 0:
                    self.checkwithfile.insert('', "end", rootIndex, text=str(fileSize))
                else:
                    self.checkwithfile.insert(rootIndex, "end", childIndex, text=fileList[i])
            index = index+1


        #if self.grid.GetNumberRows() > 0:


    def addFileRow(self, rowNum, fileName, fileSize, isCheck=False):
        #self.checkButton = ttk.Checkbutton(self.left_frame)
        #elf.checkButton.grid(sticky=tk.W)
        #self.checkMap[rowNum] = self.checkButton
        #self.tree.insert('', 'end')
        self.table.insert('', 'end', iid=rowNum, values=(fileName, fileSize))

    def getAllFileListByPath(self, pathname):
        try:
            if os.path.isdir(pathname):
                fileList = os.listdir(pathname)
                print('pathname')
                print(pathname)
                print('filelist:')
                print(fileList)

                for file in fileList:
                    if not file.startswith('.'):
                        fullPath = os.path.join(pathname, file)
                        if os.path.isdir(fullPath):
                            self.getAllFileListByPath(fullPath)
                        else:
                            self.fileLists.append(fullPath)
            else:
                self.fileLists.append(pathname)

        except IOError:
            wx.LogError("Cannot open Directoy '%s'." % pathname)

    def compareFiles(self):
        print("compare")
        self.groupFileListSameSize()
        self.groupFileListCompair()
        for i in range(len(self.groupCompairIndex)):
            attr = grid.GridCellAttr()
            attr.SetBackgroundColour("pink")
            if(len(self.groupCompairIndex[i]) > 1):
                for row in self.groupCompairIndex[i]:
                    #evt = self.grid.GridEvent()
                    #evt.col = 0
                    #evt.row = row
                    attr = self.grid.GetOrCreateCellAttr(row, 0)
                    celleditor = attr.GetEditor(self.grid, row, 0)
                    render = attr.GetRenderer(self.grid, row, 0)
                    #render.Draw(self.grid, attr,)
                    #attr.SetRenderer(render)
                    print(attr)
                    #evt = grid.GridEditorCreatedEvent(self.grid.GetId(), 10270, self.grid, row=row)
                    #evt.SetCol(0)
                    #evt.SetRow(row)
                    #msg = grid.GridTableMessage(self, grid.GRIDTABLE_NOTIFY_ROWS_INSERTED, row, 1)
                    #self.GetView().ProcessTableMessage(msg)
                    #evt = grid.GridEvent(self.grid.GetId(), 10250, self.grid, row=row, col=0)
                    #wx.PostEvent(evt)
                    #evt = wx.CommandEvent(wx.EVT_CHECKBOX.typeId, self.grid.GetId())
                    #self.grid.onMouse(evt)
                    #wx.PostEvent(self.GetEventHandler(), evt)
            if (i%2 == 0):
                print(self.groupCompairIndex[i])
                for row in range(self.groupCompairIndex[i][0], self.groupCompairIndex[i][1]):
                    self.grid.SetRowAttr(row, attr)
        self.grid.ForceRefresh()

    def groupFileListSameSize(self):
        groupNum = 0
        self.groupIndex=[]
        if (len(self.fileLists)>0):
            start = 0
            stop = 1
            fileSize = os.path.getsize(self.fileLists[0])

            for i in range(len(self.fileLists)-1):
                stop = i + 1
                if(fileSize != os.path.getsize(self.fileLists[i+1])):
                    groupInfo=[start, stop]
                    fileSize = os.path.getsize(self.fileLists[i+1])
                    self.groupIndex.append(groupInfo)
                    start = i+1
            groupInfo = [start, stop+1]
            self.groupIndex.append(groupInfo)
        print(self.groupIndex)

    def groupFileListCompair(self):
        self.groupCompairIndex=[]
        for group in self.groupIndex:
            if(group and len(group)>1):
                start = group[0]
                end = group[1]
                print("compare from "+str(start)+" to "+str(end))
                self.compairFilesInRange(start, end)
                print("get contet result")
                print(self.groupCompairIndex)
        print("content compair")
        print(self.groupCompairIndex)

    def compairFilesInRange(self, start, end):
        if((end-start)==1):
            indexlist = [start, start+1]
            self.groupCompairIndex.append(indexlist)
        elif((end-start)==2 and filecmp.cmp(self.fileLists[start], self.fileLists[start+1])):
            indexlist = [start, (start+1)]
            self.groupCompairIndex.append(indexlist)
        else:
            allList = []
            loopList = list(range(start, end-1))
            for i in loopList:
                indexlist = [i]
                exist = False
                found = False
                for j in range(start+1, end):
                    for li in allList:
                        if((start in li) and (j in li)):
                            exist = True
                            if(start in loopList):
                                loopList.remove(start)
                            if(j in loopList):
                                loopList.remove(j)
                    if (exist):
                        continue
                    elif(filecmp.cmp(self.fileLists[start], self.fileLists[j])):
                        indexlist.append(j)
                for li in allList:
                    for i in indexlist:
                        if(i in li):
                            found = True;
                            break
                    if(found):
                        break
                if(not found):
                    allList.append(indexlist)
            for singleList in allList:
                self.groupCompairIndex.append(singleList)
            orgList = list(range(start, end))
            for sameList in self.groupCompairIndex:
                for i in sameList:
                    if i in(orgList):
                        orgList.remove(i)
            for i in orgList:
                self.groupCompairIndex.append([i,i+1])

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