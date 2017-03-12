import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

words1 = 'It would be very worrying if you were talking to the Queen and saw the handbag move from one hand to the other'
words2 = 'royal historian Hugo Vickers told People You see this is a signal the Queen uses to indicate to her staff that she ready to wrap up her current conversation'
words3 = 'According to the Telegraph if she puts her handbag on the table at dinner it means she wants the event to end in the next five minutes'

words1 = set(words1.lower().split(' '))
words2 = set(words2.lower().split(' '))
words3 = set(words3.lower().split(' '))


class MyWindow(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title='My Window Title')
        self.set_title('English Reading Companion')
        self.set_default_size(800, 600)
        self.set_border_width(10)
        self.connect('delete-event', Gtk.main_quit)
        self.connect('key-press-event', self.on_key_click)
        accel = Gtk.AccelGroup()      
        
        ## Left List
        self.wl_store = Gtk.ListStore(str)
        self.wl_treeview = Gtk.TreeView(model=self.wl_store)
        self.wl_treeview.append_column(Gtk.TreeViewColumn('New',
                                                          Gtk.CellRendererText(), text=0))
        self.wl_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wl_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        self.wl_scrolled_window = Gtk.ScrolledWindow()
        self.wl_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wl_scrolled_window.add(self.wl_treeview)

        
        ## Middle List
        self.wm_store = Gtk.ListStore(str)
        self.wm_treeview = Gtk.TreeView(model=self.wm_store)

        self.wm_treeview.append_column(Gtk.TreeViewColumn('Undertermined',
                                                          Gtk.CellRendererText(), text=0))
        self.wm_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wm_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        self.wm_scrolled_window = Gtk.ScrolledWindow()
        self.wm_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wm_scrolled_window.add(self.wm_treeview)

        
        ## Right List
        self.wr_store = Gtk.ListStore(str)
        self.wr_treeview = Gtk.TreeView(model=self.wr_store)
        self.wr_treeview.append_column(Gtk.TreeViewColumn('Mastered',
                                                          Gtk.CellRendererText(), text=0))
        self.wr_treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
        self.wr_treeview.override_background_color(Gtk.StateType.NORMAL,
                                                   Gdk.RGBA.from_color(Gdk.color_parse('CadetBlue3')))

        self.wr_scrolled_window = Gtk.ScrolledWindow()
        self.wr_scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.wr_scrolled_window.add(self.wr_treeview)


        box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        ## Left Part
        l_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        push_btn = Gtk.Button(label='Push To Shanbay.com')
        push_btn.connect('clicked', self.push_to_shanbay)
        l_box.pack_start(self.wl_scrolled_window, True, True, 0)
        l_box.pack_start(push_btn, False, False, 0)

        box_outer.pack_start(l_box, True, True, 0)

        ## Middle Part
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
        m_box.pack_start(self.wm_scrolled_window, True, True, 0)
        m_box.pack_start(m_btn_box, False, False, 0)
        m_box.pack_start(import_btn, False, False, 0)

        box_outer.pack_start(m_box, True, True, 0)


        ## Right Part
        r_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        save_btn = Gtk.Button(label='Save To File & Clear')
        save_btn.connect('clicked', self.save_to_file)
        r_box.pack_start(self.wr_scrolled_window, True, True, 0)
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

    def word_move_right(self, *args):
        selection = self.wm_treeview.get_selection()
        model, paths = selection.get_selected_rows()
        for path in paths:
            self.wr_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wr_treeview.set_cursor(Gtk.TreePath(0))
    
    def move_right_back(self, widget):
        model, paths = self.wr_treeview.get_selection().get_selected_rows()
        for path in paths:
            self.wm_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wm_treeview.set_cursor(Gtk.TreePath(0))

    def move_left_back(self, widget):
        model, paths = self.wl_treeview.get_selection().get_selected_rows()
        for path in paths:
            self.wm_store.insert(0, model[path][:])
        for path in paths[::-1]:
            model.remove(model.get_iter(path))
        self.wm_treeview.set_cursor(Gtk.TreePath(0))

    def save_to_file(self, widget):
        words_to_save = [row[:][0] for row in self.wr_store]
        self.wr_store.clear()

    def push_to_shanbay(self, widget):
        words_to_push = [row[:][0] for row in self.wl_store]
        self.wl_store.clear()
    
    def import_words(self, widget):
        words_in_window = set([row[:][0] for row in self.wl_store] + 
                              [row[:][0] for row in self.wm_store] + 
                              [row[:][0] for row in self.wr_store])
        words = words1
        for word in words:
            self.wm_store.append([word])

    def on_key_click(self, widget, ev, data=None):
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

win = MyWindow()
Gtk.main()
