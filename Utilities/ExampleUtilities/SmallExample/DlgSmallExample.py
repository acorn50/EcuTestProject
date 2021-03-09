#Boa:Dialog:DlgSmallExample

# //Utility created by TraceTronic\

import wx

from tts.core.common.gui.ExpressionCtrls import ExpressionTextCtrl

[wxID_DLGSMALLEXAMPLE, wxID_DLGSMALLEXAMPLEBUTTON_CANCEL,
 wxID_DLGSMALLEXAMPLEBUTTON_OK, wxID_DLGSMALLEXAMPLESTATICTEXT1,
 wxID_DLGSMALLEXAMPLESTATICTEXT2, wxID_DLGSMALLEXAMPLEVARFROM,
 wxID_DLGSMALLEXAMPLEVARTO,
] = wx.NewIdRef(7)

_custom_classes = {"wx.TextCtrl": ["ExpressionTextCtrl"]}


class DlgSmallExample(wx.Dialog):
    def _init_coll_sizerButtons_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.button_OK, 0, border=8, flag=wx.ALL)
        parent.Add(self.button_Cancel, 0, border=8, flag=wx.ALL)

    def _init_coll_sizerMain_Items(self, parent):
        # generated method, don't edit

        parent.AddSpacer(8)
        parent.Add(self.staticText1, 0, border=8,
              flag=wx.LEFT | wx.RIGHT | wx.EXPAND)
        parent.Add(self.varFrom, 0, border=8,
              flag=wx.RIGHT | wx.LEFT | wx.EXPAND)
        parent.AddSpacer(8)
        parent.Add(self.staticText2, 0, border=8,
              flag=wx.EXPAND | wx.RIGHT | wx.LEFT)
        parent.Add(self.varTo, 0, border=8,
              flag=wx.EXPAND | wx.RIGHT | wx.LEFT)
        parent.AddSpacer(8)
        parent.Add(self.sizerButtons, 0, border=8,
              flag=wx.ALIGN_CENTER | wx.ALIGN_BOTTOM)
        parent.AddSpacer(8)

    def _init_sizers(self):
        # generated method, don't edit
        self.sizerMain = wx.BoxSizer(orient=wx.VERTICAL)

        self.sizerButtons = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_sizerMain_Items(self.sizerMain)
        self._init_coll_sizerButtons_Items(self.sizerButtons)

        self.SetSizer(self.sizerMain)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DLGSMALLEXAMPLE, name='', parent=prnt,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1),
              style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
              title='SmallExample')
        self.SetClientSize(wx.Size(263, 173))
        self.SetToolTip('Cancel')

        self.button_OK = wx.Button(id=wxID_DLGSMALLEXAMPLEBUTTON_OK, label='OK',
              name='button_OK', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0)
        self.button_OK.SetToolTip('OK')
        self.button_OK.Bind(wx.EVT_BUTTON, self.OnCmdOkButton,
              id=wxID_DLGSMALLEXAMPLEBUTTON_OK)

        self.button_Cancel = wx.Button(id=wxID_DLGSMALLEXAMPLEBUTTON_CANCEL,
              label='Cancel', name='button_Cancel', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)
        self.button_Cancel.Bind(wx.EVT_BUTTON, self.OnCmdCancelButton,
              id=wxID_DLGSMALLEXAMPLEBUTTON_CANCEL)

        self.varTo = ExpressionTextCtrl(id=wxID_DLGSMALLEXAMPLEVARTO, name='varTo',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0,
              value='var2')

        self.varFrom = ExpressionTextCtrl(id=wxID_DLGSMALLEXAMPLEVARFROM,
              name='varFrom', parent=self, pos=wx.Point(-1, -1),
              size=wx.Size(-1, -1), style=0, value='var1')

        self.staticText1 = wx.StaticText(id=wxID_DLGSMALLEXAMPLESTATICTEXT1,
              label='Save value from variable:', name='staticText1',
              parent=self, pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self.staticText2 = wx.StaticText(id=wxID_DLGSMALLEXAMPLESTATICTEXT2,
              label='to variable:', name='staticText2', parent=self,
              pos=wx.Point(-1, -1), size=wx.Size(-1, -1), style=0)

        self._init_sizers()

    def __init__(self, parent, aTestStep):
        self._init_ctrls(parent)
        self.SetInitialSize(self.GetEffectiveMinSize())
        self.SetMinSize(self.GetEffectiveMinSize())

        self.theTestStep = aTestStep
        self.varFrom.SetValue(self.theTestStep.varFrom)
        self.varTo.SetValue(self.theTestStep.varTo)

    def OnCmdCancelButton(self, event):
        ##Add your code here
        self.EndModal(wx.ID_CANCEL)

    def OnCmdOkButton(self, event):
        self.theTestStep.varFrom = self.varFrom.GetValue()
        self.theTestStep.varTo = self.varTo.GetValue()

        self.EndModal(wx.ID_OK)

##Add your required functions here
