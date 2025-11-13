import streamlit as st
import pandas as pd

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(page_title="123 Pollachi AC - SIR 2002 Search", layout="wide")

# -----------------------------------
# PAGE TITLE
# -----------------------------------
st.title("🗳️ 123 POLLACHI ASSEMBLY CONSTITUENCY")
st.header("🔍 SEARCH ELECTOR DETAILS - 2002")

# -----------------------------------
# LOAD EXCEL DATA
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("old_data.xlsx")

    # No uppercase — keep Tamil exactly as stored
    df["FM_NAME_V2"] = df["FM_NAME_V2"].astype(str).str.strip()
    df["RLN_FM_NM_V2"] = df["RLN_FM_NM_V2"].astype(str).str.strip()

    return df

df = load_data()

# -----------------------------------
# SEARCH INPUTS (TAMIL)
# -----------------------------------
st.subheader("விவரங்களை உள்ளிடவும் (Enter Details)")

name_input = st.text_input("பெயர் (NAME) – Tamil Only")
rname_input = st.text_input("உறவு பெயர் (RELATION NAME) – Tamil Only")

# -----------------------------------
# SEARCH BUTTON
# -----------------------------------
if st.button("தேடு (SEARCH)"):

    name_part = name_input.strip()
    rname_part = rname_input.strip()

    if not name_part and not rname_part:
        st.warning("⚠️ Please enter NAME or RELATION NAME in Tamil.")
        st.stop()

    # Start with full data
    results = df.copy()

    # Partial Tamil matching
    if name_part:
        results = results[results["FM_NAME_V2"].str.contains(name_part, na=False)]

    if rname_part:
        results = results[results["RLN_FM_NM_V2"].str.contains(rname_part, na=False)]

    # Display final result
    if not results.empty:
        st.success(f"✔ {len(results)} matching record(s) found.")
        st.dataframe(results, use_container_width=True)
    else:
        st.error("❌ No records found for the given Tamil name(s).")
