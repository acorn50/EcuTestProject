import wx
import wx.lib.gizmos


class RunDialogExample(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY,
                           title="Counter", size=(220, 140))
        self.clock = wx.lib.gizmos.LEDNumberCtrl(self, -1,
                                             pos=(10, 10), size=(200, 40),
                                             style=wx.lib.gizmos.LED_ALIGN_RIGHT)
        self.okButton = wx.Button(self, wx.ID_OK, "Ok",
                                  pos=(10, 60), size=(200, 21))
        self.okButton.Bind(wx.EVT_BUTTON, self.OnOk)

    def OnOk(self, event):
        """ """
        # TODO: doctring type
        self.EndModal(wx.ID_OK)

    def SetValue(self, name, value):
        """ """
        # TODO: doctring type
        if name == "count":
            self.clock.SetValue(value)

    def GetValue(self, name):
        """ """
        # TODO: doctring type
        if name == "count":
            return self.clock.GetValue()
