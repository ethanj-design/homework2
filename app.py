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
                        item_price = item["price"]

                        #check the stock level
                        if stock < order_quantity: 
                            st.warning("Not enough stock to fulfill your order.")
                        else: 

                            #reduce stock
                            item["stock"] -= order_quantity
                            order_price = order_quantity * item_price


                            #now add order
                            orders.append(
                                {
                                    "id" : str(uuid.uuid4()),
                                    "item" : selected_item,
                                    "quantity" : order_quantity,
                                    "price" : order_price,
                                    "name" : customer_name,
                                    "status" : "Placed"
                                }
                            )


                            #rewrite the infomation into the json files to ensure stateful app
                            with json_file_orders.open("w",encoding="utf-8") as f:
                                json.dump(orders,f, indent=4)
                            
                            with json_file.open("w",encoding="utf-8") as f:
                                json.dump(inventory, f,indent=4)
                            

                            #successful output
                            st.success("Order is created!")

with read:

    inv_items = []
    for item in inventory:
        inv_items.append(item["name"])

    selected_search_item = st.selectbox("Select an item", inv_items, key="search_item")

    query_data = []
    order_metric = 0

    for item in inventory:
        if item["name"] == selected_search_item:
            query_data.append(item)
            stock_metric = item["stock"]
            price_metric = item["price"]
    
    for o in orders: 
        if o["item"] == selected_search_item:
            order_metric += 1


    col1, col2, col3 = st.columns([1,1,1])

    
    st.markdown(f"### Table for {selected_search_item}")


    if query_data:
        
        with col1: 
            stock_info = st.metric("Total items in stock: ", stock_metric)
        with col2: 
            price_info = st.metric("Item Price", price_metric)
        with col3:
            order_info = st.metric("Orders with Item", order_metric)
            

        st.dataframe(query_data)

with update:

    inv_items = []
    for item in inventory:
        inv_items.append(item["name"])

    selected_restock_item = st.selectbox("Select an item", inv_items, key="restock_item")
    added_amount = st.number_input("Restock Quantity",min_value=1,step=1,key="added_amount")
    add_btn = st.button("Add items to stock",width="stretch", disabled=False,key="add_btn")

    if add_btn:

        with st.spinner("Updating inventory level..."):

            time.sleep(5)

            for item in inventory:
                if item["name"] == selected_restock_item:
                    item["stock"] += added_amount
            
            with json_file.open("w",encoding="utf-8") as f:
                json.dump(inventory, f,indent=4)
            
            st.success("Items added to stock!")
            time.sleep(3)
            st.rerun()


with delete:


    # ui elements
    selected_order = st.text_input("Order ID",placeholder="Ex: 1",
                                    help="Copy the ID from the dataframe and paste it into the box.", key="selected_order")
    delete_btn = st.button("Cancel this order", width="stretch", disabled=False, key="delete_btn")
    st.dataframe(orders)



    if delete_btn:

        found_order = False
        alr_cancelled = False

        if not selected_order:
            st.warning("Please select an order ID. See the help section for more information.")

        else:
            with st.spinner("Cancelling order..."):
                time.sleep(5)


                for o in orders:
                    if o["id"] == selected_order:

                        found_order = True

                        # check if order already cancelled
                        if o["status"] == "Cancelled":
                            st.warning("Order already cancelled.")
                            alr_cancelled = True
                            
                        else:

                            # set order status
                            o["status"] = "Cancelled"



                            # add back stock
                            for item in inventory:
                                if item["name"] == o["item"]:
                                    item["stock"] += o["quantity"]



                            
                            # update the json files
                            with json_file.open("w",encoding="utf-8") as f:
                                json.dump(inventory, f,indent=4)
                            
                            with json_file_orders.open("w",encoding="utf-8") as f:
                                json.dump(orders,f,indent=4)
                            
        

        # success if found
        if found_order and not alr_cancelled:
            st.success("Order cancelled!")
            time.sleep(3)
            st.rerun()
        elif not found_order and not alr_cancelled:
            st.warning("Order ID was not found.")

                            
                            

             




