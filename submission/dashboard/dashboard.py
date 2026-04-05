import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# load data
main_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("data/hour.csv")

# konversi kolom tanggal
main_df["dteday"] = pd.to_datetime(main_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# mapping label
hour_df["season_label"] = hour_df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
hour_df["day_type"] = hour_df["workingday"].map({1: "Hari Kerja", 0: "Hari Libur/Weekend"})


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.header("Filter Data")

min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

season_options = main_df["season_label"].unique().tolist()
selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    options=season_options,
    default=season_options
)

# filter dataframe
filtered_df = main_df[
    (main_df["dteday"] >= pd.Timestamp(start_date)) &
    (main_df["dteday"] <= pd.Timestamp(end_date)) &
    (main_df["season_label"].isin(selected_season))
]

filtered_hour_df = hour_df[
    (hour_df["dteday"] >= pd.Timestamp(start_date)) &
    (hour_df["dteday"] <= pd.Timestamp(end_date)) &
    (hour_df["season_label"].isin(selected_season))
]


# ── HEADER ───────────────────────────────────────────────────────────────────
st.title("🚲 Dashboard Analisis Bike Sharing")
st.markdown("Data peminjaman sepeda di Washington D.C. tahun 2011–2012")
st.markdown("---")


# ── METRIK UTAMA ─────────────────────────────────────────────────────────────
st.subheader("Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Peminjaman",   f"{filtered_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian",   f"{filtered_df['cnt'].mean():.0f}")
col3.metric("Peminjam Kasual",    f"{filtered_df['casual'].sum():,}")
col4.metric("Peminjam Terdaftar", f"{filtered_df['registered'].sum():,}")

st.markdown("---")


# ── PERTANYAAN 1: PENGARUH MUSIM ─────────────────────────────────────────────
st.subheader("Pertanyaan 1: Bagaimana pengaruh musim terhadap jumlah peminjaman sepeda harian?")

season_order  = ["Spring", "Summer", "Fall", "Winter"]
season_colors = ["#4FC3F7", "#FFA726", "#66BB6A", "#AB47BC"]

season_avg = filtered_df.groupby("season_label")["cnt"].mean().reindex(season_order).dropna()

col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(season_avg.index, season_avg.values, color=season_colors[:len(season_avg)])
    for bar, val in zip(bars, season_avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                f"{val:.0f}", ha="center", fontsize=10, fontweight="bold")
    ax.set_title("Rata-rata Peminjaman per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
    plt.close()

with col_b:
    fig, ax = plt.subplots(figsize=(7, 5))
    data_plot  = [filtered_df[filtered_df["season_label"] == s]["cnt"].values
                  for s in season_order if s in filtered_df["season_label"].values]
    label_plot = [s for s in season_order if s in filtered_df["season_label"].values]
    bp = ax.boxplot(data_plot, labels=label_plot, patch_artist=True,
                    medianprops=dict(color="red", linewidth=2))
    for patch, color in zip(bp["boxes"], season_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax.set_title("Distribusi Peminjaman per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Peminjaman")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
    plt.close()

with st.expander("Insight Pertanyaan 1", expanded=True):
    st.markdown("""
    - **Fall (Gugur) mendominasi** dengan rata-rata tertinggi **5.644 peminjaman/hari**, hampir **2x lipat dibanding Spring** (2.604). Ini menunjukkan musim gugur adalah periode emas bagi operator bike-sharing.
    - **Spring (Semi) menjadi musim terendah** sekaligus paling konsisten, std dev-nya paling kecil (1.400) dibanding musim lain, artinya permintaan memang rendah tapi stabil, bukan karena fluktuasi.
    - **Winter memiliki variasi tertinggi** (std dev = 1.700) dengan gap ekstrem antara min (22) dan max (8.555). Ini mengindikasikan cuaca buruk di musim dingin sangat menentukan, hari-hari dengan cuaca baik tetap ramai, tapi saat salju/hujan deras permintaan bisa hampir nol.
    - **Median Fall (5.354) sedikit di bawah mean-nya (5.644)**, artinya distribusi bersifat *right-skewed*
    - **Rekomendasi bisnis:** Operator perlu menambah armada secara signifikan di musim Fall–Summer, serta menyiapkan strategi promosi khusus di Spring untuk mendongkrak permintaan yang stagnan.
    """)

st.markdown("---")


# ── PERTANYAAN 2: POLA PER JAM ───────────────────────────────────────────────
st.subheader("Pertanyaan 2: Bagaimana pola peminjaman per jam pada hari kerja dibandingkan hari libur?")

hourly_avg = filtered_hour_df.groupby(["hr", "day_type"])["cnt"].mean().reset_index()

workday_df = hourly_avg[hourly_avg["day_type"] == "Hari Kerja"]
holiday_df = hourly_avg[hourly_avg["day_type"] == "Hari Libur/Weekend"]

col_c, col_d = st.columns(2)

with col_c:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(workday_df["hr"], workday_df["cnt"], color="#1565C0",
            linewidth=2, marker="o", markersize=4, label="Hari Kerja")
    ax.plot(holiday_df["hr"], holiday_df["cnt"], color="#E53935",
            linewidth=2, marker="s", markersize=4, label="Hari Libur/Weekend")
    ax.fill_between(workday_df["hr"], workday_df["cnt"], alpha=0.1, color="#1565C0")
    ax.fill_between(holiday_df["hr"], holiday_df["cnt"], alpha=0.1, color="#E53935")
    ax.set_title("Pola Peminjaman per Jam")
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rata-rata Peminjaman")
    ax.set_xticks(range(0, 24, 2))
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)
    plt.close()

with col_d:
    heatmap_pivot = filtered_hour_df.groupby(["hr", "season_label"])["cnt"].mean().unstack()
    heatmap_pivot = heatmap_pivot.reindex(columns=[s for s in season_order if s in heatmap_pivot.columns])
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(heatmap_pivot.T, ax=ax, cmap="YlOrRd",
                linewidths=0.3, linecolor="white",
                cbar_kws={"label": "Rata-rata Peminjaman"})
    ax.set_title("Heatmap Jam vs Musim")
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Musim")
    st.pyplot(fig)
    plt.close()

with st.expander("Insight Pertanyaan 2", expanded=True):
    st.markdown("""
    - **Hari Kerja menunjukkan pola bimodal yang jelas**, puncak pertama di **jam 17:00 (525 peminjaman)** dan puncak kedua di **jam 08:00 (477 peminjaman)**. Ini mengindikasikan mayoritas pengguna memanfaatkan sepeda sebagai alat transportasi komuter (berangkat dan pulang kerja).
    - **Hari Libur/Weekend menunjukkan pola unimodal** dengan puncak merata antara **jam 12:00–15:00** (352–373 peminjaman). Tidak ada lonjakan di pagi hari, yang membuktikan pengguna weekend bersifat rekreasional dan tidak terikat jadwal tetap.
    - **Puncak hari kerja (525) lebih tinggi dibanding puncak hari libur (373)**, menunjukkan pengguna terdaftar (komuter tetap) mendominasi sistem secara keseluruhan.
    - **Rekomendasi bisnis:** Strategi redistribusi sepeda harus dibedakan. Pada hari kerja fokus pada stasiun dekat perkantoran dan transportasi umum di jam 07:00–09:00 dan 16:00–18:00; pada hari libur fokus pada area rekreasi dan pusat perbelanjaan di jam 11:00–16:00.
    """)

# ── ANALISIS LANJUTAN: CLUSTERING DENGAN BINNING ─────────────────────────────
st.subheader("Analisis Lanjutan: Clustering Permintaan dengan Binning")
 
st.markdown("Data peminjaman harian dikelompokkan ke dalam 4 kategori menggunakan teknik **binning**.")
 
# buat kolom cluster berdasarkan jumlah peminjaman
bins   = [0, 2000, 4000, 6000, filtered_df["cnt"].max() + 1]
labels = ["Low (<2000)", "Medium (2000-4000)", "High (4000-6000)", "Very High (>6000)"]
 
filtered_df = filtered_df.copy()
filtered_df["demand_cluster"] = pd.cut(filtered_df["cnt"], bins=bins, labels=labels, right=False)
 
cluster_colors = ["#90CAF9", "#A5D6A7", "#FFCC80", "#EF9A9A"]
cluster_counts = filtered_df["demand_cluster"].value_counts().sort_index()
 
col_e, col_f = st.columns(2)
 
with col_e:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        cluster_counts.values,
        labels=cluster_counts.index,
        colors=cluster_colors[:len(cluster_counts)],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops=dict(linewidth=1.5, edgecolor="white")
    )
    ax.set_title("Proporsi Cluster Permintaan Harian")
    st.pyplot(fig)
    plt.close()
 
with col_f:
    st.markdown("**Jumlah Hari per Cluster**")
    cluster_summary = filtered_df.groupby("demand_cluster", observed=False)["cnt"].agg(
        Jumlah_Hari="count",
        Rata_rata="mean",
        Minimum="min",
        Maksimum="max"
    ).round(0)
    st.dataframe(cluster_summary, use_container_width=True)
 
    st.markdown("**Distribusi Cluster per Musim**")
    cluster_season = pd.crosstab(filtered_df["season_label"], filtered_df["demand_cluster"])
    cluster_season = cluster_season.reindex([s for s in season_order if s in cluster_season.index])
    st.dataframe(cluster_season, use_container_width=True)
 
with st.expander("Insight Analisis Clustering", expanded=True):
    st.markdown("""
    - Mayoritas hari (~33%) masuk kategori **Medium (2.000–4.000)**, menunjukkan permintaan sedang adalah kondisi paling umum sepanjang tahun.
    - Cluster **Very High (>6.000)** hampir sepenuhnya terkonsentrasi pada musim **Fall dan Summer**, mengonfirmasi temuan pada pertanyaan bisnis pertama.
    - Cluster **Low (<2.000)** didominasi oleh musim **Spring** dan sebagian **Winter**, menandakan permintaan sangat rendah di kedua musim tersebut.
    - **Rekomendasi bisnis:** Operator dapat menggunakan segmentasi ini untuk merancang strategi harga dinamis dengan menaikkan tarif di cluster High/Very High (musim ramai) dan memberikan diskon di cluster Low (musim sepi) untuk menjaga utilitas armada tetap optimal.
    """)