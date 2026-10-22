import streamlit as st
from datetime import date
import database as db

# Initialize database on startup
db.init_db()

st.set_page_config(
    page_title="CampusConnect | Lost & Found",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 12px;
    }
    .status-lost {
        color: #d32f2f;
        font-weight: bold;
    }
    .status-found {
        color: #2e7d32;
        font-weight: bold;
    }
    .status-resolved {
        color: #757575;
        text-decoration: line-through;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎓 CampusConnect")
st.sidebar.markdown("**Smart Campus Lost & Found**")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📢 Report Lost Item", "🎁 Report Found Item", "🔍 Search & Browse", "ℹ️ Help & Guidelines"]
)

st.sidebar.divider()
st.sidebar.caption("CampusConnect v2.0 • Mini Project")
st.sidebar.caption("Persistent SQLite Database Enabled")

CATEGORIES = [
    "ID Card",
    "Books & Notebooks",
    "Electronics",
    "Bags & Wallets",
    "Keys",
    "Clothing & Accessories",
    "Water Bottle",
    "Other"
]

# ----------------- HOME -----------------
if menu == "🏠 Home":
    st.title("🎓 Campus Lost & Found Portal")
    st.write(
        "Welcome to **CampusConnect**, a centralized portal for students and staff to "
        "report, discover, and recover lost belongings across the campus."
    )

    stats = db.get_stats()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📦 Total Reports", stats["total"])
    with c2:
        st.metric("🔴 Active Lost Items", stats["lost"])
    with c3:
        st.metric("🟢 Active Found Items", stats["found"])
    with c4:
        st.metric("✅ Reclaimed / Resolved", stats["resolved"])

    st.divider()

    st.subheader("📌 How It Works")
    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown("### 1. Report It")
        st.write("Lost something or found someone's belonging? Submit details and location in seconds.")
    with step2:
        st.markdown("### 2. Match & Connect")
        st.write("Browse active listings or search by category and keywords to find matches.")
    with step3:
        st.markdown("### 3. Reclaim Safely")
        st.write("Contact the reporter or head to the designated security desk to collect the item.")

    st.divider()
    st.subheader("🕒 Recent Submissions")
    recent = db.get_items()[:4]
    if recent:
        r_cols = st.columns(min(len(recent), 4))
        for idx, item in enumerate(recent):
            with r_cols[idx]:
                with st.container(border=True):
                    badge = "🔴 Lost" if item["type"] == "Lost" else "🟢 Found"
                    st.caption(f"{badge} • {item['category']}")
                    st.markdown(f"**{item['name']}**")
                    st.write(f"📍 {item['location']}")
                    st.caption(f"Date: {item['date_event'] or item['created_at'][:10]}")
    else:
        st.info("No items reported yet. Be the first to add one!")


# ------------- REPORT LOST ITEM -------------
elif menu == "📢 Report Lost Item":
    st.title("📢 Report a Lost Item")
    st.write("Fill in the details below. Providing specific details helps others identify your item.")

    with st.form("lost_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Item Name *", placeholder="e.g. Black Lenovo Laptop Charger")
            category = st.selectbox("Category", CATEGORIES)
            lost_date = st.date_input("Date Lost", value=date.today())
        with col2:
            location = st.text_input("Estimated Location Lost *", placeholder="e.g. Library 3rd Floor study desk")
            contact_name = st.text_input("Your Name *", placeholder="e.g. Jordan Smith")
            contact_info = st.text_input("Your Contact (Email or Phone) *", placeholder="e.g. jsmith@campus.edu / 9876543210")

        description = st.text_area(
            "Detailed Description",
            placeholder="Mention color, brand, stickers, serial numbers, scratches, or any unique identifiers."
        )

        submitted = st.form_submit_button("Submit Lost Report", use_container_width=True)

    if submitted:
        if not name.strip() or not location.strip() or not contact_info.strip():
            st.error("Please fill in all required fields (Item Name, Location, and Contact).")
        else:
            item_id = db.add_item(
                item_type="Lost",
                name=name.strip(),
                category=category,
                location=location.strip(),
                date_event=str(lost_date),
                contact_name=contact_name.strip(),
                contact_info=contact_info.strip(),
                description=description.strip()
            )
            st.success(f"Report submitted successfully! (Reference ID: #{item_id})")
            st.info("Tip: You can search or view your listing anytime from the 'Search & Browse' tab.")


# ------------- REPORT FOUND ITEM -------------
elif menu == "🎁 Report Found Item":
    st.title("🎁 Report a Found Item")
    st.write("Thank you for helping someone recover their belongings! Please provide details below.")

    with st.form("found_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Item Name *", placeholder="e.g. Blue Titan Wristwatch")
            category = st.selectbox("Category", CATEGORIES)
            found_date = st.date_input("Date Found", value=date.today())
        with col2:
            location = st.text_input("Location Where Found *", placeholder="e.g. Science Block Ground Floor Cafeteria")
            contact_name = st.text_input("Finder's Name / Office", placeholder="e.g. Main Gate Security / Self")
            contact_info = st.text_input("Contact Info / Current Item Location *", placeholder="e.g. Kept at Security Room 101, ext 4402")

        description = st.text_area(
            "Detailed Description",
            placeholder="Describe the item condition, markings, or where the owner can verify ownership."
        )

        submitted = st.form_submit_button("Submit Found Report", use_container_width=True)

    if submitted:
        if not name.strip() or not location.strip() or not contact_info.strip():
            st.error("Please fill in all required fields (Item Name, Location, and Current Location / Contact).")
        else:
            item_id = db.add_item(
                item_type="Found",
                name=name.strip(),
                category=category,
                location=location.strip(),
                date_event=str(found_date),
                contact_name=contact_name.strip(),
                contact_info=contact_info.strip(),
                description=description.strip()
            )
            st.success(f"Found item report registered successfully! (Reference ID: #{item_id})")


# ------------- SEARCH & BROWSE -------------
elif menu == "🔍 Search & Browse":
    st.title("🔍 Search & Browse Items")

    # Search & Filter controls
    col_search, col_type, col_cat, col_status = st.columns([3, 1, 1.5, 1])
    with col_search:
        search_kw = st.text_input("Keyword Search", placeholder="Search by name, location, or description...")
    with col_type:
        filter_type = st.selectbox("Type", ["All", "Lost", "Found"])
    with col_cat:
        filter_cat = st.selectbox("Category", ["All"] + CATEGORIES)
    with col_status:
        filter_status = st.selectbox("Status", ["All", "Open", "Resolved"])

    items = db.get_items(
        search_query=search_kw,
        item_type=filter_type,
        category=filter_cat,
        status=filter_status
    )

    st.write(f"Showing **{len(items)}** results:")

    if items:
        for it in items:
            with st.container(border=True):
                c_head1, c_head2 = st.columns([4, 1])
                with c_head1:
                    type_badge = "🔴 LOST" if it["type"] == "Lost" else "🟢 FOUND"
                    status_badge = "✅ Resolved" if it["status"] == "Resolved" else "⏳ Active"
                    st.markdown(f"### {type_badge}: {it['name']} `#{it['id']}`")
                with c_head2:
                    st.caption(f"Status: **{status_badge}**")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"📂 **Category:** {it['category']}")
                    st.write(f"📍 **Location:** {it['location']}")
                    st.write(f"📅 **Date:** {it['date_event'] or it['created_at'][:10]}")
                with col_b:
                    st.write(f"👤 **Reported By:** {it['contact_name'] or 'Anonymous'}")
                    st.write(f"📞 **Contact / Location:** `{it['contact_info']}`")

                if it["description"]:
                    st.markdown(f"📝 **Description:** {it['description']}")

                # Actions
                act1, act2, _ = st.columns([1.5, 1, 5])
                with act1:
                    if it["status"] == "Open":
                        if st.button("Mark Resolved / Claimed", key=f"res_{it['id']}"):
                            db.update_item_status(it["id"], "Resolved")
                            st.rerun()
                    else:
                        if st.button("Re-open Item", key=f"reopen_{it['id']}"):
                            db.update_item_status(it["id"], "Open")
                            st.rerun()
                with act2:
                    if st.button("🗑️ Delete", key=f"del_{it['id']}"):
                        db.delete_item(it["id"])
                        st.rerun()
    else:
        st.info("No matching items found. Try adjusting your search query or filters.")


# ------------- HELP & GUIDELINES -------------
elif menu == "ℹ️ Help & Guidelines":
    st.title("ℹ️ Guidelines & Campus Support")

    st.markdown("""
    ### 🛡️ Campus Lost & Found Guidelines
    
    1. **Lost an item?**
       - Submit a report immediately with clear identifying features.
       - Check the **Search & Browse** section periodically as items are frequently turned in days later.
       - Visit the Campus Security Central Office if an item of high value (laptop, wallet, gold jewelry) was lost.

    2. **Found an item?**
       - Submit a report here so the owner can identify it.
       - Please hand over high-value items and official ID cards to the **Campus Security Desk** or **Central Library Reception**.
       - Never hand over an item to someone without verifying reasonable proof of ownership (e.g. unlocking a phone, matching ID, receipt, or unique details).

    3. **Campus Contacts**
       - **Campus Security Emergency Desk:** Ext 100 / +1 (555) 019-2834
       - **Central Library Information Desk:** Ext 220
       - **Student Affairs Helpdesk:** studentaffairs@campus.edu
    """)
