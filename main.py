import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# -------- GLOBAL --------
df = None
result_df = None

# -------- APP --------
app = tk.Tk()
app.title("Data Analyzer App")
app.geometry("600x500")

# -------- FUNKCJE --------

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

        cols = list(df.columns)

        combo_index['values'] = cols
        combo_columns['values'] = cols
        combo_values['values'] = cols
        combo_analyze['values'] = cols

        messagebox.showinfo("Ok", "File loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def show_data():
    if df is None:
        messagebox.showerror("Error", "No data")
        return
    
    text.delete(1.0, tk.END)
    text.insert(tk.END, df.head().to_string())


def show_columns():
    if df is None:
        messagebox.showerror("Error", "No data")
        return
    
    messagebox.showinfo("Columns", "\n".join(df.columns))


def make_pivot():
    global result_df
    if df is None:
        messagebox.showerror("Error", "No data")
        return

    index = combo_index.get().strip()
    columns = combo_columns.get().strip()
    values = combo_values.get().strip()
    agg = combo_agg.get()

    if not index or not columns or not values:
        messagebox.showerror("Error", "Fill all fields")
        return

    try:
        result_df = pd.pivot_table(
            df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=agg
        )

        text.delete(1.0, tk.END)
        text.insert(tk.END, result_df.to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))


def analyze_column():
    global result_df
    if df is None:  
        messagebox.showerror("Error", "No data")
        return

    col = combo_analyze.get().strip()
    agg = combo_agg.get()

    if not col:
        messagebox.showerror("Error", "Select column")
        return

    try:
        if agg == "sum":
            result = df[col].sum()
        elif agg == "mean":
            result = df[col].mean()
        elif agg == "count":
            result = df[col].count()

        result_df = pd.DataFrame({
            "Column": [col],
            "Aggregation": [agg],
            "Result": [result]
        })
        text.delete(1.0, tk.END)
        text.insert(tk.END, f"{agg} of {col} = {result}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_to_excel():
    global result_df, df

    if result_df is None and df is None:
        messagebox.showerror("Error", "No data to export")
        return

    path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if not path:
        return

    try:
        if result_df is not None:
            result_df.to_excel(path)
        else:
            df.to_excel(path)

        messagebox.showinfo("Success", "File saved")

    except Exception as e:
        messagebox.showerror("Error", str(e))
# -------- UI --------

frame_top = tk.Frame(app)
frame_top.pack(pady=10)

frame_pivot = tk.Frame(app)
frame_pivot.pack(pady=10)

# --- buttons top ---
tk.Button(frame_top, text="Load file", command=load_file).pack(side="left", padx=5)
tk.Button(frame_top, text="Show Data", command=show_data).pack(side="left", padx=5)
tk.Button(frame_top, text="Show Columns", command=show_columns).pack(side="left", padx=5)

# --- pivot section ---
tk.Label(frame_pivot, text="Index").grid(row=0, column=0)
combo_index = ttk.Combobox(frame_pivot)
combo_index.grid(row=0, column=1)

tk.Label(frame_pivot, text="Columns").grid(row=1, column=0)
combo_columns = ttk.Combobox(frame_pivot)
combo_columns.grid(row=1, column=1)

tk.Label(frame_pivot, text="Values").grid(row=2, column=0)
combo_values = ttk.Combobox(frame_pivot)
combo_values.grid(row=2, column=1)

tk.Label(frame_pivot, text="Aggregation").grid(row=3, column=0)
combo_agg = ttk.Combobox(frame_pivot)
combo_agg['values'] = ["sum", "mean", "count"]
combo_agg.current(0)
combo_agg.grid(row=3, column=1)

tk.Label(frame_pivot, text="Analyze Column").grid(row=4, column=0)
combo_analyze = ttk.Combobox(frame_pivot)
combo_analyze.grid(row=4, column=1)

tk.Button(app, text="Export to Excel", command=export_to_excel).pack(pady=5)
# --- actions ---
tk.Button(app, text="Make Pivot", command=make_pivot).pack(pady=5)
tk.Button(app, text="Analyze", command=analyze_column).pack(pady=5)

# --- output ---
text = tk.Text(app, height=15)
text.pack()

# -------- START --------
app.mainloop()