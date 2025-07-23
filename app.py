import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.title("🍬CANDY DATASETS ANALYSIS")
st.write("Dự án này tập trung vào việc phân tích dữ liệu bán hàng của các sản phẩm tiêu dùng nhanh từ nhiều nhà sản xuất và thương hiệu khác nhau, được phân phối qua nhiều kênh siêu thị, cửa hàng đặc sản và các chuỗi bán lẻ. Bộ dữ liệu phản ánh chi tiết về khối lượng tiêu thụ và doanh thu của các sản phẩm theo thời gian (năm, tháng), kênh phân phối, loại sản phẩm, bao bì và nhà sản xuất")
st.write("Mục tiêu của dự án là hiểu rõ hơn về hiệu suất bán hàng của các sản phẩm trên từng kênh và thị trường, phân tích sự thay đổi trong xu hướng tiêu dùng và xác định yếu tố ảnh hưởng đến doanh thu và khối lượng tiêu thụ. Kết quả cảu phân tích này sẽ hỗ trợ các bên liên quan đưa ra quyết định chiến lược nhằm tối ưu hóa hoạt động kinh doanh và phân phối sản phẩm")
# ==== 1. Đọc dữ liệu từ file Excel, sheet "c1" ====
df = pd.read_excel("data.xlsx", sheet_name="c1")

# ==== 2. Giao diện Streamlit ====
st.header("📈 Doanh số theo từng năm")

# ==== 3. Vẽ biểu đồ line ====
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df, x="YEAR", y="SALESAMOUNT", marker="o", ax=ax)
ax.set_ylabel("Doanh số")
ax.set_xlabel("Năm")
ax.set_title("Doanh số theo từng năm")
ax.grid(True)

# Hiển thị biểu đồ trên Streamlit
st.pyplot(fig)

# ==== 4. Hiển thị bảng dữ liệu nếu muốn ====
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)


df_volume = pd.read_excel("data.xlsx", sheet_name="c2")   
st.header("📦 Khối lượng bán theo tháng trong từng năm")

# Cho phép chọn năm để lọc
years = sorted(df_volume["YEAR"].unique())
selected_years = st.multiselect("Chọn năm:", years, default=years)

filtered_volume = df_volume[df_volume["YEAR"].isin(selected_years)]

fig2, ax2 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=filtered_volume,
    x="MONTH",
    y="TOTALSALES",
    hue="YEAR",
    marker="o",
    ax=ax2
)
ax2.set_xticks(range(1, 13))
ax2.set_xlabel("Tháng")
ax2.set_ylabel("Khối lượng bán")
ax2.set_title("Khối lượng bán theo từng tháng")
ax2.legend(title="Năm", bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True)
st.pyplot(fig2)

# ==== 4. Bảng dữ liệu nếu cần ====
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(filtered_volume)
    
    
# ==== 5. Biểu đồ tổng doanh số theo năm và quý ====
st.header("📆 Doanh số theo từng quý trong năm")

# Đọc dữ liệu từ sheet 'c3'
df_quarter = pd.read_excel("data.xlsx", sheet_name="c3")

# Bộ lọc năm nếu muốn
selected_years_q = st.multiselect(
    "Chọn năm để xem theo quý:", 
    sorted(df_quarter["YEAR"].unique()), 
    default=sorted(df_quarter["YEAR"].unique())
)

filtered_quarter = df_quarter[df_quarter["YEAR"].isin(selected_years_q)]

# Vẽ biểu đồ line hoặc bar
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=filtered_quarter,
    x="QUARTER",
    y="SALESAMOUNT",
    hue="YEAR",
    marker="o",
    ax=ax3
)
ax3.set_xticks([1, 2, 3, 4])
ax3.set_xlabel("Quý")
ax3.set_ylabel("Doanh số")
ax3.set_title("Doanh số theo từng quý")
ax3.legend(title="Năm", bbox_to_anchor=(1.05, 1), loc='upper left')
ax3.grid(True)
st.pyplot(fig3)

# Hiển thị bảng dữ liệu nếu cần
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(filtered_quarter)
    
# Cấu hình matplotlib tiếng Việt (nếu cần hiển thị dấu tiếng Việt)
plt.rcParams['font.family'] = 'DejaVu Sans'

st.header("📊 Biểu đồ tăng trưởng doanh số theo năm (%)")

# Đọc sheet c4
df = pd.read_excel("data.xlsx", sheet_name="c4")

# Tạo nhãn năm ghép (ví dụ: 2018–2019)
df["YEAR_LABEL"] = df["YEAR1"].astype(str) + "-" + df["YEAR2"].astype(str)

# Tạo màu: xanh nếu dương, đỏ nếu âm
colors = df["GROWTHPERCENT"].apply(lambda x: "green" if x >= 0 else "red")

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df["YEAR_LABEL"], df["GROWTHPERCENT"], color=colors)

# Vẽ đường mức 0
ax.axhline(0, color="black", linewidth=1)

# Gắn nhãn phần trăm trên đầu cột
for bar, value in zip(bars, df["GROWTHPERCENT"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + (0.3 if value >= 0 else -0.8),
        f"{value:.2f}%",
        ha='center',
        va='bottom' if value >= 0 else 'top',
        fontsize=10,
        color='black'
    )

ax.set_title("Tăng trưởng doanh số theo năm (%)")
ax.set_ylabel("Tăng trưởng (%)")
ax.set_xlabel("Giai đoạn")
plt.xticks(rotation=45)
plt.tight_layout()

# Hiển thị biểu đồ trong Streamlit
st.pyplot(fig)

# Tuỳ chọn: hiển thị bảng dữ liệu
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
    
    
st.header("📊 Doanh số cao nhất và thấp nhất theo tháng trong từng năm")

# Đọc dữ liệu từ sheet 'c6'
df = pd.read_excel("data.xlsx", sheet_name="c5")

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.35
x = range(len(df))

# Bar Max và Min
bars1 = ax.bar(
    [i - bar_width / 2 for i in x],
    df['MAXSALESAMOUNT'],
    width=bar_width,
    color='orange',
    label='MAXSALESAMOUNT'
)

bars2 = ax.bar(
    [i + bar_width / 2 for i in x],
    df['MINSALESAMOUNT'],
    width=bar_width,
    color='yellow',
    label='MINSALESAMOUNT'
)

# Thêm nhãn tháng trên đầu cột
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    ax.text(
        bar1.get_x() + bar1.get_width() / 2,
        bar1.get_height() + 50000,
        f"Tháng {df.loc[i, 'MAXMONTH']}",
        ha='center',
        va='bottom',
        fontsize=9
    )
    ax.text(
        bar2.get_x() + bar2.get_width() / 2,
        bar2.get_height() + 50000,
        f"Tháng {df.loc[i, 'MINMONTH']}",
        ha='center',
        va='bottom',
        fontsize=9
    )

ax.set_xticks(x)
ax.set_xticklabels(df['YEAR'])
ax.set_ylabel("Sales Amount")
ax.set_title("MAX và MIN SALES AMOUNT theo năm và tháng")
ax.legend()

plt.tight_layout()
st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
    
st.header("📈 Top sản phẩm có tăng trưởng cao nhất từng năm")

# Đọc dữ liệu từ sheet c7
df = pd.read_excel("data.xlsx", sheet_name="c6")

# Tạo cột nhãn năm
df['YEAR_LABEL'] = df['YEAR1'].astype(str) + '-' + df['YEAR2'].astype(str)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df['YEAR_LABEL'], df['GROWTHSALES'], color='mediumseagreen')

# Hiển thị nhãn tên sản phẩm và phần trăm tăng trưởng trên đầu mỗi cột
# for bar, name, percent in zip(bars, df['PRODUCTNAME'], df['GROWTHPERCENT']):
#     ax.text(
#         bar.get_x() + bar.get_width()/2,
#         bar.get_height() + 100000,
#         f"{name}\n{percent:,.2f}%",
#         ha='center',
#         va='bottom',
#         rotation=90,
#         fontsize=8
#     )

ax.set_ylabel("Tăng trưởng (%)")
ax.set_title("Top sản phẩm có tăng trưởng cao nhất từng năm")
plt.tight_layout()
st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
 
    
st.header("🏬 Doanh số và khối lượng bán theo Distribution Channel")

# Đọc dữ liệu từ sheet 'c8'
df = pd.read_excel("data.xlsx", sheet_name='c7')

fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(df['DISTRIBUTION_CHANNEL']))
width = 0.35

# Vẽ TOTALSALES
ax.bar(x - width/2, df['TOTALSALES'], width, label='Tổng sản phẩm (TOTALSALES)', color='royalblue')

# Vẽ SALESAMOUNT
ax.bar(x + width/2, df['SALESAMOUNT'], width, label='Doanh số (SALESAMOUNT)', color='darkorange')

ax.set_xlabel("Kênh phân phối")
ax.set_ylabel("Giá trị")
ax.set_title("Doanh số và khối lượng bán theo từng Distribution Channel")
ax.set_xticks(x)
ax.set_xticklabels(df['DISTRIBUTION_CHANNEL'], rotation=15, ha='right')
ax.legend()
plt.tight_layout()

st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)

# Đọc dữ liệu
df = pd.read_excel("data.xlsx", sheet_name="c8")

# Tạo cột 'YEAR_LABEL'
df['YEAR_LABEL'] = df['YEAR_1'].astype(str) + '–' + df['YEAR_2'].astype(str)

# Giao diện Streamlit
st.header("📈 Tăng trưởng doanh số theo từng kênh phân phối")

# Lọc kênh phân phối nếu muốn
channels = df['DISTRIBUTION_CHANNEL'].unique()
selected_channels = st.multiselect("Chọn kênh phân phối:", channels, default=channels)

# Lọc dữ liệu theo lựa chọn
filtered_df = df[df['DISTRIBUTION_CHANNEL'].isin(selected_channels)]

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(
    data=filtered_df,
    x="YEAR_LABEL",
    y="GROWTHPERCENT",
    hue="DISTRIBUTION_CHANNEL",
    marker="o",
    ax=ax
)

ax.axhline(0, color='gray', linestyle='--')
ax.set_title("Tăng trưởng doanh số theo từng kênh phân phối qua các năm")
ax.set_ylabel("Tăng trưởng (%)")
ax.set_xlabel("Năm")
plt.xticks(rotation=45)
ax.legend(title="Kênh phân phối", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Hiển thị trên Streamlit
st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)

st.header("🏆 Nhà sản xuất có doanh số cao nhất từng năm")

# Đọc dữ liệu từ sheet "c9"
df = pd.read_excel("data.xlsx", sheet_name="c9")

# Tìm nhà sản xuất có doanh số cao nhất từng năm
top_manu_each_year = (
    df.groupby(['YEAR', 'MANUFACTURER'])['SALESAMOUNT']
    .sum()
    .reset_index()
    .sort_values(['YEAR', 'SALESAMOUNT'], ascending=[True, False])
    .drop_duplicates(subset='YEAR')
)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=top_manu_each_year, x='YEAR', y='SALESAMOUNT', hue='MANUFACTURER', dodge=False, palette='Set2', ax=ax)


ax.set_title("Nhà sản xuất có doanh số cao nhất từng năm")
ax.set_ylabel("Doanh số")
ax.set_xlabel("Năm")
# ax.legend_.remove()  # Ẩn legend nếu không cần
st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(top_manu_each_year)
    
    
    
# Đọc dữ liệu
df = pd.read_excel("data.xlsx", sheet_name="c10")

# Streamlit App
st.header("📈 Doanh số theo từng Nhà sản xuất theo từng năm")

# Lọc theo Manufacturer
manufacturers = df['MANUFACTURER'].dropna().unique()
selected_manufacturers = st.multiselect(
    "Chọn nhà sản xuất:", manufacturers, default=manufacturers
)

# Áp dụng lọc
filtered_df = df[df['MANUFACTURER'].isin(selected_manufacturers)]

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=filtered_df, x="YEAR", y="SALESAMOUNT", hue="MANUFACTURER", marker="o", ax=ax)

ax.set_title("Sales Amount by Manufacturer (2018–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Sales Amount")
ax.legend(title="Manufacturer", bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig)

# Xem bảng dữ liệu gốc đã lọc
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(filtered_df)


# Đọc dữ liệu
df = pd.read_excel("data.xlsx", sheet_name="c11")  # Sheet chứa bảng bạn cung cấp

# Hiển thị tiêu đề
st.header("🏅 Thương hiệu có hiệu suất doanh số trung bình mỗi sản phẩm tốt nhất trong từng kênh phân phối")

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=df, x="DISTRIBUTION_CHANNEL", y="AVG_SALES_PER_PRODUCT", hue="BRAND", dodge=False, palette="pastel", ax=ax)

# Ghi nhãn trên từng cột
for i, row in df.iterrows():
    ax.text(i, row["AVG_SALES_PER_PRODUCT"] + 5000, row["BRAND"], ha="center", fontsize=9, fontweight='bold')

# Tuỳ chỉnh trục
ax.set_title("Thương hiệu có hiệu suất doanh số trung bình mỗi sản phẩm tốt nhất trong từng kênh phân phối")
ax.set_ylabel("Average Sales per Product")
ax.set_xlabel("Distribution Channel")
plt.xticks(rotation=30, ha='right')

st.pyplot(fig)

# Tuỳ chọn hiển thị dữ liệu
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
    
# Đọc dữ liệu
df = pd.read_excel("data.xlsx", sheet_name="c12")  # Sheet chứa bảng bạn đưa

# Hiển thị tiêu đề
st.header("📊 Doanh số theo từng Loại Sản phẩm (Product Category) từ 2018 đến 2024")

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df, x="YEAR", y="SALESAMOUNT", hue="CATEGORY", marker="o", ax=ax)

# Tùy chỉnh biểu đồ
ax.set_title("Sales Amount by Product Category (2018–2024)")
ax.set_xlabel("Year")
ax.set_ylabel("Sales Amount")
ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Hiển thị biểu đồ
st.pyplot(fig)

# Hiển thị bảng dữ liệu nếu muốn
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
    
# Đọc dữ liệu
df = pd.read_excel("data.xlsx", sheet_name="c13")  # Sheet chứa bảng BRAND bạn đưa

# Tiêu đề
st.header("🏆 Thương hiệu có doanh số cao nhất trong từng Category theo từng năm")

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(14, 6))

# Tạo biểu đồ cột nhóm theo CATEGORY và YEAR
sns.barplot(data=df, x="YEAR", y="TOTALSALES", hue="CATEGORY", palette="Set2", ax=ax)

# Thêm nhãn tên BRAND lên trên mỗi cột
# for i, row in df.iterrows():
#     ax.text(
#         x=row.name, 
#         y=row["TOTALSALES"] + 5000, 
#         s=row["BRAND"], 
#         rotation=90, 
#         ha="center", 
#         fontsize=8, 
#         color="black"
#     )

# Tùy chỉnh trục và tiêu đề
ax.set_title("Top Selling Brand per Category per Year")
ax.set_ylabel("Total Sales")
ax.set_xlabel("Year")
ax.set_xticks(range(len(df["YEAR"].unique())))
ax.set_xticklabels(sorted(df["YEAR"].unique()))

# Đưa chú thích ra ngoài
ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')

# Hiển thị biểu đồ
st.pyplot(fig)

# Tuỳ chọn xem bảng
with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)
    
    

st.header("🏆 Sản phẩm có doanh số cao nhất trong từng Manufacturer")
df = pd.read_excel("data.xlsx", sheet_name="c14")

# Tính tổng doanh số theo năm và nhà sản xuất
total_sales = df.groupby(["YEAR", "MANUFACTURER"])["SALESAMOUNT"].sum().reset_index()

# Tìm sản phẩm bán chạy nhất cho mỗi nhà sản xuất và năm
top_products = df.groupby(["YEAR", "MANUFACTURER"]).apply(
    lambda x: x.loc[x["SALESAMOUNT"].idxmax()]
).reset_index(drop=True)

# Gộp dữ liệu tổng doanh số với tên sản phẩm bán chạy
total_sales = total_sales.merge(
    top_products[["YEAR", "MANUFACTURER", "PRODUCTNAME"]],
    on=["YEAR", "MANUFACTURER"]
)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(20, 10))
chart = sns.barplot(
    data=total_sales,
    x="YEAR",
    y="SALESAMOUNT",
    hue="MANUFACTURER"
)

# # Ghi nhãn sản phẩm lên cột
# for index, row in total_sales.iterrows():
#     ax.text(
#         x=index, 
#         y=row["SALESAMOUNT"] , 
#         s=row["PRODUCTNAME"], 
#         rotation=90, 
#         ha="center", 
#         fontsize=8
#     )

# Cấu hình biểu đồ
plt.title("Doanh số theo năm và nhà sản xuất (hiển thị tên sản phẩm bán chạy nhất)", fontsize=16)
plt.xlabel("Năm", fontsize=12)
plt.ylabel("Tổng doanh số", fontsize=12)
plt.legend(title="Nhà sản xuất", bbox_to_anchor=(1.05, 1), loc='upper left')

# Hiển thị trên Streamlit
st.pyplot(fig)

with st.expander("📄 Xem dữ liệu gốc"):
    st.dataframe(df)