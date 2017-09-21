#!/usr/bin/env python

import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

from utilities import preferences as prefs


class PrefEntry(Gtk.Entry):
    def __init__(self, section, option, default_value=''):
        Gtk.Entry.__init__(self)

        self.section = section
        self.option = option
        self.default_value = default_value

        self.connect('focus-out-event', self.on_focus_out)
        self.connect('key-press-event', self.on_key_press)
        self.connect('activate', self.on_activate)

        self.value = prefs.get(self.section, self.option, self.default_value, str)
        self.set_text(str(self.value))

    def on_activate(self, widget):
        self.set_preference()

    def on_focus_out(self, widget, data=None):
        self.set_preference()

    def on_key_press(self, widget, event, data=None):
        if event.keyval == Gdk.KEY_Escape:
            self.set_text(self.value) # Revert
            self.get_toplevel().set_focus(None)

    def set_preference(self):
        self.value = self.get_text()
        prefs.set(self.section, self.option, self.value, str)
        self.select_region(0, 0)
        self.get_toplevel().set_focus(None)


class PrefComboBox(Gtk.ComboBox):
    def __init__(self, section, option, items=[], default_item=None):
        Gtk.ComboBox.__init__(self)

        self.section = section
        self.option = option
        self.items = items
        self.default_item = default_item

        self.model = Gtk.ListStore(str)
        self.set_model(self.model)

        for item in self.items:
            self.model.append([item])

        renderer_text = Gtk.CellRendererText()
        self.pack_start(renderer_text, True)
        self.add_attribute(renderer_text, "text", 0)

        self.item = prefs.get(self.section, self.option, self.default_item, str)
        self.set_selected(self.item)

        self.connect("changed", self.on_selection_changed)

    def set_selected(self, item):
        for row in range(len(self.model)):
            if self.model[row][0] == item:
                self.set_active_iter(self.model.get_iter(row))
                break

    def on_selection_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter != None:
            self.value = self.model[tree_iter][0]
            prefs.set(self.section, self.option, self.value)


class PrefCheckButton(Gtk.CheckButton):
    def __init__(self, section, option, default_value=False):
        Gtk.CheckButton.__init__(self)

        self.section = section
        self.option = option
        self.default_value = default_value

        self.connect('toggled', self.on_toggle)

        self.value = prefs.get(self.section, self.option, self.default_value, bool)
        self.set_active(self.value)

    def on_toggle(self, widget):
        self.value = self.get_active()
        prefs.set(self.section, self.option, self.value)


class PrefSwitch(Gtk.Switch):
    def __init__(self, section, option, default_value=False):
        Gtk.Switch.__init__(self)

        self.section = section
        self.option = option
        self.default_value = default_value

        self.connect('state-set', self.on_state_set)

        self.value = prefs.get(self.section, self.option, self.default_value, bool)
        self.set_active(self.value)

    def on_state_set(self, widget, event):
        self.value = self.get_state()
        prefs.set(self.section, self.option, self.value)


class PrefFeild(Gtk.Box):
    def __init__(self, feild, group):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label(feild.option)
        self.pack_start(label, True, True, 0)
        self.pack_start(feild, True, True, 0)
        group.add_widget(label)
        group.add_widget(feild)
