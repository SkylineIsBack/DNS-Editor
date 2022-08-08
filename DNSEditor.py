import sys
import os
import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class Main:
    def __init__(self):

        self.homel = os.environ['HOME']

        self.check_installation()

        self.network_stuff_init()

        self.current_dns()

        self.combobox_init_stuff()

        gladefile = "/usr/share/DNSEditor/DNSEditor.ui"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)

        self.main_window = self.builder.get_object("main_window")
        self.main_window.connect("delete_event", gtk.main_quit)

        self.main_stack = self.builder.get_object("main_stack")

        self.current_dns_label = self.builder.get_object("current_dns_label")

        self.dns_added_combobox = self.builder.get_object("dns_added_combobox")
        self.dns_added_combobox.set_entry_text_column(0)
        self.dns_added_combobox.connect("changed", self.new_dns_selected)
        for dns in self.dns_to_be_selected_from:
            self.dns_added_combobox.append_text(dns)
        self.dns_added_combobox.set_active(0)

        self.add_dns_stack_btn = self.builder.get_object("add_dns_stack_btn")
        self.add_dns_stack_btn.connect("clicked", self.add_dns_stack_switcher)

        self.switch = self.builder.get_object("switch")
        self.switch.connect("notify::active", self.switchfunc)

        self.new_dns_entry = self.builder.get_object("new_dns_entry")

        self.add_new_dns_btn = self.builder.get_object("add_new_dns_btn")
        self.add_new_dns_btn.connect("clicked", self.add_new_dns_btn_clicked)

        self.cancel_btn = self.builder.get_object("cancel_btn")
        self.cancel_btn.connect("clicked", self.cancel)

        self.main_window.show()

        self.is_the_app_restarted()

    def new_dns_selected(self, dns_added_combobox):
        self.dns_chosen = dns_added_combobox.get_active_text()
        if self.dns_chosen != "Select a DNS":
            self.current_dns_label.set_text(self.dns_chosen)
            self.switch.set_active(False)
            with open(f"{self.homel}/.config/DNSEditor/state.txt", "w+") as g:
                g.write("disabled")
        else:
            self.current_dns_label.set_text("DNS")

    def add_dns_stack_switcher(self, widget):
        pages = self.main_stack.get_children()
        self.main_stack.set_visible_child(pages[1])

    def switchfunc(self, switch, gparam):
        if switch.get_active():
            if self.switch_state == "disabled":
                if self.dns_chosen != "Select a DNS":
                    subprocess.Popen(f"nmcli con mod \"{self.connected_device_name}\" ipv4.ignore-auto-dns yes && nmcli con mod \"{self.connected_device_name}\" ipv4.dns {self.dns_chosen} && nmcli con down \"{self.connected_device_name}\" && nmcli con up \"{self.connected_device_name}\"", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    with open(f"{self.homel}/.config/DNSEditor/currentDNS.txt", "w+") as h:
                        h.write(self.dns_chosen)
                    with open(f"{self.homel}/.config/DNSEditor/state.txt", "w+") as i:
                        i.write("enabled")
                else:
                    self.error_dialog(self)
                    self.switch.set_active(False)
            elif self.switch_state == "enabled":
                with open(f"{self.homel}/.config/DNSEditor/currentDNS.txt", "w+") as j:
                    j.write(self.dns_chosen)
                with open(f"{self.homel}/.config/DNSEditor/state.txt") as a:
                    self.switch_state = a.read().strip()
                if self.switch_state == "restarted":
                    if self.dns_chosen != "Select a DNS":
                        subprocess.Popen(f"nmcli con mod \"{self.connected_device_name}\" ipv4.ignore-auto-dns yes && nmcli con mod \"{self.connected_device_name}\" ipv4.dns {self.dns_chosen} && nmcli con down \"{self.connected_device_name}\" && nmcli con up \"{self.connected_device_name}\"", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                        with open(f"{self.homel}/.config/DNSEditor/currentDNS.txt", "w+") as k:
                            k.write(self.dns_chosen)
                        with open(f"{self.homel}/.config/DNSEditor/state.txt", "w+") as l:
                            l.write("enabled")
        else:
            if self.dns_chosen != "Select a DNS":
                empty_dns = '""'
                subprocess.Popen(f"nmcli con mod \"{self.connected_device_name}\" ipv4.ignore-auto-dns no && nmcli con mod \"{self.connected_device_name}\" ipv4.dns {empty_dns} && nmcli con down \"{self.connected_device_name}\" && nmcli con up \"{self.connected_device_name}\"", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                with open(f"{self.homel}/.config/DNSEditor/currentDNS.txt", "w+") as m:
                    m.write("")
                with open(f"{self.homel}/.config/DNSEditor/state.txt", "w+") as n:
                    n.write("disabled")
            else:
                print("Please select a DNS.")

    def add_new_dns_btn_clicked(self, widget):
        self.new_dns = self.new_dns_entry.get_text()
        if self.new_dns != "":
            with open(f"{self.dns_list_file_path}", f"{self.fopenmode}") as o:
                o.write(f"{self.sline}{self.new_dns}")
            self.combobox_init_stuff()
            self.dns_added_combobox.append_text(self.new_dns)
            self.new_dns_entry.set_text("")
            pages = self.main_stack.get_children()
            self.main_stack.set_visible_child(pages[0])
        else:
            dialog2 = gtk.MessageDialog(parent=self.main_window, flags=0, message_type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK, text="Missing DNS value.")
            dialog2.run()
            dialog2.destroy()

    def cancel(self, widget):
        pages = self.main_stack.get_children()
        self.main_stack.set_visible_child(pages[0])

    def combobox_init_stuff(self):
        self.dns_list_file_path = os.path.join(self.homel, ".config/DNSEditor/DNSList.txt")
        with open(self.dns_list_file_path) as f:
            self.is_list_empty = f.read()
        with open(self.dns_list_file_path) as b:
            self.dns_added = b.read().strip().split("\n")
        first_string_list = ["Select a DNS"]
        if self.is_list_empty == "":
            self.fopenmode = "w+"
            self.sline = ""
            self.dns_to_be_selected_from = first_string_list
        else:
            self.fopenmode = "a+"
            self.sline = "\n"
            self.dns_to_be_selected_from = first_string_list + self.dns_added

    def network_stuff_init(self):
        self.connected_device_name = subprocess.Popen("nmcli -t con show --active | cut -f1 -d':'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read().decode("utf-8").strip()
        with open(f"{self.homel}/.config/DNSEditor/defaultDNS.txt") as c:
            self.defult_dns = c.read().strip()

    def current_dns(self):
        with open(f"{self.homel}/.config/DNSEditor/currentDNS.txt") as d:
            self.current_dns = d.read().strip()

    def is_the_app_restarted(self):
        with open(f"{self.homel}/.config/DNSEditor/state.txt") as e:
            self.switch_state = e.read().strip()
        if self.switch_state == "enabled":
            lp = self.dns_to_be_selected_from.index(self.current_dns)
            self.dns_added_combobox.set_active(lp)
            self.switch.set_active(True)
            with open(f"{self.homel}/.config/DNSEditor/state.txt", "w+") as p:
                p.write("restarted")

    def error_dialog(self, widget):
        dialog = gtk.MessageDialog(parent=self.main_window, flags=0, message_type=gtk.MessageType.ERROR, buttons=gtk.ButtonsType.OK, text="Select a DNS to continue.")
        dialog.run()
        dialog.destroy()

    def check_installation(self):
        self.flocation = f"{self.homel}/.config/DNSEditor"
        if not os.path.exists(f"{self.flocation}/defaultDNS.txt") and os.path.exists(f"{self.flocation}/state.txt"):
            print("Some necessary file(s) are not present in the folder they should be.")
            print("Try re-installing the app or create the files manually.")
            sys.exit()

if __name__ == '__main__':
    main = Main()
    gtk.main()