import wx

class DlgCalculator(wx.Dialog):

    def __init__(self, parent, aParamGenerator):
        wx.Dialog.__init__(self, id=wx.NewIdRef(), name='', parent=parent,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, title='')
        self.SetClientSize(wx.Size(356, 101))
    
        self.sizerMain = wx.BoxSizer(orient=wx.VERTICAL)
        self.sizerButtons = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.boxSizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)
        
        self.sizerMain.Add(self.boxSizer1, 0, border=15, flag=wx.ALL | wx.EXPAND)
        self.sizerMain.Add(self.sizerButtons, 0, border=0,
              flag=wx.ALIGN_BOTTOM | wx.ALIGN_CENTER)
              
        self.txtFileName = wx.TextCtrl(id=wx.NewIdRef(),
              name='txtFileName', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='')
        self.boxSizer1.Add(self.txtFileName, 1, border=0, flag=0)
        
        self.boxSizer1.AddSpacer(8)

        self.button_Browse = wx.Button(id=wx.NewIdRef(),
              label='...', name='button_Browse', parent=self, pos=wx.Point(-1,
              - 1), size=wx.Size(-1, -1), style=0)
        self.button_Browse.SetMinSize(wx.Size(23, 23))
        self.button_Browse.Bind(wx.EVT_BUTTON, self.OnCmdBrowseButton)
        self.boxSizer1.Add(self.button_Browse, 0, border=0, flag=0)
        
        self.button_OK = wx.Button(id=wx.NewIdRef(), label='OK',
              name='button_OK', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)
        self.button_OK.SetToolTip('OK')
        self.button_OK.Bind(wx.EVT_BUTTON, self.OnCmdOkButton)
        self.sizerButtons.Add(self.button_OK, 0, border=5, flag=wx.ALL)

        self.button_Cancel = wx.Button(id=wx.NewIdRef(),
              label='Cancel', name='button_Cancel', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.button_Cancel.Bind(wx.EVT_BUTTON, self.OnCmdCancelButton)
        self.sizerButtons.Add(self.button_Cancel, 0, border=5, flag=wx.ALL)
        
        self.SetSizer(self.sizerMain)

        self.theParamGenerator = aParamGenerator
        self.txtFileName.SetValue(self.theParamGenerator.GetFilename())
        self.SetTitle(self.theParamGenerator.GetName())

    def OnCmdCancelButton(self, event):
        self.EndModal(wx.ID_CANCEL)

    def OnCmdOkButton(self, event):
        self.theParamGenerator.SetFilename(self.txtFileName.GetValue())
        self.EndModal(wx.ID_OK)

    def OnCmdBrowseButton(self, event):
        fileDlg = wx.FileDialog(parent=self,
                                style=wx.FD_OPEN,
                                message='CSV-Datei auswählen',
                                wildcard='CSV-Datei|*.csv',
                                defaultDir=r'',
                                defaultFile='')

        if fileDlg.ShowModal() == wx.ID_OK:
            self.txtFileName.SetValue(fileDlg.GetPath())

        fileDlg.Destroy()
