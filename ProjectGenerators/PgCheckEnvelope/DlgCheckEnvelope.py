#Boa:Dialog:DlgCheckEnvelope

import wx
import os

def create(parent):
    return DlgCheckEnvelope(parent)

[wxID_DLGCHECKENVELOPE, wxID_DLGCHECKENVELOPEBTNBROWSE,
 wxID_DLGCHECKENVELOPEBTNCANCEL, wxID_DLGCHECKENVELOPEBTNOK,
 wxID_DLGCHECKENVELOPESLBUTTONS, wxID_DLGCHECKENVELOPESLENVSETTINGSHDR,
 wxID_DLGCHECKENVELOPESLRECORDINGSHDR, wxID_DLGCHECKENVELOPESTDIRECTORY,
 wxID_DLGCHECKENVELOPESTENVSETTINGSHDR, wxID_DLGCHECKENVELOPESTFORMATDETAILS,
 wxID_DLGCHECKENVELOPESTDELTAT, wxID_DLGCHECKENVELOPESTDELTAY,
 wxID_DLGCHECKENVELOPESTRECORDINGSHDR, wxID_DLGCHECKENVELOPETCDIRECTORY,
 wxID_DLGCHECKENVELOPETCFORMATDETAILS, wxID_DLGCHECKENVELOPETCDELTAT,
 wxID_DLGCHECKENVELOPETCDELTAY,
] = wx.NewIdRef(17)

class DlgCheckEnvelope(wx.Dialog):
    def _init_coll_szDirectory_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.tcDirectory, 1, border=0, flag=0)
        parent.AddSpacer(8)
        parent.Add(self.btnBrowse, 0, border=0, flag=0)

    def _init_coll_szRecSettings_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.stDirectory, 0, border=0, flag=0)
        parent.Add(self.szDirectory, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(8)
        parent.Add(self.stFormatDetails, 0, border=0, flag=0)
        parent.Add(self.tcFormatDetails, 0, border=0, flag=wx.EXPAND)

    def _init_coll_szContent_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.szRecSettingsHdr, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(8)
        parent.Add(self.szRecSettings, 0, border=16,
              flag=wx.EXPAND | wx.LEFT)
        parent.AddSpacer(16)
        parent.Add(self.szEnvSettingsHdr, 0, border=0, flag=wx.EXPAND)
        parent.AddSpacer(8)
        parent.Add(self.szEnvSettings, 0, border=16, flag=wx.LEFT)

    def _init_coll_szRecSettingsHdr_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.stRecordingsHdr, 0, border=0, flag=0)
        parent.AddSpacer(8)
        parent.Add(self.slRecordingsHdr, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)

    def _init_coll_szButtons_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.btnOk, 0, border=0, flag=0)
        parent.AddSpacer(8)
        parent.Add(self.btnCancel, 0, border=0, flag=0)

    def _init_coll_szEnvSettings_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.stDeltaT, 0, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.Add(self.tcDeltaT, 0, border=0, flag=0)
        parent.Add(self.stDeltaY, 0, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)
        parent.Add(self.tcDeltaY, 0, border=0, flag=0)

    def _init_coll_szEnvSettingsHdr_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.stEnvSettingsHdr, 0, border=0, flag=0)
        parent.AddSpacer(8)
        parent.Add(self.slEnvSettingsHdr, 1, border=0,
              flag=wx.ALIGN_CENTER_VERTICAL)

    def _init_coll_szMain_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.szContent, 1, border=8, flag=wx.EXPAND | wx.ALL)
        parent.Add(self.slButtons, 0, border=0, flag=wx.EXPAND)
        parent.Add(self.szButtons, 0, border=8,
              flag=wx.ALL | wx.ALIGN_RIGHT)

    def _init_sizers(self):
        # generated method, don't edit
        self.szMain = wx.BoxSizer(orient=wx.VERTICAL)

        self.szContent = wx.BoxSizer(orient=wx.VERTICAL)

        self.szButtons = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.szRecSettingsHdr = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.szDirectory = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.szRecSettings = wx.BoxSizer(orient=wx.VERTICAL)

        self.szEnvSettingsHdr = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.szEnvSettings = wx.FlexGridSizer(cols=4, hgap=8, rows=1, vgap=4)

        self._init_coll_szMain_Items(self.szMain)
        self._init_coll_szContent_Items(self.szContent)
        self._init_coll_szButtons_Items(self.szButtons)
        self._init_coll_szRecSettingsHdr_Items(self.szRecSettingsHdr)
        self._init_coll_szDirectory_Items(self.szDirectory)
        self._init_coll_szRecSettings_Items(self.szRecSettings)
        self._init_coll_szEnvSettingsHdr_Items(self.szEnvSettingsHdr)
        self._init_coll_szEnvSettings_Items(self.szEnvSettings)

        self.SetSizer(self.szMain)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGCHECKENVELOPE,
              name='DlgCheckEnvelope', parent=prnt, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=wx.DEFAULT_DIALOG_STYLE,
              title='Check Envelope - Settings')
        self.SetClientSize(wx.Size(500, 240))

        self.slButtons = wx.StaticLine(id=wxID_DLGCHECKENVELOPESLBUTTONS,
              name='slButtons', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self.btnOk = wx.Button(id=wx.ID_OK, label='OK', name='btnOk',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.btnOk.Bind(wx.EVT_BUTTON, self.OnBtnOk,
              id=wx.ID_OK)

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label='Abbrechen',
              name='btnCancel', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self.slRecordingsHdr = wx.StaticLine(id=wxID_DLGCHECKENVELOPESLRECORDINGSHDR,
              name='slRecordingsHdr', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self.stRecordingsHdr = wx.StaticText(id=wxID_DLGCHECKENVELOPESTRECORDINGSHDR,
              label='Settings for the recordings', name='stRecordingsHdr',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.stRecordingsHdr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.tcDirectory = wx.TextCtrl(id=wxID_DLGCHECKENVELOPETCDIRECTORY,
              name='tcDirectory', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='')

        self.btnBrowse = wx.Button(id=wxID_DLGCHECKENVELOPEBTNBROWSE,
              label='...', name='btnBrowse', parent=self, pos=wx.Point(-1,
              -1), size=wx.Size(-1, -1), style=0)
        self.btnBrowse.SetMinSize(wx.Size(21, 21))
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.OnBtnBrowse,
              id=wxID_DLGCHECKENVELOPEBTNBROWSE)

        self.stDirectory = wx.StaticText(id=wxID_DLGCHECKENVELOPESTDIRECTORY,
              label='Directrory with recordings', name='stDirectory',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.stFormatDetails = wx.StaticText(id=wxID_DLGCHECKENVELOPESTFORMATDETAILS,
              label='Format details', name='stFormatDetails', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.tcFormatDetails = wx.TextCtrl(id=wxID_DLGCHECKENVELOPETCFORMATDETAILS,
              name='tcFormatDetails', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='')

        self.slEnvSettingsHdr = wx.StaticLine(id=wxID_DLGCHECKENVELOPESLENVSETTINGSHDR,
              name='slEnvSettingsHdr', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)

        self.stEnvSettingsHdr = wx.StaticText(id=wxID_DLGCHECKENVELOPESTENVSETTINGSHDR,
              label='Settings for the Envelope', name='stEnvSettingsHdr',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.stEnvSettingsHdr.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'Tahoma'))

        self.stDeltaT = wx.StaticText(id=wxID_DLGCHECKENVELOPESTDELTAT,
              label='deltaT', name='stDeltaT', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.stDeltaY = wx.StaticText(id=wxID_DLGCHECKENVELOPESTDELTAY,
              label='deltaY', name='stDeltaY', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.tcDeltaT = wx.TextCtrl(id=wxID_DLGCHECKENVELOPETCDELTAT,
              name='tcDeltaT', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='')
        self.tcDeltaT.SetMinSize(wx.Size(60, -1))

        self.tcDeltaY = wx.TextCtrl(id=wxID_DLGCHECKENVELOPETCDELTAY,
              name='tcDeltaY', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='')
        self.tcDeltaY.SetMinSize(wx.Size(60, -1))

        self._init_sizers()

    def __init__(self, parent, paramGenerator):
        self._init_ctrls(parent)
        self.paramGenerator = paramGenerator

        self.tcDirectory.SetValue(paramGenerator.directory)
        self.tcFormatDetails.SetValue(paramGenerator.formatDetails)
        self.tcDeltaT.SetValue(str(paramGenerator.deltaT))
        self.tcDeltaY.SetValue(str(paramGenerator.deltaY))

        self.CenterOnScreen()

    def OnBtnBrowse(self, event):
        with wx.DirDialog(self, 'Choose directory with recordings',
                          style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.tcDirectory.SetValue(dlg.GetPath())

    def AlertInvalidValue(self, wnd, msg):
        with wx.MessageDialog(self, msg, 'Value is invalid',
                              wx.OK | wx.ICON_ERROR) as dlg:
            dlg.ShowModal()
            wnd.SetFocus()
            wnd.SetSelection(-1, -1)
        raise ValueError()

    def Validate(self):
        try:
            if not os.path.isdir(self.tcDirectory.GetValue()):
                self.AlertInvalidValue(self.tcDirectory, 'Directory must exist!')

            wnds = None
            try:
                for tc, st in [(self.tcDeltaT, self.stDeltaT),
                               (self.tcDeltaY, self.stDeltaY)]:
                    wnds = (tc, st)
                    float(tc.GetValue())

            except ValueError:
                self.AlertInvalidValue(wnds[0], '%s must be a float value!' % wnds[1].GetLabel())

        except ValueError:
            return False
        return True

    def OnBtnOk(self, event):
        if self.Validate():
            self.paramGenerator.directory     = self.tcDirectory.GetValue()
            self.paramGenerator.formatDetails = self.tcFormatDetails.GetValue()
            self.paramGenerator.deltaT        = float(self.tcDeltaT.GetValue())
            self.paramGenerator.deltaY        = float(self.tcDeltaY.GetValue())
            event.Skip()
