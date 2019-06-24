import wx
import os
import tkinter as tk
import wx.grid as grid
import wx.lib.inspection


class CompareApp(wx.Frame):

    def __init__(self, parent, title):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER
        super(CompareApp, self).__init__(parent, title=title, style=style, size=(1200, 800))
        self.fileLists=[]

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        btnOpen = wx.Button(panel, label='Select Folder', size=(120, 30))
        #st1 = wx.StaticText(panel, label='Class Name')
        btnOpen.SetFont(font)
        self.Bind(
            event=wx.EVT_BUTTON,
            handler=self.OnOpen,
            source=btnOpen,
        )
        hbox1.Add(btnOpen, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label='File List')
        st2.SetFont(font)
        hbox2.Add(st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = MyGrid(panel)
        #self.grid.setAttribute()

        #self.grid.CreateGrid(100, 10);
        #self.grid.SetRowSize(0, 60)
        #self.grid.SetColSize(0, 120)
        #self.filebox = wx.CheckListBox(panel, choices=self.fileLists, style=wx.LB_MULTIPLE, name="listBox")
        #tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.grid, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox3.Fit(panel)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND | wx.RIGHT | wx.EXPAND, border=10)
        size3 = hbox3.GetSize()
        print(size3)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        btnCompare = wx.Button(panel, label='Compare Files', size=(120, 30))
        #cb1 = wx.CheckBox(panel, label='Compare')
        self.Bind(
            event=wx.EVT_BUTTON,
            handler=self.compareFiles,
            source=btnCompare,
        )
        btnCompare.SetFont(font)
        hbox4.Add(btnCompare)

        btnDel = wx.Button(panel, label='Deleted Selected', size=(120, 30))
        #cb2 = wx.CheckBox(panel, label='Deleted Selected')
        btnDel.SetFont(font)
        hbox4.Add(btnDel, flag=wx.LEFT, border=10)
        #cb3 = wx.CheckBox(panel, label='Non-Project classes')
        #cb3.SetFont(font)
        #hbox4.Add(cb3, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        hbox5.Add(btn1)
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT | wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        wx.lib.inspection.InspectionTool().Show()

    def OnOpen(self, event):

        # otherwise ask the user what new file to open
        with wx.DirDialog(self, "Select Folder", style=1) as dialog:

            if dialog.ShowModal() == wx.ID_OK:
                # Proceed loading the folder chosen by the user
                pathname = dialog.GetPath()
                print(pathname)
            else:
                return
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
            if self.grid.GetNumberRows() > 0:
                self.grid.DeleteRows(0, self.grid.GetNumberRows(), False)
            self.grid.AppendRows(len(self.fileLists))
            for i in range(len(self.fileLists)):
                fileSize = os.path.getsize(self.fileLists[i])
                fileStr = str(fileSize) + 'b'
                if(float(fileSize/1024) >= 1):
                    fileStrKB = "{:.3f}".format(float(fileSize)/1024)
                    if(float(fileSize/1024/1024) >= 1):
                        fileStrMB = "{:.3f}".format(float(fileSize)/1024/1024)
                        if(float(fileSize/1024/1024/1024) >= 1):
                            fileStrTB = "{:.3f}".format(float(fileSize)/1024/1024/1024)
                            fileStr = fileStrTB
                        else:
                            fileStr = fileStrMB + 'M'
                    else:
                        fileStr = fileStrKB+'K'
                self.grid.addRow(i, self.fileLists[i], fileStr)
            self.grid.setAttribute()
            self.grid.ForceRefresh()
            #self.filebox.Set(self.fileLists)

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

    def compareFiles(self, event):
        print("compare")
        self.groupFileListSameSize()
        for i in range(len(self.groupIndex)):
            attr = grid.GridCellAttr()
            attr.SetBackgroundColour("pink")
            if (i%2 == 0):
                for row in range(self.groupIndex[i][0], self.groupIndex[i][1]+1):
                    print(row)
                    self.grid.SetRowAttr(row, attr)

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
            groupInfo = [start, stop]
            self.groupIndex.append(groupInfo)

        print(self.groupIndex)

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
        if evt.Col == 0:
            wx.CallLater(100,self.toggleCheckBox)
        evt.Skip()

    def toggleCheckBox(self):
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
    app = wx.App()
    CompareApp(None, title='Search the duplicated files')
    app.MainLoop()