import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

df = None

app = tk.Tk()

app.title("Data Analyzer App")
app.geometry("600x400")

def load_file():
    global df

    path = filedialog.askopenfilename()

    if not path:
        return
    
    try:
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".xlsx"):
            df = pdf.read_excel(path)
        else:
            messagebox.showerror("Error", "Incorrect file format")
            return
        
        messagebox.showinfo("Ok", "The file has been loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))

btn_load = tk.Button(app, text="Load file", command=load_file)
btn_load.pack()

text = tk.Text(app, height=15)
text.pack()

def show_data():
    global df

    if df is None:
        messagebox.showerror("Error", "No data")
        return
    
    text.delete(1.0, tk.END)
    text.insert(tk.END, df.head().to_string())

btn_show = tk.Button(app, text="Show Data", command=show_data)
btn_show.pack()

app.mainloop()


