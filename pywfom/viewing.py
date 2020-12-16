import numpy as np
import time, cv2, json, os
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw

from pywfom import imaging
from pywfom.control import Arduino
from pywfom.file import Writer

class Main(tk.Frame):

    def __init__(self, parent, config):

        self.config = config

        # Initiate each component Class
        self.cameras = [
            imaging.DEVICES[cfg['device']](cfg) for cfg in self.config["cameras"]
        ]
        self.arduino = Arduino(self.config["arduino"])
        self.file = Writer(config=self.config["file"])

        print("Opening Viewing Frame...")

        self.root = parent
        self.root.resizable(width=False, height=False)
        self.root.bind("<Escape>", self.close)
        self.set_icon()
        self.root.title("pywfom")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.rect = None
        self.drawing = False
        self.selected_frame, self.ix, self.iy, self.x, self.y = 0,0,0,0,0
        self.offset_x, self.offset_y, self.scale = 0,0,0

        # Create widgets
        self.create_widgets()
        # Establish event bindings
        self.set_bindings()
        # Set each item on the grid
        self.set_grid()
        # Begin Updating the images
        self.update()

    def set_icon(self, name="icon"):
        photo = tk.PhotoImage(
            file = os.path.dirname(imaging.__file__)+"/lib/{0}.png".format(name)
        )
        self.root.iconphoto(False, photo)

    def set_bindings(self):
        self.canvas.bind("<Button-1>", self.set_aoi_start)
        self.canvas.bind("<ButtonRelease-1>", self.set_aoi_end)
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<Button-3>", self.reset_aoi)
        self.canvas.bind("<Button-2>", self.reset_aoi)

    def create_widgets(self):
        # Create Left Side of Frame
        self.left_side = tk.Frame(self.root)
        self.canvas = tk.Canvas(self.left_side, cursor="cross", width=1000, height=800)
        self.main_label = tk.Label(self.left_side, font=("Helvetica", 14))
        # Create Right Side of Frame
        self.right_side = tk.Frame(self.root)
        # Create empty thumnails
        self.thumnails_frame = tk.Frame(self.right_side)
        self.thumbnails, self.thumbnail_labels = [], []
        # Create thumbnails
        for cam in self.cameras:
            self.add_thumnail(cam.name)
        # Create Arduino Status
        self.arduino_frame = tk.Frame(self.right_side)
        self.arduino_status = tk.Label(self.arduino_frame, text="Arduino Status")
        self.arduino_color = tk.Button(self.arduino_frame, height=1, width=1)
        # Create File Directory
        self.dir_frame = tk.Frame(self.right_side)
        self.dir_label = tk.Label(self.dir_frame, text="Save to:", font=("Helvetica", 10, 'bold'))
        self.dir_name = tk.Label(self.dir_frame)
        self.dir_button = tk.Button(self.dir_frame, text="Browse", command=self.set_dir)
        # Create buttons
        self.btn_frame = tk.Frame(self.right_side)
        self.settings_btn = tk.Button(      self.btn_frame,
                                        text="Configure",
                                        command=self.configure)
        self.close_btn = tk.Button(     self.btn_frame,
                                        text="Quit",
                                        command=self.close)
        self.acquire_btn = tk.Button(  self.btn_frame,
                                        text="Acquire",
                                        command=self.acquire)

    def add_thumnail(self, name):
        self.thumbnails.append(tk.Label(self.thumnails_frame))
        self.thumbnail_labels.append(tk.Label(self.thumnails_frame, text=name))

    def set_grid(self):
        pad = 10
        # pack left side
        self.left_side.pack(side="left")
        self.main_label.pack()
        self.canvas.pack()
        # pack right Side
        self.right_side.pack(side="right")
        self.thumnails_frame.pack()
        # pack thumnails
        for i, cam in enumerate(self.cameras):
            self.thumbnail_labels[i].pack()
            self.thumbnails[i].pack()
        # pack arduino status
        self.arduino_frame.pack(padx=pad, pady=pad)
        self.arduino_status.pack(side="left",padx=pad, pady=pad)
        self.arduino_color.pack(side="left",padx=pad, pady=pad)
        # pack directory status
        self.dir_frame.pack(padx=pad, pady=pad)
        self.dir_label.pack(side="left",padx=pad, pady=pad)
        self.dir_name.pack(side="left",padx=pad, pady=pad)
        self.dir_button.pack(side="left",padx=pad, pady=pad)
        # pack button
        self.btn_frame.pack(padx=pad, pady=pad)
        for i, btn in enumerate([self.acquire_btn, self.settings_btn, self.close_btn]):
            btn.pack(side="right",padx=pad, pady=pad)

    def update(self):

        t = time.time()

        cam = self.cameras[self.selected_frame]

        # Create main viewing frame
        image = self.convert_frame(cam.frame, (800,1000), True)

        h, w, fr = cam.Height, cam.Width, cam.AcquisitionFrameRate

        self.main_label.config(
            text="{0} ({1}): {2}x{3}, {4} fps".format(
                cam.name,
                cam.device.title(),
                h,
                w,
                fr
            )
        )

        self.canvas.config(height=image.height(), width=image.width())
        self.canvas.create_image(0,0,image=image,anchor="nw")
        self.canvas.delete(self.rect)
        if 0 in [self.ix, self.iy, self.x, self.y]:
            pass
        else:
            self.rect = self.canvas.create_rectangle(self.ix, self.iy, self.x, self.y, fill="", outline="green")
        self.canvas.image = image

        thumbnail_size = (600/len(self.cameras), 150)

        # Create subframes
        for i, cam in enumerate(self.cameras):
            img = self.convert_frame(cam.frame, thumbnail_size, False)
            self.thumbnails[i].img = img
            self.thumbnails[i].config(image=img, borderwidth=10, relief="flat", bg="white")
            self.thumbnails[i].bind("<Button-1>",lambda event, idx=i: self.change_main_frame(event, idx))

        color = "green" if not self.arduino.ERROR else "red"
        self.arduino_color.config(background=color)
        self.dir_name.config(text=self.file.directory)

        self.thumbnails[self.selected_frame].config(borderwidth=10,relief="ridge", bg="green")

        self.root.after(1, self.update)

    def set_dir(self):
        self.file.directory = tk.filedialog.askdirectory()

    def configure(self):
        self.set_icon("configure")
        Configure(self, self.root)

    def acquire(self):

        result = tk.messagebox.askyesno("pywfom", message="Start acquistion?")

        if result:
            self.file.write(self.arduino, self.cameras)
        else:
            pass

    def close(self, event=""):
        print("Closing pywfom...")
        [cam.close() for cam in self.cameras]
        self.arduino.close()
        self.root.destroy()

    def set_aoi_start(self, event):

        self.ix = event.x
        self.iy = event.y

    def set_aoi_end(self, event):

        self.x = event.x
        self.y = event.y
        w = self.x-self.ix
        h = self.y-self.iy

        if 0 in [w,h]:
            self.ix, self.iy, self.x, self.y = 0,0,0,0
            return

        if w < 0:
            self.ix = self.x
            w = abs(w)
        if h < 0:
            self.iy = self.y
            h = abs(h)

        cam = self.cameras[self.selected_frame]

        x, y, he, wi = "OffsetX", "OffsetY", "Height", "Width"

        cam.set({
            he:int(h/self.scale),
            wi:int(w/self.scale),
            x:int(getattr(cam,x)+self.ix/self.scale),
            y:int(getattr(cam,y)+self.iy/self.scale)
        })

        self.ix, self.iy, self.x, self.y = 0,0,0,0

    def draw_rectangle(self, event):
        self.x, self.y = event.x, event.y

    def reset_aoi(self, event):
        cam = self.cameras[self.selected_frame]
        cam.set({
            "Height":cam.get_max("Height"),
            "Width":cam.get_max("Width"),
            "OffsetX":1,
            "OffsetY":1
        })

    def change_main_frame(self, event, idx):
        self.selected_frame = idx

    def convert_frame(self, frame, max_size, main):

        if frame.dtype == "uint16":
            frame = np.sqrt(frame).astype(np.uint8)
        else:
            pass

        # Create main viewing frame
        max_dim = max(frame.shape[0], frame.shape[1])
        if max_dim < max_size[0]:
            scale = max_size[0]/max_dim
        elif max_dim > max_size[1]:
            scale = max_size[1]/max_dim
        else:
            scale = 1

        w, h = int(scale*frame.shape[0]), int(scale*frame.shape[1])

        if main:
            self.scale = scale

        img = ImageTk.PhotoImage(image = Image.fromarray(frame).resize((h, w)))

        return img

class Configure(tk.Toplevel):

    def __init__(self, parent=None, master=None):

        super().__init__(master = master)

        # Establish root + configuration
        self.parent = parent
        self.root = parent.root
        self.config = parent.config
        self.title("Configure WFOM")
        self.focus_force()

        self.buttons = [
            {
                "name":"LEDs",
                "command":self._leds,
                "widget":None
            },
            {
                "name":"Stim",
                "command":self._stim,
                "widget":None
            },
            {
                "name":"Edit Settings",
                "command":self._settings,
                "widget":None
            },
            {
                "name":"Done",
                "command":self._close,
                "widget":None
            },

        ]

        # Populate and organize window
        self._create_widgets()
        self._pack_widgets()

    def _create_widgets(self):
        for btn in self.buttons:
            btn['widget'] = tk.Button(self, text=btn['name'], command=btn['command'])

    def _pack_widgets(self):
        [btn['widget'].pack(pady=10) for btn in self.buttons]

    def _leds(self):
        print(self.parent.arduino.ERROR)
        LedConfig(self, self.root)

    def _stim(self):
        StimConfig(self, self.root)

    def _settings(self):
        SettingsConfig(self, self.root)

    def _close(self, event=None):
        self.parent.set_icon()
        self.destroy()

class SettingsConfig(tk.Toplevel):

    def __init__(self, parent=None, master=None):

        super().__init__(master = master)
        # TODO: Catch arduino error better
        self.ignore = [
            "_pointers",
            "settings",
            "methods",
            "system",
            "active",
            "camera",
            "frame",
            "default",
            "ser",
            "writing"
        ]

        # Get parent window, config settings, and types
        self.parent = parent
        self.cameras = parent.parent.cameras
        self.arduino = parent.parent.arduino
        self.file = parent.parent.file
        self.resizable(width=False, height=False)
        self.root = parent.root

        # Store initial settings in case of reset
        self.init_cameras = [cam.__dict__.copy() for cam in self.cameras]
        self.init_arduino = self.arduino.__dict__.copy()

        # Create Treeview
        self.tree = ttk.Treeview(self, columns=["A", "B"])
        self.tree.column("#0", width=90, anchor='center')
        self.tree.column("A", width=70, anchor='center')
        self.tree.column("B", width=50, anchor='center')
        self.tree.pack()
        self.title("Settings")

        # Add ability to edit
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.right_click)
        self.tree.bind("<Button-2>", self.right_click)

        self.populate_tree()

        self.create_buttons()

    def populate_tree(self):

        # Clear previous settings from the tree
        self.tree.delete(*self.tree.get_children())

        # Create tree branch for file info
        file = self.tree.insert("", 0, text="File")
        for i, values in enumerate(self.file.__dict__.items()):
            self.tree.insert(file,i, values=values)

        # Create Cameras tab
        cameras = self.tree.insert("", 1, text="Cameras")
        # Create tabs for each camera
        for i, cam in enumerate(self.cameras):
            cam_settings = {}
            parent = self.tree.insert(cameras, i, text=cam.name.title())
            # Add setting for each attribute
            for j, attr in enumerate(cam.__dict__.keys()):
                if attr in self.ignore:
                    continue
                else:
                    self.tree.insert(parent, j, values=(attr, getattr(cam, attr)))

        # Create Arduino Tab
        arduino = self.tree.insert("", 2, text="Arduino")
        # Go through each Arduino attribute
        for i, attr in enumerate(self.arduino.__dict__.keys()):
            if attr in self.ignore:
                continue
            elif attr == "ERROR":
                if not self.arduino.ERROR:
                    continue
                else:
                    self.tree.insert(arduino, i, text=self.arduino.ERROR)
            parent = self.tree.insert(arduino, i, text=attr)
            settings = getattr(self.arduino, attr)
            if attr == "port":
                self.tree.insert(parent, i, values=("Port", self.arduino.port))
            elif attr == "strobing":
                self.tree.insert(parent, 0, values=("Trigger", settings['trigger']))
                for j, led in enumerate(settings['leds']):
                    self.tree.insert(parent, j+1, values=(led["name"], led["pin"]))
            elif attr == "stim":
                for k, stim in enumerate(settings):
                    stim_parent = self.tree.insert(parent, k, text=stim["name"])
                    for m, setting in enumerate(stim):
                        self.tree.insert(stim_parent, m, values=(setting, stim[setting]))

    def create_buttons(self):
        reset = tk.Button(self, text="Reset", command=self.reset)
        save = tk.Button(self, text="Save", command=self.save)
        load = tk.Button(self, text="Load", command=self.load)
        cancel = tk.Button(self, text="Done", command=self.close)

        for i, btn in enumerate([cancel, reset, save, load]):
            btn.pack(side='right',pady=10, padx=10)

    def leds(self):
        LedConfig(self, self.root)

    def close(self):
        self.destroy()

    def save(self):

        f = filedialog.asksaveasfile(mode="w", parent=self, defaultextension=".json")
        if f is None:
            return
        json.dump(self.settings, f)
        f.close()

    def load(self):

        fname = filedialog.askopenfilename(parent=self)
        if fname == "":
            return
        with open(fname) as f:
            settings = json.load(f)
        f.close()

        self.settings = settings
        self.populate_tree()

    def reset(self):
        [self.cameras[i].set(settings) for i, settings in enumerate(self.init_cameras)]
        self.arduino.set(self.init_arduino)
        self.populate_tree()

    def on_double_click(self, event):

        item = self.tree.selection()[0]
        if not self.tree.parent(item) or self.tree.item(item)["text"] != "":
            return
        else:
            parent = self.tree.parent(item)
            self.edit_setting(item, parent)

    def right_click(self, event):

        # TODO: Focus on right clicked row

        item = self.tree.identify_row(event.y)
        parent = self.tree.parent(item)
        menu = tk.Menu(self.root, tearoff=0)

        if self.tree.item(item)['text'] in ["Arduino", "File"]:
            return
        elif "Cameras" == self.tree.item(parent)['text']:
            menu.add_command(label="Add Camera", command=lambda:self.add_setting(item, parent))
            menu.add_command(label="Delete Camera", command=lambda:self.delete_setting(item, parent))
        elif "Cameras" == self.tree.item(item)['text']:
            menu.add_command(label="Add Camera", command=lambda:self.add_setting(item, parent))
        elif "Stim" == self.tree.item(parent)['text']:
            menu.add_command(label="Add Stim", command=lambda:self.add_setting(item, parent))
            menu.add_command(label="Delete Stim", command=lambda:self.delete_setting(item, parent))
        elif "Stim" == self.tree.item(item)['text']:
            menu.add_command(label="Add Stim", command=lambda:self.add_setting(item, parent))
        elif "Strobing" == self.tree.item(parent)['text'] and "Trigger" != self.tree.item(item)['values'][0]:
            menu.add_command(label="Add LED", command=lambda:self.add_setting(item, parent))
            menu.add_command(label="Delete LED", command=lambda:self.delete_setting(item, parent))
        elif "Strobing" == self.tree.item(item)['text']:
            menu.add_command(label="Add LED", command=lambda:self.add_setting(item, parent))
        else:
            menu.add_command(label="Edit", command=lambda:self.edit_setting(item, parent))

        menu.tk_popup(event.x_root, event.y_root)

    def edit_setting(self, item_iid, parent_iid):

        parent = self.tree.item(parent_iid)['text']
        category = self.tree.item(self.tree.parent(parent_iid))['text']
        setting = self.tree.item(item_iid)['values'][0].lower()

        idx = self.tree.get_children(self.tree.parent(parent_iid)).index(parent_iid)

        new_value = None

        if setting in ["device", "master", "dtype", "port"]:
            combo = ComboboxSelectionWindow(self, self.root, setting)
            self.root.wait_window(combo)
            new_value = combo.value

        elif setting == "directory":
            new_value = tk.filedialog.askdirectory()

        elif setting in ["user", "mouse", "name"]:
            new_value = simpledialog.askstring(
                parent=self,
                title="Setting {0}:".format(setting),
                prompt=setting
            )
        elif setting in ["Height", "index", "Width", "OffsetX", "OffsetY", "runs", "pin", "trigger"]:
            new_value = simpledialog.askinteger(
                parent=self,
                title="Setting {0}:".format(setting),
                prompt=setting
            )
        elif setting in ["AcquisitionFrameRate", "pre_stim", "stim", "post_stim", "run_length"]:
            new_value = simpledialog.askfloat(
                parent=self,
                title="Setting {0}:".format(setting),
                prompt=setting
            )
        elif parent == "Strobing" and setting != "trigger":
            name = simpledialog.askstring(
                parent=self,
                title="Strobe LED",
                prompt="Choose a name for the LED:"
            )
            pin = simpledialog.askinteger(
                parent=self,
                title="Strobe LED",
                prompt="Choose a Pin on the Arduino:"
            )
            new_value = {"name":name,"pin":pin}


        if new_value == None:
            return

        for i, child_iid in enumerate(self.tree.get_children(parent_iid)):
            if child_iid == item_iid:
                self.tree.delete(item_iid)
                item = self.tree.insert(parent_iid, i, values=(setting, new_value))
                self.tree.see(item)
                cat = self.tree.item(self.tree.parent(parent_iid))['text'].lower()
                if cat == "arduino":
                    self.arduino.set(setting, new_value)
                else:
                    if setting == "device":
                        # Close current device and open a new one
                        self.cameras[idx].close()
                        self.cameras[idx] = imaging.DEVICES[new_value](self.cameras[idx])
                    else:
                        self.cameras[idx].set(setting, new_value)

    def add_setting(self, item_iid, parent_iid):

        cat = [self.tree.item(parent_iid)['text'], self.tree.item(item_iid)['text']]

        if "Cameras" in cat:
            self.cameras.append(imaging.Camera())
            self.parent.add_thumnail("default")
        elif "Stim" in cat:
            stims = getattr(self.arduino, 'stim')
            self.arduino.stim.append({
                "name":"default",
                "pre_stim":4.0,
                "stim":7.0,
                "post_stim":8.0
            })
        elif "Strobing" in cat:
            name = simpledialog.askstring(
                parent=self,
                title="Strobe LED",
                prompt="Choose a name for the LED:"
            )
            pin = simpledialog.askinteger(
                parent=self,
                title="Strobe LED",
                prompt="Choose a Pin on the Arduino:"
            )
            strobing = getattr(self.arduino, 'strobing')
            strobing["leds"].append({
                "name":name,
                "pin":pin
            })

        self.parent.set_grid()
        self.populate_tree()

    def delete_setting(self, item_iid, parent_iid):

        if len(self.tree.get_children(self.tree.parent(item_iid))) == 1:
            return

        idx = self.tree.get_children(self.tree.parent(item_iid)).index(item_iid)
        cat = [self.tree.item(parent_iid)['text'], self.tree.item(item_iid)['text']]

        if "Cameras" in cat:
            self.cameras.pop(idx).close()
            self.parent.thumbnails.pop(idx).grid_forget()
            self.parent.thumbnail_labels.pop(idx).grid_forget()
            self.parent.selected_frame = 0
        elif "Stim" in cat:
            stims = getattr(self.arduino, 'stim')
            stims.pop(idx)
        elif "Strobing" in cat:
            strobing = getattr(self.arduino, 'strobing')
            strobing['leds'].pop(idx-1)

        self.populate_tree()

class LedConfig(tk.Toplevel):

    def __init__(self, parent=None, master=None):

        super().__init__(master = master)

        self.resizable(width=False, height=False)
        self.root = parent.root
        self.arduino = parent.parent.arduino
        self.title("LED Configuration")

        self.make_notice()
        self.make_buttons()

    def make_notice(self):
        lbl = tk.Label(
            master=self,
            text="1. Switch your LED drivers to\n'Constant Current (CM)' Mode"
        )
        pic = os.path.dirname(imaging.__file__)+"/lib/driverDemo.png"
        img = ImageTk.PhotoImage(Image.open(pic))
        panel = tk.Label(master=self, image=img)
        panel.image = img

        lbl.pack()
        panel.pack()

    def make_buttons(self):
        lbl = tk.Label(
            master=self,
            text="2. Select an LED"
        )
        lbl.pack()
        for i, led in enumerate(self.arduino.strobing['leds']):
            btn = tk.Button(
                master=self,
                text=led['name'],
                command=lambda p=led['pin'] :self.arduino.toggle_led(p),
                height=3,
                width=20
            )
            btn.pack(pady=10)

class StimConfig(tk.Toplevel):

    def __init__(self, parent=None, master=None):

        super().__init__(master = master)
        self.resizable(width=False, height=False)
        self.root = parent.root
        self.arduino = parent.arduino
        self.title("Stim Configuration")

        self.make_notice()
        self.make_buttons()

    def make_notice(self):
        lbl = tk.Label(
            master=self,
            text="1. Switch your LED drivers to\n'Constant Current (CM)' Mode"
        )
        pic = os.path.dirname(pywfom.__file__)+"/lib/driverDemo.png"
        img = ImageTk.PhotoImage(Image.open(pic))
        panel = tk.Label(master=self, image=img)
        panel.image = img

        lbl.pack()
        panel.pack()

    def make_buttons(self):
        lbl = tk.Label(
            master=self,
            text="2. Select an LED"
        )
        lbl.pack()
        for i, led in enumerate(self.arduino.strobing['leds']):
            btn = tk.Button(
                master=self,
                text=led['name'],
                command=lambda p=led['pin'] :self.arduino.toggle_led(p),
                height=3,
                width=20
            )
            btn.pack(pady=10)

class ComboboxSelectionWindow(tk.Toplevel):

    def __init__(self, parent=None, master=None, setting=None):

        super().__init__(master = master)
        self.root = parent.root
        self.title(setting.title())
        self.resizable(width=False, height=False)
        self.setting = setting
        self.options = {
            "device":[
                "spinnaker",
                "andor",
                "test",
                "webcam"
            ],
            "master":[
                True,
                False
            ],
            "dtype":[
                "uint16",
                "uint8"
            ],
            "port":["COM{0}".format(i) for i in range(10)]
        }
        self.create_widgets()

    def create_widgets(self):

        self.combo = ttk.Combobox(master=self, values=self.options[self.setting])
        self.combo.current(1)
        self.combo.pack()
        self.done_btn = tk.Button(master=self, text="Done", command=self.callback)
        self.done_btn.pack()

    def callback(self):
        self.value = self.combo.get()
        self.destroy()
