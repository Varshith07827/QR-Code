import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import os

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="QR Code Generator",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=10)

        # Input field
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=10)

        self.url_label = ttk.Label(
            self.input_frame,
            text="Enter URL or Text:",
            font=('Helvetica', 10)
        )
        self.url_label.pack(anchor=tk.W)

        self.url_entry = ttk.Entry(
            self.input_frame,
            font=('Helvetica', 10),
            width=40
        )
        self.url_entry.pack(fill=tk.X, pady=5)

        # Generate button
        self.generate_button = ttk.Button(
            self.main_frame,
            text="Generate QR Code",
            command=self.generate_qr,
            style='Accent.TButton'
        )
        self.generate_button.pack(pady=10)

        # QR Code display
        self.qr_frame = ttk.Frame(self.main_frame)
        self.qr_frame.pack(pady=10)

        self.qr_label = ttk.Label(self.qr_frame)
        self.qr_label.pack()

        # Save button
        self.save_button = ttk.Button(
            self.main_frame,
            text="Save QR Code",
            command=self.save_qr,
            state=tk.DISABLED
        )
        self.save_button.pack(pady=10)

        # Configure styles
        self.configure_styles()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 10, 'bold'))

    def generate_qr(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL or text")
            return

        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)

            # Create image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(qr_image)
            
            # Update label
            self.qr_label.configure(image=photo)
            self.qr_label.image = photo
            
            # Enable save button
            self.save_button.configure(state=tk.NORMAL)
            
            # Store the QR image for saving
            self.current_qr_image = qr_image

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def save_qr(self):
        if not hasattr(self, 'current_qr_image'):
            return

        try:
            # Create 'qr_codes' directory if it doesn't exist
            if not os.path.exists('qr_codes'):
                os.makedirs('qr_codes')

            # Generate filename
            filename = f"qr_codes/qr_code_{len(os.listdir('qr_codes')) + 1}.png"
            
            # Save the image
            self.current_qr_image.save(filename)
            messagebox.showinfo("Success", f"QR Code saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()