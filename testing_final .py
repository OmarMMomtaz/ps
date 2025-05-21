import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os


class PlayStationManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("PlayStation Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg="#003791")  # PlayStation blue background
        
        # Initialize variables
        self.ps4_single_price = 100
        self.ps4_multi_price = 120
        self.ps5_single_price = 150
        self.ps5_multi_price = 180
        self.bar_item_price = 50
        
        # Room status (0=available, 1=occupied)
        self.rooms = {
            "PS4-1": {"status": 0, "type": "PS4", "player": "", "contact": "", "start_time": None, "bar_items": []},
            "PS4-2": {"status": 0, "type": "PS4", "player": "", "contact": "", "start_time": None, "bar_items": []},
            "PS4-3": {"status": 0, "type": "PS4", "player": "", "contact": "", "start_time": None, "bar_items": []},
            "PS5-1": {"status": 0, "type": "PS5", "player": "", "contact": "", "start_time": None, "bar_items": []},
            "PS5-2": {"status": 0, "type": "PS5", "player": "", "contact": "", "start_time": None, "bar_items": []},
            "PS5-3": {"status": 0, "type": "PS5", "player": "", "contact": "", "start_time": None, "bar_items": []},
        }
        
        self.daily_revenue = 0
        self.daily_sessions = 0
        self.current_room = None
        self.receipts = {}
        
        self.create_scrollable_ui()
        
    def create_scrollable_ui(self):
        # Main container with scrollbar
        self.main_container = tk.Frame(self.root, bg="#003791")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self.main_container, bg="#003791", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create a frame inside the canvas
        self.main_frame = tk.Frame(self.canvas, bg="#003791")
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Bind mousewheel to scroll
        self.main_frame.bind("<Enter>", self._bind_mousewheel)
        self.main_frame.bind("<Leave>", self._unbind_mousewheel)
        
        # Header with PlayStation styling
        self.header_frame = tk.Frame(self.main_frame, bg="#000000", padx=15, pady=10)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # PlayStation logo
        self.ps_logo = tk.Label(self.header_frame, 
                              text="PS", 
                              font=("Arial", 20, "bold"), 
                              fg="white", 
                              bg="#000000")
        self.ps_logo.pack(side=tk.LEFT, padx=10)
        
        self.logo_label = tk.Label(self.header_frame, 
                                 text="MANAGEMENT SYSTEM", 
                                 font=("Arial", 16, "bold"), 
                                 fg="white", 
                                 bg="#000000")
        self.logo_label.pack(side=tk.LEFT)
        
        # Controller symbols
        controller_symbols = tk.Label(self.header_frame,
                                    text="△ ○ × □",
                                    font=("Arial", 16),
                                    fg="white",
                                    bg="#000000")
        controller_symbols.pack(side=tk.RIGHT, padx=10)
        
        self.date_label = tk.Label(self.header_frame, 
                                 text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                 font=("Arial", 12), 
                                 fg="white", 
                                 bg="#000000")
        self.date_label.pack(side=tk.RIGHT, padx=10)
        
        # Content frame
        self.content_frame = tk.Frame(self.main_frame, bg="#003791")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Room management (black with blue border)
        self.left_panel = tk.Frame(self.content_frame, bg="#000000", bd=2, relief=tk.RIDGE,
                                 highlightbackground="#5c7cfa", highlightcolor="#5c7cfa", highlightthickness=2)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 10))
        
        # Right panel - Bar menu (black with blue border)
        self.right_panel = tk.Frame(self.content_frame, bg="#000000", bd=2, relief=tk.RIDGE,
                                  highlightbackground="#5c7cfa", highlightcolor="#5c7cfa", highlightthickness=2)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=(0, 10))
        
        # Create all UI components
        self.create_room_status_section()
        self.create_management_section()
        self.create_bar_menu_section()
        self.create_status_bar()
        
        # Update time every second
        self.update_time()
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_room_status_section(self):
        # Room status display
        self.room_status_frame = tk.LabelFrame(self.left_panel, 
                                            text="Room Status Overview", 
                                            font=("Arial", 12, "bold"),
                                            bd=0, 
                                            relief=tk.FLAT,
                                            bg="#000000",
                                            fg="#5c7cfa",
                                            padx=10,
                                            pady=10)
        self.room_status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create room status indicators in a grid
        self.room_indicators = {}
        for i, room in enumerate(self.rooms.keys()):
            frame = tk.Frame(self.room_status_frame, bg="#000000", bd=1, relief=tk.SOLID,
                            highlightbackground="#5c7cfa", highlightthickness=1)
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            
            status_color = "#5c7cfa" if self.rooms[room]["status"] == 0 else "#ff0000"  # Blue for available, red for occupied
            status_text = "AVAILABLE" if self.rooms[room]["status"] == 0 else "OCCUPIED"
            
            self.room_indicators[room] = {
                "frame": frame,
                "label": tk.Label(frame, text=room, font=("Arial", 10, "bold"), bg="#000000", fg="white"),
                "status": tk.Label(frame, text=status_text, font=("Arial", 10, "bold"), 
                                 fg="white", bg=status_color, width=12, padx=5),
                "time": tk.Label(frame, text="", font=("Arial", 8), bg="#000000", fg="#aaaaaa"),
                "player": tk.Label(frame, text="", font=("Arial", 9), bg="#000000", fg="white", wraplength=120)
            }
            
            self.room_indicators[room]["label"].pack(pady=(5, 0))
            self.room_indicators[room]["status"].pack()
            self.room_indicators[room]["time"].pack()
            self.room_indicators[room]["player"].pack(pady=(0, 5))
        
        # Configure grid weights for room status
        for i in range(3):
            self.room_status_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            self.room_status_frame.grid_rowconfigure(i, weight=1)
    
    def create_management_section(self):
        # Room management controls
        self.control_frame = tk.LabelFrame(self.left_panel, 
                                         text="New Booking", 
                                         font=("Arial", 12, "bold"),
                                         bd=0, 
                                         relief=tk.FLAT,
                                         bg="#000000",
                                         fg="#5c7cfa",
                                         padx=10,
                                         pady=10)
        self.control_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        # Player info
        self.player_frame = tk.Frame(self.control_frame, bg="#000000")
        self.player_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.player_frame, 
                text="Player Name:", 
                font=("Arial", 10), 
                bg="#000000",
                fg="white").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.player_name = tk.Entry(self.player_frame, 
                                  width=30,
                                  font=("Arial", 10),
                                  bd=1,
                                  relief=tk.SOLID,
                                  bg="#111111",
                                  fg="white",
                                  insertbackground="white")
        self.player_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.player_frame, 
                text="Contact Number:", 
                font=("Arial", 10), 
                bg="#000000",
                fg="white").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        self.contact_number = tk.Entry(self.player_frame, 
                                     width=30,
                                     font=("Arial", 10),
                                     bd=1,
                                     relief=tk.SOLID,
                                     bg="#111111",
                                     fg="white",
                                     insertbackground="white")
        self.contact_number.grid(row=1, column=1, padx=5, pady=5)
        
        # Console and mode selection
        self.selection_frame = tk.Frame(self.control_frame, bg="#000000")
        self.selection_frame.pack(fill=tk.X, pady=5)
        
        # Console type
        self.console_frame = tk.LabelFrame(self.selection_frame, 
                                         text="Console Type", 
                                         font=("Arial", 10),
                                         bd=1, 
                                         relief=tk.SOLID,
                                         bg="#000000",
                                         fg="white",
                                         padx=5,
                                         pady=5)
        self.console_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.console_type = tk.StringVar()
        self.console_type.set("PS4")
        
        ttk.Radiobutton(self.console_frame, 
                       text="PlayStation 4", 
                       variable=self.console_type, 
                       value="PS4",
                       command=self.update_room_dropdown,
                       style="PlayStation.TRadiobutton").pack(anchor="w")
        ttk.Radiobutton(self.console_frame, 
                       text="PlayStation 5", 
                       variable=self.console_type, 
                       value="PS5",
                       command=self.update_room_dropdown,
                       style="PlayStation.TRadiobutton").pack(anchor="w")
        
        # Game mode
        self.mode_frame = tk.LabelFrame(self.selection_frame, 
                                      text="Game Mode", 
                                      font=("Arial", 10),
                                      bd=1, 
                                      relief=tk.SOLID,
                                      bg="#000000",
                                      fg="white",
                                      padx=5,
                                      pady=5)
        self.mode_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.game_mode = tk.StringVar()
        self.game_mode.set("Single")
        
        ttk.Radiobutton(self.mode_frame, 
                       text="Single Player", 
                       variable=self.game_mode, 
                       value="Single",
                       style="PlayStation.TRadiobutton").pack(anchor="w")
        ttk.Radiobutton(self.mode_frame, 
                       text="Multi Player", 
                       variable=self.game_mode, 
                       value="Multi",
                       style="PlayStation.TRadiobutton").pack(anchor="w")
        
        # Room selection
        self.room_select_frame = tk.Frame(self.control_frame, bg="#000000")
        self.room_select_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(self.room_select_frame, 
                text="Select Room:", 
                font=("Arial", 10), 
                bg="#000000",
                fg="white").pack(side=tk.LEFT, padx=5)
        
        self.room_var = tk.StringVar()
        self.room_dropdown = ttk.Combobox(self.room_select_frame, 
                                         textvariable=self.room_var, 
                                         state="readonly",
                                         font=("Arial", 10),
                                         width=27)
        self.room_dropdown.pack(side=tk.LEFT, padx=5)
        self.update_room_dropdown()
        
        # Style configuration
        style = ttk.Style()
        style.configure("PlayStation.TRadiobutton", background="#000000", foreground="white")
        style.configure("TCombobox", fieldbackground="#111111", background="#111111", foreground="white")
        
        # Action buttons (PlayStation controller colors)
        self.button_frame = tk.Frame(self.control_frame, bg="#000000")
        self.button_frame.pack(fill=tk.X, pady=10)
        
        button_style = {
            "font": ("Arial", 10, "bold"), 
            "width": 15, 
            "bd": 0,
            "padx": 10,
            "pady": 8,
            "activebackground": "#003791",
            "highlightthickness": 0,
            "relief": tk.RAISED
        }
        
        self.start_btn = tk.Button(self.button_frame, 
                                  text="▶ Start Session", 
                                  command=self.start_session,
                                  bg="#5c7cfa",  # Blue like X button
                                  fg="white",
                                  **button_style)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.end_btn = tk.Button(self.button_frame, 
                                text="■ End Session", 
                                command=self.end_selected_session,
                                bg="#ff0000",  # Red like O button
                                fg="white",
                                **button_style)
        self.end_btn.pack(side=tk.LEFT, padx=5)
        
        self.receipt_btn = tk.Button(self.button_frame, 
                                    text="🖶 Print Receipt", 
                                    command=self.print_selected_receipt,
                                    bg="#ff9500",  # Orange like △
                                    fg="black",
                                    **button_style)
        self.receipt_btn.pack(side=tk.LEFT, padx=5)
        
        self.eod_btn = tk.Button(self.button_frame, 
                                text="📊 End of Day", 
                                command=self.end_of_day,
                                bg="#00c800",  # Green like □
                                fg="black",
                                **button_style)
        self.eod_btn.pack(side=tk.RIGHT, padx=5)
    
    def create_bar_menu_section(self):
        # Bar menu section
        self.bar_menu_frame = tk.LabelFrame(self.right_panel, 
                                          text="Bar Menu (50 EGP each)", 
                                          font=("Arial", 12, "bold"),
                                          bd=0, 
                                          relief=tk.FLAT,
                                          bg="#000000",
                                          fg="#5c7cfa",
                                          padx=10,
                                          pady=10)
        self.bar_menu_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create a canvas for the bar menu items
        self.bar_canvas = tk.Canvas(self.bar_menu_frame, bg="#000000", highlightthickness=0)
        self.bar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar for bar menu
        self.bar_scrollbar = ttk.Scrollbar(self.bar_menu_frame, orient=tk.VERTICAL, command=self.bar_canvas.yview)
        self.bar_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.bar_canvas.configure(yscrollcommand=self.bar_scrollbar.set)
        self.bar_canvas.bind('<Configure>', lambda e: self.bar_canvas.configure(scrollregion=self.bar_canvas.bbox("all")))
        
        # Frame for bar items
        self.bar_items_frame = tk.Frame(self.bar_canvas, bg="#000000")
        self.bar_canvas.create_window((0, 0), window=self.bar_items_frame, anchor="nw")
        
        # Bind mousewheel to bar menu scroll
        self.bar_items_frame.bind("<Enter>", lambda e: self.bar_canvas.bind_all("<MouseWheel>", lambda event: self.bar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")))
        self.bar_items_frame.bind("<Leave>", lambda e: self.bar_canvas.unbind_all("<MouseWheel>"))
        
        self.bar_items = [
            {"name": "Pepsi", "color": "#5c7cfa", "icon": "🥤"},
            {"name": "Tea", "color": "#5c7cfa", "icon": "🍵"},
            {"name": "Coffee", "color": "#5c7cfa", "icon": "☕"},
            {"name": "Water", "color": "#5c7cfa", "icon": "💧"},
            {"name": "Chips", "color": "#5c7cfa", "icon": "🍟"},
            {"name": "Chocolate", "color": "#5c7cfa", "icon": "🍫"},
            {"name": "Juice", "color": "#5c7cfa", "icon": "🧃"},
            {"name": "Soda", "color": "#5c7cfa", "icon": "🥤"}
        ]
        
        for item in self.bar_items:
            btn_frame = tk.Frame(self.bar_items_frame, bg="#000000", bd=1, relief=tk.SOLID,
                               highlightbackground="#5c7cfa", highlightthickness=1)
            btn_frame.pack(fill=tk.X, pady=5)
            
            btn = tk.Button(btn_frame, 
                          text=f"{item['icon']} {item['name']}", 
                          font=("Arial", 12, "bold"),
                          bg="#003791",
                          fg="white",
                          activebackground="#5c7cfa",
                          bd=0,
                          padx=20,
                          pady=10,
                          command=lambda x=item['name']: self.add_bar_item(x))
            btn.pack(fill=tk.X)
    
    def create_status_bar(self):
        # Status bar at bottom (PlayStation style)
        self.status_frame = tk.Frame(self.main_frame, bg="#000000", height=30)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="Status: Ready", 
                                   font=("Arial", 10, "bold"),
                                   fg="#5c7cfa", 
                                   bg="#000000",
                                   anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def update_time(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.date_label.config(text=now)
        self.root.after(1000, self.update_time)
    
    def update_room_dropdown(self):
        available_rooms = [room for room, info in self.rooms.items() 
                         if info["status"] == 0 and info["type"] == self.console_type.get()]
        self.room_dropdown["values"] = available_rooms
        if available_rooms:
            self.room_var.set(available_rooms[0])
        else:
            self.room_var.set("")
        
        self.update_room_indicators()
    
    def update_room_indicators(self):
        for room, indicator in self.room_indicators.items():
            room_info = self.rooms[room]
            status_color = "#5c7cfa" if room_info["status"] == 0 else "#ff0000"
            status_text = "AVAILABLE" if room_info["status"] == 0 else "OCCUPIED"
            
            indicator["status"].config(text=status_text, bg=status_color)
            
            if room_info["status"] == 1:
                start_time = room_info["start_time"].strftime("%H:%M:%S") if room_info["start_time"] else ""
                player_text = f"{room_info['player']}\n({room_info['contact']})"
                indicator["time"].config(text=f"Started: {start_time}")
                indicator["player"].config(text=player_text)
            else:
                indicator["time"].config(text="")
                indicator["player"].config(text="")
    
    def start_session(self):
        player_name = self.player_name.get().strip()
        contact_number = self.contact_number.get().strip()
        
        if not player_name:
            messagebox.showerror("Error", "Please enter player name")
            return
            
        if not contact_number:
            messagebox.showerror("Error", "Please enter contact number")
            return
            
        room = self.room_var.get()
        if not room:
            messagebox.showerror("Error", "No available rooms for selected console type")
            return
            
        # Start the session
        self.rooms[room]["status"] = 1
        self.rooms[room]["player"] = player_name
        self.rooms[room]["contact"] = contact_number
        self.rooms[room]["start_time"] = datetime.now()
        self.rooms[room]["bar_items"] = []
        
        # Clear input fields for next booking
        self.player_name.delete(0, tk.END)
        self.contact_number.delete(0, tk.END)
        
        self.update_status(f"Session started in {room} for {player_name}")
        self.update_room_dropdown()
        
        # Auto-select next available room if exists
        available_rooms = [r for r, info in self.rooms.items() 
                          if info["status"] == 0 and info["type"] == self.console_type.get()]
        if available_rooms:
            self.room_var.set(available_rooms[0])
    
    def end_selected_session(self):
        # Let user select which room to end
        occupied_rooms = [room for room, info in self.rooms.items() if info["status"] == 1]
        if not occupied_rooms:
            messagebox.showerror("Error", "No active sessions to end")
            return
            
        # Create selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Room to End")
        selection_window.geometry("300x200")
        selection_window.resizable(False, False)
        selection_window.configure(bg="#000000")
        
        tk.Label(selection_window, 
                text="Select room to end session:", 
                font=("Arial", 10),
                bg="#000000",
                fg="white").pack(pady=10)
        
        room_var = tk.StringVar()
        room_dropdown = ttk.Combobox(selection_window, 
                                    textvariable=room_var, 
                                    values=occupied_rooms,
                                    state="readonly",
                                    font=("Arial", 10))
        room_dropdown.pack(pady=5)
        room_var.set(occupied_rooms[0])
        
        def confirm_end():
            selected_room = room_var.get()
            if selected_room:
                self.current_room = selected_room
                self.end_session()
                selection_window.destroy()
        
        tk.Button(selection_window, 
                 text="End Session", 
                 command=confirm_end,
                 bg="#ff0000",
                 fg="white",
                 font=("Arial", 10, "bold"),
                 bd=0,
                 padx=10,
                 pady=5).pack(pady=10)
    
    def end_session(self):
        if not self.current_room:
            messagebox.showerror("Error", "No room selected to end")
            return
            
        room_info = self.rooms[self.current_room]
        end_time = datetime.now()
        start_time = room_info["start_time"]
        duration = (end_time - start_time).total_seconds() / 3600  # in hours
        
        # Calculate gaming cost
        if room_info["type"] == "PS4":
            price = self.ps4_single_price if self.game_mode.get() == "Single" else self.ps4_multi_price
        else:
            price = self.ps5_single_price if self.game_mode.get() == "Single" else self.ps5_multi_price
        
        gaming_cost = round(duration * price, 2)
        
        # Calculate bar items cost
        bar_items_cost = len(room_info["bar_items"]) * self.bar_item_price
        
        total_cost = gaming_cost + bar_items_cost
        
        # Update daily revenue
        self.daily_revenue += total_cost
        self.daily_sessions += 1
        
        # Store receipt info
        self.receipts[self.current_room] = {
            "room": self.current_room,
            "player": room_info["player"],
            "contact": room_info["contact"],
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": f"{duration:.2f} hours",
            "console": room_info["type"],
            "mode": self.game_mode.get(),
            "hourly_rate": price,
            "gaming_cost": gaming_cost,
            "bar_items": room_info["bar_items"],
            "bar_items_cost": bar_items_cost,
            "total_cost": total_cost
        }
        
        # Reset room
        self.rooms[self.current_room]["status"] = 0
        self.rooms[self.current_room]["player"] = ""
        self.rooms[self.current_room]["contact"] = ""
        self.rooms[self.current_room]["start_time"] = None
        self.rooms[self.current_room]["bar_items"] = []
        
        self.update_status(f"Session ended in {self.current_room}. Total cost: {total_cost} EGP")
        self.update_room_dropdown()
        self.current_room = None
    
    def print_selected_receipt(self):
        occupied_rooms = [room for room, info in self.rooms.items() if info["status"] == 1]
        if not occupied_rooms and not hasattr(self, 'receipts'):
            messagebox.showerror("Error", "No active sessions or receipts available")
            return
            
        # Create selection dialog
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Receipt to Print")
        selection_window.geometry("300x200")
        selection_window.resizable(False, False)
        selection_window.configure(bg="#000000")
        
        tk.Label(selection_window, 
                text="Select room receipt to print:", 
                font=("Arial", 10),
                bg="#000000",
                fg="white").pack(pady=10)
        
        room_var = tk.StringVar()
        # Include both active sessions and completed ones with receipts
        available_receipts = list(self.receipts.keys()) + occupied_rooms
        room_dropdown = ttk.Combobox(selection_window, 
                                    textvariable=room_var, 
                                    values=available_receipts,
                                    state="readonly",
                                    font=("Arial", 10))
        room_dropdown.pack(pady=5)
        if available_receipts:
            room_var.set(available_receipts[0])
        
        def confirm_print():
            selected_room = room_var.get()
            if selected_room:
                self.current_room = selected_room
                if selected_room in self.receipts:
                    self.receipt_info = self.receipts[selected_room]
                else:
                    # Create receipt info for active session
                    room_info = self.rooms[selected_room]
                    end_time = datetime.now()
                    start_time = room_info["start_time"]
                    duration = (end_time - start_time).total_seconds() / 3600
                    
                    if room_info["type"] == "PS4":
                        price = self.ps4_single_price if self.game_mode.get() == "Single" else self.ps4_multi_price
                    else:
                        price = self.ps5_single_price if self.game_mode.get() == "Single" else self.ps5_multi_price
                    
                    gaming_cost = round(duration * price, 2)
                    bar_items_cost = len(room_info["bar_items"]) * self.bar_item_price
                    total_cost = gaming_cost + bar_items_cost
                    
                    self.receipt_info = {
                        "room": selected_room,
                        "player": room_info["player"],
                        "contact": room_info["contact"],
                        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "duration": f"{duration:.2f} hours",
                        "console": room_info["type"],
                        "mode": self.game_mode.get(),
                        "hourly_rate": price,
                        "gaming_cost": gaming_cost,
                        "bar_items": room_info["bar_items"],
                        "bar_items_cost": bar_items_cost,
                        "total_cost": total_cost
                    }
                
                self.print_receipt()
                selection_window.destroy()
        
        tk.Button(selection_window, 
                 text="Print Receipt", 
                 command=confirm_print,
                 bg="#ff9500",
                 fg="black",
                 font=("Arial", 10, "bold"),
                 bd=0,
                 padx=10,
                 pady=5).pack(pady=10)
    
    def add_bar_item(self, item):
        if not any(info["status"] == 1 for info in self.rooms.values()):
            messagebox.showerror("Error", "No active sessions to add bar items")
            return
            
        # Create selection dialog if multiple rooms are active
        occupied_rooms = [room for room, info in self.rooms.items() if info["status"] == 1]
        if len(occupied_rooms) > 1:
            selection_window = tk.Toplevel(self.root)
            selection_window.title("Select Room")
            selection_window.geometry("300x200")
            selection_window.resizable(False, False)
            selection_window.configure(bg="#000000")
            
            tk.Label(selection_window, 
                    text="Select room to add item:", 
                    font=("Arial", 10),
                    bg="#000000",
                    fg="white").pack(pady=10)
            
            room_var = tk.StringVar()
            room_dropdown = ttk.Combobox(selection_window, 
                                        textvariable=room_var, 
                                        values=occupied_rooms,
                                        state="readonly",
                                        font=("Arial", 10))
            room_dropdown.pack(pady=5)
            room_var.set(occupied_rooms[0])
            
            def confirm_add():
                selected_room = room_var.get()
                if selected_room:
                    self.rooms[selected_room]["bar_items"].append(item)
                    self.update_status(f"Added {item} to {selected_room}")
                    selection_window.destroy()
            
            tk.Button(selection_window, 
                     text=f"Add {item}", 
                     command=confirm_add,
                     bg="#5c7cfa",
                     fg="white",
                     font=("Arial", 10, "bold"),
                     bd=0,
                     padx=10,
                     pady=5).pack(pady=10)
        else:
            # Only one room is active, add to it directly
            self.rooms[occupied_rooms[0]]["bar_items"].append(item)
            self.update_status(f"Added {item} to {occupied_rooms[0]}")
    
    def print_receipt(self):
        if not hasattr(self, 'receipt_info'):
            messagebox.showerror("Error", "No receipt information available")
            return
            
        receipt = f"""
{'='*50}
{'PLAYSTATION RECEIPT'.center(50)}
{'='*50}
{'Date:':<25}{datetime.now().strftime("%Y-%m-%d %H:%M:%S"):>25}
{'Room:':<25}{self.receipt_info['room']:>25}
{'Player:':<25}{self.receipt_info['player']:>25}
{'Contact:':<25}{self.receipt_info['contact']:>25}
{'-'*50}
{'Start Time:':<25}{self.receipt_info['start_time']:>25}
{'End Time:':<25}{self.receipt_info['end_time']:>25}
{'Duration:':<25}{self.receipt_info['duration']:>25}
{'Console:':<25}{self.receipt_info['console']:>25}
{'Game Mode:':<25}{self.receipt_info['mode']:>25}
{'Hourly Rate:':<25}{self.receipt_info['hourly_rate']:>25} EGP
{'Gaming Cost:':<25}{self.receipt_info['gaming_cost']:>25} EGP
{'Bar Items:':<25}{', '.join(self.receipt_info['bar_items']) or 'None':>25}
{'Bar Items Cost:':<25}{self.receipt_info['bar_items_cost']:>25} EGP
{'='*50}
{'TOTAL COST:':<25}{self.receipt_info['total_cost']:>25} EGP
{'='*50}
{'THANK YOU!'.center(50)}
{'='*50}
"""
        
        # Show receipt in messagebox
        messagebox.showinfo("Receipt", receipt)
        
        # Save receipt to application directory
        app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        receipt_file = os.path.join(app_path, f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        try:
            with open(receipt_file, "w") as f:
                f.write(receipt)
            self.update_status(f"Receipt saved to {receipt_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save receipt: {str(e)}")

    def end_of_day(self):
        eod_report = f"""
{'='*50}
{'END OF DAY REPORT'.center(50)}
{'='*50}
{'Date:':<25}{datetime.now().strftime("%Y-%m-%d"):>25}
{'Total Sessions:':<25}{self.daily_sessions:>25}
{'Total Revenue:':<25}{self.daily_revenue:>25} EGP
{'='*50}
{'ROOMS STATUS'.center(50)}
{'='*50}
"""
        
        for room, info in self.rooms.items():
            status = "Occupied" if info["status"] else "Available"
            eod_report += f"{room:<25}{status:>25}\n"
        
        eod_report += "="*50
        
        # Show report in messagebox
        messagebox.showinfo("End of Day Report", eod_report)
        
        # Save report to application directory
        app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        eod_file = os.path.join(app_path, f"eod_report_{datetime.now().strftime('%Y%m%d')}.txt")
        
        try:
            with open(eod_file, "w") as f:
                f.write(eod_report)
            self.update_status(f"End of day report saved to {eod_file}")
            
            # Reset daily counters
            self.daily_revenue = 0
            self.daily_sessions = 0
            # Clear receipts
            self.receipts = {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save EOD report: {str(e)}")
    
    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayStationManagementSystem(root)
    root.mainloop()