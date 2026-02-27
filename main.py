import pandas as pd
import tkinter as tk
import os
from tkinter import filedialog, messagebox, ttk

# -------- GLOBAL --------
df = None
df2 = None
result_df = None

# -------- APP --------
app = tk.Tk()
app.title("Data Analyzer App")
app.geometry("650x600")
app.configure(bg="#2b2b2b")

style = ttk.Style()
style.theme_use("default")

style.configure("TLabel", background="#2b2b2b", foreground="white")
style.configure("TFrame", background="#2b2b2b")
style.configure("TLabelframe", background="#2b2b2b", foreground="white")
style.configure("TLabelframe.Label", background="#2b2b2b", foreground="white")
style.configure("TButton", padding=6)
style.configure("TCombobox", padding=5)

# -------- FUNKCJE --------

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
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        combo_analyze['values'] = numeric_cols
        combo_merge_left['values'] = cols

        app.title(f"Data Analyzer - {path}")

        messagebox.showinfo("OK", "File 1 loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    label_file1.config(text=f"File 1: {os.path.basename(path)}")

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

        combo_merge_right['values'] = list(df2.columns)

        messagebox.showinfo("OK", "File 2 loaded")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    label_file2.config(text=f"File 2: {os.path.basename(path)}")

def show_data():
    if df is None:
        messagebox.showerror("Error", "No data")
        return

    text.delete(1.0, tk.END)
    text.insert(tk.END, df.to_string())


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

    index = combo_index.get()
    columns = combo_columns.get()
    values = combo_values.get()
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
        text.insert(tk.END, f"Rows: {len(result_df)}\n\n")
        text.insert(tk.END, result_df.head(20).to_string())
    except Exception as e:
        messagebox.showerror("Error", str(e))


def analyze_column():
    global result_df

    if df is None:
        messagebox.showerror("Error", "No data")
        return

    col = combo_analyze.get()
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
        text.insert(tk.END, f"Rows: {len(result_df)}\n\n")
        text.insert(tk.END, result_df.head(20).to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))


def merge_data():
    global result_df

    if df is None or df2 is None:
        messagebox.showerror("Error", "Load both files")
        return

    left = combo_merge_left.get()
    right = combo_merge_right.get()
    how = combo_merge_type.get()

    if not left or not right:
        messagebox.showerror("Error", "Select columns")
        return

    try:
        result_df = pd.merge(df, df2, left_on=left, right_on=right, how=how)

        text.delete(1.0, tk.END)
        text.insert(tk.END, f"Rows: {len(result_df)}\n\n")
        text.insert(tk.END, result_df.head(20).to_string())

    except Exception as e:
        messagebox.showerror("Error", str(e))


def export_to_excel():
    if result_df is None and df is None:
        messagebox.showerror("Error", "No data")
        return

    path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if not path:
        return

    try:
        (result_df if result_df is not None else df).to_excel(path)
        messagebox.showinfo("Success", "Saved")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------- UI --------

# TOP BAR
frame_top = ttk.Frame(app)
frame_top.pack(pady=10)

label_file1 = tk.Label(app, text="File 1: not loaded", fg="white", bg="#2b2b2b")
label_file1.pack()

label_file2 = tk.Label(app, text="File 2: not loaded", fg="white", bg="#2b2b2b")
label_file2.pack()
ttk.Button(frame_top, text="Load File 1", command=load_file).grid(row=0, column=0, padx=5)
ttk.Button(frame_top, text="Load File 2", command=load_file2).grid(row=0, column=1, padx=5)
ttk.Button(frame_top, text="Show Data", command=show_data).grid(row=0, column=2, padx=5)
ttk.Button(frame_top, text="Columns", command=show_columns).grid(row=0, column=3, padx=5)

# ANALYSIS
frame_analysis = ttk.LabelFrame(app, text="Analysis")
frame_analysis.pack(fill="x", padx=10, pady=5)

combo_index = ttk.Combobox(frame_analysis, state="readonly")
combo_columns = ttk.Combobox(frame_analysis, state="readonly")
combo_values = ttk.Combobox(frame_analysis, state="readonly")
combo_analyze = ttk.Combobox(frame_analysis, state="readonly")
combo_agg = ttk.Combobox(frame_analysis, state="readonly")

combo_agg['values'] = ["sum", "mean", "count"]
combo_agg.current(0)

labels = ["Index", "Columns", "Values", "Aggregation", "Analyze"]
widgets = [combo_index, combo_columns, combo_values, combo_agg, combo_analyze]

for i, (label, widget) in enumerate(zip(labels, widgets)):
    tk.Label(frame_analysis, text=label).grid(row=i, column=0, padx=5, pady=5)
    widget.grid(row=i, column=1, padx=5, pady=5)

# MERGE
frame_merge = ttk.LabelFrame(app, text="Merge")
frame_merge.pack(fill="x", padx=10, pady=5)

combo_merge_left = ttk.Combobox(frame_merge, state="readonly")
combo_merge_right = ttk.Combobox(frame_merge, state="readonly")
combo_merge_type = ttk.Combobox(frame_merge, state="readonly")

combo_merge_type['values'] = ["inner", "left", "right"]
combo_merge_type.current(0)

merge_labels = ["Left Column", "Right Column", "Type"]
merge_widgets = [combo_merge_left, combo_merge_right, combo_merge_type]

for i, (label, widget) in enumerate(zip(merge_labels, merge_widgets)):
    tk.Label(frame_merge, text=label).grid(row=i, column=0, padx=5, pady=5)
    widget.grid(row=i, column=1, padx=5, pady=5)

# ACTIONS
frame_actions = ttk.Frame(app)
frame_actions.pack(pady=10)

ttk.Button(frame_actions, text="Pivot", command=make_pivot).grid(row=0, column=0, padx=5)
ttk.Button(frame_actions, text="Analyze", command=analyze_column).grid(row=0, column=1, padx=5)
ttk.Button(frame_actions, text="Merge", command=merge_data).grid(row=0, column=2, padx=5)
ttk.Button(frame_actions, text="Export", command=export_to_excel).grid(row=0, column=3, padx=5)

# OUTPUT
text = tk.Text(app, bg="#1e1e1e", fg="#00ffcc", font=("Consolas", 10))
text.pack(fill="both", expand=True, padx=10, pady=10)

# START
app.mainloop()