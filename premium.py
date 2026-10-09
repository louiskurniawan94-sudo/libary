import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUCCESS, FONT_NAV, FONT_BUTTON,
    HoverButton, is_user_premium, upgrade_user_to_premium
)


class PremiumPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        navbar = tk.Frame(self, bg=COLOR_PRIMARY, height=60)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(
            navbar, text="Digital Library",
            bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=20)

        nav_left = tk.Frame(navbar, bg=COLOR_PRIMARY)
        nav_left.pack(side="left", padx=10)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Books", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BookManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Borrowing", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BorrowingManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Users", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("UsersManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Home", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="left", padx=4)

        self.nav_right = tk.Frame(navbar, bg=COLOR_PRIMARY)
        self.nav_right.pack(side="right", padx=20)

        self.user_label = tk.Label(
            self.nav_right, text="", bg=COLOR_PRIMARY, fg="white", font=FONT_NAV
        )
        self.user_label.pack(side="left", padx=(0, 12))

        HoverButton(
            self.nav_right, bg_normal="#f1c40f", bg_hover="#f39c12",
            text="⭐ Premium", fg="black", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("PremiumPage")
        ).pack(side="left", padx=(0, 8))

        HoverButton(
            self.nav_right, bg_normal="#c0392b", bg_hover="#a93226",
            text="Log Out", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2", command=controller.logout
        ).pack(side="left")

        card = tk.Frame(self, bg=COLOR_CARD, padx=40, pady=30,
                        highlightthickness=1, highlightbackground="#dfe6e9")
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="⭐ Upgrade to a Premium Account", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(0, 10))

        desc_text = (
            "Dapatkan akses penuh untuk fitur pembuatan dan penambahan buku baru!\n"
            "Dengan akun Premium, Anda dapat mengelola koleksi buku tanpa batasan."
        )
        tk.Label(
            card, text=desc_text, bg=COLOR_CARD, fg=COLOR_MUTED,
            font=("Segoe UI", 11), justify="center"
        ).pack(pady=(0, 20))

        price_frame = tk.Frame(card, bg="#f8f9fa", padx=20, pady=15, relief="solid", bd=1)
        price_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            price_frame, text="Regular Price: $10.00", bg="#f8f9fa", fg=COLOR_MUTED,
            font=("Segoe UI", 11, "overstrike")
        ).pack()

        tk.Label(
            price_frame, text="100% OFF PROMOTION -> FREE $0", bg="#f8f9fa", fg=COLOR_SUCCESS,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(5, 0))

        self.btn_action = HoverButton(
            card, bg_normal=COLOR_SUCCESS, bg_hover="#1e8449",
            text="Activate Premium Now (Free)", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_upgrade
        )
        self.btn_action.pack(fill="x", ipady=8)

        self.status_label = tk.Label(
            card, text="", bg=COLOR_CARD, fg=COLOR_SUCCESS, font=("Segoe UI", 11, "bold")
        )
        self.status_label.pack(pady=(15, 0))

    def on_show(self):
        if not self.controller.current_user:
            self.controller.show_frame("SignInPage")
            return
        
        self.user_label.config(text=f"👤 {self.controller.current_user}")
        
        if is_user_premium(self.controller.current_user):
            self.status_label.config(text="Status: Your Account Is Already PREMIUM ⭐", fg=COLOR_SUCCESS)
            self.btn_action.config(state="disabled", bg=COLOR_MUTED, text="Already Active")
        else:
            self.status_label.config(text="Status: Regular Account", fg=COLOR_MUTED)
            self.btn_action.config(state="normal", bg=COLOR_SUCCESS, text="Activate Premium Now (Free)")

    def handle_upgrade(self):
        user = self.controller.current_user
        if not user:
            return
        
        success, msg = upgrade_user_to_premium(user)
        if success:
            messagebox.showinfo("Success", msg)
            self.on_show()