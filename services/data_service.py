import pandas as pd


class DataService:

    def load_file(self, path):
        if path.endswith(".csv"):
            return pd.read_csv(path)

        if path.endswith(".xlsx"):
            return pd.read_excel(path)

        raise ValueError("Unsupported file format")


    def pivot(self, df, index, columns, values, agg):
        return pd.pivot_table(
            df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=agg
        )


    def analyze(self, df, column, agg):

        if agg == "sum":
            result = df[column].sum()

        elif agg == "mean":
            result = df[column].mean()

        else:
            result = df[column].count()

        return pd.DataFrame({
            "Column": [column],
            "Result": [result]
        })


    def filter(self, df, column, value):
        return df[df[column].astype(str).str.contains(value, na=False)]


    def merge(self, df1, df2, left, right, how):
        return pd.merge(df1, df2, left_on=left, right_on=right, how=how)
    
    def groupby(self, df, group_col, value_col, agg):

        result = (
            df
            .groupby(group_col)[value_col]
            .agg(agg)
            .reset_index()
        )

        return result
    
def sort(self, df, column, ascending=True):

    return df.sort_values(by=column, ascending=ascending)

def value_counts(self, df, column):

    result = df[column].value_counts().reset_index()

    result.columns = [column, "count"]

    return result