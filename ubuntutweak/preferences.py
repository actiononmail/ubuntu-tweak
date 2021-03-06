# Ubuntu Tweak - PyGTK based desktop configuration tool
# coding: utf-8
# Copyright (C) 2007-2008 TualatriX <tualatrix@gmail.com>
#
# Ubuntu Tweak is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ubuntu Tweak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ubuntu Tweak; if not, write to the Free Software Foundation, Inc.,

import os
import gtk
import gobject

from ubuntutweak.common.consts import *
from ubuntutweak.common.gui import GuiWorker
from ubuntutweak.common.config import TweakSettings
from ubuntutweak.common.utils import set_label_for_stock_button
from ubuntutweak.common.factory import WidgetFactory

class PreferencesDialog:
    def __init__(self):
        self.worker = GuiWorker('preferences.ui')
        self.dialog = self.worker.get_object('preferences_dialog')

        self.setup_window_preference()
        self.setup_launch_function()
        self.setup_other_features()

    def setup_window_preference(self):
        table = self.worker.get_object('table1')

        win_width = WidgetFactory.create('GconfSpinButton',
                                        key='window_width', 
                                        min=640, max=1280, step=1)
        win_width.show()
        win_width.connect('value-changed', self.on_value_changed)
        table.attach(win_width, 1, 3, 0, 1)

        win_height = WidgetFactory.create('GconfSpinButton',
                                          key='window_height', 
                                          min=480, max=1280, step=1)
        win_height.show()
        win_height.connect('value-changed', self.on_value_changed)
        table.attach(win_height, 1, 3, 1, 2)

        toolbar_size = WidgetFactory.create('GconfSpinButton',
                                            key='toolbar_size',
                                            min=100, max=500, step=1)
        toolbar_size.show()
        toolbar_size.connect('value-changed', self.on_value_changed)
        table.attach(toolbar_size, 1, 3, 2, 3)

    def setup_launch_function(self):
        from ubuntutweak.mainwindow import MLOADER
        from ubuntutweak.mainwindow import MainWindow as MW
        function_box = self.worker.get_object('function_box')

        model = gtk.ListStore(
                gobject.TYPE_STRING,
                gtk.gdk.Pixbuf,
                gobject.TYPE_STRING)

        iter = model.append(None)
        model.set(iter,
                MW.ID_COLUMN, 0,
                MW.LOGO_COLUMN, None,
                MW.TITLE_COLUMN, _('None')
        )
        for module in MLOADER.get_all_module():
            iter = model.append(None)
            pixbuf = MLOADER.get_pixbuf(module.__name__)

            model.set(iter,
                    MW.ID_COLUMN, module.__name__,
                    MW.LOGO_COLUMN, pixbuf,
                    MW.TITLE_COLUMN, module.__title__,
            )

        function_box.set_model(model)
        textcell = gtk.CellRendererText()
        pixbufcell = gtk.CellRendererPixbuf()
        function_box.pack_start(pixbufcell, False)
        function_box.pack_start(textcell, True)
        function_box.add_attribute(textcell, 'text', MW.TITLE_COLUMN)
        function_box.add_attribute(pixbufcell, 'pixbuf', MW.LOGO_COLUMN)
        id = TweakSettings.get_default_launch()
        for i, row in enumerate(model):
            _id = model.get_value(row.iter, MW.ID_COLUMN)
            if id == _id:
                function_box.set_active(i)
        function_box.connect('changed', self.on_launch_changed)

    def setup_other_features(self):
        vbox = self.worker.get_object('vbox5')

        button = WidgetFactory.create('GconfCheckButton', 
                                      label=_('Enable Check Update'), 
                                      key='check_update',
                                      default=False)
        vbox.pack_start(button, False, False, 0)

        button = WidgetFactory.create('GconfCheckButton', 
                                      label=_('Use Separated Sources'), 
                                      key='separated_sources',
                                      default=True)
        vbox.pack_start(button, False, False, 0)

        button = WidgetFactory.create('GconfCheckButton', 
                                      label = _('Enable the synchronous notification'),
                                      key='sync_notify',
                                      default=True)
        vbox.pack_start(button, False, False, 0)

        if os.getenv('LANG').startswith('zh_CN'):
            button = WidgetFactory.create('GconfCheckButton',
                                          label='使用PPA镜像（如果可用）',
                                          key='use_mirror_ppa',
                                          default=False)
            vbox.pack_start(button, False, False, 0)

        vbox.show_all()

    def on_launch_changed(self, widget, data=None):
        index = widget.get_active()
        liststore = widget.get_model()
        iter = liststore.get_iter(index)
        id = liststore.get_value(iter, 0)
        TweakSettings.set_default_launch(id)

    def on_value_changed(self, widget):
        TweakSettings.need_save = False

    def run(self):
        self.dialog.run()

    def destroy(self):
        self.dialog.destroy()
