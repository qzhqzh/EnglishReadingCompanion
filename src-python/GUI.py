from extract_words import extract_words
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, Gdk, WebKit


class MainWindow(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.AUTHEN_CODE = None  # authentication code for API of Shanbay.com
        self.set_title('English Reading Companion')
        self.set_default_size(800, 600)
        self.set_border_width(10)
        self.connect('delete-event', self.quit)
        self.connect('key-press-event', self.on_key_click)

        # Left List
        self.wl_store = Gtk.ListStore(str)
        self.wl_treeview = Gtk.TreeView(model=self.wl_store)
        self.wl_column = Gtk.TreeViewColumn('New [%d]' % len(self.wl_store), Gtk.CellRendererText(), text=0)
        self.wl_treeview.append_column(self.wl_column)
        self.wl_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wl_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        wl_scrolled_window = Gtk.ScrolledWindow()
        wl_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        wl_scrolled_window.add(self.wl_treeview)

        # Middle List
        self.wm_store = Gtk.ListStore(str)
        try:
            with open('undetermined_words.dat', 'r') as f:
                for line in f:
                    self.wm_store.append([line.strip()])
        except FileNotFoundError:
            pass
        self.wm_treeview = Gtk.TreeView(model=self.wm_store)
        self.wm_column = Gtk.TreeViewColumn('Undertermined [%d]' % len(self.wm_store), Gtk.CellRendererText(), text=0)
        self.wm_treeview.append_column(self.wm_column)
        self.wm_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wm_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        wm_scrolled_window = Gtk.ScrolledWindow()
        wm_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        wm_scrolled_window.add(self.wm_treeview)

        # Right List
        self.wr_store = Gtk.ListStore(str)
        self.wr_treeview = Gtk.TreeView(model=self.wr_store)
        self.wr_column = Gtk.TreeViewColumn('Mastered [%d]' % len(self.wr_store), Gtk.CellRendererText(), text=0)
        self.wr_treeview.append_column(self.wr_column)
        self.wr_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wr_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        wr_scrolled_window = Gtk.ScrolledWindow()
        wr_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        wr_scrolled_window.add(self.wr_treeview)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        # Left Part
        l_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        push_btn = Gtk.Button(label='Push To Shanbay.com')
        push_btn.connect('clicked', self.push_to_shanbay)
        l_box.pack_start(wl_scrolled_window, True, True, 0)
        l_box.pack_start(push_btn, False, False, 0)

        box_outer.pack_start(l_box, True, True, 0)

        # Middle Part
        m_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        m_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        left_btn = Gtk.Button()
        left_btn.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        left_btn.connect('clicked', self.word_move_left)

        right_btn = Gtk.Button()
        right_btn.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        right_btn.connect('clicked', self.word_move_right)

        m_btn_box.pack_start(left_btn, True, True, 0)
        m_btn_box.pack_start(right_btn, True, True, 0)

        import_btn = Gtk.Button(label='Import Words')
        import_btn.connect('clicked', self.import_words)
        m_box.pack_start(wm_scrolled_window, True, True, 0)
        m_box.pack_start(m_btn_box, False, False, 0)
        m_box.pack_start(import_btn, False, False, 0)

        box_outer.pack_start(m_box, True, True, 0)

        # Right Part
        r_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        save_btn = Gtk.Button(label='Save To File & Clear')
        save_btn.connect('clicked', self.save_to_file)
        r_box.pack_start(wr_scrolled_window, True, True, 0)
        r_box.pack_start(save_btn, False, False, 0)
        box_outer.pack_start(r_box, True, True, 0)

        self.add(box_outer)
        self.show_all()

    def word_move_left(self, *args):
        selection = self.wm_treeview.get_selection()
        model, paths = selection.get_selected_rows()

        for path in paths:
            self.wl_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wl_treeview.set_cursor(Gtk.TreePath(0))
        self.wl_column.set_title('New [%d]' % len(self.wl_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def word_move_right(self, *args):
        selection = self.wm_treeview.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            self.wr_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wr_treeview.set_cursor(Gtk.TreePath(0))
        self.wr_column.set_title('Mastered [%d]' % len(self.wr_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def move_right_back(self, widget):
        model, paths = self.wr_treeview.get_selection().get_selected_rows()
        for path in paths:
            self.wm_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wm_treeview.set_cursor(Gtk.TreePath(0))
        self.wr_column.set_title('Mastered [%d]' % len(self.wr_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def move_left_back(self, widget):
        model, paths = self.wl_treeview.get_selection().get_selected_rows()
        for path in paths:
            self.wm_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wm_treeview.set_cursor(Gtk.TreePath(0))
        self.wl_column.set_title('New [%d]' % len(self.wl_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def save_to_file(self, widget):
        words_to_save = [row[:][0] for row in self.wr_store]
        if len(words_to_save) > 0:
            with open('known_words.dat', 'a') as f:
                f.write('\n'.join(words_to_save) + '\n')
        self.wr_store.clear()
        self.wr_column.set_title('Mastered [%d]' % len(self.wr_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def push_to_shanbay(self, widget):
        if self.AUTHEN_CODE is None:
            self.AUTHEN_CODE = self.authenticate(self)
        if self.AUTHEN_CODE is None:
            return
        words_to_push = [row[:][0] for row in self.wl_store]
        if len(words_to_push) > 0:
            with open('learning_words.dat', 'a') as f:
                f.write('\n'.join(words_to_push) + '\n')
        self.wl_store.clear()
        self.wl_column.set_title('New [%d]' % len(self.wl_store))
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def import_words(self, widget):
        words_in_window = set([row[:][0] for row in self.wl_store] +
                              [row[:][0] for row in self.wm_store] +
                              [row[:][0] for row in self.wr_store])
        dialog = Gtk.FileChooserDialog("Select file to be opened", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.show()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            words = extract_words(dialog.get_filename(), words_in_window)
        elif response == Gtk.ResponseType.CANCEL:
            words = []
        dialog.destroy()
        for word in words:
            self.wm_store.append([word])
        self.wm_column.set_title('Undetermined [%d]' % len(self.wm_store))

    def on_key_click(self, widget, ev):
        ctrl = ev.state & Gdk.ModifierType.CONTROL_MASK

        if ctrl:
            if ev.keyval == Gdk.KEY_Left:
                self.move_right_back(widget)
            elif ev.keyval == Gdk.KEY_Right:
                self.move_left_back(widget)
            else:
                pass
        else:
            if ev.keyval == Gdk.KEY_Left:
                self.word_move_left(widget)
            elif ev.keyval == Gdk.KEY_Right:
                self.word_move_right(widget)
            else:
                pass

    def _javascript_console_message(self, view, message, line, sourceid):
        return True  # True prevents calling original handler

    def authenticate(self, *args, **kwargs):
        dialog = Gtk.Dialog("Authenticate", self, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        dialog.set_default_size(800, 600)
        box = dialog.get_content_area()
        box.set_homogeneous(False)

        webview = WebKit.WebView()
        webview.connect("console-message", self._javascript_console_message)
        webview.load_uri("https://api.shanbay.com/oauth2/authorize/?cliend_id=05623ce286a180e4e8c1&response_type=code&state=123")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(webview)
        scrolled_window.set_size_request(750, 650)
        box.add(scrolled_window)
        dialog.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            uri = webview.get_uri()
        elif response == Gtk.ResponseType.CANCEL:
            uri = None
        dialog.destroy()
        self.AUTHEN_CODE = uri

    def quit(self, *args, **kwargs):
        with open('undetermined_words.dat', 'w') as f:
            f.write('\n'.join([row[:][0] for row in self.wm_store]))
        Gtk.main_quit(self, *args, **kwargs)


win = MainWindow()
Gtk.main()
