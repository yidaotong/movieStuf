import wx
import gettext

class MyFrame(wx.Frame):
    def __init__(self):
        _ = gettext.gettext
        self.title = _('Duplicate File Removal')
        super().__init__(parent=None, title=self.title)
        self.my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self)
        self.initUI()

    def initUI(self):
        self.menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        newItem = wx.MenuItem(fileMenu, id=wx.ID_NEW, text="New search", kind=wx.ITEM_NORMAL)
        fileMenu.AppendItem(newItem)

        my_btn = wx.Button(self.panel, label='Open Folder')
        my_btn.Bind(wx.EVT_BUTTON, self.on_press)
        self.my_sizer.Add(my_btn, 0, wx.ALL | wx.LEFT, 5)
        self.panel.SetSizer(self.my_sizer)
        self.menuBar.Append(fileMenu, title='File')
        self.SetMenuBar(self.menuBar)
        self.Show()

    def showFolderList(self):
        folderList=['c:', 'd:']
        self.FileList = wx.TextCtrl(self.panel,style = wx.TE_MULTILINE)
        lst = wx.ListBox(self.panel, size=(100, -1), choices=folderList, style=wx.LB_SINGLE)
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        box.Add(lst, 0, wx.EXPAND)
        box.Add(self.text, 1, wx.EXPAND)
        self.panel.SetSizer(box)
        self.panel.Fit()
        self.Centre()
        self.Bind(wx.EVT_LISTBOX, self.onListBox, lst)

        #self.my_sizer.Add(self.FileList, 30, wx.ALL | wx.EXPAND, 35)
        self.Show(True)

    def onListBox(self, event):
        self.text.AppendText("Current selection:"+event.GetEventObject().GetStringSelection()+"\n")

    def on_press(self, event):
        self.showFolderList()
        value = self.FileList.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()