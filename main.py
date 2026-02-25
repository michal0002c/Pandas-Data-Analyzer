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
            df = pd.read_excel(path)
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

def show_columns():
    global df

    if df is None:
        messagebox.showerror("Error", "No data")
        return
    
    cols = "\n".join(df.columns)
    messagebox.showinfo("Columns", cols)

btn_cols = tk.Button(app, text="Show Columns", command=show_columns)
btn_cols.pack()

tk.Label(app, text="Index").pack()
entry_index = tk.Entry(app)
entry_index.pack()

tk.Label(app, text="Columns").pack()
entry_columns = tk.Entry(app)
entry_columns.pack()

tk.Label(app, text="Values").pack()
entry_values = tk.Entry(app)
entry_values.pack()

def make_pivot():
    global df

    if df is None:
        messagebox.showerror("Error", "No data")
        return

    index = entry_index.get()
    columns = entry_columns.get()
    values = entry_values.get()

    try:
        pivot = pd.pivot_table(
            df,
            index=index,
            columns=columns,
            values=values,
            aggfunc="sum"
        )

        text.delete(1.0, tk.END)
        text.insert(tk.END, pivot.to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))

btn_pivot = tk.Button(app, text="Make Pivot", command=make_pivot)
btn_pivot.pack()

app.mainloop()


