import streamlit as st
import sqlite3

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('curd.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS curd_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            quantity INTEGER,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- CRUD Functions ----------
def insert_entry(name, quantity, price):
    conn = sqlite3.connect('curd.db')
    c = conn.cursor()
    c.execute('INSERT INTO curd_inventory (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect('curd.db')
    c = conn.cursor()
    c.execute('SELECT * FROM curd_inventory')
    data = c.fetchall()
    conn.close()
    return data

def update_entry(entry_id, name, quantity, price):
    conn = sqlite3.connect('curd.db')
    c = conn.cursor()
    c.execute('''
        UPDATE curd_inventory SET name = ?, quantity = ?, price = ? WHERE id = ?
    ''', (name, quantity, price, entry_id))
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    conn = sqlite3.connect('curd.db')
    c = conn.cursor()
    c.execute('DELETE FROM curd_inventory WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()

# ---------- Streamlit UI ----------
st.title("🥣 Curd Inventory Manager (CRUD App)")
init_db()

menu = ["Create", "Read", "Update", "Delete"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- Create ----------
if choice == "Create":
    st.subheader("➕ Add New Curd Product")
    name = st.text_input("Curd Name")
    quantity = st.number_input("Quantity (kg)", min_value=0, step=1)
    price = st.number_input("Price (₹ per kg)", min_value=0.0, step=0.5)

    if st.button("Add"):
        if name:
            insert_entry(name, quantity, price)
            st.success(f"Added '{name}' successfully!")
        else:
            st.warning("Please enter a valid curd name.")

# ---------- Read ----------
elif choice == "Read":
    st.subheader("📋 All Curd Inventory")
    entries = get_all_entries()
    if entries:
        st.table(entries)
    else:
        st.info("No entries found.")

# ---------- Update ----------
elif choice == "Update":
    st.subheader("✏️ Update a Curd Entry")
    entries = get_all_entries()

    if entries:
        entry_dict = {f"{e[0]} - {e[1]}": e for e in entries}
        selected = st.selectbox("Select an entry to update", list(entry_dict.keys()))
        entry = entry_dict[selected]

        new_name = st.text_input("Curd Name", value=entry[1])
        new_quantity = st.number_input("Quantity", value=entry[2], min_value=0)
        new_price = st.number_input("Price", value=entry[3], min_value=0.0)

        if st.button("Update"):
            update_entry(entry[0], new_name, new_quantity, new_price)
            st.success("Updated successfully!")
    else:
        st.info("No curd entries found. Please add some products first.")

# ---------- Delete ----------
elif choice == "Delete":
    st.subheader("🗑️ Delete a Curd Entry")
    entries = get_all_entries()

    if entries:
        entry_dict = {f"{e[0]} - {e[1]}": e[0] for e in entries}
        selected = st.selectbox("Select an entry to delete", list(entry_dict.keys()))

        if st.button("Delete"):
            delete_entry(entry_dict[selected])
            st.success("Deleted successfully!")
    else:
        st.info("No curd entries to delete. Please add some products first.")
