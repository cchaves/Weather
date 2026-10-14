import cv2
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random
import math
from datetime import datetime

class PolaroidCameraApp:
    def __init__(self):
        # Configuration
        self.default_picture_folder = self.get_default_pictures_folder()
        self.selected_camera = 0
        
        # Standard polaroid dimensions (in pixels, approximating 3.5" x 4.2" at 300 DPI)
        self.polaroid_width = 1050  # 3.5 inches at 300 DPI
        self.polaroid_height = 1260  # 4.2 inches at 300 DPI
        self.border_width = 60  # Standard polaroid border
        self.bottom_border = 200  # Standard bottom area for 32pt text
        
        # Standard sayings for all photos
        self.random_sayings = [
            # General Happy Messages
            "Have a great day!",
            "Happy Day!",
            "Smile!",
            "Beautiful moment!",
            "Capture the joy!",
            "Life is beautiful!",
            "Make it count!",
            "Cherish this moment!",
            "Joy to the world!",
            "Happy times!",
            "Best day ever!",
            "So happy!",
            "Pure joy!",
            "Wonderful memories!",
            "Living the dream!",
            "Good vibes only!",
            "Happiness overload!",
            "Smile more!",
            "Stay positive!",
            "Choose happiness!",
            
            # Love & Romance
            "Forever & Always",
            "Love is in the air",
            "Happily Ever After",
            "Two hearts, one love",
            "Happy Anniversary!",
            "Years of love",
            "Love you forever!",
            "My heart is yours",
            "Together forever",
            "True love",
            "Soulmates",
            "Love wins!",
            "Endless love",
            "My person",
            "Better together",
            
            # Birthday
            "Happy Birthday!",
            "Make a wish!",
            "Celebrating YOU!",
            "Another year older!",
            "Birthday vibes!",
            "Party time!",
            "Best birthday ever!",
            "Aging like fine wine!",
            "Birthday magic!",
            "Celebrate good times!",
            
            # Congratulations
            "Congratulations!",
            "Well done!",
            "You did it!",
            "Way to go!",
            "Proud of you!",
            "Amazing job!",
            "You rock!",
            "Success!",
            "Achievement unlocked!",
            "Bravo!",
            
            # Easter
            "Happy Easter!",
            "Easter blessings!",
            "Egg-cellent day!",
            "Spring has sprung!",
            "Easter joy!",
            "Hoppy Easter!",
            "Blessed Easter!",
            "Easter happiness!",
            
            # Christmas
            "Merry Christmas!",
            "Happy Holidays!",
            "Christmas magic!",
            "Season's greetings!",
            "Joy to the world!",
            "Christmas cheer!",
            "Ho Ho Ho!",
            "Winter wonderland!",
            "Christmas blessings!",
            "Holiday magic!",
            
            # Halloween
            "Happy Halloween!",
            "Spooky season!",
            "Boo!",
            "Trick or treat!",
            "Witching you happiness!",
            "Halloween fun!",
            "Creepin' it real!",
            "Spooky vibes!",
            
            # Thanksgiving
            "Happy Thanksgiving!",
            "Grateful heart!",
            "Give thanks!",
            "Thankful for you!",
            "Turkey day!",
            "Blessed Thanksgiving!",
            "Family time!",
            "Harvest blessings!",
            
            # New Year
            "Happy New Year!",
            "New beginnings!",
            "Fresh start!",
            "Cheers!",
            "New Year, New You!",
            "Best year yet!",
            "New Year magic!",
            "Celebrate new beginnings!",
            
            # Valentine's Day
            "Happy Valentine's Day!",
            "Be my Valentine!",
            "Love is in the air!",
            "Valentine vibes!",
            "My Valentine!",
            "Love you!",
            "Sweetest day!",
            
            # Graduation
            "Congratulations Graduate!",
            "Graduation day!",
            "You made it!",
            "Future is bright!",
            "Graduation success!",
            "Proud graduate!",
            "Next chapter!",
            
            # Wedding
            "Just Married!",
            "Wedding bells!",
            "Happily married!",
            "Wedding day!",
            "Here comes the bride!",
            "Love and laughter!",
            "Wedding bliss!",
            "Mr. & Mrs.!",
            
            # Baby/Children
            "Baby on the way!",
            "Welcome baby!",
            "New parents!",
            "Baby joy!",
            "Little miracle!",
            "Sweet baby!",
            "Bundle of joy!",
            "Growing family!",
            
            # Retirement
            "Happy Retirement!",
            "Retired and loving it!",
            "Golden years!",
            "Freedom at last!",
            "Retirement bliss!",
            "Well deserved!",
            "The adventure begins!",
            
            # St. Patrick's Day
            "Happy St. Patrick's Day!",
            "Lucky day!",
            "Irish blessings!",
            "Shamrock joy!",
            "Green with envy!",
            "Luck of the Irish!",
            
            # Mother's Day
            "Happy Mother's Day!",
            "Best mom ever!",
            "Mom love!",
            "Super mom!",
            "Mom of the year!",
            "Mother's love!",
            
            # Father's Day
            "Happy Father's Day!",
            "Best dad ever!",
            "Dad love!",
            "Super dad!",
            "Father's pride!",
            "World's best dad!",
            
            # Independence Day / July 4th
            "Happy 4th of July!",
            "Freedom!",
            "Proud to be free!",
            "Stars and stripes!",
            "Fireworks and fun!",
            "Independence Day!",
            
            # General Events
            "Party time!",
            "Celebration!",
            "Special occasion!",
            "Making memories!",
            "Good times!",
            "Let's celebrate!",
            "Fun times!",
            "Memories made!"
        ]
        
        # Border mode configuration
        self.border_mode = "Solid Color"  # Options: "Solid Color", "Image Background"
        
        # Text selection configuration
        self.text_mode = "Random"  # Options: "Random", "From List", "Custom"
        self.selected_saying = ""  # For "From List" mode
        self.custom_text = ""  # For "Custom" mode
        
        # Picture mode configuration
        self.picture_mode = "Single"  # Options: "Single", "2X", "3X"
        self.multi_photo_images = []  # Store images for multi-photo modes
        self.multi_photo_count = 0  # Track number of photos taken
        
        # Sticker configuration
        self.sticker_mode = "Random"  # Default to Random
        self.sticker_texts = ["Random", "None", "#J4F", "I HATE Photos!", "AHHHH!", "LOL!", "ROFL!", "BAE!", "143!", "OMG!", "SO MUCH FUN!", "WHAT!?", "PARTY TIME!", "SELFIE TIME!", "#BFF", "BEST DAY EVER!"]
        self.sticker_shapes = ["Random", "Bubble", "Star", "Cloud", "Heart"]
        self.sticker_shape = "Random"  # Default to Random shape
        self.sticker_fill_colors = ["Hot Pink", "Blue", "Yellow", "Green", "Lime", "White", "Grey", "Purple"]
        self.sticker_fill_color = "Hot Pink"  # Default fill color
        
        # Text color configuration
        self.text_color = "black"  # Default text color
        self.text_colors = ["black", "white", "pink", "red", "blue", "gray", "yellow", "purple", "green"]
        
        # Font size configuration
        self.font_size = 36  # Default font size for main text
        self.font_sizes = [26, 31, 36, 41, 46, 51, 56, 66, 76]  # 5pt increments from 16
        
        # Print configuration
        self.paper_sizes = {
            "2.5x3.5": (750, 1050),  # inches at 300 DPI
            "4x6": (1200, 1800),
            "5x7": (1500, 2100),
            "8x10": (2400, 3000)
        }
        self.selected_paper_size = "4x6"  # Default
        self.last_saved_image_path = None  # Track last saved image
        
        # Result display
        self.current_result_image = None
        
        # Camera filters
        self.filters = {
            "None": None,
            "Random Filter": self.apply_random_filter,
            "Black & White": self.apply_black_white,
            "Cinematic": self.apply_cinematic,
            "Vintage": self.apply_vintage,
            "Watercolor": self.apply_watercolor,
            "Cross-hatch": self.apply_cross_hatch,
            "Glitch": self.apply_glitch,
            "Beauty Mode": self.apply_beauty_mode,
            "Cartoon": self.apply_cartoon,
            "Oil Painting": self.apply_oil_painting,
            "Pencil Sketch": self.apply_pencil_sketch,
            "Charcoal": self.apply_charcoal,
            "Pastel": self.apply_pastel,
            "Pop Art": self.apply_pop_art,
            "Neon": self.apply_neon,
            "Cyberpunk": self.apply_cyberpunk,
            "Blur": self.apply_blur,
            "Sharpen": self.apply_sharpen,
            "Emboss": self.apply_emboss,
            "Edge Detect": self.apply_edge_detect,
            "Solarize": self.apply_solarize,
            "Pixelate": self.apply_pixelate,
            "HDR": self.apply_hdr,
            "Vignette": self.apply_vignette,
            "Film Grain": self.apply_film_grain,
            "Mirror": self.apply_mirror,
            "Autumn": self.apply_autumn,
            "Winter": self.apply_winter,
            "Summer": self.apply_summer,
            "Spring": self.apply_spring,
            "Sunset": self.apply_sunset,
            "Night": self.apply_night
        }
        
        # Initialize GUI
        self.setup_gui()
        
    def get_default_pictures_folder(self):
        """Get the default pictures folder for Windows"""
        return os.path.join(os.path.expanduser('~'), 'Pictures')
    
    def get_available_cameras(self):
        """Detect available cameras"""
        available_cameras = []
        for i in range(10):  # Check first 10 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
    
    def setup_gui(self):
        """Create the main GUI window"""
        self.root = tk.Tk()
        self.root.title("Polaroid Camera App")
        
        # Set window size to about 1/3 of screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width // 3
        window_height = screen_height // 2
        self.root.geometry(f"{window_width}x{window_height}")
        
        # Configure modern, fun styling
        style = ttk.Style()
        style.theme_use('clam')
        
        # Fun colors for special occasions
        style.configure('Fun.TLabelframe', background='#FFE5B4', foreground='#FF6B6B', font=('Comic Sans MS', 10, 'bold'))
        style.configure('Fun.TLabel', background='#FFE5B4', foreground='#333333', font=('Comic Sans MS', 9))
        style.configure('Fun.TCombobox', fieldbackground='#FFFFFF', background='#FFFFFF', font=('Comic Sans MS', 9))
        style.configure('Fun.TButton', font=('Comic Sans MS', 10, 'bold'))
        
        self.root.configure(bg='#FFE5B4')
        
        # Main controls container
        controls_frame = ttk.Frame(self.root, style='Fun.TFrame')
        controls_frame.pack(padx=5, pady=5, fill='x')
        
        # Row 1: Camera, Border Mode, Filter (side by side)
        row1 = ttk.Frame(controls_frame, style='Fun.TFrame')
        row1.pack(fill='x', pady=2)
        
        # Camera selection
        camera_frame = ttk.LabelFrame(row1, text="📷 Camera", style='Fun.TLabelframe')
        camera_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(camera_frame, textvariable=self.camera_var, state="readonly", style='Fun.TCombobox')
        self.camera_combo['values'] = [f"Camera {i}" for i in self.get_available_cameras()]
        if self.camera_combo['values']:
            self.camera_combo.current(0)
        self.camera_combo.pack(padx=2, pady=2, fill='x')
        
        # Border mode selection
        self.border_mode_frame = ttk.LabelFrame(row1, text="🎨 Border", style='Fun.TLabelframe')
        self.border_mode_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.border_mode_var = tk.StringVar(value="Solid Color")
        border_mode_combo = ttk.Combobox(self.border_mode_frame, textvariable=self.border_mode_var,
                                        values=["Solid Color", "Image Background"], state="readonly", style='Fun.TCombobox')
        border_mode_combo.current(0)
        border_mode_combo.pack(padx=2, pady=2, fill='x')
        border_mode_combo.bind("<<ComboboxSelected>>", self.on_border_mode_change)
        
        # Filter selection
        filter_frame = ttk.LabelFrame(row1, text="✨ Filter", style='Fun.TLabelframe')
        filter_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.filter_var = tk.StringVar(value="None")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                    values=list(self.filters.keys()), state="readonly", style='Fun.TCombobox')
        filter_combo.current(0)
        filter_combo.pack(padx=2, pady=2, fill='x')
        
        # Border image selection (hidden by default)
        self.border_image_frame = ttk.LabelFrame(controls_frame, text="🖼️ Border Image", style='Fun.TLabelframe')
        self.border_image_path = tk.StringVar()
        self.border_image_entry = ttk.Entry(self.border_image_frame, textvariable=self.border_image_path)
        self.border_image_entry.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        border_image_button = ttk.Button(self.border_image_frame, text="Browse", command=self.browse_border_image, style='Fun.TButton')
        border_image_button.pack(side='left', padx=2, pady=2)
        
        # Initially hide the border image frame
        self.border_image_frame.pack_forget()
        
        # Row 2: Text Selection, Text Color, Font Size (side by side)
        row2 = ttk.Frame(controls_frame, style='Fun.TFrame')
        row2.pack(fill='x', pady=2)
        
        # Text selection
        self.text_frame = ttk.LabelFrame(row2, text="💬 Text", style='Fun.TLabelframe')
        self.text_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.text_mode_var = tk.StringVar(value="Random")
        text_mode_combo = ttk.Combobox(self.text_frame, textvariable=self.text_mode_var,
                                      values=["Random", "From List", "Custom"], state="readonly", style='Fun.TCombobox')
        text_mode_combo.current(0)
        text_mode_combo.pack(padx=2, pady=2, fill='x')
        text_mode_combo.bind("<<ComboboxSelected>>", self.on_text_mode_change)
        
        # Text color selection
        color_frame = ttk.LabelFrame(row2, text="🎨 Color", style='Fun.TLabelframe')
        color_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.text_color_var = tk.StringVar(value="black")
        color_combo = ttk.Combobox(color_frame, textvariable=self.text_color_var,
                                   values=self.text_colors, state="readonly", style='Fun.TCombobox')
        color_combo.current(0)
        color_combo.pack(padx=2, pady=2, fill='x')
        
        # Font size selection
        size_frame = ttk.LabelFrame(row2, text="📏 Size", style='Fun.TLabelframe')
        size_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.font_size_var = tk.StringVar(value="36")
        size_combo = ttk.Combobox(size_frame, textvariable=self.font_size_var,
                                  values=[str(s) for s in self.font_sizes], state="readonly", style='Fun.TCombobox')
        size_combo.current(4)  # Default to 36pt (index 4)
        size_combo.pack(padx=2, pady=2, fill='x')
        
        # Sticker selection
        sticker_frame = ttk.LabelFrame(row2, text="🎭 Sticker", style='Fun.TLabelframe')
        sticker_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.sticker_var = tk.StringVar(value="Random")
        sticker_combo = ttk.Combobox(sticker_frame, textvariable=self.sticker_var,
                                     values=self.sticker_texts, state="readonly", style='Fun.TCombobox')
        sticker_combo.current(0)  # Default to Random
        sticker_combo.pack(padx=2, pady=2, fill='x')
        
        # Sticker shape selection
        self.sticker_shape_var = tk.StringVar(value="Random")
        shape_combo = ttk.Combobox(sticker_frame, textvariable=self.sticker_shape_var,
                                   values=self.sticker_shapes, state="readonly", style='Fun.TCombobox')
        shape_combo.current(0)  # Default to Random
        shape_combo.pack(padx=2, pady=2, fill='x')
        
        # Sticker fill color selection
        self.sticker_fill_color_var = tk.StringVar(value="Hot Pink")
        fill_color_combo = ttk.Combobox(sticker_frame, textvariable=self.sticker_fill_color_var,
                                       values=self.sticker_fill_colors, state="readonly", style='Fun.TCombobox')
        fill_color_combo.current(0)  # Default to Hot Pink
        fill_color_combo.pack(padx=2, pady=2, fill='x')
        
        # Saying selection from list (hidden by default)
        self.saying_frame = ttk.LabelFrame(controls_frame, text="💭 Select Saying", style='Fun.TLabelframe')
        self.saying_var = tk.StringVar()
        self.saying_combo = ttk.Combobox(self.saying_frame, textvariable=self.saying_var,
                                         values=self.random_sayings, state="readonly", style='Fun.TCombobox')
        if self.saying_combo['values']:
            self.saying_combo.current(0)
        self.saying_combo.pack(padx=2, pady=2, fill='x')
        self.saying_frame.pack_forget()
        
        # Custom text entry (hidden by default)
        self.custom_text_frame = ttk.LabelFrame(controls_frame, text="✏️ Custom Message", style='Fun.TLabelframe')
        self.custom_text_var = tk.StringVar()
        self.custom_text_entry = ttk.Entry(self.custom_text_frame, textvariable=self.custom_text_var)
        self.custom_text_entry.pack(padx=2, pady=2, fill='x')
        self.custom_text_frame.pack_forget()
        
        # Row 3: Output Folder
        row3 = ttk.Frame(controls_frame, style='Fun.TFrame')
        row3.pack(fill='x', pady=2)
        
        folder_frame = ttk.LabelFrame(row3, text="📁 Folder", style='Fun.TLabelframe')
        folder_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.folder_path = tk.StringVar(value=self.default_picture_folder)
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path)
        folder_entry.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder, style='Fun.TButton')
        browse_button.pack(side='left', padx=2, pady=2)
        
        # Row 4: Picture Mode
        row4 = ttk.Frame(controls_frame, style='Fun.TFrame')
        row4.pack(fill='x', pady=2)
        
        picture_mode_frame = ttk.LabelFrame(row4, text="📸 Picture Mode", style='Fun.TLabelframe')
        picture_mode_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.picture_mode_var = tk.StringVar(value="Single")
        picture_mode_combo = ttk.Combobox(picture_mode_frame, textvariable=self.picture_mode_var,
                                         values=["Single", "2X", "3X"], state="readonly", style='Fun.TCombobox')
        picture_mode_combo.current(0)
        picture_mode_combo.pack(padx=2, pady=2, fill='x')
        picture_mode_combo.bind("<<ComboboxSelected>>", self.on_picture_mode_change)
        
        # Take picture button (prominent location with camera icon)
        self.take_picture_button = tk.Button(self.root, text="📷\nTake Picture\n(📷)", 
                                             command=self.start_countdown_capture,
                                             font=("Comic Sans MS", 14, "bold"),
                                             height=3, width=22,
                                             bg="#FF6B6B", fg="white",
                                             activebackground="#FF5252",
                                             relief="raised", bd=5,
                                             cursor="hand2")
        self.take_picture_button.pack(pady=10)
        
        # Print settings (below take picture button)
        print_frame = ttk.LabelFrame(self.root, text="🖨️ Print", style="Fun.TLabelframe")
        print_frame.pack(padx=10, pady=5, fill='x')
        
        self.paper_size_var = tk.StringVar(value="4x6")
        paper_size_combo = ttk.Combobox(print_frame, textvariable=self.paper_size_var,
                                        values=list(self.paper_sizes.keys()), state="readonly")
        paper_size_combo.current(1)
        paper_size_combo.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        print_button = tk.Button(print_frame, text="🖨️ Print", command=self.print_image,
                               font=("Comic Sans MS", 10, "bold"),
                               bg="#4ECDC4", fg="white",
                               activebackground="#45B7AF",
                               relief="raised", bd=3,
                               cursor="hand2")
        print_button.pack(side='left', padx=5, pady=5)
        
        # Result display section
        result_frame = ttk.LabelFrame(self.root, text="🖼️ Result", style='Fun.TLabelframe')
        result_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Result image label (adjusted for polaroid aspect ratio with standard bottom border)
        self.result_label = tk.Label(result_frame, bg="black", width=525, height=630)
        self.result_label.pack(padx=5, pady=5)
        
        # Countdown label (overlay)
        self.countdown_label = tk.Label(self.result_label, text="", font=("Arial", 48, "bold"), 
                                       bg="black", fg="white")
        self.countdown_label.place(relx=0.5, rely=0.5, anchor='center')
        
    def browse_folder(self):
        """Open folder browser to select output directory"""
        folder = filedialog.askdirectory(initialdir=self.default_picture_folder)
        if folder:
            self.folder_path.set(folder)
    
    def print_image(self):
        """Print the last saved image with selected paper size"""
        if self.last_saved_image_path is None or not os.path.exists(self.last_saved_image_path):
            messagebox.showwarning("No Image", "Please take a picture first!")
            return
        
        try:
            # Load the last saved image
            print_image = Image.open(self.last_saved_image_path)
            print_image = print_image.convert('RGB')
            
            # Get selected paper size
            paper_size = self.paper_size_var.get()
            target_width, target_height = self.paper_sizes[paper_size]
            
            # Get current image dimensions
            img_width, img_height = print_image.size
            
            # Calculate aspect ratios
            img_aspect = img_width / img_height
            paper_aspect = target_width / target_height
            
            # Determine if rotation is needed for best fit
            if img_aspect > paper_aspect:
                # Image is wider than paper, rotate 90 degrees
                print_image = print_image.rotate(90, expand=True)
                img_width, img_height = print_image.size
            else:
                print_image = print_image.copy()
            
            # Calculate scaling to fit within paper dimensions with margins
            margin = 50  # 50 pixel margin
            available_width = target_width - (2 * margin)
            available_height = target_height - (2 * margin)
            
            # Calculate scale factors
            scale_x = available_width / img_width
            scale_y = available_height / img_height
            scale = min(scale_x, scale_y)  # Use the smaller scale to fit both dimensions
            
            # Resize image
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            print_image = print_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a white canvas with paper dimensions
            canvas = Image.new('RGB', (target_width, target_height), 'white')
            
            # Center the image on the canvas
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
            canvas.paste(print_image, (paste_x, paste_y))
            
            # Save to a temporary file for printing
            temp_path = os.path.join(self.folder_path.get(), "temp_print.png")
            canvas.save(temp_path, "PNG")
            
            # Use Windows default print dialog
            os.startfile(temp_path, "print")
            
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print image: {e}")
    
    def on_border_mode_change(self, event):
        """Handle border mode dropdown change"""
        mode = self.border_mode_var.get()
        if mode == "Image Background":
            # Show the border image frame after the border mode frame
            self.border_image_frame.pack(padx=5, pady=2, fill='x', after=self.border_mode_frame)
        else:
            self.border_image_frame.pack_forget()
    
    def browse_border_image(self):
        """Open file browser to select border image"""
        image_path = filedialog.askopenfilename(
            title="Select Border Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if image_path:
            self.border_image_path.set(image_path)
    
    def on_text_mode_change(self, event):
        """Handle text mode dropdown change"""
        mode = self.text_mode_var.get()
        if mode == "From List":
            # Show the saying selection frame
            self.saying_frame.pack(padx=5, pady=2, fill='x', after=self.text_frame)
            self.custom_text_frame.pack_forget()
        elif mode == "Custom":
            # Show the custom text entry frame
            self.custom_text_frame.pack(padx=5, pady=2, fill='x', after=self.text_frame)
            self.saying_frame.pack_forget()
        else:  # Random
            # Hide both frames
            self.saying_frame.pack_forget()
            self.custom_text_frame.pack_forget()
    
    def on_picture_mode_change(self, event):
        """Handle picture mode dropdown change"""
        mode = self.picture_mode_var.get()
        if mode == "Single":
            self.take_picture_button.config(text="📷\nTake Picture\n(6s Total)")
        elif mode == "2X":
            self.take_picture_button.config(text="📷\n2X Mode\n(6s Total)")
        else:  # 3X
            self.take_picture_button.config(text="📷\n3X Mode\n(6s Total)")
    
    def start_countdown_capture(self):
        """Start the countdown before capturing the photo"""
        self.take_picture_button.config(state='disabled')
        picture_mode = self.picture_mode_var.get()
        
        if picture_mode == "Single":
            # Single photo mode
            self.countdown = 5
            self.update_countdown()
        else:
            # Multi-photo mode (2X or 3X)
            self.multi_photo_images = []
            self.multi_photo_count = 0
            self.countdown = 5
            self.update_multi_photo_countdown()
    
    def update_countdown(self):
        """Update the countdown display"""
        if self.countdown > 0:
            self.countdown_label.config(text=str(self.countdown))
            self.countdown -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.countdown_label.config(text="Smile!")
            self.root.after(1000, self.capture_photo_with_countdown)  # Show Smile! for 1 second, then capture
    
    def update_multi_photo_countdown(self):
        """Update the countdown display for multi-photo mode"""
        target_photos = 2 if self.picture_mode_var.get() == "2X" else 3
        if self.countdown > 0:
            self.countdown_label.config(text=f"Photo {self.multi_photo_count + 1}/{target_photos}\n{self.countdown}")
            self.countdown -= 1
            self.root.after(1000, self.update_multi_photo_countdown)
        else:
            self.countdown_label.config(text="Smile!")
            self.root.after(1000, self.capture_multi_photo)  # Show Smile! for 1 second, then capture
    
    def capture_photo_with_countdown(self):
        """Capture photo after countdown"""
        try:
            camera_index = int(self.camera_var.get().split()[1])
            cap = cv2.VideoCapture(camera_index)
            
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                self.take_picture_button.config(state='normal')
                self.countdown_label.config(text="")
                return
            
            # Capture frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                messagebox.showerror("Error", "Could not capture frame")
                self.take_picture_button.config(state='normal')
                self.countdown_label.config(text="")
                return
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Apply selected filter
            selected_filter = self.filter_var.get()
            actual_filter_name = selected_filter  # Track the actual filter used
            
            if selected_filter == "Random Filter":
                # Apply random filter and get the actual filter name
                filter_names = [name for name in self.filters.keys() if name not in ["None", "Random Filter"]]
                actual_filter_name = random.choice(filter_names)
                if self.filters[actual_filter_name]:
                    pil_image = self.filters[actual_filter_name](pil_image)
            elif selected_filter != "None" and self.filters[selected_filter]:
                pil_image = self.filters[selected_filter](pil_image)
            
            # Add polaroid border and text
            border_mode = self.border_mode_var.get()
            border_image = self.border_image_path.get() if border_mode == "Image Background" else None
            polaroid_image = self.add_polaroid_effect(pil_image, border_mode, border_image)
            
            # Display the result
            self.display_result(polaroid_image)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"polaroid_{actual_filter_name}_{timestamp}.jpg"
            filepath = os.path.join(self.folder_path.get(), filename)
            polaroid_image.save(filepath)
            
            # Store the last saved image path for printing
            self.last_saved_image_path = filepath
            
            self.take_picture_button.config(state='normal')
            self.countdown_label.config(text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.take_picture_button.config(state='normal')
            self.countdown_label.config(text="")
    
    def capture_multi_photo(self):
        """Capture a single photo for multi-photo mode"""
        try:
            camera_index = int(self.camera_var.get().split()[1])
            cap = cv2.VideoCapture(camera_index)
            
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not open camera")
                self.take_picture_button.config(state='normal')
                self.countdown_label.config(text="")
                return
            
            # Capture frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                messagebox.showerror("Error", "Could not capture frame")
                self.take_picture_button.config(state='normal')
                self.countdown_label.config(text="")
                return
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Apply selected filter
            selected_filter = self.filter_var.get()
            if selected_filter == "Random Filter":
                # Apply random filter
                filter_names = [name for name in self.filters.keys() if name not in ["None", "Random Filter"]]
                random_filter_name = random.choice(filter_names)
                if self.filters[random_filter_name]:
                    pil_image = self.filters[random_filter_name](pil_image)
            elif selected_filter != "None" and self.filters[selected_filter]:
                pil_image = self.filters[selected_filter](pil_image)
            
            # Store the image
            self.multi_photo_images.append(pil_image)
            self.multi_photo_count += 1
            
            # Show preview of captured photo
            self.display_result(pil_image)
            
            # Check if we need more photos
            target_photos = 2 if self.picture_mode_var.get() == "2X" else 3
            if self.multi_photo_count < target_photos:
                # Start countdown for next photo
                self.countdown = 5
                self.update_multi_photo_countdown()
            else:
                # All photos captured, create side-by-side polaroid
                self.create_side_by_side_polaroid()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.take_picture_button.config(state='normal')
            self.countdown_label.config(text="")
    
    def create_side_by_side_polaroid(self):
        """Create side-by-side polaroid from captured images"""
        try:
            # Get number of photos
            num_photos = len(self.multi_photo_images)
            picture_mode = self.picture_mode_var.get()
            
            # Create canvas
            border_mode = self.border_mode_var.get()
            border_image = self.border_image_path.get() if border_mode == "Image Background" else None
            
            if border_mode == "Image Background" and border_image and os.path.exists(border_image):
                try:
                    border_bg = Image.open(border_image)
                    border_bg = border_bg.resize((self.polaroid_width, self.polaroid_height), Image.Resampling.LANCZOS)
                    polaroid = border_bg.convert('RGB')
                except Exception as e:
                    print(f"Error loading border image: {e}")
                    polaroid = Image.new('RGB', (self.polaroid_width, self.polaroid_height), 'white')
            else:
                polaroid = Image.new('RGB', (self.polaroid_width, self.polaroid_height), 'white')
            
            if picture_mode == "2X":
                # 2X Mode: Two photos side by side with 0.2 inch separation
                separation = 60  # 0.2 inch at 300 DPI
                image_area_width = self.polaroid_width - 2 * self.border_width - separation
                image_area_height = self.polaroid_height - self.border_width - self.bottom_border
                
                photo_width = image_area_width // 2
                photo_height = image_area_height
                
                # Place photos side by side
                for i, pil_image in enumerate(self.multi_photo_images):
                    # Calculate position with separation
                    x = self.border_width + i * (photo_width + separation)
                    y = self.border_width
                    
                    # Resize photo to fit its area (maintain aspect ratio)
                    original_width, original_height = pil_image.size
                    aspect_ratio = original_width / original_height
                    
                    if aspect_ratio > (photo_width / photo_height):
                        new_width = photo_width
                        new_height = int(photo_width / aspect_ratio)
                    else:
                        new_height = photo_height
                        new_width = int(photo_height * aspect_ratio)
                    
                    photo_resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Center the photo in its area
                    paste_x = x + (photo_width - new_width) // 2
                    paste_y = y + (photo_height - new_height) // 2
                    
                    # Paste photo
                    polaroid.paste(photo_resized, (paste_x, paste_y))
                    
            elif picture_mode == "3X":
                # 3X Mode: One large image on top, two smaller images below
                # Top image gets 60% of space, bottom images get 40% total
                image_area_width = self.polaroid_width - 2 * self.border_width
                image_area_height = self.polaroid_height - self.border_width - self.bottom_border
                
                # Top large image
                top_height = int(image_area_height * 0.6)
                bottom_height = image_area_height - top_height
                
                # Place large image on top
                pil_image = self.multi_photo_images[0]
                original_width, original_height = pil_image.size
                aspect_ratio = original_width / original_height
                
                if aspect_ratio > (image_area_width / top_height):
                    new_width = image_area_width
                    new_height = int(image_area_width / aspect_ratio)
                else:
                    new_height = top_height
                    new_width = int(top_height * aspect_ratio)
                
                photo_resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                paste_x = self.border_width + (image_area_width - new_width) // 2
                paste_y = self.border_width
                polaroid.paste(photo_resized, (paste_x, paste_y))
                
                # Place two smaller images side by side below
                separation = 60  # 0.2 inch at 300 DPI
                bottom_image_width = (image_area_width - separation) // 2
                
                for i in range(2):
                    pil_image = self.multi_photo_images[i + 1]
                    original_width, original_height = pil_image.size
                    aspect_ratio = original_width / original_height
                    
                    if aspect_ratio > (bottom_image_width / bottom_height):
                        new_width = bottom_image_width
                        new_height = int(bottom_image_width / aspect_ratio)
                    else:
                        new_height = bottom_height
                        new_width = int(bottom_height * aspect_ratio)
                    
                    photo_resized = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    x = self.border_width + i * (bottom_image_width + separation)
                    y = self.border_width + top_height
                    
                    paste_x = x + (bottom_image_width - new_width) // 2
                    paste_y = y + (bottom_height - new_height) // 2
                    
                    polaroid.paste(photo_resized, (paste_x, paste_y))
            
            # Add sticker if selected
            sticker_text = self.sticker_var.get()
            if sticker_text != "None":
                self.apply_sticker(polaroid, sticker_text)
            
            # Add text at bottom
            draw = ImageDraw.Draw(polaroid)
            text_mode = self.text_mode_var.get()
            
            if text_mode == "Random":
                saying = random.choice(self.random_sayings)
            elif text_mode == "From List":
                saying = self.saying_var.get()
            else:  # Custom
                saying = self.custom_text_var.get()
                if not saying:
                    saying = random.choice(self.random_sayings)
            
            current_date = datetime.now().strftime("%B %d, %Y")
            text_color = self.text_color_var.get()
            font_size = int(self.font_size_var.get())
            
            comic_path = 'C:\\Windows\\Fonts\\Comicbd.ttf'
            font = ImageFont.truetype(comic_path, font_size)
            date_font_size = int(font_size * 0.8)
            date_font = ImageFont.truetype(comic_path, date_font_size)
            
            center_x = self.polaroid_width // 2
            
            # Adjust text position based on picture mode
            if self.picture_mode_var.get() == "3X":
                # Move text lower for 3X mode to avoid overlapping with images
                text_y = 1050
                date_y = 1110
            else:
                # Standard position for Single and 2X modes
                text_y = 950
                date_y = 1010
            
            draw.text((center_x, text_y), saying, fill=text_color, font=font, anchor='mm')
            draw.text((center_x, date_y), current_date, fill=text_color, font=date_font, anchor='mm')
            
            # Display the result
            self.display_result(polaroid)
            
            # Save image
            selected_filter = self.filter_var.get()
            actual_filter_name = selected_filter
            
            # If Random Filter, pick a random filter name for the filename
            if selected_filter == "Random Filter":
                filter_names = [name for name in self.filters.keys() if name not in ["None", "Random Filter"]]
                actual_filter_name = random.choice(filter_names)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mode_suffix = self.picture_mode_var.get().lower()
            filename = f"polaroid_{mode_suffix}_{actual_filter_name}_{timestamp}.jpg"
            filepath = os.path.join(self.folder_path.get(), filename)
            polaroid.save(filepath)
            
            # Store the last saved image path for printing
            self.last_saved_image_path = filepath
            
            self.take_picture_button.config(state='normal')
            self.countdown_label.config(text="")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.take_picture_button.config(state='normal')
            self.countdown_label.config(text="")
    
    def display_result(self, image):
        """Display the captured image in the result label"""
        # Resize for display (maintain aspect ratio to fit in display area)
        display_width = 525
        display_height = 630  # Standard polaroid aspect ratio
        
        # Calculate aspect ratio
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        # Calculate display dimensions maintaining aspect ratio
        if aspect_ratio > (display_width / display_height):
            # Width is the limiting factor
            new_width = display_width
            new_height = int(display_width / aspect_ratio)
        else:
            # Height is the limiting factor
            new_height = display_height
            new_width = int(display_height * aspect_ratio)
        
        image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo_image = PIL.ImageTk.PhotoImage(image_resized)
        
        # Update the result label
        self.result_label.config(image=photo_image)
        self.result_label.image = photo_image  # Keep a reference
    
    def add_polaroid_effect(self, image, border_mode="Solid Color", border_image=None):
        """Add polaroid border and random saying with standard polaroid dimensions"""
        
        # Resize image to fit within polaroid dimensions (maintaining aspect ratio)
        image_width = self.polaroid_width - 2 * self.border_width
        image_height = self.polaroid_height - self.border_width - self.bottom_border  # 250px bottom border for text
        
        # Calculate aspect ratio
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        # Calculate dimensions maintaining aspect ratio
        if aspect_ratio > (image_width / image_height):
            # Width is the limiting factor
            new_width = image_width
            new_height = int(image_width / aspect_ratio)
        else:
            # Height is the limiting factor
            new_height = image_height
            new_width = int(image_height * aspect_ratio)
        
        # Resize image
        image_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate centering offsets
        x_offset = (image_width - new_width) // 2
        y_offset = (image_height - new_height) // 2
        
        # Create background based on mode
        if border_mode == "Image Background" and border_image and os.path.exists(border_image):
            try:
                # Load and resize the border image to fit the polaroid dimensions
                border_bg = Image.open(border_image)
                border_bg = border_bg.resize((self.polaroid_width, self.polaroid_height), Image.Resampling.LANCZOS)
                polaroid = border_bg.convert('RGB')
            except Exception as e:
                # Fallback to solid color if image loading fails
                print(f"Error loading border image: {e}")
                polaroid = Image.new('RGB', (self.polaroid_width, self.polaroid_height), 'white')
        else:
            # Create new image with white background (standard polaroid)
            polaroid = Image.new('RGB', (self.polaroid_width, self.polaroid_height), 'white')
        
        # Paste resized image in the center-top area
        paste_x = self.border_width + x_offset
        paste_y = self.border_width + y_offset
        polaroid.paste(image_resized, (paste_x, paste_y))
        
        # Add saying and current date based on text mode
        draw = ImageDraw.Draw(polaroid)
        text_mode = self.text_mode_var.get()
        
        if text_mode == "Random":
            saying = random.choice(self.random_sayings)
        elif text_mode == "From List":
            saying = self.saying_var.get()
        else:  # Custom
            saying = self.custom_text_var.get()
            if not saying:  # Fallback to random if custom text is empty
                saying = random.choice(self.random_sayings)
        
        # Get current date for second line
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Get selected text color
        text_color = self.text_color_var.get()
        
        # Get selected font size
        font_size = int(self.font_size_var.get())
        
        # Load Comic font at selected size for main text (Windows-specific path)
        comic_path = 'C:\\Windows\\Fonts\\Comicbd.ttf'
        font = ImageFont.truetype(comic_path, font_size)
        
        # Load Comic font at 80% of main font size for date
        date_font_size = int(font_size * 0.8)
        date_font = ImageFont.truetype(comic_path, date_font_size)
        
        # Center the text horizontally
        center_x = self.polaroid_width // 2  # 525 (center of 1050)
        
        # Position text in the white area below the image
        text_y = 950  # In white area
        date_y = 1010  # Below saying
        
        # Draw centered text with selected color
        draw.text((center_x, text_y), saying, fill=text_color, font=font, anchor='mm')
        draw.text((center_x, date_y), current_date, fill=text_color, font=date_font, anchor='mm')
        
        # Add sticker if selected
        sticker_text = self.sticker_var.get()
        if sticker_text != "None":
            self.apply_sticker(polaroid, sticker_text)
        
        return polaroid
    
    def apply_black_white(self, image):
        """Convert image to black and white"""
        return image.convert('L').convert('RGB')
    
    def apply_cinematic(self, image):
        """Apply cinematic filter with enhanced contrast and slight color grading"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Enhance color saturation slightly
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        # Add slight warmth
        r, g, b = image.split()
        r = r.point(lambda x: min(255, x * 1.1))
        image = Image.merge('RGB', (r, g, b))
        
        return image
    
    def apply_vintage(self, image):
        """Apply vintage filter with sepia tone and reduced contrast"""
        # Convert to grayscale
        gray = image.convert('L')
        
        # Apply sepia tone
        r, g, b = gray, gray, gray
        r = r.point(lambda x: min(255, x * 1.1))
        g = g.point(lambda x: min(255, x * 0.9))
        b = b.point(lambda x: min(255, x * 0.7))
        image = Image.merge('RGB', (r, g, b))
        
        # Reduce contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.8)
        
        # Add slight blur
        image = image.filter(ImageFilter.SMOOTH)
        
        return image
    
    def apply_watercolor(self, image):
        """Apply watercolor effect with blur and color enhancement"""
        # Apply blur
        image = image.filter(ImageFilter.SMOOTH_MORE)
        
        # Enhance color
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)
        
        # Reduce contrast for softer look
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.8)
        
        return image
    
    def apply_cross_hatch(self, image):
        """Apply cross-hatch effect using edge detection"""
        # Convert to grayscale
        gray = image.convert('L')
        
        # Apply edge detection
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # Invert edges
        edges = Image.eval(edges, lambda x: 255 - x)
        
        # Blend with original
        edges_rgb = edges.convert('RGB')
        image = Image.blend(image, edges_rgb, 0.5)
        
        return image
    
    def apply_glitch(self, image):
        """Apply glitch effect with color channel shifting"""
        r, g, b = image.split()
        
        # Shift channels
        r = r.transform(image.size, Image.AFFINE, (1, 0, 10, 0, 1, 0))
        b = b.transform(image.size, Image.AFFINE, (1, 0, -10, 0, 1, 0))
        
        image = Image.merge('RGB', (r, g, b))
        
        return image
    
    def apply_beauty_mode(self, image):
        """Apply beauty mode with skin smoothing and brightening"""
        # Brighten the image
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.1)
        
        # Smooth the image slightly
        image = image.filter(ImageFilter.SMOOTH)
        
        # Enhance color saturation slightly
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        # Reduce contrast for softer look
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.9)
        
        # Add subtle sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def apply_cartoon(self, image):
        """Apply cartoon filter with edge detection and color quantization"""
        # Convert to grayscale for edge detection
        gray = image.convert('L')
        
        # Apply edge detection
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # Invert edges so they appear as black lines
        edges = Image.eval(edges, lambda x: 255 - x)
        
        # Enhance edges
        edges = edges.filter(ImageFilter.SHARPEN)
        
        # Color quantization - reduce colors for cartoon effect
        # Posterize to reduce color palette
        quantized = image.quantize(colors=8)
        quantized = quantized.convert('RGB')
        
        # Enhance brightness for bright colors
        enhancer = ImageEnhance.Brightness(quantized)
        quantized = enhancer.enhance(1.2)
        
        # Enhance color saturation for vibrant cartoon look
        enhancer = ImageEnhance.Color(quantized)
        quantized = enhancer.enhance(2.0)
        
        # Enhance contrast for bold colors
        enhancer = ImageEnhance.Contrast(quantized)
        quantized = enhancer.enhance(1.5)
        
        # Combine edges with quantized image
        # Convert edges to RGB
        edges_rgb = edges.convert('RGB')
        
        # Blend edges with quantized image
        cartoon = Image.blend(quantized, edges_rgb, 0.3)
        
        return cartoon
    
    def apply_oil_painting(self, image):
        """Apply oil painting filter with brush stroke simulation"""
        # Apply median filter to smooth colors
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        # Enhance contrast for oil paint look
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        # Apply slight blur for painterly effect
        image = image.filter(ImageFilter.SMOOTH)
        
        # Apply edge enhancement to preserve details
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        
        return image
    
    def apply_pencil_sketch(self, image):
        """Apply pencil sketch filter"""
        # Convert to grayscale
        gray = image.convert('L')
        
        # Apply edge detection
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # Invert edges to get black lines on white
        edges = Image.eval(edges, lambda x: 255 - x)
        
        # Enhance edges for sharper pencil lines
        edges = edges.filter(ImageFilter.SHARPEN)
        
        # Convert back to RGB
        sketch = edges.convert('RGB')
        
        return sketch
    
    def apply_charcoal(self, image):
        """Apply charcoal drawing filter"""
        # Convert to grayscale
        gray = image.convert('L')
        
        # Apply edge detection
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        # Invert edges
        edges = Image.eval(edges, lambda x: 255 - x)
        
        # Apply strong contrast for dark charcoal look
        enhancer = ImageEnhance.Contrast(edges)
        edges = enhancer.enhance(2.0)
        
        # Darken the image
        edges = Image.eval(edges, lambda x: int(x * 0.7))
        
        # Convert back to RGB
        charcoal = edges.convert('RGB')
        
        return charcoal
    
    def apply_pastel(self, image):
        """Apply pastel filter with soft colors"""
        # Reduce color saturation for soft pastel look
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.5)
        
        # Increase brightness for light pastel colors
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.3)
        
        # Reduce contrast for soft appearance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(0.8)
        
        # Apply slight blur for soft effect
        image = image.filter(ImageFilter.SMOOTH)
        
        return image
    
    def apply_pop_art(self, image):
        """Apply pop art filter with bold, high-contrast colors like Warhol"""
        # Reduce color palette for pop art effect
        quantized = image.quantize(colors=4)
        quantized = quantized.convert('RGB')
        
        # Enhance contrast significantly
        enhancer = ImageEnhance.Contrast(quantized)
        quantized = enhancer.enhance(2.0)
        
        # Enhance color saturation for bold colors
        enhancer = ImageEnhance.Color(quantized)
        quantized = enhancer.enhance(2.0)
        
        # Apply sharpening for crisp edges
        quantized = quantized.filter(ImageFilter.SHARPEN)
        
        return quantized
    
    def apply_neon(self, image):
        """Apply neon filter with glowing effect"""
        # Enhance color saturation for neon look
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(2.5)
        
        # Increase contrast for vibrant colors
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Increase brightness for glow effect
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        
        # Apply edge enhancement to make colors pop
        image = image.filter(ImageFilter.EDGE_ENHANCE)
        
        # Apply slight blur for glow
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        
        return image
    
    def apply_cyberpunk(self, image):
        """Apply cyberpunk filter with futuristic color grading"""
        # Split into RGB channels
        r, g, b = image.split()
        
        # Enhance red and blue channels for cyberpunk look
        r = r.point(lambda x: min(255, int(x * 1.3)))
        b = b.point(lambda x: min(255, int(x * 1.4)))
        
        # Slightly reduce green for cool tone
        g = g.point(lambda x: int(x * 0.9))
        
        # Merge channels back
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.3)
        
        # Apply slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def apply_blur(self, image):
        """Apply soft focus/blur effect"""
        return image.filter(ImageFilter.GaussianBlur(radius=3))
    
    def apply_sharpen(self, image):
        """Apply enhanced sharpness"""
        return image.filter(ImageFilter.SHARPEN)
    
    def apply_emboss(self, image):
        """Apply 3D raised effect"""
        return image.filter(ImageFilter.EMBOSS)
    
    def apply_edge_detect(self, image):
        """Show only edges"""
        gray = image.convert('L')
        edges = gray.filter(ImageFilter.FIND_EDGES)
        return edges.convert('RGB')
    
    def apply_solarize(self, image):
        """Apply partial color inversion"""
        return ImageOps.solarize(image, threshold=128)
    
    def apply_pixelate(self, image):
        """Apply retro pixel art effect"""
        # Small size for pixelation
        small_size = (image.width // 10, image.height // 10)
        pixelated = image.resize(small_size, Image.NEAREST)
        # Scale back up
        return pixelated.resize(image.size, Image.NEAREST)
    
    def apply_hdr(self, image):
        """Apply high dynamic range simulation"""
        # Enhance contrast significantly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.8)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)
        
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        
        # Apply sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def apply_vignette(self, image):
        """Apply dark edges, bright center"""
        # Create a gradient mask
        width, height = image.size
        mask = Image.new('L', (width, height), 0)
        
        # Draw radial gradient
        center_x, center_y = width // 2, height // 2
        max_radius = min(width, height) // 2
        
        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                normalized_distance = distance / max_radius
                brightness = int(255 * (1 - normalized_distance ** 2))
                mask.putpixel((x, y), brightness)
        
        # Apply vignette using the mask
        vignette = Image.composite(image, Image.new('RGB', image.size, 'black'), mask)
        return vignette
    
    def apply_film_grain(self, image):
        """Add noise/grain texture"""
        # Add random noise
        import random
        pixels = image.load()
        width, height = image.size
        
        for y in range(height):
            for x in range(width):
                # Add random noise
                noise = random.randint(-30, 30)
                r, g, b = pixels[x, y]
                pixels[x, y] = (
                    max(0, min(255, r + noise)),
                    max(0, min(255, g + noise)),
                    max(0, min(255, b + noise))
                )
        
        return image
    
    def apply_mirror(self, image):
        """Apply horizontal mirror effect"""
        return ImageOps.mirror(image)
    
    def apply_random_filter(self, image):
        """Apply a random filter from the available filters"""
        # Get all filter names except "None" and "Random Filter"
        filter_names = [name for name in self.filters.keys() if name not in ["None", "Random Filter"]]
        
        # Randomly select a filter
        random_filter_name = random.choice(filter_names)
        random_filter = self.filters[random_filter_name]
        
        # Apply the random filter
        if random_filter:
            return random_filter(image)
        else:
            return image
    
    def apply_autumn(self, image):
        """Apply orange/brown tones"""
        r, g, b = image.split()
        
        # Enhance red and reduce blue for autumn look
        r = r.point(lambda x: min(255, int(x * 1.2)))
        b = b.point(lambda x: int(x * 0.7))
        
        # Slightly reduce green
        g = g.point(lambda x: int(x * 0.9))
        
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        return image
    
    def apply_winter(self, image):
        """Apply cool blue tones"""
        r, g, b = image.split()
        
        # Enhance blue and reduce red for winter look
        b = b.point(lambda x: min(255, int(x * 1.3)))
        r = r.point(lambda x: int(x * 0.8))
        
        # Slightly enhance green
        g = g.point(lambda x: min(255, int(x * 1.1)))
        
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def apply_summer(self, image):
        """Apply bright, warm colors"""
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.3)
        
        # Enhance color saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.4)
        
        # Enhance red and green for warm look
        r, g, b = image.split()
        r = r.point(lambda x: min(255, int(x * 1.15)))
        g = g.point(lambda x: min(255, int(x * 1.1)))
        image = Image.merge('RGB', (r, g, b))
        
        return image
    
    def apply_spring(self, image):
        """Apply fresh green tones"""
        r, g, b = image.split()
        
        # Enhance green for spring look
        g = g.point(lambda x: min(255, int(x * 1.3)))
        
        # Slightly enhance blue
        b = b.point(lambda x: min(255, int(x * 1.1)))
        
        # Slightly reduce red
        r = r.point(lambda x: int(x * 0.9))
        
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.15)
        
        return image
    
    def apply_sunset(self, image):
        """Apply warm golden hour colors"""
        r, g, b = image.split()
        
        # Enhance red and orange tones
        r = r.point(lambda x: min(255, int(x * 1.4)))
        g = g.point(lambda x: min(255, int(x * 1.1)))
        
        # Reduce blue for warm sunset look
        b = b.point(lambda x: int(x * 0.6))
        
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Enhance saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)
        
        return image
    
    def apply_night(self, image):
        """Apply dark, moody tones"""
        # Reduce brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(0.6)
        
        # Enhance blue for night look
        r, g, b = image.split()
        b = b.point(lambda x: min(255, int(x * 1.2)))
        r = r.point(lambda x: int(x * 0.8))
        g = g.point(lambda x: int(x * 0.8))
        image = Image.merge('RGB', (r, g, b))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)
        
        return image
    
    def apply_sticker(self, polaroid, sticker_text):
        """Apply a cartoon-style sticker to the polaroid image with random selection, multiple shapes, and dynamic styling"""
        draw = ImageDraw.Draw(polaroid)
        
        # Handle Random selection
        if sticker_text == "Random":
            # Randomly select from sticker texts (excluding "Random" and "None")
            available_stickers = [s for s in self.sticker_texts if s not in ["Random", "None"]]
            sticker_text = random.choice(available_stickers)
        
        # Skip if None
        if sticker_text == "None":
            return
        
        # Get dynamic styling from UI
        text_color_name = self.text_color_var.get()
        font_size = int(self.font_size_var.get())
        
        # Convert color name to RGB
        color_map = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "pink": (255, 192, 203),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "gray": (128, 128, 128),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
            "green": (0, 128, 0)
        }
        text_color = color_map.get(text_color_name, (0, 0, 0))
        
        # Get selected shape (use Random if selected)
        selected_shape = self.sticker_shape_var.get()
        if selected_shape == "Random":
            shape = random.choice([s for s in self.sticker_shapes if s != "Random"])
        else:
            shape = selected_shape
        
        # Get selected fill color and convert to RGB
        fill_color_name = self.sticker_fill_color_var.get()
        fill_color_map = {
            "Hot Pink": (255, 105, 180),
            "Blue": (0, 0, 255),
            "Yellow": (255, 255, 0),
            "Green": (0, 128, 0),
            "Lime": (50, 205, 50),
            "White": (255, 255, 255),
            "Grey": (128, 128, 128),
            "Purple": (128, 0, 128)
        }
        fill_color = fill_color_map.get(fill_color_name, (255, 105, 180))
        
        # Sticker configuration
        sticker_font_size = max(24, min(font_size, 48))  # Scale font size but keep within reasonable range
        padding = 40  # Increased padding for larger shapes
        border_width = 4  # Thicker border for larger shapes
        border_color = (0, 0, 0)  # Black border
        
        # Load comic font
        comic_path = 'C:\\Windows\\Fonts\\Comicbd.ttf'
        try:
            font = ImageFont.truetype(comic_path, sticker_font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate sticker position (top right corner of image area)
        image_area_top = self.border_width
        image_area_left = self.border_width
        image_area_right = self.polaroid_width - self.border_width
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), sticker_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate sticker dimensions based on shape (make them larger)
        if shape == "Bubble":
            sticker_width = text_width + 3 * padding
            sticker_height = text_height + 3 * padding
        elif shape == "Star":
            sticker_width = max(text_width + 3 * padding, 180)
            sticker_height = max(text_height + 3 * padding, 180)
        elif shape == "Cloud":
            sticker_width = text_width + 4 * padding
            sticker_height = text_height + 3 * padding
        elif shape == "Heart":
            sticker_width = max(text_width + 3 * padding, 160)
            sticker_height = max(text_height + 3 * padding, 160)
        
        # Position sticker in top right of image area (allow overlap on image)
        sticker_x = image_area_right - sticker_width + 10  # Allow overlap on right edge
        sticker_y = image_area_top - 10  # Allow overlap on top edge
        
        # Draw based on shape
        if shape == "Bubble":
            self._draw_bubble_sticker(draw, sticker_x, sticker_y, sticker_width, sticker_height, 
                                     sticker_text, font, text_color, border_color, border_width, fill_color)
        elif shape == "Star":
            self._draw_star_sticker(draw, sticker_x, sticker_y, sticker_width, sticker_height,
                                   sticker_text, font, text_color, border_color, border_width, fill_color)
        elif shape == "Cloud":
            self._draw_cloud_sticker(draw, sticker_x, sticker_y, sticker_width, sticker_height,
                                    sticker_text, font, text_color, border_color, border_width, fill_color)
        elif shape == "Heart":
            self._draw_heart_sticker(draw, sticker_x, sticker_y, sticker_width, sticker_height,
                                    sticker_text, font, text_color, border_color, border_width, fill_color)
    
    def _draw_bubble_sticker(self, draw, x, y, width, height, text, font, text_color, border_color, border_width, fill_color):
        """Draw speech bubble sticker"""
        # Draw rounded rectangle with larger corner radius
        draw.rounded_rectangle(
            [x, y, x + width, y + height],
            radius=25,  # Larger corner radius for larger bubble
            fill=fill_color,
            outline=border_color,
            width=border_width
        )
        
        # Draw speech bubble tail (larger for larger bubble)
        tail_width = 25
        tail_height = 35
        tail_x = x + width // 2
        tail_y = y + height
        
        tail_points = [
            (tail_x - tail_width // 2, tail_y),
            (tail_x + tail_width // 2, tail_y),
            (tail_x, tail_y + tail_height)
        ]
        draw.polygon(tail_points, fill=fill_color, outline=border_color, width=border_width)
        
        # Draw text centered
        text_x = x + width // 2
        text_y = y + height // 2
        draw.text((text_x, text_y), text, fill=text_color, font=font, anchor='mm')
    
    def _draw_star_sticker(self, draw, x, y, width, height, text, font, text_color, border_color, border_width, fill_color):
        """Draw star-shaped sticker"""
        # Calculate star points
        cx = x + width // 2
        cy = y + height // 2
        outer_radius = min(width, height) // 2
        inner_radius = outer_radius * 0.4
        
        points = []
        for i in range(10):
            angle = i * 36 - 90  # Start from top
            angle_rad = math.radians(angle)
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = cx + radius * math.cos(angle_rad)
            py = cy + radius * math.sin(angle_rad)
            points.append((px, py))
        
        draw.polygon(points, fill=fill_color, outline=border_color, width=border_width)
        
        # Draw text centered
        draw.text((cx, cy), text, fill=text_color, font=font, anchor='mm')
    
    def _draw_cloud_sticker(self, draw, x, y, width, height, text, font, text_color, border_color, border_width, fill_color):
        """Draw cloud-shaped sticker"""
        # Draw cloud using multiple overlapping circles (larger circles)
        cx = x + width // 2
        cy = y + height // 2
        
        # Main cloud circles (increased sizes)
        circles = [
            (cx, cy - height * 0.25, height * 0.45),  # Top center (larger)
            (cx - width * 0.3, cy, height * 0.4),   # Left (larger)
            (cx + width * 0.3, cy, height * 0.4),   # Right (larger)
            (cx, cy + height * 0.25, height * 0.35),  # Bottom center (larger)
            (cx - width * 0.15, cy - height * 0.1, height * 0.3),  # Top left
            (cx + width * 0.15, cy - height * 0.1, height * 0.3),  # Top right
        ]
        
        for circle_x, circle_y, radius in circles:
            draw.ellipse(
                [circle_x - radius, circle_y - radius, circle_x + radius, circle_y + radius],
                fill=fill_color,
                outline=border_color,
                width=border_width
            )
        
        # Draw text centered
        draw.text((cx, cy), text, fill=text_color, font=font, anchor='mm')
    
    def _draw_heart_sticker(self, draw, x, y, width, height, text, font, text_color, border_color, border_width, fill_color):
        """Draw heart-shaped sticker"""
        # Calculate heart shape points
        cx = x + width // 2
        cy = y + height // 2
        scale = min(width, height) // 2
        
        # Create heart shape using bezier-like curves with polygons
        points = []
        num_points = 50
        for i in range(num_points):
            t = 2 * math.pi * i / num_points
            # Heart parametric equation
            heart_x = 16 * math.sin(t) ** 3
            heart_y = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
            
            px = cx + heart_x * scale / 16
            py = cy + heart_y * scale / 16
            points.append((px, py))
        
        draw.polygon(points, fill=fill_color, outline=border_color, width=border_width)
        
        # Draw text centered
        draw.text((cx, cy), text, fill=text_color, font=font, anchor='mm')
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PolaroidCameraApp()
    app.run()
