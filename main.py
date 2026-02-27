import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# -------- GLOBAL --------
df = None
df2 = None
result_df = None

# -------- APP --------
app = tk.Tk()
app.title("Data Analyzer App")
app.geometry("650x600")

# -------- FUNKCJE --------

# -------- LOAD FILE 1 --------
def load_file():
    global df, result_df

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

        result_df = None

        cols = list(df.columns)

        combo_index['values'] = cols
        combo_columns['values'] = cols
        combo_values['values'] = cols
        combo_analyze['values'] = cols
        combo_merge_left['values'] = cols

        app.title(f"Data Analyzer - {path}")

        messagebox.showinfo("OK", "File 1 loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------- LOAD FILE 2 --------
def load_file2():
    global df2

    path = filedialog.askopenfilename()

    if not path:
        return

    try:
        if path.endswith(".csv"):
            df2 = pd.read_csv(path)
        elif path.endswith(".xlsx"):
            df2 = pd.read_excel(path)
        else:
            messagebox.showerror("Error", "Incorrect file format")
            return

        cols = list(df2.columns)
        combo_merge_right['values'] = cols

        messagebox.showinfo("OK", "File 2 loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------- SHOW DATA --------
def show_data():
    global df

    if df is None:
        messagebox.showerror("Error", "No data")
        return

    text.delete(1.0, tk.END)
    text.insert(tk.END, df.head().to_string())


# -------- SHOW COLUMNS --------
def show_columns():
    global df

    if df is None:
        messagebox.showerror("Error", "No data")
        return

    messagebox.showinfo("Columns", "\n".join(df.columns))


# -------- PIVOT --------
def make_pivot():
    global df, result_df

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


# -------- ANALYZE --------
def analyze_column():
    global df, result_df

    if df is None:
        messagebox.showerror("Error", "No data")
        return

    col = combo_analyze.get().strip()
    agg = combo_agg.get()

    if col not in df.columns:
        messagebox.showerror("Error", "Column not found")
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
        text.insert(tk.END, result_df.to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------- MERGE --------
def merge_data():
    global df, df2, result_df

    if df is None or df2 is None:
        messagebox.showerror("Error", "Load both files")
        return

    left_col = combo_merge_left.get().strip()
    right_col = combo_merge_right.get().strip()
    how = combo_merge_type.get()

    if not left_col or not right_col:
        messagebox.showerror("Error", "Select columns")
        return

    try:
        result_df = pd.merge(
            df,
            df2,
            left_on=left_col,
            right_on=right_col,
            how=how
        )

        text.delete(1.0, tk.END)
        text.insert(tk.END, result_df.head().to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------- EXPORT --------
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

frame_main = tk.Frame(app)
frame_main.pack(pady=10)

# --- buttons ---
tk.Button(frame_top, text="Load File 1", command=load_file).pack(side="left", padx=5)
tk.Button(frame_top, text="Load File 2", command=load_file2).pack(side="left", padx=5)
tk.Button(frame_top, text="Show Data", command=show_data).pack(side="left", padx=5)
tk.Button(frame_top, text="Columns", command=show_columns).pack(side="left", padx=5)

# --- comboboxes ---
combo_index = ttk.Combobox(frame_main, state="readonly")
combo_columns = ttk.Combobox(frame_main, state="readonly")
combo_values = ttk.Combobox(frame_main, state="readonly")
combo_analyze = ttk.Combobox(frame_main, state="readonly")

combo_merge_left = ttk.Combobox(frame_main, state="readonly")
combo_merge_right = ttk.Combobox(frame_main, state="readonly")
combo_merge_type = ttk.Combobox(frame_main, state="readonly")

combo_agg = ttk.Combobox(frame_main, state="readonly")
combo_agg['values'] = ["sum", "mean", "count"]
combo_agg.current(0)

# --- labels + grid ---
labels = [
    ("Index", combo_index),
    ("Columns", combo_columns),
    ("Values", combo_values),
    ("Aggregation", combo_agg),
    ("Analyze Column", combo_analyze),
    ("Merge Left", combo_merge_left),
    ("Merge Right", combo_merge_right),
    ("Merge Type", combo_merge_type),
]

for i, (text_label, widget) in enumerate(labels):
    tk.Label(frame_main, text=text_label).grid(row=i, column=0)
    widget.grid(row=i, column=1)

combo_merge_type['values'] = ["inner", "left", "right"]
combo_merge_type.current(0)

# --- actions ---
tk.Button(app, text="Make Pivot", command=make_pivot).pack(pady=5)
tk.Button(app, text="Analyze", command=analyze_column).pack(pady=5)
tk.Button(app, text="Merge Data", command=merge_data).pack(pady=5)
tk.Button(app, text="Export", command=export_to_excel).pack(pady=5)

# --- output ---
text = tk.Text(app, height=15)
text.pack()

# -------- START --------
app.mainloop()