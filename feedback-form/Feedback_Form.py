#!/usr/bin/python3
# Feedback_Form.py by Griffin Ongoya

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class Feedback:

    def __init__(self, master):
        master.title("Feedback Form")
        master.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Text.TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))

        # ================= HEADER =================
        self.frame_header = ttk.Frame(master, padding=15)
        self.frame_header.pack(fill="x")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "Griffinpic.png")

        image = Image.open(image_path)
        image = image.resize((130, 130), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(image)

        tk.Label(self.frame_header, image=self.logo).grid(
            row=0, column=0, rowspan=2, padx=(0, 15)
        )

        ttk.Label(
            self.frame_header,
            text=(
                "Financial Engineer | Data Analytics | Finance Technology | "
                "Business Intelligence Developer | Financial Reporting | "
                "Credit Risk Modelling"
            ),
            wraplength=360,
            style="Header.TLabel"
        ).grid(row=0, column=1, sticky="w")

        ttk.Label(
            self.frame_header,
            text="I value your feedback. Please share your experience below.",
            wraplength=360,
            style="Text.TLabel"
        ).grid(row=1, column=1, sticky="w")

        # ================= CONTENT =================
        self.frame_content = ttk.Frame(master, padding=15)
        self.frame_content.pack()

        ttk.Label(self.frame_content, text="Name:", style="Text.TLabel").grid(
            row=0, column=0, sticky="e", pady=4)
        ttk.Label(self.frame_content, text="Email:", style="Text.TLabel").grid(
            row=1, column=0, sticky="e", pady=4)
        ttk.Label(self.frame_content, text="Message:", style="Text.TLabel").grid(
            row=2, column=0, sticky="ne", pady=4)

        self.entry_name = ttk.Entry(self.frame_content, width=32)
        self.entry_email = ttk.Entry(self.frame_content, width=32)

        self.entry_name.grid(row=0, column=1, sticky="w", pady=4)
        self.entry_email.grid(row=1, column=1, sticky="w", pady=4)

        self.text_comments = tk.Text(
            self.frame_content, width=48, height=8, wrap="word"
        )
        self.text_comments.grid(row=2, column=1, pady=4)

        # ================= STAR RATING =================
        ttk.Label(self.frame_content, text="Rating:", style="Text.TLabel").grid(
            row=3, column=0, sticky="e", pady=6
        )

        self.rating = 0
        self.star_buttons = []

        star_frame = ttk.Frame(self.frame_content)
        star_frame.grid(row=3, column=1, sticky="w")

        for i in range(1, 6):
            btn = tk.Label(
                star_frame,
                text="★",
                font=("Segoe UI", 20),
                fg="light gray",
                cursor="hand2"
            )
            btn.pack(side="left")

            btn.bind("<Enter>", lambda e, s=i: self._hover_stars(s))
            btn.bind("<Leave>", lambda e: self._refresh_stars())
            btn.bind("<Button-1>", lambda e, s=i: self.set_rating(s))

            self.star_buttons.append(btn)

        # ================= BUTTONS =================
        button_frame = ttk.Frame(master, padding=10)
        button_frame.pack()

        ttk.Button(button_frame, text="Submit", command=self.submit).pack(
            side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(
            side="left", padx=5)

    # ================= STAR LOGIC =================
    def _hover_stars(self, star_count):
        for i, star in enumerate(self.star_buttons):
            star.config(fg="gold" if i < star_count else "light gray")

    def _refresh_stars(self):
        for i, star in enumerate(self.star_buttons):
            star.config(fg="gold" if i < self.rating else "light gray")

    def set_rating(self, rating):
        self.rating = rating
        self._refresh_stars()

    # ================= FORM ACTIONS =================
    def submit(self):
        if not self.entry_name.get() or not self.entry_email.get():
            messagebox.showwarning("Missing Information", "Name and Email are required.")
            return

        if self.rating == 0:
            messagebox.showwarning("Rating Required", "Please select a star rating.")
            return

        print("Name:", self.entry_name.get())
        print("Email:", self.entry_email.get())
        print("Message:", self.text_comments.get("1.0", "end").strip())
        print("Rating:", f"{self.rating}/5")

        messagebox.showinfo("Feedback Received", "Thank you for your feedback!")
        self.clear()

    def clear(self):
        self.entry_name.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.text_comments.delete("1.0", "end")
        self.rating = 0
        self._refresh_stars()


def main():
    root = tk.Tk()
    Feedback(root)
    root.mainloop()


if __name__ == "__main__":
    main()