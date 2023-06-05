import tkinter as tk
from tkinter import filedialog, font, colorchooser

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.text_area = tk.Text(self.root)
        self.file_path = None
        self.current_font_family = "Arial"
        self.current_font_size = 12
        self.text_area.configure(font=(self.current_font_family, self.current_font_size))

        self.text_area.pack(fill=tk.BOTH, expand=1)

    def set_title(self):
        if self.file_path:
            self.root.title(self.file_path + " - TextEditor")
        else:
            self.root.title("Untitled - TextEditor")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.set_title()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                    filetypes=[("All Files", "*.*"),
                                                               ("Text Files", "*.txt"),
                                                               ("Python Scripts", "*.py")])
        if self.file_path:
            self.text_area.delete(1.0, tk.END)
            with open(self.file_path, "r") as file:
                self.text_area.insert(tk.INSERT, file.read())
                self.set_title()

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                          filetypes=[("All Files", "*.*"),
                                                                     ("Text Files", "*.txt"),
                                                                     ("Python Scripts", "*.py")])
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
                self.set_title()

    def change_font(self, *args):
        self.current_font_family = self.font_var.get()
        self.text_area.configure(font=(self.current_font_family, self.current_font_size))

    def change_bold(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
            bold_font = font.Font(self.text_area, self.text_area.cget("font"))
            bold_font.configure(weight="bold")
            self.text_area.tag_configure("bold", font=bold_font)

    def change_italic(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
            italic_font = font.Font(self.text_area, self.text_area.cget("font"))
            italic_font.configure(slant="italic")
            self.text_area.tag_configure("italic", font=italic_font)

    def highlight(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_add("highlight", "sel.first", "sel.last")
            self.text_area.tag_configure("highlight", background=color)


if __name__ == "__main__":
    root = tk.Tk()
    te = TextEditor(root)
    
    # Creating the menu bar
    menubar = tk.Menu(root)
    
    # Adding File menu
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=te.new_file)
    filemenu.add_command(label="Open", command=te.open_file)
    filemenu.add_command(label="Save", command=te.save_file)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    # Adding Font menu
    te.font_var = tk.StringVar(root)
    te.font_var.set("Arial")
    fontmenu = tk.Menu(menubar, tearoff=0)
    fonts = list(font.families())
    fonts.sort()
    for f in fonts:
        fontmenu.add_radiobutton(label=f, variable=te.font_var, command=te.change_font)
    menubar.add_cascade(label="Font", menu=fontmenu)

    # Adding Style menu
    stylemenu = tk.Menu(menubar, tearoff=0)
    stylemenu.add_command(label="Bold", command=te.change_bold)
    stylemenu.add_command(label="Italic", command=te.change_italic)
    stylemenu.add_command(label="Highlight", command=te.highlight)
    menubar.add_cascade(label="Style", menu=stylemenu)
    
    root.config(menu=menubar)
    root.mainloop()