# Created by Mark Litak
# POS System

'''
IMPORT STUFF THE PROGRAM NEEDS
'''
from datetime import datetime #used to generate receipt numbers
from datetime import date #used for file titles and such
import pickle #used for receipts in the receipts file

'''

"HOW THE STORE WORKS" FUNCTIONS

main():
    start-up to the program

StoreFunct():
    make the whole thing work

'''

def main():
    print("Welcome to the POS System!")
    
    user = StoreLogin()
    
    if user == False:
        return None
    else:
        pass
        
    while True:
        a = StoreFunct(user)
        if a == True:
            return main()
        else:
            break
    
    return None

'''
LOGIN FUNCTION
'''
def StoreLogin():
    userdict = {'Manager':'securepassword', 'Mark':'asdfasdf', 'Lock':'hardpassword'}
    
    attempts = 3
    locked_out = []
    
    def check_login(a):
        user = str(input("Please enter User ID: "))
        
        if user in locked_out:
            print(user, "is locked out! Please contact a system administrator.")
            return check_login(3)
        
        p = input("Please enter password: ")
        
        if user in userdict:
            if userdict[user] == p:
                return user
            elif a <= 1:
                locked_out.append(user)
                print(user, ": You are locked out of your account! Please contact a system administrator.",sep='')
                return check_login(3)
            else:
                print("Not a valid login!")
                print("You have", a - 1, "attempts remaining.")
                return check_login(a - 1)
        
        elif a <= 1:
            print("You are locked out of this POS system. Please contact a system administrator.",sep='')
            return False
        
        else:
            print("Not a valid login!")
            print("You have", a - 1, "attempts remaining.")
            return check_login(a - 1)
   
    user = check_login(attempts)
    
    return user

def StoreFunct(user):
    if user == 'Manager':
        print("""
        1 = New Sale\t2 = Return Item/s\t3 = Backroom Operations\t4 = Log Out\t9 = Exit Application""")
        homescreen_option = int(input("Please select your option: "))
        
        if homescreen_option == 1:
            print("New Sale")
            NewSale()
            return StoreFunct(user)
        elif homescreen_option == 2:
            print("Return Item/s")
            Return()
            return StoreFunct(user)
        elif homescreen_option == 3:
            print("Backroom Operations")
            Backroom()
            return StoreFunct(user)
        elif homescreen_option == 9:
            print("Exit Application")
            Exit()
            return False
        elif homescreen_option == 4:
            print("Log Out")
            return True
        else:
            return StoreFunct(user)
    
    else:
        print("""
        1 = New Sale    2 = Return Item/s    4 = Log Out    9 = Exit Application""")
        homescreen_option = int(input("Please select your option: "))
        
        if homescreen_option == 1:
            print("New Sale")
            NewSale()
            return StoreFunct(user)
        elif homescreen_option == 2:
            print("Return Item/s")
            Return()
            return StoreFunct(user)
        elif homescreen_option == 4:
            print("Log Out")
            return True
        elif homescreen_option == 9:
            print("Exit Application")
            Exit()
            return False
        else:
            return StoreFunct(user)

'''

SALE FUNCTION
SUB-FUNCTIONS:
    Enter_Item
    Return_Item

'''

def NewSale():
    
    sale = []
    
    def Enter_Item():
        
        sale_UPC = str(input("Enter UPC: "))
        
        try:
            i = myStore.itemDict[sale_UPC]
            print("You entered:", i.desc)
            qty = float(input("Enter quantity: "))
            
            if qty > i.stock:
                print("There are too many items being sold!")
                print("You have attempted to sell", qty, "items.")
                print("There are", i.stock, "items.")
                return Enter_Item()
            else:
                item = ItemSold(i.UPC, i.desc, i.maxim, i.repl, i.thresh, i.stock, i.price, i.order, qty)
                sale_price = round(item.price * item.qty, 2)
                print("The price is:    $", sale_price, sep='')
    
                i.updateStock(qty)
                
                sale.append(item)
                
                return sale_price
        
        except KeyError:
            print("Not a valid UPC!")
            return Enter_Item()
    
    def Return_Item():
        #return an item by its UPC within this particular sale, bypassing any need for an entered receipt number
        UPC = str(input("Enter UPC: "))
        
        if UPC in myStore.itemDict:
            all_UPCs = []
            try:
                for item in sale:                    
                    all_UPCs.append(item.UPC)
                
                if UPC in all_UPCs:
                    pass
                else:
                    print("This item is not in the sale!")
                    return Return_Item()
                
                for item in sale:
                    if UPC == item.UPC:
                        i = myStore.itemDict[UPC]
                        print("You entered:", item.desc)
                        qty = float(input("Enter quantity to be returned: "))
                        if qty > item.qty:
                            print("There are too many items being returned!")
                            print("You have attempted to return", qty, "items.")
                            print("The receipt has", item.qty, "items.")
                            return Return_Item()
                        else:
                            item.qty -= qty
                            x = -qty
                            i.updateStock(x)
                            x = qty * item.price
                            x = round(x, 2)
                            print("The price is:    $", x, sep='')
                            return x
            except KeyError:
                print("Not a valid UPC!")
                return Return_Item()
        
        else:
            print("Not a valid UPC!")
            return Return_Item()
        
    total = Enter_Item()
    
    while True:
        print("""
        1 = Sell another item    2 = Return Item/s    9 = Complete Sale""")
        sale_option = int(input("Please select your option: "))
        if sale_option == 1:
            print("Sell another item")
            new_price = Enter_Item()
            total += new_price
            total = round(total, 2)
            print("Total:", total)
        elif sale_option == 2:
            print("Return Item/s")
            r_price = Return_Item()
            total -= r_price
            total = round(total, 2)
            print("Total:", total)
        elif sale_option == 9:
            break
    
    r = Receipt()
    num = r.getNumber()
    f_sale = [num] #Formatted sale
    
    for sold in sale:
        rItem = ReceiptItem(sold)
        r.setReceipt(rItem)
        x = rItem.getReceiptItemList()
        
        f_sale.append(x)
    
    myStore.setSaleReceipt(r)
    
    myStore.sales_today.append(r)
    
    myStore.total_amt_sold += total
    
    print("Your receipt number is", r.getNumber())    
    print("Your total is:    $", total, sep='')
    
    return None

'''

RETURN FUNCTION
SUB-FUNCTIONS:
    Return_Choice
    
'''

def Return():
    #print(myStore.getSaleReceipts())
    #first look up a receipt number in the dictionary of receipts
    number = int(input("Enter receipt number: "))
    
    #then ask if the whole receipt is to be returned or just one item
    def Return_Choice():
        print("""
        1 = Return single item    2 = Return all items    9 = Cancel""")
        choice = int(input("Please select your option: "))
        
        if choice == 1:
            return 1
        elif choice == 2:
            return 2
        elif choice == 9:
            return 9
        else:
            print("Not a valid choice!")
            return Return_Choice()
    
    try:
        r = myStore.receiptDict[number]
        formattedreceipt = r.getFormattedReceipt()
        print(formattedreceipt)
        choice = Return_Choice()
        if choice == 1:
            UPC = str(input("Enter UPC to be returned: "))
            listUPC = []
            
            for i in r.receipt:
                listUPC.append(i.upc)
                
            if UPC in listUPC:
                pass
            else:
                print("This item is not in the receipt!")
                return Return()
            
            for i in r.receipt:
                if UPC == i.upc:
                    item = myStore.itemDict[i.upc]
                    print("You entered: ", i.desc)
                    qty = float(input("Enter quantity to be returned: "))
                    if qty > i.qty:
                        print("There are too many items being returned!")
                        print("You have attempted to return", qty, "items.")
                        print("The receipt has", i.qty, "items.")
                        return 0
                    else:
                        i.qty -= qty
                        item.updateStock(-qty)
                        x = qty * i.price
                        x = round(x, 2)
                        myStore.total_amt_sold -= x
                        print("The price is:    $", x, sep='')
                        return x
            
        elif choice == 2:
            print("""Are you sure you want to return all items?
            Y = Yes    N = No""")
            rusure = str(input("Please select your option: "))
            if rusure == 'Y':
                print("\n")
                total = 0.00
                
                itemslist = r.receipt
                
                for i in itemslist:
                    item = myStore.itemDict[i.upc]
                    print(i.desc)
                    print(i.qty, "@", i.price, "each.\n")
                    total += i.price * i.qty
                    total = round(total, 2)
                    item.updateStock(-i.qty)
                print("Total to be returned: $", total, sep='')
                myStore.total_amt_sold -= total
                
                r.receipt.clear()
                    
            if rusure == 'N':
                return Return()
        
        elif choice == 9:
            return None
        
        else:
            return Return()
    
    except KeyError:
        print("Not a valid receipt number!")
        return Return()

'''

BACKROOM FUNCTION
SUB-FUNCTIONS:
    InventoryMgmt
    generateInventoryReport
    generateSalesToday

'''


def Backroom():
    
    def InventoryMgmt():
        order_total = 0.00
        to_order = []
        today_date = date.today()

        for key in myStore.itemDict:
            item = myStore.itemDict[key]
            if item.stock <= item.thresh:
                upc = item.UPC
                desc = item.desc
                price = item.price
                qty = item.getOrderQty()

                total = round(qty * price, 2)
                order_total += total

                order_text = """{upc}        {desc}
                        {qty} @ {price}                               {total}
                """.format(upc=upc, desc=desc, qty=qty, price=price, total=total)

                to_order.append(order_text)
                
                item.setOrderPlaced('Y')
            else:
                pass
        
        order_total = round(order_total, 2)
        
        order_title = "C:/Users/mlita/SEIS603/{date} Inventory Orders ${total}.txt".format(date = today_date, total = order_total)
        orders = '\n'.join(to_order)
        
        file = open(order_title, "w")
        file.write(orders)
        file.close
        
        complete = "Complete"
        
        return complete

    def generateInventoryReport():

        list_yes = ["PENDING ORDERS"]
        list_no = ["NO PENDING ORDERS"]

        for key in myStore.itemDict:
            i = myStore.itemDict[key]
            if i.order == 'Y':
                qty = i.getOrderQty()
                s="{d}\tSTOCK: {s}\tORDER THRESHOLD: {o}\tAMT ORDERED: {q}".format(d=i.desc,s=i.stock,o=i.thresh,q=qty)
                list_yes.append(s)
            else:
                s = "{d}\tSTOCK: {s}\tORDER THRESHOLD: {o}\tAMT ORDERED: N/A".format(d=i.desc,s=i.stock,o=i.thresh)
                list_no.append(s)

        pending = '\n'.join(list_yes)
        not_pending = '\n'.join(list_no)

        inventory_items_formatted = [pending, not_pending]
        
        inventory_report = '\n\n'.join(inventory_items_formatted)

        print(inventory_report)

    def generateSalesToday():
        sales_today = myStore.sales_today
        sales_list = []
        
        for r in sales_today:
            x = r.getFormattedReceipt()
            sales_list.append(str(x))
            
            
        total = myStore.total_amt_sold
        total = round(total, 2)
        
        f_sales = '\n'.join(sales_list)
        
        print("Total sold today:    $", total, sep='')
        print("TOTAL SALES:")
        print("{sales}".format(sales=f_sales))
    
    while True:
        print('''
1 = Create Orders for Replenishment\t2 = Print Inventory Report\t3 = Create Today's Item Sold Report\t9 = Exit Backroom
''')
        option = int(input("Please select your option: "))
        if option == 1:
            print("Create Orders for Replenishment")
            print(InventoryMgmt())
        elif option == 2:
            print("Create Today's Item Sold Report")
            generateInventoryReport()
        elif option == 3:
            print("Create Today's Item Sold Report")
            generateSalesToday()
        elif option == 9:
            break

'''

EXIT FUNCTION
SUB-FUNCTIONS:
    StoreDataDump():
        returns completion
    ReceiptFileDump:
        returns completion
    ItemsSoldDump:
        returns completion

'''

def Exit():        
    #Dump the data in memory for the store into the StoreData file, overwriting it
    def StoreDataDump():
        f = open("C:/Users/mlita/SEIS603/StoreData.txt", "w")
        
        f.write("UPC,Description,Item_Max_Qty,Order_Threshold,")
        f.write("replenishment_order_qty,Item_on_hand,Unit price,Order_placed,,\n")
        
        for key in myStore.itemDict:
            i = myStore.itemDict[key]
            
            UPC = i.UPC
            desc = i.desc
            maxim = i.maxim
            repl = i.repl
            thresh = i.thresh
            stock = i.stock
            price = i.price 
            order = i.order
            
            s = "{u},{d},{m},{r},{t},{s},{p},{o},,\n".format(u=UPC,d=desc,m=maxim,r=repl,t=thresh,s=stock,p=price,o=order)
            
            f.write(s)
        
        f.close()
        
        return ". . . STORE DATA UPDATE COMPLETE . . ."
            
    #Dump the data in the list of receipts into a Receipts file, appending to it
    def ReceiptFileDump():
        f = open("C:/Users/mlita/SEIS603/Receipts.txt", "wb")
        
        for key in myStore.receiptDict:
            r = myStore.receiptDict[key]
            
            pickle.dump(r, f)
        
        f.close()
        
        return ". . . RECEIPT FILE UPDATE COMPLETE . . ."
    
    #Dump the data of all items sold at this register into a file by appending (myStore.sales_today)
    def ItemsSoldDump():
        f = open("C:/Users/mlita/SEIS603/ItemsSold.txt", "a")
        today_date = date.today()
        heading = "\n{date}\n\n".format(date=today_date)
        
        f.write(heading)
        
        for sale in myStore.sales_today:
            x = sale.getFormattedReceipt()
            s = "{sale}\n\n".format(sale = x)
            f.write(s)
        
        f.close()
        
        return ". . . ITEMS SOLD FILE UPDATE COMPLETE . . ."
    
    print("PROCESSING. . .")
    print(StoreDataDump())
    print(ReceiptFileDump())
    print(ItemsSoldDump())
    print("GOODBYE")

'''

CLASSES

'''
'''

ITEM CLASSES

Item(UPC,desc,maxim,repl,thresh,stock,price,order):
    ATTRIBUTES:
        UPC,desc,maxim,repl,thresh,stock,price,order
    METHODS:
        updateStock(qty)
        getOrderQty()
    
ItemSold(super of Item, qty):
    ATTRIBUTES:
        UPC,desc,maxim,repl,thresh,stock,price,order,qty
    METHODS:
        n/a

'''
class Item:
    def __init__(self,UPC,description,item_max_qty,repl_order_qty,order_threshold,item_on_hand,price,order_placed):
        self.UPC = UPC
        self.desc = description
        self.maxim = float(item_max_qty)
        self.repl = float(repl_order_qty)
        self.thresh = float(order_threshold)
        self.stock = float(item_on_hand)
        self.price = float(price)
        self.order = order_placed
    
    def updateStock(self, qty): #used
        self.stock = self.stock - qty
    
    def setOrderPlaced(self, response): #used
        self.order = response
    
    def getOrderQty(self): #used
        x = self.stock + self.repl
        
        if x < self.thresh:
            qty = self.thresh - self.stock
        else:
            qty = self.repl
        
        return qty

class ItemSold(Item): # inheritance seemed easier to do for me than not inheritance
    def __init__(self, UPC, desc, max_qty, repl, thresh, stock, price, order, saleQty):
        super().__init__(UPC, desc, max_qty, repl, thresh, stock, price, order)
        self.qty = saleQty

'''

RECEIPT CLASSES

ReceiptItem(item_sold), pass in an ItemSold:
    ATTRIBUTES:
        upc,desc,qty,price,tot_price
    METHODS:
        getReceiptItemList()

Receipt():
    ATTRIBUTES:
        receipt (a list), number
    METHODS:
        setReceipt(receipt_item)
        getReceipt()
        getNumber()
        getFormattedReceipt()
        
'''

class ReceiptItem:
    def __init__(self, item_sold): #pass in ItemSold as item
        self.upc = item_sold.UPC
        self.desc = item_sold.desc
        self.qty = item_sold.qty
        self.price =item_sold.price
        self.tot_price = round(item_sold.qty * item_sold.price, 2)

    def getReceiptItemList(self):
        x = [self.upc, self.desc, self.price, self.qty, self.tot_price] #for use in formatting receipts
        s = "{u} {d}: {q} @ {p} each\tPRICE: {t}".format(u=x[0], d=x[1], p=x[2], q=x[3], t=x[4])
        return s

class Receipt:
    def __init__(self):
        self.receipt = []
        
        #generate receipt number by taking the time and date and formatting into one long string
        saletime = datetime.now()
        x = str(saletime)
        x = x.split()

        x[0] = x[0].split('-')
        x[0] = ''.join(x[0])

        x[1] = x[1].split(':')
        x[1][2] = x[1][2].split('.')
        x[1][2] = ''.join(x[1][2])
        x[1] = ''.join(x[1])
        
        x = ''.join(x)
        
        self.number = x

    def setReceipt(self, receipt_item): #appends a ReceiptItem into the list of objects in a receipt
        self.receipt.append(receipt_item)
    
    def getReceipt(self): #returns the list of items, unformatted
        return self.receipt

    def getNumber(self): #gets you the number of the receipt
        return self.number
    
    def getFormattedReceipt(self): #for use in formatted receipts, such as when appending to the sales_today file
        num = self.number
        r_item_list = []
        total = 0.00
        
        for i in self.receipt:
            total += round(i.tot_price, 2)
            r_strng = i.getReceiptItemList()
            r_item_list.append(r_strng)
        
        total = round(total, 2)
        
        x = '\n'.join(r_item_list)
        
        to_return = """{n}:\n{x}\n\t\t{t}""".format(n=num, x=x, t=total)
        
        return to_return
        

'''

STORE CLASS

Store(filename, receiptsfile):
    ATTRIBUTES:
        itemDict,receiptDict,sales_today,total_amt_sold, filename, rfile
    METHODS:
        getItem()
        setSaleReceipt()
        getSaleReceipts

'''

class Store:
    itemDict = {}
    receiptDict = {}
    sales_today = []
    total_amt_sold = 0.00
    
    def __init__(self, filename, receiptsfile): #when a store is made
        self.filename = filename
        self.rfile = receiptsfile
        
        df = open(self.filename) #open the data and read the text
        df.readline() #skip the first line
        
        for line in df: #makes an Item out of every line and adds it to the itemDict
            sep = line.split(",")
            
            UPC = str(sep[0])
            desc = sep[1]
            maxim = sep[2]
            repl = sep[3]
            thresh = sep[4]
            stock = sep[5]
            price = float(sep[6])
            order = sep[7]
            
            item = Item(UPC, desc, maxim, repl, thresh, stock, price, order)
            
            self.itemDict.update({UPC:item})
        
        rf = open(self.rfile, "rb")
        
        try: #unpickles the receipts file, appends each receipt to the receiptDict
            while True:
                rec = pickle.load(rf)
                r_num = rec.number
                num = int(r_num)
                self.receiptDict.update({num:rec})
        except EOFError: #when the file ends, ignore the error and don't do anything
            pass
        
        rf.close()
    
    def setSaleReceipt(self, receipt): #appends a receipt to the receiptDict
        num = int(receipt.number)
        self.receiptDict.update({num:receipt}) #send in a Receipt as the value for versatility
    
    def getSaleReceipts(self):
        return self.receiptDict



myStore = Store("StoreData.txt", "Receipts.txt")

main()