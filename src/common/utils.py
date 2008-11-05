import gtk
from gnome import ui

__all__ = (
    'set_label_for_stock_button',
    'get_icon_with_type',
    'get_icon_with_app',
    'get_icon_with_cate',
    'get_icon_with_name',
)

icontheme = gtk.icon_theme_get_default()

def set_label_for_stock_button(button, text):
    label = button.get_child().get_child().get_children()[1]
    label.set_text(text)

def get_icon_with_type(filepath, size):
    icon = ui.icon_lookup(icontheme, None, filepath)

    pixbuf = icontheme.load_icon(icon[0], size, 0)

    if pixbuf.get_height() != size:
        return pixbuf.scale_simple(24, 24, gtk.gdk.INTERP_BILINEAR)
    
    return pixbuf

def get_icon_with_app(app, size):
    pass

def get_icon_with_cate(cate, size):
    pass

def get_icon_with_name(name, size):
    try:
        pixbuf = icontheme.load_icon(name, size, 0)
    except:
        pixbuf = icontheme.load_icon('binary', size, 0)

    if pixbuf.get_height() != size:
        return pixbuf.scale_simple(24, 24, gtk.gdk.INTERP_BILINEAR)

    return pixbuf

if __name__ == '__main__':
    print get_icon_with_type('/home/tualatrixx', 24)
    print get_icon_with_name('start-here', 24)