import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import webbrowser
from Pantry import add, get, remove, update, load
from Api import get_recipes

class PantryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantry Pal")
        self.root.geometry("1800x750")
        self.root.configure(bg="#EBFFCE")
        load()

        self.ingredient_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="count")

        font_normal = ("Segoe UI", 10)
        font_bold = ("Segoe UI", 10, "bold")

        tk.Label(root, text="Ingredient:", font=font_normal, bg="#EBFFCE").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.ingredient_var, bg="#DDF6D2").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Amount:", font=font_normal, bg="#EBFFCE").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(root, textvariable=self.amount_var, width=7, bg="#DDF6D2").grid(row=0, column=3, padx=5, pady=5)

        units = ["count", "oz", "pound", "gallon"]
        tk.OptionMenu(root, self.unit_var, *units).grid(row=0, column=4, padx=5, pady=5)

        tk.Button(root, text="+ Add", command=self.add_item, bg="#B0DB9C", activebackground="#CAE8BD").grid(row=0, column=5, padx=5, pady=5)

        tk.Label(root, text="Pantry:", font=font_bold, bg="#EBFFCE").grid(row=1, column=0, sticky="w", padx=10)
        self.pantry_frame = tk.Frame(root, bg="#EBFFCE")
        self.pantry_frame.grid(row=2, column=0, columnspan=6, padx=10, sticky="w")

        self.pantry_rows = []
        self.refresh_pantry()

        banner_img = Image.open("banner_logo.png")
        banner_img = banner_img.resize((1200, 300), Image.LANCZOS)
        self.banner_photo = ImageTk.PhotoImage(banner_img)

        banner_label = tk.Label(root, image=self.banner_photo, bg="#EBFFCE")
        banner_label.grid(row=2, column=1, columnspan=4, padx=0, pady=10, sticky="w")

        tk.Button(root, text="Find Recipes", command=self.find_recipes, bg="#B0DB9C", activebackground="#CAE8BD").grid(row=3, column=0, pady=10)

        tk.Label(root, text="0–1 Missing", font=font_bold, bg="#EBFFCE").grid(row=4, column=0, pady=(10, 0))
        tk.Label(root, text="2–4 Missing", font=font_bold, bg="#EBFFCE").grid(row=4, column=1, pady=(10, 0))
        tk.Label(root, text="5–8 Missing", font=font_bold, bg="#EBFFCE").grid(row=4, column=2, pady=(10, 0))
        tk.Label(root, text="Recipes & Links", font=font_bold, bg="#EBFFCE").grid(row=4, column=3, pady=(10, 0))

        self.build_output_boxes()

    def build_output_boxes(self):
        style = {"bg": "#DDF6D2", "fg": "#2E2E2E", "wrap": "word", "state": "disabled"}

        f0 = tk.Frame(self.root); f0.grid(row=5, column=0, padx=10, pady=5)
        self.match_box = tk.Text(f0, height=20, width=40, **style)
        tk.Scrollbar(f0, command=self.match_box.yview).pack(side="right", fill="y")
        self.match_box.pack(side="left", fill="both")
        self.match_box.config(yscrollcommand=lambda *args: None)

        f1 = tk.Frame(self.root); f1.grid(row=5, column=1, padx=10, pady=5)
        self.mid_box = tk.Text(f1, height=20, width=40, **style)
        tk.Scrollbar(f1, command=self.mid_box.yview).pack(side="right", fill="y")
        self.mid_box.pack(side="left", fill="both")
        self.mid_box.config(yscrollcommand=lambda *args: None)

        f2 = tk.Frame(self.root); f2.grid(row=5, column=2, padx=10, pady=5)
        self.loose_box = tk.Text(f2, height=20, width=40, **style)
        tk.Scrollbar(f2, command=self.loose_box.yview).pack(side="right", fill="y")
        self.loose_box.pack(side="left", fill="both")
        self.loose_box.config(yscrollcommand=lambda *args: None)

        f3 = tk.Frame(self.root); f3.grid(row=5, column=3, padx=10, pady=5)
        self.links_box = tk.Text(f3, height=20, width=40, **style, cursor="hand2")
        tk.Scrollbar(f3, command=self.links_box.yview).pack(side="right", fill="y")
        self.links_box.pack(side="left", fill="both")
        self.links_box.config(yscrollcommand=lambda *args: None)
        self.links_box.bind("<Button-1>", self.open_link)

        f4 = tk.Frame(self.root, bg="#EBFFCE")
        f4.grid(row=5, column=4, padx=10, pady=5)
        img = Image.open("mascot.png").resize((300, 300), Image.LANCZOS)
        self.mascot_photo = ImageTk.PhotoImage(img)
        tk.Label(f4, image=self.mascot_photo, bg="#EBFFCE").pack()

    def add_item(self):
        name = self.ingredient_var.get().strip()
        unit = self.unit_var.get()
        try:
            amt = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        if not name:
            messagebox.showerror("Missing Input", "Ingredient name is required.")
            return
        full = f"{name} ({unit})"
        add(full, amt)
        self.ingredient_var.set("")
        self.amount_var.set("")
        self.refresh_pantry()

    def refresh_pantry(self):
        for row in self.pantry_rows:
            for widget in row:
                widget.destroy()
        self.pantry_rows.clear()

        data = get()
        for i, (item, amt) in enumerate(data.items()):
            var = tk.IntVar()
            cb = tk.Checkbutton(self.pantry_frame, variable=var, bg="#EBFFCE")
            cb.grid(row=i, column=0, sticky="w")
            label = tk.Label(self.pantry_frame, text=f"{item} – {amt}", bg="#EBFFCE", fg="#2E2E2E")
            label.grid(row=i, column=1, sticky="w")
            label.bind("<Button-3>", lambda e, n=item: self.show_menu(e, n))
            self.pantry_rows.append((cb, label))

    def show_menu(self, event, name):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="+", command=lambda: self.change(name, 1))
        menu.add_command(label="-", command=lambda: self.change(name, -1))
        menu.add_command(label="x", command=lambda: self.remove(name))
        menu.post(event.x_root, event.y_root)

    def change(self, name, delta):
        update(name, delta)
        self.refresh_pantry()

    def remove(self, name):
        remove(name)
        self.refresh_pantry()

    def find_recipes(self):
        pantry = get()
        r = get_recipes()
        match, mid, loose, links = [], [], [], []

        for recipe in r:
            miss = recipe.get("missedIngredientCount", 0)
            title = recipe["title"]
            rid = recipe["id"]
            line = f"{title} ({miss} missing)"
            if miss <= 1:
                match.append(line)
            elif 2 <= miss <= 4:
                mid.append(line)
            elif 5 <= miss <= 8:
                loose.append(line)
            url = f"https://spoonacular.com/recipes/{'-'.join(title.lower().split())}-{rid}"
            links.append((title, url))

        self.show(self.match_box, match)
        self.show(self.mid_box, mid)
        self.show(self.loose_box, loose)
        self.show_links(links)

    def show(self, box, items):
        box.config(state="normal")
        box.delete("1.0", tk.END)
        for line in items:
            if "(" in line and "missing" in line:
                title, miss = line.rsplit("(", 1)
                title = title.strip()
                miss = miss.replace("missing)", "").strip()
            else:
                title, miss = line, "?"
            box.insert(tk.END, "———————————————\n")
            box.insert(tk.END, f"{title}\n")
            box.insert(tk.END, f"Missing: {miss}\n")
            box.insert(tk.END, "———————————————\n\n")
        box.config(state="disabled")

    def show_links(self, links):
        self.links_box.config(state="normal")
        self.links_box.delete("1.0", tk.END)
        for title, url in links:
            self.links_box.insert(tk.END, "———————————————\n", url)
            self.links_box.insert(tk.END, f"{title}\n", url)
            self.links_box.insert(tk.END, "———————————————\n\n", url)
            start = float(self.links_box.index("end")) - 4
            self.links_box.tag_add(url, f"{start}", "end")
            self.links_box.tag_bind(url, "<Enter>", lambda e: self.links_box.config(cursor="hand2"))
            self.links_box.tag_bind(url, "<Leave>", lambda e: self.links_box.config(cursor="arrow"))
        self.links_box.config(state="disabled")

    def open_link(self, event):
        idx = self.links_box.index(f"@{event.x},{event.y}")
        tags = self.links_box.tag_names(idx)
        for tag in tags:
            if tag.startswith("http"):
                webbrowser.open(tag)
