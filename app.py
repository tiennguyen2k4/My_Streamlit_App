import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Cấu hình page
st.set_page_config(
    page_title="Candy Dataset Analysis",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cấu hình matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('default')  # Sử dụng style mặc định cho tốc độ

# Cache function để đọc dữ liệu
@st.cache_data
def load_data():
    """Load all data sheets at once and cache them"""
    try:
        data_sheets = {}
        sheet_names = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13', 'c14']
        
        for sheet in sheet_names:
            data_sheets[sheet] = pd.read_excel("data.xlsx", sheet_name=sheet)
        
        return data_sheets
    except Exception as e:
        st.error(f"Lỗi khi đọc dữ liệu: {e}")
        return None

# Cache function cho việc tạo biểu đồ
@st.cache_data
def create_yearly_sales_chart(df):
    """Create yearly sales chart"""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x="YEAR", y="SALESAMOUNT", marker="o", ax=ax)
    ax.set_ylabel("Doanh số")
    ax.set_xlabel("Năm")
    ax.set_title("Doanh số theo từng năm")
    ax.grid(True)
    plt.tight_layout()
    return fig

@st.cache_data
def create_monthly_volume_chart(df_volume, selected_years):
    """Create monthly volume chart"""
    filtered_volume = df_volume[df_volume["YEAR"].isin(selected_years)]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=filtered_volume,
        x="MONTH",
        y="TOTALSALES",
        hue="YEAR",
        marker="o",
        ax=ax
    )
    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Tháng")
    ax.set_ylabel("Khối lượng bán")
    ax.set_title("Khối lượng bán theo từng tháng")
    ax.legend(title="Năm", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    plt.tight_layout()
    return fig

@st.cache_data
def create_quarterly_chart(df_quarter, selected_years_q):
    """Create quarterly sales chart"""
    filtered_quarter = df_quarter[df_quarter["YEAR"].isin(selected_years_q)]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=filtered_quarter,
        x="QUARTER",
        y="SALESAMOUNT",
        hue="YEAR",
        marker="o",
        ax=ax
    )
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xlabel("Quý")
    ax.set_ylabel("Doanh số")
    ax.set_title("Doanh số theo từng quý")
    ax.legend(title="Năm", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    plt.tight_layout()
    return fig

@st.cache_data
def create_growth_chart(df):
    """Create growth percentage chart"""
    df_copy = df.copy()
    df_copy["YEAR_LABEL"] = df_copy["YEAR1"].astype(str) + "-" + df_copy["YEAR2"].astype(str)
    colors = df_copy["GROWTHPERCENT"].apply(lambda x: "green" if x >= 0 else "red")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df_copy["YEAR_LABEL"], df_copy["GROWTHPERCENT"], color=colors)
    ax.axhline(0, color="black", linewidth=1)
    
    for bar, value in zip(bars, df_copy["GROWTHPERCENT"]):
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
    return fig

# Main app
def main():
    st.title("🍬 CANDY DATASETS ANALYSIS")
    
    # Load data
    with st.spinner("Đang tải dữ liệu..."):
        data_sheets = load_data()
    
    if data_sheets is None:
        st.error("Không thể tải dữ liệu. Vui lòng kiểm tra file data.xlsx")
        return
    
    # Introduction
    st.write("""
    Dự án này tập trung vào việc phân tích dữ liệu bán hàng của các sản phẩm tiêu dùng nhanh từ nhiều nhà sản xuất 
    và thương hiệu khác nhau, được phân phối qua nhiều kênh siêu thị, cửa hàng và các chuỗi bán lẻ.
    """)
    
    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    analysis_options = [
        "Doanh số theo năm",
        "Khối lượng bán theo tháng", 
        "Doanh số theo quý",
        "Tăng trưởng doanh số",
        "Min/Max doanh số",
        "Top sản phẩm tăng trưởng",
        "Doanh số theo kênh phân phối",
        "Tăng trưởng theo kênh",
        "Top nhà sản xuất",
        "Doanh số theo nhà sản xuất",
        "Thương hiệu theo kênh",
        "Doanh số theo loại sản phẩm",
        "Top thương hiệu theo category",
        "Top sản phẩm theo nhà sản xuất"
    ]
    
    selected_analysis = st.sidebar.selectbox("Chọn phân tích:", analysis_options)
    
    # Display selected analysis
    if selected_analysis == "Doanh số theo năm":
        st.header("📈 Doanh số theo từng năm")
        fig = create_yearly_sales_chart(data_sheets['c1'])
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(data_sheets['c1'])
    
    elif selected_analysis == "Khối lượng bán theo tháng":
        st.header("📦 Khối lượng bán theo tháng trong từng năm")
        
        years = sorted(data_sheets['c2']["YEAR"].unique())
        selected_years = st.multiselect("Chọn năm:", years, default=years)
        
        if selected_years:
            fig = create_monthly_volume_chart(data_sheets['c2'], selected_years)
            st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            filtered_data = data_sheets['c2'][data_sheets['c2']["YEAR"].isin(selected_years)]
            st.dataframe(filtered_data)
    
    elif selected_analysis == "Doanh số theo quý":
        st.header("📆 Doanh số theo từng quý trong năm")
        
        years_q = sorted(data_sheets['c3']["YEAR"].unique())
        selected_years_q = st.multiselect("Chọn năm:", years_q, default=years_q)
        
        if selected_years_q:
            fig = create_quarterly_chart(data_sheets['c3'], selected_years_q)
            st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            filtered_data = data_sheets['c3'][data_sheets['c3']["YEAR"].isin(selected_years_q)]
            st.dataframe(filtered_data)
    
    elif selected_analysis == "Tăng trưởng doanh số":
        st.header("📊 Biểu đồ tăng trưởng doanh số theo năm (%)")
        fig = create_growth_chart(data_sheets['c4'])
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(data_sheets['c4'])
    
    elif selected_analysis == "Min/Max doanh số":
        st.header("📊 Doanh số cao nhất và thấp nhất theo tháng trong từng năm")
        
        df = data_sheets['c5']
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bar_width = 0.35
        x = range(len(df))
        
        bars1 = ax.bar([i - bar_width / 2 for i in x], df['MAXSALESAMOUNT'], 
                      width=bar_width, color='orange', label='MAXSALESAMOUNT')
        bars2 = ax.bar([i + bar_width / 2 for i in x], df['MINSALESAMOUNT'], 
                      width=bar_width, color='yellow', label='MINSALESAMOUNT')
        
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            ax.text(bar1.get_x() + bar1.get_width() / 2, bar1.get_height() + 50000,
                   f"Tháng {df.loc[i, 'MAXMONTH']}", ha='center', va='bottom', fontsize=9)
            ax.text(bar2.get_x() + bar2.get_width() / 2, bar2.get_height() + 50000,
                   f"Tháng {df.loc[i, 'MINMONTH']}", ha='center', va='bottom', fontsize=9)
        
        ax.set_xticks(x)
        ax.set_xticklabels(df['YEAR'])
        ax.set_ylabel("Sales Amount")
        ax.set_title("MAX và MIN SALES AMOUNT theo năm và tháng")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Top sản phẩm tăng trưởng":
        st.header("📈 Top sản phẩm có tăng trưởng cao nhất từng năm")
        
        df = data_sheets['c6'].copy()
        df['YEAR_LABEL'] = df['YEAR1'].astype(str) + '-' + df['YEAR2'].astype(str)
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.bar(df['YEAR_LABEL'], df['GROWTHSALES'], color='mediumseagreen')
        
        # Thêm tên sản phẩm lên trên mỗi cột
        for i, (bar, row) in enumerate(zip(bars, df.itertuples())):
            # Rút ngắn tên sản phẩm nếu quá dài
            product_name = row.PRODUCTNAME if hasattr(row, 'PRODUCTNAME') else f"Product {i+1}"
            if len(product_name) > 15:
                product_name = product_name[:12] + "..."
            
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(df['GROWTHSALES']) * 0.02,  # Offset 2% từ đỉnh cột
                product_name,
                rotation=90,
                ha="left",
                va="bottom",
                fontsize=9,
                color="black",
                fontweight='bold'
            )
        
        # Tăng margin top để có chỗ cho text
        ax.set_ylim(0, max(df['GROWTHSALES']) * 1.3)
        
        ax.set_ylabel("Tăng trưởng (%)")
        ax.set_xlabel("Giai đoạn")
        ax.set_title("Top sản phẩm có tăng trưởng cao nhất từng năm")
        plt.xticks(rotation=15)
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Doanh số theo kênh phân phối":
        st.header("🏬 Doanh số và khối lượng bán theo Distribution Channel")
        
        df = data_sheets['c7']
        fig, ax = plt.subplots(figsize=(10, 5))
        
        x = np.arange(len(df['DISTRIBUTION_CHANNEL']))
        width = 0.35
        
        ax.bar(x - width/2, df['TOTALSALES'], width, 
               label='Tổng sản phẩm (TOTALSALES)', color='royalblue')
        ax.bar(x + width/2, df['SALESAMOUNT'], width, 
               label='Doanh số (SALESAMOUNT)', color='darkorange')
        
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
    
    elif selected_analysis == "Tăng trưởng theo kênh":
        st.header("📈 Tăng trưởng doanh số theo từng kênh phân phối")
        
        df = data_sheets['c8'].copy()
        df['YEAR_LABEL'] = df['YEAR_1'].astype(str) + '–' + df['YEAR_2'].astype(str)
        
        channels = df['DISTRIBUTION_CHANNEL'].unique()
        selected_channels = st.multiselect("Chọn kênh phân phối:", channels, default=channels)
        
        if selected_channels:
            filtered_df = df[df['DISTRIBUTION_CHANNEL'].isin(selected_channels)]
            
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
            st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Top nhà sản xuất":
        st.header("🏆 Nhà sản xuất có doanh số cao nhất từng năm")
        
        df = data_sheets['c9']
        top_manu_each_year = (
            df.groupby(['YEAR', 'MANUFACTURER'])['SALESAMOUNT']
            .sum()
            .reset_index()
            .sort_values(['YEAR', 'SALESAMOUNT'], ascending=[True, False])
            .drop_duplicates(subset='YEAR')
        )
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(data=top_manu_each_year, x='YEAR', y='SALESAMOUNT', 
                   hue='MANUFACTURER', dodge=False, palette='Set2', ax=ax)
        
        ax.set_title("Nhà sản xuất có doanh số cao nhất từng năm")
        ax.set_ylabel("Doanh số")
        ax.set_xlabel("Năm")
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(top_manu_each_year)
    
    elif selected_analysis == "Doanh số theo nhà sản xuất":
        st.header("📈 Doanh số theo từng Nhà sản xuất theo từng năm")
        
        df = data_sheets['c10']
        manufacturers = df['MANUFACTURER'].dropna().unique()
        selected_manufacturers = st.multiselect(
            "Chọn nhà sản xuất:", manufacturers, default=manufacturers
        )
        
        if selected_manufacturers:
            filtered_df = df[df['MANUFACTURER'].isin(selected_manufacturers)]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=filtered_df, x="YEAR", y="SALESAMOUNT", 
                        hue="MANUFACTURER", marker="o", ax=ax)
            
            ax.set_title("Sales Amount by Manufacturer (2018–2024)")
            ax.set_xlabel("Year")
            ax.set_ylabel("Sales Amount")
            ax.legend(title="Manufacturer", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            filtered_data = df[df['MANUFACTURER'].isin(selected_manufacturers)] if selected_manufacturers else df
            st.dataframe(filtered_data)
    
    elif selected_analysis == "Thương hiệu theo kênh":
        st.header("🏅 Thương hiệu có hiệu suất doanh số trung bình mỗi sản phẩm tốt nhất trong từng kênh phân phối")
        
        df = data_sheets['c11']
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df, x="DISTRIBUTION_CHANNEL", y="AVG_SALES_PER_PRODUCT", 
                   hue="BRAND", dodge=False, palette="pastel", ax=ax)
        
        for i, row in df.iterrows():
            ax.text(i, row["AVG_SALES_PER_PRODUCT"] + 5000, row["BRAND"], 
                   ha="center", fontsize=9, fontweight='bold')
        
        ax.set_title("Thương hiệu có hiệu suất doanh số trung bình mỗi sản phẩm tốt nhất trong từng kênh phân phối")
        ax.set_ylabel("Average Sales per Product")
        ax.set_xlabel("Distribution Channel")
        plt.xticks(rotation=30, ha='right')
        ax.legend().remove()  # Remove legend since we have text labels
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Doanh số theo loại sản phẩm":
        st.header("📊 Doanh số theo từng Loại Sản phẩm (Product Category) từ 2018 đến 2024")
        
        df = data_sheets['c12']
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=df, x="YEAR", y="SALESAMOUNT", hue="CATEGORY", marker="o", ax=ax)
        
        ax.set_title("Sales Amount by Product Category (2018–2024)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Sales Amount")
        ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Top thương hiệu theo category":
        st.header("🏆 Thương hiệu có doanh số cao nhất trong từng Category theo từng năm")
        
        df = data_sheets['c13']
        fig, ax = plt.subplots(figsize=(16, 10))
        
        chart = sns.barplot(data=df, x="YEAR", y="TOTALSALES", hue="CATEGORY", palette="Set2", ax=ax)
        
        # Thêm tên thương hiệu lên trên mỗi cột
        # Lấy vị trí các cột từ matplotlib patches
        bars = ax.patches
        
        # Tạo dictionary để mapping vị trí cột với dữ liệu
        bar_data = []
        for i, (_, row) in enumerate(df.iterrows()):
            bar_data.append({
                'x': bars[i].get_x() + bars[i].get_width() / 2,
                'y': bars[i].get_height(),
                'brand': row['BRAND']
            })
        
        # Hiển thị tên thương hiệu trên mỗi cột
        for bar_info in bar_data:
            # Rút ngắn tên thương hiệu nếu quá dài
            brand_name = bar_info['brand']
            if len(brand_name) > 12:
                brand_name = brand_name[:9] + "..."
            
            ax.text(
                bar_info['x'], 
                bar_info['y'] + max(df['TOTALSALES']) * 0.01,  # Offset 1% từ đỉnh cột
                brand_name, 
                rotation=90, 
                ha="left", 
                va="bottom",
                fontsize=9, 
                color="black",
                fontweight='bold'
            )
        
        # Tăng margin top để có chỗ cho text
        ax.set_ylim(0, max(df['TOTALSALES']) * 1.25)
        
        ax.set_title("Top Selling Brand per Category per Year", fontsize=16)
        ax.set_ylabel("Total Sales")
        ax.set_xlabel("Year")
        ax.set_xticks(range(len(df["YEAR"].unique())))
        ax.set_xticklabels(sorted(df["YEAR"].unique()))
        ax.legend(title="Category", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    elif selected_analysis == "Top sản phẩm theo nhà sản xuất":
        st.header("🏆 Sản phẩm có doanh số cao nhất trong từng Manufacturer")
        
        df = data_sheets['c14']
        
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
        
        fig, ax = plt.subplots(figsize=(18, 10))
        chart = sns.barplot(
            data=total_sales,
            x="YEAR",
            y="SALESAMOUNT",
            hue="MANUFACTURER",
            ax=ax
        )
        
        # Thêm tên sản phẩm lên trên mỗi cột
        # Lấy vị trí các cột từ matplotlib patches
        bars = ax.patches
        
        # Tạo dictionary để mapping vị trí cột với dữ liệu
        bar_data = []
        for i, (_, row) in enumerate(total_sales.iterrows()):
            bar_data.append({
                'x': bars[i].get_x() + bars[i].get_width() / 2,
                'y': bars[i].get_height(),
                'product': row['PRODUCTNAME']
            })
        
        # Hiển thị tên sản phẩm trên mỗi cột
        for bar_info in bar_data:
            # Rút ngắn tên sản phẩm nếu quá dài
            product_name = bar_info['product']
            if len(product_name) > 15:
                product_name = product_name[:12] + "..."
            
            ax.text(
                bar_info['x'], 
                bar_info['y'] + max(total_sales['SALESAMOUNT']) * 0.01,  # Offset 1% từ đỉnh cột
                product_name, 
                rotation=90, 
                ha="left", 
                va="bottom",
                fontsize=8, 
                color="black",
                fontweight='bold'
            )
        
        # Tăng margin top để có chỗ cho text
        ax.set_ylim(0, max(total_sales['SALESAMOUNT']) * 1.3)
        
        plt.title("Doanh số theo năm và nhà sản xuất (với tên sản phẩm bán chạy nhất)", fontsize=16)
        plt.xlabel("Năm", fontsize=12)
        plt.ylabel("Tổng doanh số", fontsize=12)
        plt.legend(title="Nhà sản xuất", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Show detailed data with product names
        with st.expander("📄 Xem dữ liệu chi tiết (bao gồm tên sản phẩm bán chạy)"):
            st.dataframe(total_sales[['YEAR', 'MANUFACTURER', 'PRODUCTNAME', 'SALESAMOUNT']])
        
        with st.expander("📄 Xem dữ liệu gốc"):
            st.dataframe(df)
    
    else:
        st.info("Chọn một phân tích từ sidebar để xem kết quả.")

if __name__ == "__main__":
    main()