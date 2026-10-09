import hashlib
import json
import os
import tkinter as tk

APP_WIDTH = 1280
APP_HEIGHT = 720

USERS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "users.json"
)
BOOKS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "books.json"
)
BORROWINGS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "borrowings.json"
)

COLOR_PRIMARY = "#6d2b85"
COLOR_ACCENT = "#3E0F68"
COLOR_ACCENT_DARK = "#43136e"
COLOR_BG = "#f4f6f7"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#2c3e50"
COLOR_MUTED = "#7f8c8d"
COLOR_SUCCESS = "#27ae60"
COLOR_DANGER = "#c0392b"

FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SUBTITLE = ("Segoe UI", 12)
FONT_NAV = ("Segoe UI", 11, "bold")
FONT_CARD_TITLE = ("Segoe UI", 14, "bold")
FONT_CARD_BODY = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 11, "bold")

ARTIKEL_PERPUSTAKAAN = [
    {
        "judul": "5 Fiction Book Recommendations This Month",
        "ringkasan": (
            "Temukan lima judul fiksi terbaru yang tersedia di rak perpustakaan "
            "kami, mulai dari novel misteri hingga fantasi epik."
        ),
        "kategori": "Recommendations",
    },
    {
        "judul": "Effective Speed-Reading Tips",
        "ringkasan": (
            "Pelajari teknik speed reading sederhana agar kamu bisa"
            " menyelesaikan lebih banyak buku tanpa kehilangan pemahaman isi"
            " bacaan."
        ),
        "kategori": "Tips & Tricks",
    },
    {
        "judul": "Visiting Schedule & Opening Hours",
        "ringkasan": (
            "Perpustakaan buka setiap hari Senin-Sabtu pukul 08.00-16.00. Cek"
            " jadwal lengkap dan agenda kegiatan bulanan di sini."
        ),
        "kategori": "Announcements",
    },
    {
        "judul": "How to Borrow Books Online",
        "ringkasan": (
            "Setelah login, anggota dapat memesan buku secara online dan"
            " mengambilnya langsung di meja sirkulasi perpustakaan."
        ),
        "kategori": "Guide",
    },
]

DEFAULT_BOOKS = [
    {
        "id": 1,
        "judul": "Laskar Pelangi",
        "penulis": "Andrea Hirata",
        "tahun": "2005",
        "stok": 5,
    },
    {
        "id": 2,
        "judul": "Bumi",
        "penulis": "Tere Liye",
        "tahun": "2014",
        "stok": 3,
    },
    {
        "id": 3,
        "judul": "Atomic Habits",
        "penulis": "James Clear",
        "tahun": "2018",
        "stok": 4,
    },
]


def hash_password(password: str) -> str:
  return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> dict:
  if not os.path.exists(USERS_FILE):
    return {}
  try:
    with open(USERS_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  except (json.JSONDecodeError, OSError):
    return {}


def save_users(users: dict) -> None:
  with open(USERS_FILE, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2, ensure_ascii=False)


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
  users = load_users()
  if username in users:
    return False, "Username is already registered. Please choose another username."
  for data in users.values():
    if data.get("email", "").lower() == email.lower():
      return False, "Email is already registered. Please use another email."
  users[username] = {
      "email": email,
      "password": hash_password(password),
      "is_premium": False,
  }
  save_users(users)
  return True, "Registration successful! Please sign in."


def is_user_premium(username: str) -> bool:
  users = load_users()
  if username in users:
    return users[username].get("is_premium", False)
  return False


def upgrade_user_to_premium(username: str) -> tuple[bool, str]:
  users = load_users()
  if username not in users:
    return False, "User not found."
  users[username]["is_premium"] = True
  save_users(users)
  return True, "Congratulations! Your account has been upgraded to Premium."


def verify_login(username: str, password: str) -> tuple[bool, str]:
  users = load_users()
  if username not in users:
    return False, "Username not found."
  if users[username]["password"] != hash_password(password):
    return False, "Incorrect password."
  return True, "Sign-in successful!"


def delete_user(username: str) -> tuple[bool, str]:
  users = load_users()
  if username not in users:
    return False, "User not found."
  del users[username]
  save_users(users)
  return True, "User deleted successfully."


def update_user(
    old_username: str, new_username: str, email: str, new_password: str = ""
) -> tuple[bool, str]:
  users = load_users()
  if old_username not in users:
    return False, "User not found."
  if new_username != old_username and new_username in users:
    return False, "The new username is already in use."
  for uname, data in users.items():
    if uname != old_username and data.get("email", "").lower() == email.lower():
      return False, "The email is already in use."
  record = users.pop(old_username)
  record["email"] = email
  if new_password:
    record["password"] = hash_password(new_password)
  users[new_username] = record
  save_users(users)
  return True, "User updated successfully."


def load_books() -> list:
  if not os.path.exists(BOOKS_FILE):
    save_books(DEFAULT_BOOKS)
    return list(DEFAULT_BOOKS)
  try:
    with open(BOOKS_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      if isinstance(data, list):
        return data
      return []
  except (json.JSONDecodeError, OSError):
    return []


def save_books(books: list) -> None:
  with open(BOOKS_FILE, "w", encoding="utf-8") as f:
    json.dump(books, f, indent=2, ensure_ascii=False)


def get_next_book_id(books: list) -> int:
  if not books:
    return 1
  return max(int(b.get("id", 0)) for b in books) + 1


def add_book(
    judul: str, penulis: str, tahun: str, stok: int
) -> tuple[bool, str]:
  books = load_books()
  new_id = get_next_book_id(books)
  books.append({
      "id": new_id,
      "judul": judul,
      "penulis": penulis,
      "tahun": tahun,
      "stok": stok,
  })
  save_books(books)
  return True, "Book added successfully."


def update_book(
    book_id: int, judul: str, penulis: str, tahun: str, stok: int
) -> tuple[bool, str]:
  books = load_books()
  for b in books:
    if int(b.get("id", 0)) == int(book_id):
      b["judul"] = judul
      b["penulis"] = penulis
      b["tahun"] = tahun
      b["stok"] = stok
      save_books(books)
      return True, "Books berhasil diperbarui."
  return False, "Books tidak ditemukan."


def delete_book(book_id: int) -> tuple[bool, str]:
  books = load_books()
  borrowings = load_borrowings()
  for p in borrowings:
    if int(p.get("book_id", 0)) == int(book_id) and p.get("status") == "Borrowed":
      return False, "Books tidak bisa dihapus karena sedang dipinjam."
  filtered = [b for b in books if int(b.get("id", 0)) != int(book_id)]
  if len(filtered) == len(books):
    return False, "Books tidak ditemukan."
  save_books(filtered)
  return True, "Books berhasil dihapus."


def find_book(book_id: int):
  for b in load_books():
    if int(b.get("id", 0)) == int(book_id):
      return b
  return None


def adjust_book_stock(book_id: int, delta: int) -> bool:
  books = load_books()
  for b in books:
    if int(b.get("id", 0)) == int(book_id):
      b["stok"] = int(b.get("stok", 0)) + delta
      if b["stok"] < 0:
        return False
      save_books(books)
      return True
  return False


def load_borrowings() -> list:
  if not os.path.exists(BORROWINGS_FILE):
    return []
  try:
    with open(BORROWINGS_FILE, "r", encoding="utf-8") as f:
      data = json.load(f)
      if isinstance(data, list):
        return data
      return []
  except (json.JSONDecodeError, OSError):
    return []


def save_borrowings(borrowings: list) -> None:
  with open(BORROWINGS_FILE, "w", encoding="utf-8") as f:
    json.dump(borrowings, f, indent=2, ensure_ascii=False)


def get_next_borrowing_id(borrowings: list) -> int:
  if not borrowings:
    return 1
  return max(int(p.get("id", 0)) for p in borrowings) + 1


def add_borrowing(
    username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str
) -> tuple[bool, str]:
  users = load_users()
  if username not in users:
    return False, "Username tidak terdaftar."
  book = find_book(book_id)
  if book is None:
    return False, "Books tidak ditemukan."
  if int(book.get("stok", 0)) <= 0:
    return False, "Stock buku habis."
  borrowings = load_borrowings()
  new_id = get_next_borrowing_id(borrowings)
  borrowings.append({
      "id": new_id,
      "username": username,
      "book_id": int(book_id),
      "judul": book.get("judul", ""),
      "tanggal_pinjam": tanggal_pinjam,
      "tanggal_kembali": tanggal_kembali,
      "status": "Borrowed",
  })
  save_borrowings(borrowings)
  adjust_book_stock(book_id, -1)
  return True, "Borrowing berhasil ditambahkan."


def update_borrowing(
    borrow_id: int,
    username: str,
    book_id: int,
    tanggal_pinjam: str,
    tanggal_kembali: str,
    status: str,
) -> tuple[bool, str]:
  borrowings = load_borrowings()
  target = None
  for p in borrowings:
    if int(p.get("id", 0)) == int(borrow_id):
      target = p
      break
  if target is None:
    return False, "Data peminjaman tidak ditemukan."
  old_status = target.get("status")
  old_book_id = int(target.get("book_id", 0))
  new_book_id = int(book_id)
  if (
      old_status == "Borrowed"
      and status == "Returned"
      and old_book_id == new_book_id
  ):
    adjust_book_stock(old_book_id, 1)
  elif old_status == "Returned" and status == "Borrowed":
    book = find_book(new_book_id)
    if book is None:
      return False, "Books tidak ditemukan."
    if int(book.get("stok", 0)) <= 0:
      return False, "Stock buku habis."
    adjust_book_stock(new_book_id, -1)
  elif (
      old_book_id != new_book_id
      and old_status == "Borrowed"
      and status == "Borrowed"
  ):
    book = find_book(new_book_id)
    if book is None:
      return False, "Books tidak ditemukan."
    if int(book.get("stok", 0)) <= 0:
      return False, "Stock buku habis."
    adjust_book_stock(old_book_id, 1)
    adjust_book_stock(new_book_id, -1)
  target["username"] = username
  target["book_id"] = new_book_id
  book_now = find_book(new_book_id)
  if book_now is not None:
    target["judul"] = book_now.get("judul", target.get("judul", ""))
  target["tanggal_pinjam"] = tanggal_pinjam
  target["tanggal_kembali"] = tanggal_kembali
  target["status"] = status
  save_borrowings(borrowings)
  return True, "Data peminjaman berhasil diperbarui."


def delete_borrowing(borrow_id: int) -> tuple[bool, str]:
  borrowings = load_borrowings()
  target = None
  for p in borrowings:
    if int(p.get("id", 0)) == int(borrow_id):
      target = p
      break
  if target is None:
    return False, "Data peminjaman tidak ditemukan."
  if target.get("status") == "Borrowed":
    adjust_book_stock(int(target.get("book_id", 0)), 1)
  filtered = [p for p in borrowings if int(p.get("id", 0)) != int(borrow_id)]
  save_borrowings(filtered)
  return True, "Data peminjaman berhasil dihapus."


class HoverButton(tk.Button):

  def __init__(self, master, bg_normal, bg_hover, **kwargs):
    super().__init__(master, bg=bg_normal, activebackground=bg_hover, **kwargs)
    self.bg_normal = bg_normal
    self.bg_hover = bg_hover
    self.bind("<Enter>", lambda e: self.config(bg=self.bg_hover))
    self.bind("<Leave>", lambda e: self.config(bg=self.bg_normal))