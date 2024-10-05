import tkinter as tk
import math
import random
import json
from tkinter import Checkbutton, IntVar, filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw
from tkinter import ttk

# Function to draw a rounded cap at branch splits
def draw_rounded_cap(canvas, x, y, radius, color):
    """
    Draws a rounded cap (circle) at the end of each branch split.
    """
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)

# Function to recursively draw a tree on a canvas
def draw_tree(canvas, x, y, angle, length, depth, angle_variation, length_factor,
              randomness, thickness, branch_color, angle_randomness, length_randomness):
    """
    Recursively draws a fractal tree on the given canvas.
    """
    if depth > 0:
        x_end = x + int(math.cos(angle) * length * random.uniform(1 - length_randomness, 1 + length_randomness))
        y_end = y + int(math.sin(angle) * length * random.uniform(1 - length_randomness, 1 + length_randomness))

        # Draw the branch on canvas
        canvas.create_line(x, y, x_end, y_end, fill=branch_color, width=int(thickness))

        # Draw rounded cap at branching points, except for the final branches
        if depth != 1:
            draw_rounded_cap(canvas, x_end, y_end, int(thickness / 2), branch_color)

        # Recursive calls with random variations in angle and length
        draw_tree(canvas, x_end, y_end, angle - math.radians(angle_variation * random.uniform(1 - angle_randomness, 1 + angle_randomness)),
                  length * length_factor, depth - 1, angle_variation, length_factor, randomness, thickness * 0.7,
                  branch_color, angle_randomness, length_randomness)

        draw_tree(canvas, x_end, y_end, angle + math.radians(angle_variation * random.uniform(1 - angle_randomness, 1 + angle_randomness)),
                  length * length_factor, depth - 1, angle_variation, length_factor, randomness, thickness * 0.7,
                  branch_color, angle_randomness, length_randomness)

# Function to recursively draw a tree on an image (for exporting)
def draw_tree_on_image(draw, x, y, angle, length, depth, angle_variation, length_factor,
                       randomness, thickness, branch_color, angle_randomness, length_randomness):
    """
    Recursively draws a fractal tree on an image (for export).
    """
    if depth > 0:
        x_end = x + int(math.cos(angle) * length * random.uniform(1 - length_randomness, 1 + length_randomness))
        y_end = y + int(math.sin(angle) * length * random.uniform(1 - length_randomness, 1 + length_randomness))

        # Draw the branch on the image
        draw.line([x, y, x_end, y_end], fill=branch_color, width=int(thickness))

        # Recursive calls with random variations in angle and length
        draw_tree_on_image(draw, x_end, y_end, angle - math.radians(angle_variation * random.uniform(1 - angle_randomness, 1 + angle_randomness)),
                           length * length_factor, depth - 1, angle_variation, length_factor, randomness, thickness * 0.7,
                           branch_color, angle_randomness, length_randomness)

        draw_tree_on_image(draw, x_end, y_end, angle + math.radians(angle_variation * random.uniform(1 - angle_randomness, 1 + angle_randomness)),
                           length * length_factor, depth - 1, angle_variation, length_factor, randomness, thickness * 0.7,
                           branch_color, angle_randomness, length_randomness)

# Function to update the canvas with new tree parameters
def update_tree():
    """
    Clears the canvas and draws a new fractal tree based on slider values.
    """
    canvas.delete("all")  # Clear the canvas

    depth = depth_slider.get()
    angle_variation = angle_slider.get()
    length_factor = length_factor_slider.get() / 100
    initial_length = length_slider.get()
    randomness = randomness_slider.get() / 100
    branch_thickness = thickness_slider.get()
    branch_color = f"#{branch_color_slider.get():02x}6540"  # Brownish branch color
    angle_randomness = angle_randomness_slider.get() / 100
    length_randomness = length_randomness_slider.get() / 100

    draw_tree(canvas, 400, 550, -math.pi / 2, initial_length, depth, angle_variation, length_factor, randomness,
              branch_thickness, branch_color, angle_randomness, length_randomness)

# Function to randomize slider values based on locked checkboxes
def randomize_tree():
    """
    Randomizes tree parameters for all unlocked sliders and redraws the tree.
    """
    if not depth_locked.get():
        depth_slider.set(random.randint(4, 10))  # Balanced range for depth
    if not angle_locked.get():
        angle_slider.set(random.randint(15, 35))  # Moderate branching angles
    if not length_factor_locked.get():
        length_factor_slider.set(random.randint(65, 80))  # Balanced branch length factors
    if not randomness_locked.get():
        randomness_slider.set(random.randint(10, 30))  # Controlled randomness
    if not thickness_locked.get():
        thickness_slider.set(random.randint(5, 12))  # Moderate thickness
    if not branch_color_locked.get():
        branch_color_slider.set(random.randint(100, 140))  # Natural branch color range
    if not angle_randomness_locked.get():
        angle_randomness_slider.set(random.randint(5, 20))  # Mild randomness for angles
    if not length_randomness_locked.get():
        length_randomness_slider.set(random.randint(5, 20))  # Mild randomness for length

    update_tree()

# Function to export the current tree as a PNG image
def export_image():
    """
    Exports the current fractal tree as a PNG image.
    """
    try:
        img = Image.new("RGB", (1600, 1600), "white")
        draw = ImageDraw.Draw(img)

        depth = depth_slider.get()
        angle_variation = angle_slider.get()
        length_factor = length_factor_slider.get() / 100
        initial_length = length_slider.get()
        randomness = randomness_slider.get() / 100
        branch_thickness = thickness_slider.get()
        branch_color = f"#{branch_color_slider.get():02x}6540"
        angle_randomness = angle_randomness_slider.get() / 100
        length_randomness = length_randomness_slider.get() / 100

        draw_tree_on_image(draw, 400, 550, -math.pi / 2, initial_length, depth, angle_variation, length_factor,
                           randomness, branch_thickness, branch_color, angle_randomness, length_randomness)

        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpeg")])
        if file_path:
            img.save(file_path)
    except Exception as e:
        tk.messagebox.showerror("Export Error", f"An error occurred while exporting the image: {e}")

# Function to save the current tree settings as a JSON file
def save_settings():
    """
    Saves the current tree parameters to a JSON file.
    """
    settings = {
        'depth': depth_slider.get(),
        'angle_variation': angle_slider.get(),
        'length_factor': length_factor_slider.get(),
        'initial_length': length_slider.get(),
        'randomness': randomness_slider.get(),
        'branch_thickness': thickness_slider.get(),
        'branch_color': branch_color_slider.get(),
        'angle_randomness': angle_randomness_slider.get(),
        'length_randomness': length_randomness_slider.get()
    }
    file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as f:
            json.dump(settings, f)

# Function to load tree settings from a JSON file
def load_settings():
    """
    Loads tree parameters from a JSON file and applies them to the sliders.
    """
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as f:
            settings = json.load(f)

        depth_slider.set(settings['depth'])
        angle_slider.set(settings['angle_variation'])
        length_factor_slider.set(settings['length_factor'])
        length_slider.set(settings['initial_length'])
        randomness_slider.set(settings['randomness'])
        thickness_slider.set(settings['branch_thickness'])
        branch_color_slider.set(settings['branch_color'])
        angle_randomness_slider.set(settings['angle_randomness'])
        length_randomness_slider.set(settings['length_randomness'])
        update_tree()

# Function to display a help dialog explaining the tool's usage
def show_help():
    """
    Displays a help message explaining how to use the fractal tree generator.
    """
    help_message = (
        "Welcome to the Fractal Tree Generator!\n\n"
        "Use the sliders on the right to adjust the tree's parameters:\n"
        "- Recursion Depth: Controls how many levels of branching occur.\n"
        "- Branch Angle: Adjusts the angle between branches.\n"
        "- Branch Length Factor: Controls how much shorter each branch is compared to the previous one.\n"
        "- Randomness: Adds variability to the tree's structure.\n"
        "- Thickness: Changes the thickness of the branches.\n"
        "- Branch Color Shade: Adjusts the color of the branches.\n"
        "- Export: Save your fractal tree as a PNG or JPEG image.\n\n"
        "Randomize: Click to randomize the settings for a unique tree."
    )
    messagebox.showinfo("Help", help_message)

# Set up the GUI window with scrollable sliders
def create_tree_gui():
    """
    Sets up the Tkinter GUI with sliders to adjust tree parameters and canvas to display the tree.
    """
    global canvas, depth_slider, angle_slider, length_factor_slider, length_slider, randomness_slider
    global thickness_slider, branch_color_slider, angle_randomness_slider, length_randomness_slider
    global depth_locked, angle_locked, length_factor_locked, randomness_locked, thickness_locked
    global branch_color_locked, angle_randomness_locked, length_randomness_locked, root

    root = tk.Tk()
    root.title("Fractal Tree Generator")
    root.geometry("1000x700")

    # Create the main frame for tree canvas and slider panel
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Canvas for displaying the fractal tree
    canvas = tk.Canvas(main_frame, width=700, height=600, bg='white')
    canvas.pack(side="left", fill="both", expand=True)

    # Create a frame for scrollable slider panel
    slider_frame = tk.Frame(main_frame)
    slider_frame.pack(side="right", fill="y")

    # Scrollbar for the sliders
    canvas_scroll = tk.Canvas(slider_frame)
    canvas_scroll.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(slider_frame, orient="vertical", command=canvas_scroll.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas_scroll)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
    )
    canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas_scroll.configure(yscrollcommand=scrollbar.set)

    # Function to create sliders with lock checkboxes
    def create_slider_with_lock(label, slider_from, slider_to, default, lock_var):
        """
        Helper function to create a slider with an accompanying lock checkbox.
        """
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill="x", pady=2)
        slider = tk.Scale(frame, from_=slider_from, to=slider_to, orient=tk.HORIZONTAL, label=label, length=200,
                          command=lambda x: update_tree())
        slider.set(default)
        slider.pack(side="left")
        check = Checkbutton(frame, text=f"Lock", variable=lock_var)
        check.pack(side="right")
        return slider

    # Initialize lock variables for checkboxes
    depth_locked = IntVar()
    angle_locked = IntVar()
    length_factor_locked = IntVar()
    randomness_locked = IntVar()
    thickness_locked = IntVar()
    branch_color_locked = IntVar()
    angle_randomness_locked = IntVar()
    length_randomness_locked = IntVar()

    # Create sliders for adjusting tree parameters
    depth_slider = create_slider_with_lock('Recursion Depth', 2, 12, 10, depth_locked)
    angle_slider = create_slider_with_lock('Branch Angle', 5, 45, 20, angle_locked)
    length_factor_slider = create_slider_with_lock('Branch Length Factor (%)', 50, 90, 70, length_factor_locked)
    length_slider = create_slider_with_lock('Initial Branch Length', 50, 150, 100, None)
    randomness_slider = create_slider_with_lock('Randomness (%)', 0, 50, 15, randomness_locked)
    thickness_slider = create_slider_with_lock('Branch Thickness', 1, 50, 10, thickness_locked)
    branch_color_slider = create_slider_with_lock('Branch Color Shade', 80, 160, 130, branch_color_locked)
    angle_randomness_slider = create_slider_with_lock('Angle Randomness (%)', 0, 50, 10, angle_randomness_locked)
    length_randomness_slider = create_slider_with_lock('Length Randomness (%)', 0, 50, 10, length_randomness_locked)

    # Add buttons for Randomize, Save, Load, Export, and Help
    tk.Button(scrollable_frame, text="Randomize", command=randomize_tree).pack(pady=10)
    tk.Button(scrollable_frame, text="Save Settings", command=save_settings).pack(pady=10)
    tk.Button(scrollable_frame, text="Load Settings", command=load_settings).pack(pady=10)
    tk.Button(scrollable_frame, text="Export as PNG", command=export_image).pack(pady=10)
    tk.Button(scrollable_frame, text="Help", command=show_help).pack(pady=10)

    # Draw the initial tree
    update_tree()

    # Start the Tkinter main loop
    root.mainloop()

# Run the GUI
create_tree_gui()
