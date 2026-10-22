# 🎓 CampusConnect: Smart Campus Lost & Found Management System

A web-based platform built with **Python**, **Streamlit**, and **SQLite** to report, track, search, and reclaim lost and found belongings across a university or college campus.

---

## 🛠️ Issues Identified in Original Repository & Fixes Applied

1. **Invalid / Colliding Filenames:**
   - The original repository had corrupted filenames containing accidental spaces and casing issues: `'App. Py'` and `'app. py'`.
   - On Windows filesystems, this created a case-insensitive name collision, preventing the file from being accessed or run via standard commands.
   - **Fix:** Consolidated and renamed to standard `app.py`.

2. **Duplicated Code:**
   - The original `app. py` contained the entire script duplicated twice back-to-back in a single file.
   - **Fix:** Cleaned up code and modularized into `app.py` and `database.py`.

3. **Lack of Persistence:**
   - The original repository only stored items in temporary `st.session_state`, so every refresh or app restart wiped all lost/found reports.
   - **Fix:** Integrated lightweight SQLite database (`campus_lost_found.db`) with automatic table creation and pre-seeded sample data.

4. **Missing Dependency Specifications:**
   - The repository did not include `requirements.txt`, making it impossible for standard tools/users to know what libraries were required.
   - **Fix:** Added `requirements.txt` with `streamlit` and `Pillow`.

5. **No Easy Run Format / Scripts:**
   - No runner scripts existed.
   - **Fix:** Added `run.bat` (1-click double-click launcher for Windows) and `run.ps1` (PowerShell launcher).

---

## ✨ Features

- **🏠 Interactive Dashboard:** Real-time statistics on total reports, active lost items, active found items, and resolved cases.
- **📢 Report Lost Items:** Log lost item name, category, location, date lost, contact information, and detailed descriptions.
- **🎁 Report Found Items:** Log found items, where they were discovered, and where they have been deposited (e.g. Security Desk, Library Reception).
- **🔍 Filter & Search Engine:** Live keyword search across names, descriptions, and locations, with filters by Type (Lost/Found), Category, and Status.
- **✅ Claim & Resolve Workflow:** Ability to mark items as resolved/claimed once returned to their owner.
- **🛡️ Help & Guidelines:** Campus directory, security contacts, and safety advice for recovering lost items.
- **💾 Persistent SQLite Database:** Retains all data automatically across app restarts.

---

## 🚀 How to Run the Project

### Option 1: 1-Click Launch (Windows - Recommended)
Simply double-click the **`run.bat`** file inside the project directory:
```
run.bat
```
This script will automatically:
1. Detect your Python environment
2. Create a local `.venv` virtual environment (if not already present)
3. Install dependencies from `requirements.txt`
4. Launch the application in your default web browser

---

### Option 2: Run via Terminal / PowerShell

1. Open PowerShell or Command Prompt in the project folder:
   ```powershell
   cd C:\Users\kamatchi\.gemini\antigravity\scratch\camp-lost-and-found
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Launch the Streamlit application:
   ```powershell
   streamlit run app.py
   ```
   *(or `python -m streamlit run app.py`)*

5. Your web browser will automatically open at:
   ```
   http://localhost:8501
   ```

---

## 📂 Project Structure

```text
camp-lost-and-found/
│
├── app.py                  # Main Streamlit web application
├── database.py             # SQLite database layer & helper functions
├── requirements.txt        # Python package dependencies
├── run.bat                 # 1-click Windows runner script
├── run.ps1                 # PowerShell runner script
├── .gitignore              # Git ignore rules for Python, DB, and venv
├── README.md               # Project documentation and guide
└── campus_lost_found.db    # Auto-created SQLite database (created on first run)
```
