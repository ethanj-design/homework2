import streamlit as st
import json
from pathlib import Path
import time
import uuid

st.set_page_config(
        page_title="Coffee Kiosk App", 
        layout="centered"
        )

json_file = Path("inventory.json")
json_file_orders = Path("orders.json")


if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = [] 

if json_file_orders.exists():
    with json_file_orders.open("r", encoding= "utf-8") as f:
        orders = json.load(f)
else: 
    orders = []




st.title("Coffee Kiosk App")

tab1, tab2, tab3, tab4 = st.tabs(["Order Creator", "Inventory Viewer", "Restock", "Manage Orders"])

with tab1:

    inv_items = []
    for items in inventory:
        inv_items.append(items["name"])


    #UI Items
    selected_item = st.selectbox("Select an item", inv_items, key="selected_item")
    order_quantity = st.number_input("Item Quantity", key="order_quantity",min_value=1,step=1)
    customer_name = st.text_input("Name",placeholder="Ex: John Doe", key = "customer_name")
    btn_order = st.button("Submit Order",width="stretch",disabled=False,key="btn_order")


    if btn_order:
        
        #check for required items
        if not selected_item or not order_quantity or not customer_name:
            st.warning("Insert all required information!")

        else:
            with st.spinner("Order is being recorded..."):
                time.sleep(5)

                #check if item is in stock
                for item in inventory:
                    if item["name"] == selected_item:
                        stock = item["stock"]
                if stock < order_quantity:
                    st.warning("item is not in stock!")

                else: 
                    
                    #add order
                    orders.append(
                        {
                            "id" : str(uuid.uuid4()),
                            "item" : selected_item,
                            "quantity" : order_quantity,
                            "name" : customer_name
                        }
                    )
                    with json_file_orders.open("w",encoding="utf-8") as f:
                        json.dump(orders,f)
                    
                    #reduce stock
                    for item in inventory:
                        if item["name"] == selected_item:
                            item["stock"] -= order_quantity
                    
                    with json_file.open("w",encoding="utf-8") as f:
                        json.dump(inventory, f)
                    
                    #output
                    st.success("Order is created!")
                


                
        
            
            


