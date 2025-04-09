import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import requests

# --- KONFIGURASI AWAL ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Multistream Video Broadcaster")
app.geometry("1200x700")

valid_license_key = "MULTISTREAM-2025"


# --- LOGO DAN SIDEBAR ---
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

content_frame = ctk.CTkFrame(app, corner_radius=15)
content_frame.pack(side="right", fill="both", expand=True)

# Tambahkan logo dengan gambar dan teks
try:
    logo_img = ctk.CTkImage(Image.open("logo.png"), size=(32, 32))
    logo_label = ctk.CTkLabel(sidebar, image=logo_img, text=" Multistream", compound="left", font=("Arial", 16, "bold"))
    logo_label.pack(pady=(20, 20))
except:
    logo_label = ctk.CTkLabel(sidebar, text="Multistream", font=("Arial", 16, "bold"))
    logo_label.pack(pady=(20, 20))

# --- TAMPILAN MENU ---
menu_spacing = 10

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_dashboard():
    clear_content()
    label = ctk.CTkLabel(content_frame, text="Dashboard\n\nVersi: 1.0.0\nAplikasi untuk multistreaming video", justify="center", font=("Arial", 16))
    label.pack(expand=True)

def show_about():
    clear_content()
    label = ctk.CTkLabel(content_frame, text="Tentang\n\nDikembangkan oleh Mulya Hermana\n© 2025 All rights reserved", justify="center", font=("Arial", 16))
    label.pack(expand=True)

def show_license():
    def save_license_local():
        nonlocal entry
        global user_license
        user_license = entry.get().strip()
        if user_license == valid_license_key:
            messagebox.showinfo("Sukses", "Lisensi valid secara lokal!")
        else:
            messagebox.showwarning("Gagal", "Lisensi tidak valid.")

    

    clear_content()
    label = ctk.CTkLabel(content_frame, text="Masukkan Lisensi", font=("Arial", 16))
    label.pack(pady=20)

    entry = ctk.CTkEntry(content_frame, placeholder_text="Masukkan License Key")
    entry.pack(pady=10)

    submit_local = ctk.CTkButton(content_frame, text="Validasi Lisensi", command=save_license_local)
    submit_local.pack(pady=5)

    

def show_streaming():
    if user_license != valid_license_key:
        messagebox.showerror("Akses Ditolak", "Masukkan lisensi yang valid terlebih dahulu.")
        return

    clear_content()
    # STREAMING LAYOUT
    scroll_frame = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

    MAX_COLUMNS = 5
    stream_widgets = []

    for col in range(MAX_COLUMNS):
        scroll_frame.grid_columnconfigure(col, weight=1, uniform="stream")

    def browse_video(entry):
        path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.mov")])
        if path:
            entry.delete(0, "end")
            entry.insert(0, path)

    def add_stream():
        idx = len(stream_widgets)
        row = idx // MAX_COLUMNS
        column = idx % MAX_COLUMNS

        stream_frame = ctk.CTkFrame(scroll_frame, corner_radius=15)
        stream_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        platform_menu = ctk.CTkOptionMenu(stream_frame, values=["YouTube", "Facebook"])
        platform_menu.set("YouTube")
        platform_menu.pack(pady=(10, 5), padx=10, fill="x")

        rtmp_entry = ctk.CTkEntry(stream_frame, placeholder_text="RTMP URL")
        rtmp_entry.pack(pady=5, padx=10, fill="x")

        key_entry = ctk.CTkEntry(stream_frame, placeholder_text="Stream Key")
        key_entry.pack(pady=5, padx=10, fill="x")

        video_entry = ctk.CTkEntry(stream_frame, placeholder_text="Video Path")
        video_entry.pack(pady=5, padx=10, fill="x")

        browse_btn = ctk.CTkButton(stream_frame, text="Browse Video", command=lambda: browse_video(video_entry))
        browse_btn.pack(pady=5, padx=10, fill="x")

        status_label = ctk.CTkLabel(stream_frame, text="Status: Not Started", text_color="yellow")
        status_label.pack(pady=5)

        control_frame = ctk.CTkFrame(stream_frame, fg_color="transparent")
        control_frame.pack(pady=5)

        start_btn = ctk.CTkButton(control_frame, text="Start", width=70)
        start_btn.pack(side="left", padx=(10, 5))

        stop_btn = ctk.CTkButton(control_frame, text="Stop", width=70)
        stop_btn.pack(side="left", padx=(5, 10))

        stream_widgets.append(stream_frame)

    add_stream_btn = ctk.CTkButton(content_frame, text="+ Add Stream", command=add_stream)
    add_stream_btn.pack(pady=10)

# --- TOMBOL MENU ---
ctk.CTkButton(sidebar, text="Dashboard", command=show_dashboard).pack(pady=(0, menu_spacing), padx=10, fill="x")
ctk.CTkButton(sidebar, text="Masukkan Lisensi", command=show_license).pack(pady=(0, menu_spacing), padx=10, fill="x")
ctk.CTkButton(sidebar, text="Streaming", command=show_streaming).pack(pady=(0, menu_spacing), padx=10, fill="x")
ctk.CTkButton(sidebar, text="Tentang", command=show_about).pack(pady=(0, menu_spacing), padx=10, fill="x")

# BUKA HALAMAN AWAL
show_dashboard()

app.mainloop()
