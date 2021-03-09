import os

import wx

__copyright__ = "Copyright © TraceTronic GmbH, Dresden"
__license__ = "This file is distributed as part of TraceTronic software products. You may use " \
              "this file only in accordance with the TraceTronic Software License Terms " \
              "(https://www.tracetronic.com/software-license-terms/"


TITEL = 'Filter generator'
LBL_FILTER = 'insert filter here'
TOOLTIP_EXTENDED_MODE = '(De-) Activate extended filter'
TOOLTIP_CLEAR_FILTER = 'Delete entered filter expression'

BTN_SIZE = (24, 24)


class WsFilterGenExampleDialog(wx.Dialog):
    """
    This is the dialog for the Filter Generator.
    """

    def __init__(self, projectGenerator):
        """
        Constructor.

        :param projectGenerator: ProjectGenerator to configure
        :type projectGenerator: FilterGenerator
        """
        wx.Dialog.__init__(self, None, title=TITEL,
                           style=wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE)

        self.__projectGenerator = projectGenerator
        self.__extendedMode = self.__projectGenerator.useExtendedMode

        self.__Setup()

        self.__ctlFilterValue.SetFocus()
        self.__ctlFilterValue.SelectAll()

    def __Setup(self):
        """
        Setup all controls and the layout.
        """

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.__CreateFilterControls(), flag=wx.EXPAND | wx.ALL, border=4)
        mainSizer.Add(wx.StaticLine(self), flag=wx.EXPAND)
        mainSizer.Add(self.__CreateDialogControls(), flag=wx.EXPAND | wx.ALL, border=4)

        # Fit
        self.SetSizerAndFit(mainSizer)
        dialogHeight = self.GetSize().GetHeight()
        dialogWidth = self.GetSize().GetWidth()
        self.SetSizeHints(minW=dialogWidth, minH=dialogHeight, maxH=dialogHeight)
        self.CentreOnParent()

    def __CreateFilterControls(self):
        """
        Create a sizer containing the filter controls.
        """
        self.__LoadFilterIcons()
        self.__CreateFilterTextControl()
        return self.__AddFilterControls()

    def __LoadFilterIcons(self):
        generatorDir = os.path.dirname(__file__)

        filterOnIconFile = os.path.join(generatorDir, 'FilterOn.png')
        filterOffIconFile = os.path.join(generatorDir, 'FilterOff.png')
        garbageIconFile = os.path.join(generatorDir, 'Garbage.png')

        # button to toggle extended filter mode
        self.__extendedFilterIcon = wx.Bitmap()
        self.__extendedFilterIcon.LoadFile(filterOnIconFile, wx.BITMAP_TYPE_PNG)
        self.__simpleFilterOffIcon = wx.Bitmap()
        self.__simpleFilterOffIcon.LoadFile(filterOffIconFile, wx.BITMAP_TYPE_PNG)
        self.__garbageIcon = wx.Bitmap()
        self.__garbageIcon.LoadFile(garbageIconFile, wx.BITMAP_TYPE_PNG)

    def _CreateFilterButtons(self):
        # button to toggle mode
        self.__btnUseExtendedMode = wx.BitmapToggleButton(self, label=self.__simpleFilterOffIcon,
                                                          size=BTN_SIZE)
        self.__btnUseExtendedMode.SetBitmapPressed(self.__extendedFilterIcon)
        self.__btnUseExtendedMode.SetMaxSize(BTN_SIZE)
        self.__btnUseExtendedMode.SetToolTip(TOOLTIP_EXTENDED_MODE)
        self.__btnUseExtendedMode.Bind(wx.EVT_BUTTON, self.__OnChangeViewModeWithButton)
        self.__btnUseExtendedMode.SetValue(self.__extendedMode)

        # button to clear filter
        self.__btn_clear_filter = wx.BitmapButton(self, bitmap=self.__garbageIcon, size=BTN_SIZE)
        self.__btn_clear_filter.SetMaxSize(BTN_SIZE)
        self.__btn_clear_filter.SetToolTip(TOOLTIP_CLEAR_FILTER)
        self.__btn_clear_filter.Bind(wx.EVT_BUTTON, self.__OnClear)

    def __CreateFilterToolBar(self):
        # toolbar with tool to toogle mode
        toolBarStyle = wx.NO_BORDER | wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_NODIVIDER
        self.__filterModeToolBar = wx.ToolBar(self, wx.ID_ANY, pos=wx.DefaultPosition,
                                              size=wx.DefaultSize,
                                              style=toolBarStyle)
        self.__filterModeToolBar.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR))
        filterModeTool = self.__filterModeToolBar.AddTool(wx.ID_ANY, '',
                                                          self.__simpleFilterOffIcon,
                                                          kind=wx.ITEM_CHECK,
                                                          shortHelp=_(TOOLTIP_EXTENDED_MODE))
        filterModeTool.Toggle(self.__extendedMode)
        self.__filterModeToolBar.Realize()
        self.Bind(wx.EVT_TOOL, self.__OnChangeFilterModeWithTool, id=filterModeTool.GetId())

        # toolbar with tool to clear filter
        self.__clearFilterToolBar = wx.ToolBar(self, wx.ID_ANY, pos=wx.DefaultPosition,
                                               size=wx.DefaultSize,
                                               style=toolBarStyle)
        self.__clearFilterToolBar.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR))
        clearTool = self.__clearFilterToolBar.AddTool(wx.ID_ANY, '',
                                                      self.__garbageIcon,
                                                      kind=wx.ITEM_NORMAL,
                                                      shortHelp=TOOLTIP_CLEAR_FILTER)
        self.__clearFilterToolBar.Realize()
        self.Bind(wx.EVT_TOOL, self.__OnClear, id=clearTool.GetId())

    def __CreateFilterTextControl(self):
        # text control to enter filter query
        self.__ctlFilterValue = wx.TextCtrl(parent=self, id=wx.NewIdRef(), name='in_filter',
                                            style=wx.TE_PROCESS_ENTER)
        self.__ctlFilterValue.SetHint(LBL_FILTER)
        self.__ctlFilterValue.Bind(wx.EVT_TEXT_ENTER, self.__OnOk)

        self.__ctlFilterValue.SetValue(self.__projectGenerator.searchCriteria)

    def __AddFilterControls(self, useToolbar=True):
        filterSizer = wx.BoxSizer(wx.HORIZONTAL)
        if useToolbar:
            self.__CreateFilterToolBar()
            filterSizer.Add(self.__filterModeToolBar, 0, flag=wx.EXPAND | wx.ALL, border=2)
            filterSizer.Add(self.__ctlFilterValue, 1, flag=wx.EXPAND | wx.ALL, border=2)
            filterSizer.Add(self.__clearFilterToolBar, 0, flag=wx.EXPAND | wx.ALL, border=2)
        else:
            self._CreateFilterButtons()
            filterSizer.Add(self.__btnUseExtendedMode, 0, flag=wx.EXPAND | wx.ALL, border=2)
            filterSizer.Add(self.__ctlFilterValue, 1, flag=wx.EXPAND | wx.ALL, border=2)
            filterSizer.Add(self.__btn_clear_filter, 0, flag=wx.EXPAND | wx.ALL, border=2)
        return filterSizer

    def __CreateDialogControls(self):
        """
        Create a sizer containing the standard dialog buttons.
        """
        btnCancel, btnOk = self.__CreateDialogButtons()
        buttonSizer = self.__AddDialogControls(btnCancel, btnOk)
        return buttonSizer

    def __CreateDialogButtons(self):
        btnOk = wx.Button(self, wx.ID_OK, label='OK', name='button_OK')
        btnOk.Bind(wx.EVT_BUTTON, self.__OnOk)
        btnCancel = wx.Button(self, wx.ID_CANCEL, label='Cancel', name='button_Cancel')
        btnCancel.Bind(wx.EVT_BUTTON, self.__OnCancel)
        return btnCancel, btnOk

    def __AddDialogControls(self, btnCancel, btnOk):
        # setup layout of dialog buttons
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.AddStretchSpacer()
        buttonSizer.Add(btnOk, flag=wx.ALL, border=2)
        buttonSizer.Add(btnCancel, flag=wx.ALL, border=2)
        return buttonSizer

    def __OnCancel(self, event):
        """
        Triggered when button Cancel is clicked.

        :param event: the triggered event
        :type event: wx.CommandEvent
        """
        self.EndModal(wx.ID_CANCEL)
        event.Skip()

    def __OnChangeViewModeWithButton(self):
        self.__extendedMode = self.__btnUseExtendedMode.GetValue()

    def __OnChangeFilterModeWithTool(self, event):
        self.__extendedMode = event.IsChecked()

    def __OnOk(self, event):
        """
        Triggered when button OK is clicked.

        :param event: the triggered event
        :type event: wx.CommandEvent
        """
        self.__projectGenerator.searchCriteria = self.__ctlFilterValue.GetValue()
        self.__projectGenerator.useExtendedMode = self.__extendedMode
        self.EndModal(wx.ID_OK)
        event.Skip()

    def __OnClear(self, event):
        """
        Triggered when button Clear is clicked.

        :param event: the triggered event
        :type event: wx.CommandEvent
        """
        self.__ctlFilterValue.Clear()
        event.Skip()
