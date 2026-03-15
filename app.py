import streamlit as st
import json
from pathlib import Path
import time
import uuid

# Setup the page
st.set_page_config(
        page_title="Coffee Kiosk App", 
        layout="centered"
        )

# Setup json files
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



# App Starts Here
st.title("Coffee Kiosk App")

create, read, update, delete = st.tabs(["Order Creator", "Inventory Viewer", "Restock", "Manage Orders"])

with create:

    inv_items = []
    for items in inventory:
        inv_items.append(items["name"])

    #UI Items
    selected_item = st.selectbox("Select an item", inv_items, key="selected_item")

    order_quantity = st.number_input("Item Quantity", key="order_quantity",
                                        min_value=1,step=1) #Ensure we cant enter negative items, or decimal amounts of items. I did lookup how to do this.

    customer_name = st.text_input("Name",placeholder="Ex: John Doe", key="customer_name")
    btn_order = st.button("Submit Order",width="stretch",disabled=False,key="btn_order")

    #READ
    if btn_order:
        
        #check for required items
        if not customer_name:
            st.warning("Please insert your name!")

        else:
            with st.spinner("Order is being recorded..."):
                time.sleep(5)

                #check if item is in stock
                for item in inventory:
                    if item["name"] == selected_item:

                        stock = item["stock"]

                        #check the stock level
                        if stock < order_quantity: 
                            st.warning("Not enough stock to fulfill your order.")
                        else: 

                            #reduce stock
                            item["stock"] -= order_quantity


                            #now add order
                            orders.append(
                                {
                                    "id" : str(uuid.uuid4()),
                                    "item" : selected_item,
                                    "quantity" : order_quantity,
                                    "name" : customer_name
                                }
                            )


                            #rewrite the infomation into the json files to ensure stateful app
                            with json_file_orders.open("w",encoding="utf-8") as f:
                                json.dump(orders,f)
                            
                            with json_file.open("w",encoding="utf-8") as f:
                                json.dump(inventory, f)
                            

                            #successful output
                            st.success("Order is created!")


