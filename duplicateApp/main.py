import wx
import os
import tkinter as tk
import wx.grid as grid

class CompareApp(wx.Frame):

    def __init__(self, parent, title):
        super(CompareApp, self).__init__(parent, title=title, size=(600, 450))
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
        self.filebox = wx.CheckListBox(panel, choices=self.fileLists, style=wx.LB_MULTIPLE, name="listBox")
        #tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(self.filebox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        btnCompare = wx.Button(panel, label='Compare Files', size=(120, 30))
        #cb1 = wx.CheckBox(panel, label='Compare')
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
            print(self.fileLists)
            self.filebox.Set(self.fileLists)

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

if __name__ == '__main__':
    app = wx.App()
    CompareApp(None, title='Search the duplicated files')
    app.MainLoop()