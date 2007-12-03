import pygtk
pygtk.require("2.0")
import gtk
import os
import gconf
import gettext

from Widgets import GConfCheckButton, ItemBox

gettext.install("ubuntu-tweak", unicode = True)

class Session(gtk.VBox):
	"""GNOME Session control"""
	def change_splash_cb(self, widget, data = None):
		dialog = gtk.FileChooserDialog(_("Choose a Splash image"),action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_OPEN, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		filter = gtk.FileFilter()
		filter.set_name(_("PNG image (*.png)"))
		filter.add_mime_type("image/png")
		dialog.set_current_folder(self.filedir)
		dialog.add_filter(filter)

		if dialog.run() == gtk.RESPONSE_ACCEPT:
			client = gconf.client_get_default()
			filename = dialog.get_filename()
			data.set_text(filename)
			original_preview = gtk.gdk.pixbuf_new_from_file(filename)
			x = original_preview.get_width()
			y = original_preview.get_height()

			new_preview = original_preview.scale_simple(x / 2, y / 2, gtk.gdk.INTERP_NEAREST)
			client.set_string("/apps/gnome-session/options/splash_image", filename)
		dialog.destroy()

	def show_splash_toggled(self, widget, data = None):
                client = gconf.client_get_default()
                if widget.get_active():
                        client.set_bool("/apps/gnome-session/options/show_splash_screen", True)
			self.button.set_sensitive(True)
                else:
                        client.set_bool("/apps/gnome-session/options/show_splash_screen", False)
			self.button.set_sensitive(False)

	def splash_hbox(self):
		client = gconf.client_get_default()
		filename = client.get_string("/apps/gnome-session/options/splash_image")
		self.filedir = os.path.dirname(filename)
		try:
			f = open(filename)
		except IOError:
			filename = "/usr/share/pixmaps/splash/gnome-splash.png"
			client.set_string("/apps/gnome-session/options/splash_image", "/usr/share/pixmaps/splash/gnome-splash.png")

		original_preview = gtk.gdk.pixbuf_new_from_file(filename)
		x = original_preview.get_width()
		y = original_preview.get_height()

		if x * 150 / y > 200:
			y = y * 200 / x
			x = 200
		else:
			x = x * 150 / y
			y = 150

		new_preview = original_preview.scale_simple(x, y, gtk.gdk.INTERP_NEAREST)
		hbox = gtk.HBox(False, 0)
		self.button = gtk.Button()
		hbox.pack_start(self.button, True, False, 0)

		if client.get_bool("/apps/gnome-session/options/show_splash_screen"):
			self.button.set_sensitive(True)
		else:
			self.button.set_sensitive(False)

		vbox = gtk.VBox(False, 2)
		self.button.add(vbox)

		alignment = gtk.Alignment(0.5, 0.5, 1, 1)
		alignment.set_size_request(200, 150)
		vbox.pack_start(alignment, False, False, 0)

		image = gtk.image_new_from_pixbuf(new_preview)
		alignment.add(image)

		label = gtk.Label(filename)
		vbox.pack_end(label, False, False, 0)

		self.button.connect("clicked", self.change_splash_cb, label)

		return hbox

	def session_control_box(self):
		button = GConfCheckButton(_("Automatically save changes to session"), "/apps/gnome-session/options/auto_save_session") 
		button2 = GConfCheckButton(_("Show Logout prompt"), "/apps/gnome-session/options/logout_prompt")
		button3 = GConfCheckButton(_("Allow TCP Connections(Remote Connect)"), "/apps/gnome-session/options/allow_tcp_connections")
		button4 = GConfCheckButton(_("Show Splash screen"), "/apps/gnome-session/options/show_splash_screen", extra = self.show_splash_toggled)

		box = ItemBox(_("<b>Session Control</b>"), (button, button2, button3, button4))
		return box

	def __init__(self):
		gtk.VBox.__init__(self)

#		main_vbox = gtk.VBox(False, 5)
#		main_vbox.set_border_width(5)
#		self.pack_start(main_vbox, False, False, 0)

		self.pack_start(self.session_control_box(), False, False, 0)

		box = ItemBox(_("<b>Click the large button to change Splash screen</b>"), (self.splash_hbox(),))
		self.pack_start(box, False, False, 0)