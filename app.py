import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import os
import seaborn as sns

from services.data_service import DataService
from ui.table_viewer import TableViewer


class DataAnalyzerApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Data Analyzer")
        self.root.geometry("1100x700")

        self.df = None
        self.df2 = None
        self.result_df = None

        self.data_service = DataService()

        self.setup_style()
        self.build_layout()


    def setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="white")
        style.configure("TButton", padding=6)


    def build_layout(self):

        top = ttk.Frame(self.root)
        top.pack(fill="x", pady=10)

        ttk.Button(top, text="Load File 1", command=self.load_file).pack(side="left", padx=5)
        ttk.Button(top, text="Load File 2", command=self.load_file2).pack(side="left", padx=5)
        ttk.Button(top, text="Columns", command=self.show_columns).pack(side="left", padx=5)

        center = ttk.Frame(self.root)
        center.pack(fill="both", expand=True)

        left_panel = ttk.Frame(center)
        left_panel.pack(side="left", fill="y", padx=10)

        ttk.Button(left_panel, text="Show Data", command=self.show_data).pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Describe", command=self.describe_data).pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Missing", command=self.show_missing).pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Plot", command=self.plot_column).pack(fill="x", pady=2)
        ttk.Button(left_panel, text="Export", command=self.export_excel).pack(fill="x", pady=2)

        ttk.Button(left_panel, text="GroupBy", command=self.groupby_data).pack(fill="x")
        ttk.Button(left_panel, text="Sort", command=self.sort_data).pack(fill="x")
        ttk.Button(left_panel, text="Value Counts", command=self.value_counts).pack(fill="x")
        ttk.Button(left_panel, text="Correlation", command=self.correlation).pack(fill="x")
        
        right_panel = ttk.Frame(center)
        right_panel.pack(side="left", fill="both", expand=True)

        self.table = TableViewer(right_panel)


    def load_file(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        try:
            self.df = self.data_service.load_file(path)
            self.table.display(self.df)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def load_file2(self):

        path = filedialog.askopenfilename()

        if not path:
            return

        try:
            self.df2 = self.data_service.load_file(path)

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def show_data(self):

        if self.df is None:
            return

        self.table.display(self.df)


    def show_columns(self):

        if self.df is None:
            return

        messagebox.showinfo("Columns", "\n".join(self.df.columns))


    def describe_data(self):

        if self.df is None:
            return

        self.result_df = self.df.describe()
        self.table.display(self.result_df)


    def show_missing(self):

        if self.df is None:
            return

        self.result_df = self.df.isna().sum().to_frame(name="Missing")
        self.table.display(self.result_df)


    def plot_column(self):

        if self.df is None:
            return

        col = self.df.select_dtypes("number").columns[0]

        self.df[col].hist()
        plt.title(col)
        plt.show()


    def export_excel(self):

        data = self.result_df if self.result_df is not None else self.df

        if data is None:
            return

        path = filedialog.asksaveasfilename(defaultextension=".xlsx")

        if not path:
            return

        data.to_excel(path)

    def groupby_data(self):

        if self.df is None:
            return

        col = self.df.columns[0]
        value = self.df.select_dtypes("number").columns[0]

        result = self.data_service.groupby(self.df, col, value, "sum")

        self.result_df = result
        self.table.display(result)

    def correlation(self):

        if self.df is None:
            return

        result = self.data_service.correlation(self.df)

        self.result_df = result
        self.table.display(result)

    def drop_nulls(self):

        if self.df is None:
            return

        result = self.data_service.drop_nulls(self.df)

        self.result_df = result
        self.table.display(result)

    def correlation_plot(self):

        corr = self.data_service.correlation(self.df)

        sns.heatmap(corr, annot=True, cmap="coolwarm")

        plt.title("Correlation matrix")

        plt.show()
    def sort_data(self):

        if self.df is None:
            return

        col = self.df.columns[0]

        result = self.data_service.sort(self.df, col)

        self.result_df = result
        self.table.display(result)
    def value_counts(self):

        if self.df is None:
            return

        col = self.df.columns[0]

        result = self.data_service.value_counts(self.df, col)

        self.result_df = result
        self.table.display(result)