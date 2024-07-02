import tkinter
from tkinter import messagebox
import customtkinter
from CTkListbox import *
import os
from pypdf import PdfMerger
# import fitz
# from PIL import Image, ImageTk
import webbrowser
import time

# Full file path
full_file_paths = []

def select_file():
    filenames = customtkinter.filedialog.askopenfilenames(
        filetypes = [('PDF files', '*.pdf')]
    )

    for file in filenames:
        full_file_paths.append(file)
        listbox.insert('end', os.path.basename(file))

def merge_pdf(name):
    merger = PdfMerger()

    pdfs = listbox.get('all')

    if len(pdfs) == 0:
        messagebox.showerror('PDF Merger Error', 'Error: You need a minimum of 1 file')
        return

    for pdf in pdfs:
        for path in full_file_paths:
            if os.path.basename(path) == pdf:
                merger.append(path)
                break

    merger.write(name)
    merger.close()

def delete_files():
    selected_files = listbox.curselection()
    for file in selected_files[::-1]:
        listbox.delete(file)
        del full_file_paths[file]

def preview_pdf():
    merge_pdf('review.pdf')
    webbrowser.open_new(os.path.abspath('review.pdf'))

    time.sleep(1)
    os.remove('review.pdf')

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("PDF Merger")

title = customtkinter.CTkLabel(app, text="Combine PDFs together", font=('Arial', 25))
title.pack(padx=10, pady=10)

listbox = CTkListbox(app, multiple_selection = True)
listbox.pack(fill='both', expand=True, padx = 10, pady = 10)

button_frame = customtkinter.CTkFrame(app)
button_frame.pack(padx = 10, pady = 10)

select_PDFs = customtkinter.CTkButton(button_frame, text = "Select PDFs", command = select_file)
select_PDFs.pack(side = 'left', padx = 10, pady = 10)

merge_PDFs = customtkinter.CTkButton(button_frame, text = "Merge PDFs", command=lambda: merge_pdf('result.pdf'))
merge_PDFs.pack(side = 'right', padx = 10, pady = 10)

delete_file = customtkinter.CTkButton(app, text = "Delete Files", command = delete_files)
delete_file.pack(padx = 10, pady = 10)

preview_PDF = customtkinter.CTkButton(app, text = "Preview Merged PDF", command = preview_pdf)
preview_PDF.pack(padx = 10, pady = 10)

app.mainloop()