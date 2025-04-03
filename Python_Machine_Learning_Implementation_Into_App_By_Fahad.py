import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk, messagebox

try:
    df = pd.read_csv('Sample_Superstore.csv')
    required_columns = {'Sales','Profit','Quantity'}
    if not required_columns.issubset(df.columns):
        raise ValueError ("Missing required columns in the dataset")
except Exception as e:
        messagebox.showerror("Error", f"Failed to load dataset: {e}")
        exit()

y = df['Quantity']
x = df[['Sales','Profit']]
x = sm.add_constant(x)
model = sm.OLS(y, x).fit()
summary_str = model.summary().as_text()


root = tk.Tk()
root.title("OLS Regression App")
root.geometry("950x950")

#data_tree is a name you can give any name you want.

data_frame = ttk.Frame(root)
data_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

data_cols = ["Sales", "Profit", "Quantity"]
data_tree = ttk.Treeview(data_frame, columns=data_cols, show='headings', height=10)
for col in data_cols:
    data_tree.heading(col, text=col)
    data_tree.column(col, width=100)


scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=data_tree.yview)
data_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
data_tree.pack()

def load_data(rows=10):
    data_tree.delete(*data_tree.get_children())
    data_subset = df[['Sales', 'Profit', 'Quantity']].head(rows)
    for index, row in data_subset.iterrows():
        data_tree.insert("", "end", values=(row["Sales"], row["Profit"], row["Quantity"]))

load_data()

summary_frame = ttk.Frame(root)
summary_frame.pack(pady=10)

cols = ["Index","Details"]
tree = ttk.Treeview(summary_frame, columns=cols,  show='headings', height=15)
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=300 if col == "Index" else 500)

summary_scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=summary_scrollbar.set)
summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack()


summary_lines = summary_str.split('\n')
for i, line in enumerate(summary_lines):
    tree.insert("","end", values=(i, line))



def show_example_graph():
    x_vals = np.array([1, 2, 3, 4, 5])
    y_vals=np.array([7, 14, 15, 18, 19])
    x_mean, y_mean = np.mean(x_vals), np.mean(y_vals)
    Sxy = np.sum((x_vals - x_mean) * (y_vals - y_mean))
    Sxx = np.sum((x_vals - x_mean) ** 2)
    b1 = Sxy/ Sxx
    b0 = y_mean - b1 * x_mean
    y_pred = b0 + b1 * x_vals
    plt.scatter(x_vals, y_vals, color='blue', label='Data points')
    plt.xlabel('Independent variable x')
    plt.ylabel('Dependent variable y')
    plt.legend()
    plt.show()

def show_profit_vs_sales_regression():
    profit = df[['Profit']]
    sales = df['Sales']
    profit = sm.add_constant(profit)
    model_profit_sales = sm.OLS(sales, profit).fit()
    y_pred = model_profit_sales.predict(profit)
    plt.scatter(df['Profit'],df['Sales'], color='blue', label='Profit vs Sales')
    plt.plot(df['Profit'], y_pred, color='red', label='Regression line')
    plt.xlabel('Profit')
    plt.ylabel('Sales')
    plt.legend()
    plt.show()


def show_smooth_scatter_chart():
    plt.figure(figsize=(8,6))
    sns.set_style("whitegrid")


    scatter = sns.scatterplot(
        x = df['Profit'],
        y = df['Sales'],
        hue=df['Profit'] >= 0,
        palette={True: "green", False: "red"},
        marker="o"
        )

    sns.regplot(
        x=df['Profit'],
        y=df['Sales'],
        scatter=False,
        lowess=True,
        line_kws={'color': 'red'}
        )

    plt.xlabel('Profit')
    plt.ylabel('Sales')
    plt.title('Sacatter Chart with Smooth Line')
    plt.legend(['Regression Line', 'Postive Profit', 'Negative Profit'])
    plt.show()


def update_data():
    try:
        num_rows = int(row_entry.get())
        if num_rows <1:
            raise ValueError("Number of rows must be postive")
        load_data(num_rows)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid positive integer")



row_selection_frame = ttk.Frame(root)
row_selection_frame.pack(pady=5)

ttk.Label(row_selection_frame, text="Rows to display:").pack(side=tk.LEFT, padx=5)
row_entry = ttk.Entry(row_selection_frame,width=5)
row_entry.insert(0, "10")
row_entry.pack(side=tk.LEFT)
ttk.Button(row_selection_frame, text="Load Data", command=update_data).pack(side=tk.LEFT, padx=5)

btn_example = tk.Button(root, text="Show Example Regression Graph", command=show_example_graph)
btn_example.pack(pady=5)

btn_profit_sales = tk.Button(root, text="Show Profit vs Sales Regression", command=show_profit_vs_sales_regression)
btn_profit_sales.pack(pady=5)

btn_smooth_scatter = tk.Button(root, text="Show Smooth Scatter Chart", command=show_smooth_scatter_chart)
btn_smooth_scatter.pack(pady=5)

root.mainloop()
