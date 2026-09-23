import cv2
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random
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
            "Cheers to 2025!",
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
            "Class of 2025!",
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
        
        # Text color configuration
        self.text_color = "black"  # Default text color
        self.text_colors = ["black", "white", "pink", "red", "blue", "gray", "yellow", "purple", "green"]
        
        # Font size configuration
        self.font_size = 36  # Default font size for main text
        self.font_sizes = [16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76]  # 5pt increments from 16
        
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
            "Black & White": self.apply_black_white,
            "Cinematic": self.apply_cinematic,
            "Vintage": self.apply_vintage,
            "Watercolor": self.apply_watercolor,
            "Cross-hatch": self.apply_cross_hatch,
            "Glitch": self.apply_glitch,
            "Beauty Mode": self.apply_beauty_mode,
            "Cartoon": self.apply_cartoon
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
        
        # Main controls container
        controls_frame = ttk.Frame(self.root)
        controls_frame.pack(padx=5, pady=5, fill='x')
        
        # Row 1: Camera, Border Mode, Filter (side by side)
        row1 = ttk.Frame(controls_frame)
        row1.pack(fill='x', pady=2)
        
        # Camera selection
        camera_frame = ttk.LabelFrame(row1, text="Camera")
        camera_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.camera_var = tk.StringVar()
        self.camera_combo = ttk.Combobox(camera_frame, textvariable=self.camera_var, state="readonly")
        self.camera_combo['values'] = [f"Camera {i}" for i in self.get_available_cameras()]
        if self.camera_combo['values']:
            self.camera_combo.current(0)
        self.camera_combo.pack(padx=2, pady=2, fill='x')
        
        # Border mode selection
        self.border_mode_frame = ttk.LabelFrame(row1, text="Border")
        self.border_mode_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.border_mode_var = tk.StringVar(value="Solid Color")
        border_mode_combo = ttk.Combobox(self.border_mode_frame, textvariable=self.border_mode_var,
                                        values=["Solid Color", "Image Background"], state="readonly")
        border_mode_combo.current(0)
        border_mode_combo.pack(padx=2, pady=2, fill='x')
        border_mode_combo.bind("<<ComboboxSelected>>", self.on_border_mode_change)
        
        # Filter selection
        filter_frame = ttk.LabelFrame(row1, text="Filter")
        filter_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.filter_var = tk.StringVar(value="None")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                    values=list(self.filters.keys()), state="readonly")
        filter_combo.current(0)
        filter_combo.pack(padx=2, pady=2, fill='x')
        
        # Border image selection (hidden by default)
        self.border_image_frame = ttk.LabelFrame(controls_frame, text="Border Image")
        self.border_image_path = tk.StringVar()
        self.border_image_entry = ttk.Entry(self.border_image_frame, textvariable=self.border_image_path)
        self.border_image_entry.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        border_image_button = ttk.Button(self.border_image_frame, text="Browse", command=self.browse_border_image)
        border_image_button.pack(side='left', padx=2, pady=2)
        
        # Initially hide the border image frame
        self.border_image_frame.pack_forget()
        
        # Row 2: Text Selection, Text Color, Font Size (side by side)
        row2 = ttk.Frame(controls_frame)
        row2.pack(fill='x', pady=2)
        
        # Text selection
        self.text_frame = ttk.LabelFrame(row2, text="Text")
        self.text_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.text_mode_var = tk.StringVar(value="Random")
        text_mode_combo = ttk.Combobox(self.text_frame, textvariable=self.text_mode_var,
                                      values=["Random", "From List", "Custom"], state="readonly")
        text_mode_combo.current(0)
        text_mode_combo.pack(padx=2, pady=2, fill='x')
        text_mode_combo.bind("<<ComboboxSelected>>", self.on_text_mode_change)
        
        # Text color selection
        color_frame = ttk.LabelFrame(row2, text="Color")
        color_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.text_color_var = tk.StringVar(value="black")
        color_combo = ttk.Combobox(color_frame, textvariable=self.text_color_var,
                                   values=self.text_colors, state="readonly")
        color_combo.current(0)
        color_combo.pack(padx=2, pady=2, fill='x')
        
        # Font size selection
        size_frame = ttk.LabelFrame(row2, text="Size")
        size_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.font_size_var = tk.StringVar(value="36")
        size_combo = ttk.Combobox(size_frame, textvariable=self.font_size_var,
                                  values=[str(s) for s in self.font_sizes], state="readonly")
        size_combo.current(4)  # Default to 36pt (index 4)
        size_combo.pack(padx=2, pady=2, fill='x')
        
        # Saying selection from list (hidden by default)
        self.saying_frame = ttk.LabelFrame(controls_frame, text="Select Saying")
        self.saying_var = tk.StringVar()
        self.saying_combo = ttk.Combobox(self.saying_frame, textvariable=self.saying_var,
                                         values=self.random_sayings, state="readonly")
        if self.saying_combo['values']:
            self.saying_combo.current(0)
        self.saying_combo.pack(padx=2, pady=2, fill='x')
        self.saying_frame.pack_forget()
        
        # Custom text entry (hidden by default)
        self.custom_text_frame = ttk.LabelFrame(controls_frame, text="Custom Message")
        self.custom_text_var = tk.StringVar()
        self.custom_text_entry = ttk.Entry(self.custom_text_frame, textvariable=self.custom_text_var)
        self.custom_text_entry.pack(padx=2, pady=2, fill='x')
        self.custom_text_frame.pack_forget()
        
        # Row 3: Print Settings and Output Folder (side by side)
        row3 = ttk.Frame(controls_frame)
        row3.pack(fill='x', pady=2)
        
        # Print settings
        print_frame = ttk.LabelFrame(row3, text="Print")
        print_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.paper_size_var = tk.StringVar(value="4x6")
        paper_size_combo = ttk.Combobox(print_frame, textvariable=self.paper_size_var,
                                        values=list(self.paper_sizes.keys()), state="readonly")
        paper_size_combo.current(1)  # Default to 4x6 (index 1)
        paper_size_combo.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        print_button = ttk.Button(print_frame, text="Print", command=self.print_image)
        print_button.pack(side='left', padx=2, pady=2)
        
        # Output folder selection
        folder_frame = ttk.LabelFrame(row3, text="Folder")
        folder_frame.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        self.folder_path = tk.StringVar(value=self.default_picture_folder)
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path)
        folder_entry.pack(side='left', padx=2, pady=2, fill='x', expand=True)
        
        browse_button = ttk.Button(folder_frame, text="Browse", command=self.browse_folder)
        browse_button.pack(side='left', padx=2, pady=2)
        
        # Take picture button (prominent location)
        self.take_picture_button = ttk.Button(self.root, text="Take Picture (5s Countdown)", 
                                             command=self.start_countdown_capture)
        self.take_picture_button.pack(pady=5)
        
        # Result display section
        result_frame = ttk.LabelFrame(self.root, text="Result")
        result_frame.pack(padx=5, pady=5, fill='both', expand=True)
        
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
            
            messagebox.showinfo("Print", f"Image sent to printer for {paper_size} paper!")
            
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
    
    def start_countdown_capture(self):
        """Start the countdown before capturing the photo"""
        self.take_picture_button.config(state='disabled')
        self.countdown = 5
        self.update_countdown()
    
    def update_countdown(self):
        """Update the countdown display"""
        if self.countdown > 0:
            self.countdown_label.config(text=str(self.countdown))
            self.countdown -= 1
            self.root.after(1000, self.update_countdown)
        else:
            self.countdown_label.config(text="Smile!")
            self.root.after(1000, self.capture_photo_with_countdown)
    
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
            if selected_filter != "None" and self.filters[selected_filter]:
                pil_image = self.filters[selected_filter](pil_image)
            
            # Add polaroid border and text
            border_mode = self.border_mode_var.get()
            border_image = self.border_image_path.get() if border_mode == "Image Background" else None
            polaroid_image = self.add_polaroid_effect(pil_image, border_mode, border_image)
            
            # Display the result
            self.display_result(polaroid_image)
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"polaroid_{selected_filter}_{timestamp}.jpg"
            filepath = os.path.join(self.folder_path.get(), filename)
            polaroid_image.save(filepath)
            
            # Store the last saved image path for printing
            self.last_saved_image_path = filepath
            
            messagebox.showinfo("Success", f"Photo saved to {filepath}")
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
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PolaroidCameraApp()
    app.run()
