from tkinter import ttk


class TableViewer:

    def __init__(self, parent):

        self.tree = ttk.Treeview(parent)
        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=scrollbar.set)


    def display(self, df):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for _, row in df.head(200).iterrows():
            self.tree.insert("", "end", values=list(row))