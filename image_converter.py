import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Constants
OUTPUT_FORMATS = ["png", "jpg", "jpeg", "webp", "bmp", "gif", "tiff"]

def convert_image(image_path, target_format):
    """Handles the core image conversion logic."""
    if not image_path or not target_format:
        return False, "Missing image path or format."

    target_format = target_format.lower()
    try:
        img = Image.open(image_path)

        # Handle transparency for formats that don't support it (like JPEG)
        if target_format in ("jpg", "jpeg") and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}.{target_format}"

        img.save(output_path, format=target_format.upper())
        return True, output_path
    except Exception as e:
        return False, str(e)

def run_converter():
    # 1. Initialize Root (and hide it)
    root = tk.Tk()
    root.withdraw() 

    # 2. Select Image File
    image_path = filedialog.askopenfilename(
        title="Select an Image to Convert",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp")]
    )

    if not image_path:
        return # User cancelled

    # 3. Create a Custom Dialog for Format Selection
    # We create a small Toplevel window to act as our format picker
    format_window = tk.Toplevel(root)
    format_window.title("Select Format")
    format_window.geometry("300x150")
    format_window.resizable(False, False)
    
    # Center the window
    format_window.update_idletasks()
    x = (format_window.winfo_screenwidth() // 2) - (150)
    y = (format_window.winfo_screenheight() // 2) - (75)
    format_window.geometry(f'+{x}+{y}')

    tk.Label(format_window, text="Choose target format:", pady=10).pack()

    # Dropdown (Combobox)
    format_var = tk.StringVar(value=OUTPUT_FORMATS[0])
    dropdown = ttk.Combobox(format_window, textvariable=format_var, values=OUTPUT_FORMATS, state="readonly")
    dropdown.pack(pady=5)

    def on_convert():
        target = format_var.get()
        format_window.destroy() # Close the selection window
        
        success, result = convert_image(image_path, target)
        
        if success:
            messagebox.showinfo("Success", f"Converted successfully!\nSaved to: {result}")
        else:
            messagebox.showerror("Error", f"Conversion failed:\n{result}")
        
        root.quit() # End the program

    # Convert Button
    convert_btn = ttk.Button(format_window, text="Convert", command=on_convert)
    convert_btn.pack(pady=10)

    # Bring to front and wait
    format_window.attributes('-topmost', True)
    root.mainloop()

if __name__ == "__main__":
    run_converter()