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

# Initialize Session State
if "user" not in st.session_state:
    st.session_state.user = None

if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False

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
    .user-badge {
        background: #e3f2fd;
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid #90caf9;
        margin-bottom: 15px;
        font-size: 0.9em;
    }
    .login-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

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

# =====================================================================
# 🔐 GATEWAY: IF NOT LOGGED IN, OPEN DIRECTLY TO THE LOGIN PAGE FIRST!
# =====================================================================
if not st.session_state.user and not st.session_state.guest_mode:
    st.sidebar.title("🎓 CampusConnect")
    st.sidebar.info("👋 Welcome! Please log in to access the campus portal.")
    st.sidebar.divider()
    st.sidebar.markdown("""
    **Demo Credentials:**
    * **Student:** `student` / `student123`
    * **Admin:** `admin` / `admin123`
    """)

    # Main Area: Clean Login Portal
    col_left, col_mid, col_right = st.columns([1, 2.5, 1])

    with col_mid:
        st.title("🎓 CampusConnect")
        st.subheader("Smart Campus Lost & Found System")
        st.write("Sign in with your campus account to report, search, and manage lost or found belongings.")

        tab_login, tab_register = st.tabs(["🔐 Sign In", "📝 Create New Account"])

        # TAB 1: LOGIN
        with tab_login:
            with st.form("main_login_form"):
                login_user = st.text_input("Username or Campus Email", placeholder="e.g. student or student@campus.edu")
                login_pass = st.text_input("Password", type="password", placeholder="Enter your password")
                login_btn = st.form_submit_button("Sign In to Portal", use_container_width=True, type="primary")

            if login_btn:
                if not login_user or not login_pass:
                    st.error("Please enter both username/email and password.")
                else:
                    user_data = db.authenticate_user(login_user, login_pass)
                    if user_data:
                        st.session_state.user = user_data
                        st.session_state.guest_mode = False
                        st.success(f"Welcome back, {user_data['username']}! Logging in...")
                        st.rerun()
                    else:
                        st.error("Invalid username/email or password.")

            st.divider()
            st.markdown("#### ⚡ 1-Click Quick Demo Sign In")
            c_demo1, c_demo2 = st.columns(2)
            with c_demo1:
                if st.button("🎓 Sign In as Student", use_container_width=True):
                    user_data = db.authenticate_user("student", "student123")
                    st.session_state.user = user_data
                    st.rerun()
            with c_demo2:
                if st.button("👑 Sign In as Admin", use_container_width=True):
                    user_data = db.authenticate_user("admin", "admin123")
                    st.session_state.user = user_data
                    st.rerun()

            st.divider()
            if st.button("👀 Continue as Guest (Search Only)", use_container_width=True):
                st.session_state.guest_mode = True
                st.rerun()

        # TAB 2: REGISTER
        with tab_register:
            st.subheader("Register New Student/Staff Account")
            with st.form("main_register_form", clear_on_submit=True):
                new_user = st.text_input("Desired Username *", placeholder="e.g. priya_sharma")
                new_email = st.text_input("Campus Email *", placeholder="e.g. priya@campus.edu")
                new_pass = st.text_input("Password (min 6 chars) *", type="password")
                role_choice = st.selectbox("Account Role", ["student", "admin"])
                register_btn = st.form_submit_button("Register Account", use_container_width=True, type="primary")

            if register_btn:
                success, msg = db.register_user(new_user, new_email, new_pass, role=role_choice)
                if success:
                    st.success(msg)
                    st.info("You can now switch to the 'Sign In' tab above to log in.")
                else:
                    st.error(msg)

    # Stop rendering the rest of the application until the user logs in
    st.stop()


# =====================================================================
# 🌟 MAIN APPLICATION (UNLOCKED AFTER LOGIN / GUEST ACCESS)
# =====================================================================

# ----------------- SIDEBAR -----------------
st.sidebar.title("🎓 CampusConnect")
st.sidebar.markdown("**Smart Campus Lost & Found**")

if st.session_state.user:
    role_icon = "👑" if st.session_state.user["role"] == "admin" else "🎓"
    st.sidebar.markdown(f"""
    <div class="user-badge">
        <b>{role_icon} {st.session_state.user['username'].capitalize()}</b> ({st.session_state.user['role']})<br>
        <span style="font-size: 0.85em; color: #555;">{st.session_state.user['email']}</span>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 Log Out", use_container_width=True):
        st.session_state.user = None
        st.session_state.guest_mode = False
        st.rerun()
else:
    st.sidebar.info("👤 Browsing as **Guest** (Read Only).")
    if st.sidebar.button("🔐 Go to Login Screen", use_container_width=True):
        st.session_state.guest_mode = False
        st.session_state.user = None
        st.rerun()

st.sidebar.divider()

nav_options = [
    "🏠 Dashboard",
    "📢 Report Lost Item",
    "🎁 Report Found Item",
    "🔍 Search & Browse",
    "🗑️ Manage & Delete Reports",
    "👤 My Profile",
    "ℹ️ Help & Guidelines"
]

menu = st.sidebar.radio("Navigation", nav_options)

st.sidebar.divider()
st.sidebar.caption("CampusConnect v2.2 • Student Mini Project")
st.sidebar.caption("SQLite Persistent Storage • User Auth Active")


# ----------------- 🏠 DASHBOARD -----------------
if menu == "🏠 Dashboard":
    st.title("🎓 Campus Lost & Found Dashboard")
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
        st.write("Lost an item or found someone's belonging? Submit details and location in seconds.")
    with step2:
        st.markdown("### 2. Search & Connect")
        st.write("Browse listings with real-time keyword and category filters to locate matches.")
    with step3:
        st.markdown("### 3. Reclaim Safely")
        st.write("Contact the reporter or security desk. Once returned, mark as resolved or delete.")

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


# ------------- 📢 REPORT LOST ITEM -------------
elif menu == "📢 Report Lost Item":
    st.title("📢 Report a Lost Item")
    st.write("Fill in the details below. Providing specific details helps others identify your item.")

    current_username = st.session_state.user["username"] if st.session_state.user else "Anonymous"
    default_name = st.session_state.user["username"] if st.session_state.user else ""
    default_email = st.session_state.user["email"] if st.session_state.user else ""

    with st.form("lost_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Item Name *", placeholder="e.g. Black Lenovo Laptop Charger")
            category = st.selectbox("Category", CATEGORIES)
            lost_date = st.date_input("Date Lost", value=date.today())
        with col2:
            location = st.text_input("Estimated Location Lost *", placeholder="e.g. Library 3rd Floor study desk")
            contact_name = st.text_input("Your Name *", value=default_name, placeholder="e.g. Jordan Smith")
            contact_info = st.text_input("Your Contact (Email or Phone) *", value=default_email, placeholder="e.g. jsmith@campus.edu / 9876543210")

        description = st.text_area(
            "Detailed Description",
            placeholder="Mention color, brand, stickers, serial numbers, scratches, or any unique identifiers."
        )

        submitted = st.form_submit_button("Submit Lost Report", use_container_width=True, type="primary")

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
                description=description.strip(),
                username=current_username
            )
            st.success(f"Lost item report registered successfully! (Reference ID: #{item_id})")
            st.info("You can track and manage this report under '🗑️ Manage & Delete Reports'.")


# ------------- 🎁 REPORT FOUND ITEM -------------
elif menu == "🎁 Report Found Item":
    st.title("🎁 Report a Found Item")
    st.write("Thank you for helping someone recover their belongings! Please provide details below.")

    current_username = st.session_state.user["username"] if st.session_state.user else "Anonymous"
    default_name = st.session_state.user["username"] if st.session_state.user else ""
    default_email = st.session_state.user["email"] if st.session_state.user else ""

    with st.form("found_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Item Name *", placeholder="e.g. Blue Titan Wristwatch")
            category = st.selectbox("Category", CATEGORIES)
            found_date = st.date_input("Date Found", value=date.today())
        with col2:
            location = st.text_input("Location Where Found *", placeholder="e.g. Science Block Ground Floor Cafeteria")
            contact_name = st.text_input("Finder's Name / Office", value=default_name, placeholder="e.g. Main Gate Security / Self")
            contact_info = st.text_input("Contact Info / Current Item Location *", value=default_email, placeholder="e.g. Kept at Security Room 101, ext 4402")

        description = st.text_area(
            "Detailed Description",
            placeholder="Describe the item condition, markings, or where the owner can verify ownership."
        )

        submitted = st.form_submit_button("Submit Found Report", use_container_width=True, type="primary")

    if submitted:
        if not name.strip() or not location.strip() or not contact_info.strip():
            st.error("Please fill in all required fields (Item Name, Location, and Contact/Deposit spot).")
        else:
            item_id = db.add_item(
                item_type="Found",
                name=name.strip(),
                category=category,
                location=location.strip(),
                date_event=str(found_date),
                contact_name=contact_name.strip(),
                contact_info=contact_info.strip(),
                description=description.strip(),
                username=current_username
            )
            st.success(f"Found item report registered successfully! (Reference ID: #{item_id})")


# ------------- 🔍 SEARCH & BROWSE -------------
elif menu == "🔍 Search & Browse":
    st.title("🔍 Search & Browse Items")

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
                c_head1, c_head2 = st.columns([4, 1.2])
                with c_head1:
                    type_badge = "🔴 LOST" if it["type"] == "Lost" else "🟢 FOUND"
                    status_badge = "✅ Resolved" if it["status"] == "Resolved" else "⏳ Active"
                    st.markdown(f"### {type_badge}: {it['name']} `#{it['id']}`")
                with c_head2:
                    st.caption(f"Status: **{status_badge}**")
                    if it.get("username") and it["username"] != "Anonymous":
                        st.caption(f"👤 Posted by: `@{it['username']}`")

                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"📂 **Category:** {it['category']}")
                    st.write(f"📍 **Location:** {it['location']}")
                    st.write(f"📅 **Date:** {it['date_event'] or it['created_at'][:10]}")
                with col_b:
                    st.write(f"👤 **Reported By:** {it['contact_name'] or 'Anonymous'}")
                    st.write(f"📞 **Contact / Deposit Location:** `{it['contact_info']}`")

                if it["description"]:
                    st.markdown(f"📝 **Description:** {it['description']}")
    else:
        st.info("No matching items found. Try adjusting your search query or filters.")


# ------------- 🗑️ MANAGE & DELETE REPORTS -------------
elif menu == "🗑️ Manage & Delete Reports":
    st.title("🗑️ Manage & Delete Reports")
    st.write("Manage active listings, toggle resolution status, or permanently delete reports.")

    is_admin = st.session_state.user and st.session_state.user["role"] == "admin"
    current_username = st.session_state.user["username"] if st.session_state.user else None

    if not st.session_state.user:
        st.warning("⚠️ You are browsing as a Guest. Log in to manage or delete your reports, or log in as an Admin.")
        items_to_manage = db.get_items()
    elif is_admin:
        st.success(f"👑 **Admin Mode Activated** (Logged in as `@{current_username}`). You can manage and delete **any** report.")
        items_to_manage = db.get_items()
    else:
        st.info(f"🎓 Showing reports submitted by **`@{current_username}`**.")
        items_to_manage = db.get_items(username=current_username)
        if not items_to_manage:
            st.info("You haven't submitted any reports yet. Reports you create will appear here.")

    if items_to_manage:
        st.write(f"Total manageable reports: **{len(items_to_manage)}**")

        for it in items_to_manage:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    type_str = "🔴 Lost Item" if it["type"] == "Lost" else "🟢 Found Item"
                    st.markdown(f"#### {type_str}: {it['name']} `(ID: #{it['id']})`")
                    st.write(f"📍 **Location:** {it['location']} | 📂 **Category:** {it['category']}")
                    st.caption(f"Reported on: {it['date_event'] or it['created_at']} | Contact: {it['contact_info']}")
                    if it["description"]:
                        st.caption(f"Details: {it['description']}")
                with c2:
                    current_status = it["status"]
                    st.write(f"Current Status: **{current_status}**")

                    if current_status == "Open":
                        if st.button("Mark Resolved ✅", key=f"res_{it['id']}"):
                            db.update_item_status(it["id"], "Resolved")
                            st.success(f"Item #{it['id']} marked as Resolved!")
                            st.rerun()
                    else:
                        if st.button("Re-open ⏳", key=f"reopen_{it['id']}"):
                            db.update_item_status(it["id"], "Open")
                            st.success(f"Item #{it['id']} re-opened!")
                            st.rerun()

                    can_delete = is_admin or (current_username and it.get("username") == current_username)
                    if can_delete:
                        st.divider()
                        delete_confirm = st.checkbox("Confirm Delete", key=f"chk_del_{it['id']}")
                        if delete_confirm:
                            if st.button("🚨 Delete Permanently", key=f"btn_del_{it['id']}", type="primary"):
                                db.delete_item(it["id"])
                                st.success(f"Report #{it['id']} deleted successfully!")
                                st.rerun()
                    else:
                        st.caption("🔒 *Log in as owner/admin to delete*")
    else:
        st.write("No reports available to manage.")


# ------------- 👤 MY PROFILE -------------
elif menu == "👤 My Profile":
    st.title("👤 My Account Profile")
    if st.session_state.user:
        u = st.session_state.user
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            ### Welcome, **{u['username'].capitalize()}**!
            * **Username:** `{u['username']}`
            * **Email:** `{u['email']}`
            * **Role:** `{u['role'].capitalize()}`
            """)

            user_stats = db.get_stats(username=u['username'])
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("My Total Reports", user_stats["total"])
            with m2:
                st.metric("My Active Lost", user_stats["lost"])
            with m3:
                st.metric("My Active Found", user_stats["found"])

        with col2:
            st.markdown("### Session Actions")
            if st.button("🚪 Logout of Account", type="primary", use_container_width=True):
                st.session_state.user = None
                st.session_state.guest_mode = False
                st.rerun()
    else:
        st.info("You are currently browsing as a Guest.")
        if st.button("🔐 Go to Login Page", type="primary"):
            st.session_state.guest_mode = False
            st.session_state.user = None
            st.rerun()


# ------------- ℹ️ HELP & GUIDELINES -------------
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

    3. **Deleting or Resolving Reports:**
       - Head to the **'🗑️ Manage & Delete Reports'** tab.
       - Toggle items to **Resolved** when returned, or use **Confirm Delete** to permanently remove outdated records.

    4. **Campus Contacts**
       - **Campus Security Emergency Desk:** Ext 100 / +1 (555) 019-2834
       - **Central Library Information Desk:** Ext 220
       - **Student Affairs Helpdesk:** studentaffairs@campus.edu
    """)
