from tkinter import *
from tkinter import ttk
import mysql.connector as mysql
import os
import pickle

mc=mysql.connect(host='localhost',user='root',passwd='',charset='utf8', use_pure=True)
crs=mc.cursor()

try:
    crs.execute("create database SHOPPINGSITE")
except:
    pass
crs.execute("use SHOPPINGSITE")

categorylist=("groceries","homeappliances","games","fashion","toys","electronics")
for table in categorylist:
    try:
        crs.execute("create table "+table+"(pid int ,pname varchar(50) ,pprice int,pseller varchar(50),pquantity int, primary key(pid,pname))")
        mc.commit()
    except:
        pass
  
def adding_to_cart():
    global buyname,ROWS,ROW,productamount,buyframedesign,continueaddtocart,frame10,tax
    searchquantity.config(state=DISABLED)
    buyname=pnamesearch.get()
    frame10=Frame(screen7)
    frame10.pack()
    buyframedesign= LabelFrame(frame10, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    buyframedesign.grid(row=1,column=0)
    ROWS=("pid","pname","pprice","pseller","pquantity")
    x1=0
    for ROW in ROWS:      
        y1=0
        crs.execute("select "+ROW+" from "+categoryID+" where pname='"+buyname+"' and pquantity!='0'")
        rec=crs.fetchall()
        for r in rec:
            products=Label(buyframedesign, text=r, font="Times 26", bg="dark orange")
            products.grid(row=1, column=x1, padx=25, pady=11)
        x1+=1
    if rec==[]:
        notavailble=Label(buyframedesign, text="No Such Product Available/Out of Stock", fg="red", font="TIMES 20")
        notavailble.grid(row=1,column=0)
        notavailble.after(1290, lambda: searchquantity.config(state=NORMAL))
        notavailble.after(1300, lambda: frame10.destroy())
    else:
        productamount=StringVar()
        reg=screen7.register(callback)
        product_headers(buyframedesign, "dark orange", "no", "yes")
        Label(buyframedesign, text="Enter Amount You want to Buy", font="Times 26", bg="dark orange").grid(row=2, column=0, columnspan=3)
        amount= Entry(buyframedesign, textvariable= productamount, font="Times 25")
        amount.grid(row=2, column=3, columnspan=2)
        amount.config(validate="key", validatecommand=(reg,'%P'))
        continueaddtocart=Button(buyframedesign, text="Enter", command= check_quantity, width=17, font="Times 18", bg="light green")
        continueaddtocart.grid(row=3, column=0, columnspan=2, pady=10)
        Button(buyframedesign, text="Cancel", command= re_search_buy, width=17, font="Times 18", bg="red").grid(row=3, column=2)
    
def callback(input):
    if input.isdigit() or input == "":
        return True
    else:
        return False

def check_quantity():
    global buyamount,addtocart
    buyamount=productamount.get()
    continueaddtocart.config(state=DISABLED)
    if buyamount=="0" or buyamount=="":
        zeroproduct=Label(screen7, text="Enter some amount", fg="red", bg="dark orange", font="TIMES 25")
        zeroproduct.pack()
        zeroproduct.after(1300, lambda: zeroproduct.destroy())
        continueaddtocart.config(state=NORMAL)
    else:
        crs.execute("select pquantity from "+categoryID+" where pquantity>="+buyamount+" and pname='"+buyname+"'")
        stock=crs.fetchall()
        if stock==[]:
            continueaddtocart.config(state=NORMAL)
            notavailble=Label(screen7, text="NOT ENOUGH STOCK", fg="red", bg="dark orange", font="TIMES 25")
            notavailble.pack()
            notavailble.after(1300, lambda: notavailble.destroy())
        else:
            crs.execute("select (pprice*"+buyamount+") from "+categoryID+" where pname='"+buyname+"'")
            rec=crs.fetchall()
            for totalprice in rec:
                Label(buyframedesign, text=totalprice, font="Times 25", bg="dark orange").grid(row=5, column=2)
            Label(buyframedesign, text="", bg="dark orange").grid(row=4, column=0, columnspan=2)
            Label(buyframedesign, text="TOTAL PRICE:", font="Times 25", bg="dark orange").grid(row=5, column=0, columnspan=2)
            Label(buyframedesign, text="Rs.", font="Times 25", bg="dark orange").grid(row=5, column=1, columnspan=2)
            addtocart=Button(buyframedesign, text="Add To Cart", width=17, height=1, command= add_to_cart, font= "TIMES 17", bg="light green")
            addtocart.grid(row=6, column=0, columnspan=2, pady=10)

def re_search_buy():
    searchquantity.config(state=NORMAL)
    frame10.destroy()
    productnamesearch.delete(0, END)
    
def add_to_cart():
    addedtocart=Label(buyframedesign, text="Added To Cart !!!", fg="green", font="TIMES 25 bold", bg="dark orange")
    addedtocart.grid(row=6, column=0, columnspan=5)
    addedtocart.after(900, lambda: refresh(screen7))
    addtocart.config(state=DISABLED)
    try:
        crs.execute("create table "+username_info+"(pid int ,pname varchar(50) ,pprice int ,pseller varchar(50) ,pquantity int, ptotalamount int, primary key(pid,pname))")
        mc.commit()
    except:
        pass
    crs.execute("select pname from "+username_info+" where pname='"+buyname+"'")
    rec=crs.fetchall()
    if rec==[]:
        crs.execute("insert into "+username_info+"(pid,pname,pprice,pseller,pquantity,ptotalamount) select pid,pname,pprice,pseller,"+buyamount+",(pprice*"+buyamount+") from "+categoryID+" where pname='"+buyname+"'")
        mc.commit()
    else:
        crs.execute("update "+username_info+" set pquantity=(pquantity+"+buyamount+") where pname='"+buyname+"'") 
        crs.execute("update "+username_info+" set ptotalamount=(pquantity*pprice) where pname='"+buyname+"'")
        mc.commit()
    crs.execute("update "+categoryID+" set pquantity=(pquantity-"+buyamount+") where pname='"+buyname+"'")
    mc.commit()

def remove_from_cart():
    global removename,screen13,searchcart,removeproduct
    screen13=Toplevel(screen9)
    screen13.attributes("-fullscreen", True)
    screen13.title("Remove from cart")
    removeID=StringVar()
    bg_photo(screen13)
    Label(screen13,text="REMOVE FROM CART", bg="gold", width="300", height="1", font="TIMES 34").pack()
    frame12=Frame(screen13)
    frame12.pack(pady=20)
    framedesign= LabelFrame(frame12, width=1400, height=700, relief='ridge', bg="gold", bd=20)
    framedesign.grid(row=1,column=0)
    removename= StringVar()
    Label(framedesign, text="Product Name:", font="TIMES 25", bg="gold").grid(row=1, column=0, padx=15, pady=20)
    removeproduct= Entry(framedesign, textvariable= removename, font="TIMES 22")
    removeproduct.grid(row=1, column=1, padx=20)
    searchcart= Button(framedesign, text="Search", height=1, width=10, command=remove_cart_frame, bg="light green", font= "TIMES 20")
    searchcart.grid(row=2, column=1, columnspan=2, pady=10)
    Button(screen13,text="go back", height=2 , width=15, command= screen13.destroy).place(x=5, y=5)

def remove_cart_frame():
    global removeamount, frame13
    frame13=Frame(screen13)
    frame13.pack()
    reg=screen13.register(callback)
    removeframedesign= LabelFrame(frame13, width=1400, height=700, relief='ridge', bg="gold", bd=20)
    removeframedesign.grid(row=1,column=0)
    removeamount=StringVar()
    ROWS=("pid","pname","pprice","pseller","pquantity")
    x1=0
    for i in ROWS:
        crs.execute("select "+i+" from "+username_info+" where pname='"+removename.get()+"'")
        rec=crs.fetchall()
        for r in rec:
            products=Label(removeframedesign, text=r, font="Times 25", bg="gold")
            products.grid(row=1, column=x1, padx=25, pady=11)
        x1+=1
    if rec==[]:
        notavailble=Label(removeframedesign, text="No Such Product Available", fg="red", bg="gold", font="Times 25")
        notavailble.grid(row=0, column=0)
        notavailble.after(1300, lambda: frame13.destroy())
    else:
        searchcart.config(state=DISABLED)
        product_headers(removeframedesign,"gold", "no")
        Button(removeframedesign,text="Remove", height=1, width=10, command=removing_product, font="TIMES 20", bg="red").grid(row=3, column=0, padx=10, pady=10)
        Button(removeframedesign,text="Re-Search Product", height=1, width=20, font="TIMES 20", bg="light green", command= re_search_remove).grid(row=3, column=1, padx=10, pady=10)
        Label(removeframedesign, text="Enter Amount:", font="TIMES 28", bg="gold").grid(row=2, column=0, pady=10)
        remove= Entry(removeframedesign, textvariable= removeamount, font="TIMES 22")
        remove.grid(row=2, column=1, padx=10)
        remove.config(validate="key", validatecommand=(reg,'%P'))

def re_search_remove():
    searchcart.config(state=NORMAL)
    removeproduct.delete(0, END)
    frame13.destroy()
    
def removing_product():
    categorylist=("groceries","homeappliances","games","fashion","toys","electronics")
    try:
        crs.execute("select* from "+username_info+" where pquantity>="+removeamount.get()+" and pname='"+removename.get()+"'")
        rec=crs.fetchall()
        if rec==[]:
            crs.execute("delete from "+username_info+" where pname='"+removename.get()+"'")
        else:
            for category in categorylist:
                try:
                    crs.execute("update "+category+" set pquantity=(pquantity+"+removeamount.get()+") where pname='"+removename.get()+"'")
                    mc.commit()
                except:
                    pass
            crs.execute("update "+username_info+" set pquantity=(pquantity-"+removeamount.get()+") where pname='"+removename.get()+"'")
            crs.execute("update "+username_info+" set ptotalamount=(pquantity*pprice) where pname='"+removename.get()+"'")
            crs.execute("delete from "+username_info+" where pquantity=0")
        mc.commit()
        screen13.destroy()
        containerframe.destroy()
        shopping_cart_frame()
    except:
        notavailble=Label(screen13, text="Invalid Entry", fg="red", bg="gold", font="Times 25")
        notavailble.pack()
        notavailble.after(1300, lambda: notavailble.destroy())

def buy_screen():
    global screen10,frame14,addressframedesign
    screen10=Toplevel(screen)
    screen10.attributes("-fullscreen",True)
    screen10.title("BUYING SCREEN")
    bg_photo(screen10)
    frame14=Frame(screen10)
    reg=screen10.register(callback)
    addressframedesign= LabelFrame(frame14, width=1400, height=700, relief='ridge', bg="green", bd=20)
    addressframedesign.grid(row=1,column=0)
    try:
        crs.execute("create table "+username_info+"address(houseno varchar(8),locality varchar(20),city varchar(20),state varchar(20),pincode int(6))")
        mc.commit()
    except:
       pass
    crs.execute("select* from "+username_info+"address")
    address=crs.fetchall()
    if address==[]:
        address_frame("no")
    else:
        payment_frame()

def payment_frame():
    global paymentheading,choosecard,frame15
    frame15=Frame(screen10)
    frame15.place(x=5,y=85)
    smalladdressframe= LabelFrame(frame15, width=1400, height=700, relief='ridge', bg="green", bd=20)
    smalladdressframe.grid(row=1,column=0)
    crs.execute("select houseno,locality from "+username_info+"address")
    address=crs.fetchall()
    for i in address:
        Label(smalladdressframe, text=i, font= "TIMES 17", bg='green').grid(row=1, column=0, padx=15, pady=10)
    crs.execute("select city,state,pincode from "+username_info+"address")
    address=crs.fetchall()
    for i in address:
        Label(smalladdressframe, text=i, font= "TIMES 17", bg='green').grid(row=2, column=0, padx=15, pady=10)
    paymentheading=Label(screen10,text="PAYMENT", bg='green', width="300", height="1", font= "TIMES 34")
    paymentheading.pack()
    Button(screen10, text="go back", height="2", width="15", command=screen10.destroy).place(x=5,y=5)
    frame14.pack(pady=25)
    Label(smalladdressframe, text="Current Address:", font= "TIMES 25", bg='green').grid(row=0, column=0, padx=15, pady=10)
    Button(smalladdressframe, text="Change Address", height="1", width="15", command= change_address, font= "TIMES 16", bg='dark blue').grid(row=3, column=0)
    Label(addressframedesign,text="Payment Options", font= "TIMES 30 bold", bg='green').grid(row=0, column=0, columnspan=3, pady=20)
    choosecard=Button(addressframedesign,text="Credit/Debit Card", command=card, font= "TIMES 18", bg="light green")
    choosecard.grid(row=7, column=0, padx=10, pady=10)
    Button(addressframedesign,text="Cash on Delivery", command= bought_product, font= "TIMES 18", bg="light green").grid(row=7, column=1, padx=10, pady=10, columnspan=2)
    
def address_frame(existingaddress):
    global paymentheading,hb_info,pincode_info,city_info,state_info,locality_info
    paymentheading=Label(screen10,text="ADD ADDRESS", bg='green', width="300", height="1", font= "TIMES 34")
    paymentheading.pack()
    frame14.pack(pady=25)
    Button(screen10, text="go back", height="2", width="15", command=screen10.destroy).place(x=5,y=5)
    hb_info=StringVar()
    pincode_info=StringVar()
    city_info=StringVar()
    state_info=StringVar()
    locality_info=StringVar()
    reg=screen10.register(callback)
    Label(addressframedesign,text="Enter your Address", font="TIMES 30", bg="green").grid(row=0, column=0, columnspan=2, pady=30)
    Label(addressframedesign,text="Block-Home no.", font="TIMES 28", bg="green").grid(row=1, column=0, pady=15, padx=10)
    hb=Entry(addressframedesign,textvariable=hb_info, font="TIMES 22")
    hb.grid(row=1, column=1, padx=15)
    Label(addressframedesign,text="Pincode", font="TIMES 28", bg="green").grid(row=2, column=0, pady=15)
    pincode=Entry(addressframedesign,textvariable=pincode_info, font="TIMES 22")
    pincode.grid(row=2, column=1)
    pincode.config(validate="key", validatecommand=(reg,'%P'))
    Label(addressframedesign,text="Locality", font="TIMES 28", bg="green").grid(row=3, column=0, pady=15)
    Locality=Entry(addressframedesign, textvariable=locality_info, font="TIMES 22")
    Locality.grid(row=3, column=1)
    Label(addressframedesign,text="City", font="TIMES 28", bg="green").grid(row=4, column=0, pady=15)
    city=Entry(addressframedesign,textvariable=city_info, font="TIMES 22")
    city.grid(row=4, column=1)
    Label(addressframedesign,text="State", font="TIMES 28", bg="green").grid(row=5, column=0, pady=15)
    state=Entry(addressframedesign,textvariable=state_info, font="TIMES 22")
    state.grid(row=5, column=1)
    if existingaddress=="yes":
        Button(addressframedesign,text="Submit",height="1",width="10", command=add_address, font="TIMES 26", bg="light green").grid(row=6, column=0, pady=20)
        Button(addressframedesign,text="cancel",height="1",width="10", command=cancel_add_address, font="TIMES 26", bg="red").grid(row=6, column=1)
    else:
        Button(addressframedesign,text="Submit",height="1",width="10", command=add_address, font="TIMES 26", bg="light green").grid(row=6, column=0, pady=20, columnspan=2)

def cancel_add_address():
    change_payment_screen()
    payment_frame()

def add_address():
    try:
        crs.execute("delete* from "+username_info+"address")
    except:
        pass
    try:
        A="insert into "+username_info+"address(houseno,locality,city,state,pincode) values(%s,%s,%s,%s,%s)"
        entry=(hb_info.get(),locality_info.get().capitalize(),city_info.get().capitalize(),state_info.get().capitalize(),pincode_info.get())
        crs.execute(A,entry)
        mc.commit()
        change_payment_screen()
        payment_frame()
    except:
        notavailble=Label(screen10, text="Invalid Entry", fg="red", bg="green", font="Times 25")
        notavailble.pack()
        notavailble.after(1300, lambda: notavailble.destroy())

def change_address():
    frame15.destroy()
    change_payment_screen()
    address_frame("yes")

def change_payment_screen():
    global frame14,addressframedesign
    frame14.destroy()
    paymentheading.destroy()
    frame14=Frame(screen10)
    addressframedesign= LabelFrame(frame14, width=1400, height=700, relief='ridge', bg="green", bd=20)
    addressframedesign.grid(row=1,column=0)
    
def card():
    global cardnumbercheck,monthcheck,yearcheck,CVVcheck
    choosecard.config(state=DISABLED)
    cardnumbercheck=StringVar()
    monthcheck=StringVar()
    yearcheck=StringVar()
    CVVcheck=StringVar()
    reg=screen10.register(callback)
    Label(addressframedesign,text="Enter your Card Details :", font= "TIMES 25", bg='green').grid(row=1, column=0, columnspan=3)
    Label(addressframedesign,text="Card Number", font= "TIMES 25", bg='green').grid(row=2, column=0, pady=15)
    cardnumber=Entry(addressframedesign, textvariable=cardnumbercheck, font= "TIMES 20")
    cardnumber.grid(row=2, column=1, columnspan=2)
    cardnumber.config(validate="key", validatecommand=(reg,'%P'))
    Label(addressframedesign,text="Expiry Date \n (MM/YYYY)", font= "TIMES 25", bg='green').grid(row=3, column=0, pady=15)
    month=Entry(addressframedesign,textvariable=monthcheck, width=8, font= "TIMES 20")
    month.grid(row=3, column=1, padx=22)
    month.config(validate="key", validatecommand=(reg,'%P'))
    Label(addressframedesign, text="                ", bg='green', font="TIMES 25").grid(row=3, column=2)
    year=Entry(addressframedesign,textvariable=yearcheck, width=14, font= "TIMES 20")
    year.grid(row=3, column=1, columnspan=3)
    year.config(validate="key", validatecommand=(reg,'%P'))
    Label(addressframedesign,text="Enter CVV", font= "TIMES 25", bg='green').grid(row=4, column=0, pady=15)
    cardCVV=Entry(addressframedesign,textvariable=CVVcheck, font= "TIMES 20", show="*")
    cardCVV.grid(row=4, column=1, columnspan=2)
    cardCVV.config(validate="key", validatecommand=(reg,'%P'))
    card=Label(addressframedesign,text="For your safety we do not store any card details", font= "TIMES 25", bg='green').grid(row=5, column=0, columnspan=3, pady=15)
    card=Button(addressframedesign, text="Pay", height="1", width="10", command= validate_card, font= "TIMES 22 bold", bg='gold').grid(row=6, column=0, columnspan=3, pady=15)

def validate_card():
    global screen10,screen9
    check1=0
    check2=0
    check3=0
    check4=0
    success=0
    for i in cardnumbercheck.get():
        check1+=1
    if check1==16:
        check1="succesful"
    for i in monthcheck.get():
        check2+=1
    if check2<=2:
        check2="succesful"
    for i in yearcheck.get():
        check3+=1
    if check3==4:
        check3="succesful"
    for i in CVVcheck.get():
        check4+=1
    if check4==3:
        check4="succesful"
    check=(check1,check2,check3,check4)        
    for i in check:
        if i!="succesful":
            invalidcard=Label(screen10, text="Check Your Card Details", fg="red", bg='green', font="TIMES 25")
            invalidcard.pack()
            invalidcard.after(1200, lambda: invalidcard.destroy())
            break
        else:
            success+=1
    if success==4:
        bought_product()
        
def bought_product():
    global screen14
    screen14=Toplevel(screen)
    bg_photo(screen14)
    screen14.attributes("-fullscreen",True)
    screen14.title("Summary")
    Label(screen14,text="ORDER PLACED", bg='green', width="300", height="1", fg="white", font="TIMES 34").pack()
    Label(screen14, text="SUMMARY", font= "TIMES 28", bg="green").pack()
    space=Label(screen14, text="", height=2)
    space.pack()
    space.lower()
    scroll_command(screen14, "yes")
    frame16=Frame(canvas)
    canvas.create_window((0,0), window= frame16, anchor="nw")
    framedesign=LabelFrame(frame16, width=1400, height=700, relief='ridge', bg='green', bd=20)
    framedesign.grid(row=1,column=0)
    Label(framedesign, text="AMOUNT", font="Times 28 bold", bg="green").grid(row=0, column=5, padx=30)
    product_headers(framedesign, "green", "yes", "yes")
    ROWS=("pid","pname","pprice","pseller","pquantity","ptotalamount")
    x1=0
    for i in ROWS:
        y1=1
        crs.execute("select "+i+" from "+username_info)
        rec=crs.fetchall()
        for r in rec:
            products=Label(framedesign, text=r, font="Times 25", bg="green").grid(row=y1, column=x1, pady=11)
            y1+=1
        x1+=1
    crs.execute("select SUM(ptotalamount) from "+username_info)
    totalprice=crs.fetchall()
    for i in totalprice:
        Label(framedesign, text=i, font="TIMES 27", bg='green').grid(row=y1+1, column=2, columnspan=2)
    Label(framedesign, text="TOTAL PRICE", font="Times 27", bg='green').grid(row=y1+1, column=1, pady=20)
    Label(framedesign, text="Rs.", font="Times 27", bg='green').grid(row=y1+1, column=2)
    Button(framedesign, text="Continue", command=exit_summary, font="Times 20", bg='light green').grid(row=y1+2, column=2, columnspan=2, pady=10)
    canvasheight=(y1-1)*65
    if canvasheight>=380:
        canvasheight=380
    canvas.configure(height=292+canvasheight)
    try:
        crs.execute("create table "+username_info+"orders(pid int ,pname varchar(50),pprice int,pseller varchar(50),pquantity int,ptotalamount int)")
    except:
        pass
    crs.execute("insert into "+username_info+"orders (pid,pname,pprice,pseller,pquantity,ptotalamount) select pid,pname,pprice,pseller,pquantity,ptotalamount from "+username_info)
    crs.execute("drop table "+username_info)
    mc.commit()

def exit_summary():
    screen10.destroy()
    screen9.destroy()
    screen14.destroy()

def adding_product():
    try:
        pid_info=product_id.get()
        pname_info=product_name.get()
        pprice_info=product_price.get()
        pquantity_info=product_quantity.get()
        counter=0
        if pquantity_info=="0" or pprice_info=="0":
            wrongentry=Label(screen5, text="Invalid Entry", fg='red', font="TIMES 25", bg="dark orange")
            wrongentry.pack()
            wrongentry.after(1200, lambda: wrongentry.destroy())
        else:
            categorylist=("groceries","homeappliances","games","fashion","toys","electronics")
            for i in categorylist:
                crs.execute("select pid from "+i+" where pid="+pid_info)
                ID=crs.fetchall()
                if ID==[]:
                    counter+=1
            if counter==6:
                Q="insert into "+categoryID+"(pid,pname,pprice,pseller,pquantity) values(%s,%s,%s,%s,%s)"
                entry=(pid_info,pname_info,pprice_info,username_info,pquantity_info)
                crs.execute(Q,entry)
                mc.commit()
                try:
                    noproductcat.destroy()
                except:
                    pass
                refresh(screen5)    
            else:
                pidexist=Label(screen5, text="pid already exists", fg='red', font="TIMES 25", bg="dark orange")
                pidexist.pack()
                pidexist.after(1200, lambda: pidexist.destroy())
    except:
        wrongentry=Label(screen5, text="Invalid Entry", fg='red', font="TIMES 25", bg="dark orange")
        wrongentry.pack()
        wrongentry.after(1200, lambda: wrongentry.destroy())

def add_product():
    global product_id,product_name,product_price,product_quantity,screen5
    screen5=Toplevel(screen)
    screen5.attributes("-fullscreen", True)
    screen5.title("Add Product to "+categoryID)
    bg_photo(screen5)
    Label(screen5, text="Add Product to "+categoryID, bg='dark orange', width="300", height="1", font= "TIMES 33").pack()
    frame5 = Frame(screen5)
    space=Label(screen5, text="", height=2)
    space.pack()
    space.lower()
    frame5.pack()
    framedesign=LabelFrame(frame5, width=1400, height=700, relief='ridge', bg='dark orange', bd=20)
    framedesign.grid(row=1,column=0)
    product_id=StringVar()
    product_name=StringVar()
    product_price=StringVar()
    product_quantity=StringVar()
    Label(framedesign, text="Please enter details below", font="Times 30", bg= "dark orange").grid(row=0 ,column=0, columnspan=2, pady=30)
    Label(framedesign, text="Product Id", font="Times 25", bg= "dark orange").grid(row=1, column=0, padx=20, pady=17)
    productid=Entry(framedesign, textvariable=product_id, font="Times 25")
    productid.grid(row=1, column=1, padx=20)
    Label(framedesign, text="Product Name", font="Times 25", bg= "dark orange").grid(row=2, column=0, padx=20, pady=17)
    productname=Entry(framedesign, textvariable=product_name, font="Times 25")
    productname.grid(row=2, column=1, padx=20)
    Label(framedesign, text="Product Price", font="Times 25", bg= "dark orange").grid(row=3, column=0, padx=20, pady=17)
    productprice=Entry(framedesign, textvariable=product_price, font="Times 25")
    productprice.grid(row=3, column=1, padx=20)
    Label(framedesign, text="Product Quantity", font="Times 25", bg= "dark orange").grid(row=4, column=0, padx=20, pady=17)
    productquantity=Entry(framedesign, textvariable=product_quantity, font="Times 25")
    productquantity.grid(row=4, column=1, padx=20)
    Button(framedesign,text="Add Product", height=1, width=15, command=adding_product, font="Times 25", bg="light green").grid(row=5, column=0, columnspan=2, pady=20)            
    Button(screen5,text="Cancel",height=2,width=15,command= screen5.destroy).place(x=5,y=5)

def delete_product():
    delete= deleteID.get()
    screen6.title("Delete from "+categoryID)
    crs.execute("delete from "+categoryID+" where pid='"+delete+"' and pseller='"+username_info+"'")
    mc.commit()
    refresh(screen6)

def add_quantity():
    global screen11,pquantityID,searchquantity,productidquantitysearch
    screen11= Toplevel(screen)
    screen11.title("ADD QUANTITY")
    screen11.attributes("-fullscreen", True)
    bg_photo(screen11)
    Label(screen11, text="Add Quantity of a Product to "+categoryID, bg='dark orange', width="300", height="1", font= "TIMES 33").pack()
    frame7=Frame(screen11)
    frame7.pack(pady=20)
    framedesign= LabelFrame(frame7, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    framedesign.grid(row=1,column=0)
    pquantityID= StringVar()
    Label(framedesign, text="Product ID:", font="TIMES 25", bg="dark orange").grid(row=1, column=0, padx=15, pady=20)
    productidquantitysearch=Entry(framedesign, textvariable=pquantityID, font="TIMES 25")
    productidquantitysearch.grid(row=1, column=1, padx=20)
    searchquantity= Button(framedesign, text="Search", height=1, width=10, command=add_quantity_frame, bg="light green", font= "TIMES 20")
    searchquantity.grid(row=2, column=1, columnspan=2, pady=10)
    Button(screen11,text="cancel", height=2 , width=15, command= screen11.destroy).place(x=5, y=5)

def add_quantity_frame():
    global productquantity,frame8
    productquantity= StringVar()
    frame8=Frame(screen11)
    frame8.pack(pady=10)
    framedesign= LabelFrame(frame8, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    framedesign.grid(row=1,column=0)
    ROWS=("pid","pname","pprice","pseller","pquantity")
    try:
        x1=0
        for i in ROWS:
            crs.execute("select "+i+" from "+categoryID+" where pid="+pquantityID.get()+" and pseller='"+username_info+"'")
            rec=crs.fetchall()
            for r in rec:
                products=Label(framedesign, text=r, font="Times 25", bg="dark orange")
                products.grid(row=1, column=x1, padx=25, pady=11)
            x1+=1
        if rec==[]:
            notavailble=Label(framedesign, text="No Such Product Available", fg="red", bg="dark orange", font="Times 25")
            notavailble.pack()
            notavailble.after(1300, lambda: frame8.destroy())
        else:
            searchquantity.config(state=DISABLED)
            product_headers(framedesign,"dark orange", "no")
            pquantity=Entry(framedesign, textvariable=productquantity, font="TIMES 25")
            pquantity.grid(row=2, column=1, padx=10)
            Label(framedesign, text="Quantity:", font="TIMES 25", bg="dark orange").grid(row=2, column=0, pady=10)
            Button(framedesign,text="Add Quantity", height=1, width=10, command=adding_quantity, font="TIMES 20", bg="light green").grid(row=3, column=0, padx=10, pady=10)
            Button(framedesign,text="Re-Search Product", height=1, width=20, font="TIMES 20", bg="red", command=re_search_addquantity).grid(row=3, column=1, padx=10, pady=10)
    except:
        notavailble=Label(framedesign, text="No Such Product Available", fg="red", bg="dark orange", font="Times 25")
        notavailble.pack()
        notavailble.after(1300, lambda: frame8.destroy())

def re_search_addquantity():
    frame8.destroy()
    searchquantity.config(state=NORMAL)
    productidquantitysearch.delete(0, END)

def adding_quantity():
    adding="select* from "+categoryID+" where pid="+pquantityID.get()+" and pseller='"+username_info+"'"
    crs.execute(adding)
    rec=crs.fetchall()
    if rec==[]:
        notfound=Label(screen11, text="Product with no such ID Entered by You in "+categoryID, fg='red')
        notfound.pack()
        notfound.after(1200, lambda: notfound.destroy())
    else:
        try:
            crs.execute("update "+categoryID+" set pquantity=(pquantity+"+productquantity.get()+") where pid="+pquantityID.get()+" and pseller='"+username_info+"'")
            mc.commit()
            refresh(screen11)
        except:
            notfound=Label(screen11, text="Check Your Entries", fg='red')
            notfound.pack()
            notfound.after(1200, lambda: notfound.destroy())

def delete_account():
    global passkey,screen4,password_info,delete_password,filename
    screen4 = Toplevel(screen2)
    screen4.title("DELETE ACCOUNT")
    screen4.attributes("-fullscreen", True)
    delete_password = StringVar()
    bg_photo(screen4)
    Label(screen4, text="DELETE ACCOUNT", bg='red', width="300", height="1", font= "TIMES 33 bold").pack()
    frame9=Frame(screen4)
    frame9.pack(pady=25)
    framedesign= LabelFrame(frame9, width=1400, height=700, relief='ridge', bg="red", bd=20)
    framedesign.grid(row=1,column=0)
    Label(framedesign, text= "Enter Password:", font="TIMES 27", bg="red").grid(row=0, column=0, padx=20, pady=10)
    password_info = Entry(framedesign, textvariable= delete_password, font="TIMES 25", show="*")
    password_info.grid(row=0, column=1, padx=20)
    Label(framedesign, text = "(continue will instantly delete your account)", fg="dark red", font="TIMES 20", bg="red").grid(row=1, column=0, columnspan=2, padx=20, pady=5)
    Button(framedesign, text = "continue", width = 10, height = 1, command= confirm_delete_account, font="TIMES 22", bg="green").grid(row=2, column=0, columnspan=2, pady=20)
    Button(screen4, text = "go back", width = 10, height = 2, command= screen4.destroy).place(x=5, y=5)
    
def confirm_delete_account():
    global categorylist
    if delete_password.get()==passkey:
        os.remove("Account Info/"+username_info+".bin")
        categorylist=("groceries","homeappliances","games","fashion","toys","electronics")
        for i in categorylist:
            crs.execute("delete from "+i+" where pseller='"+username_info+"'")
        a="drop table "+username_info
        b="drop table "+username_info+"address"
        c="drop table "+username_info+"orders"
        drop=(a,b,c)
        for i in drop:
            try:
                crs.execute(i)
            except:
                pass
        mc.commit()
        screen4.destroy()
        sign_out()
    else:
        incorrect_password=Label(screen4, text="Account not deleted Incorrect Password", fg="dark red", font="TIMES 25", bg="red")
        incorrect_password.pack()
        incorrect_password.after(1200, lambda: incorrect_password.destroy())

def groceries():
    global categoryID,categoryclr
    categoryID="groceries"
    categoryclr='cyan'
    categories()

def home_appliances():
    global categoryID,categoryclr
    categoryID="homeappliances"
    categoryclr='dark red'
    categories()
       
def games():
    global categoryID,categoryclr
    categoryID="games"
    categoryclr='blue'
    categories()

def fashion():
    global categoryID,categoryclr
    categoryID="fashion"
    categoryclr='purple'
    categories()

def toys():
    global categoryID,categoryclr
    categoryID="toys"
    categoryclr='red'
    categories()
        
def electronics():
    global categoryID,categoryclr
    categoryID="electronics"
    categoryclr='cyan'
    categories()    

def shopping_cart():
    global screen9,cartframedesign,removefromcart
    screen9=Toplevel(screen)
    screen9.title("CART")
    screen9.attributes("-fullscreen", True)
    bg_photo(screen9)
    Label(screen9, text="YOUR CART", bg='gold', width="300", height="1", font= "TIMES 34").pack()
    space=Label(screen9, text="", height=2)
    space.pack()
    space.lower()
    shopping_cart_frame()

def shopping_cart_frame():
    global frame11
    scroll_command(screen9, "yes")
    frame11=Frame(canvas)
    canvas.create_window((0,0), window= frame11, anchor="nw")
    cartframedesign= LabelFrame(frame11, width=1400, height=700, relief='ridge', bg="gold", bd=20)
    cartframedesign.grid(row=1,column=0)
    removefromcart=Button(screen9, text="Remove", height =2, width =15, command= remove_from_cart)
    removefromcart.place(x=windowwidth-117,y=5)
    try:
        ROWS=("pid","pname","pprice","pseller","pquantity","ptotalamount")
        x1=0
        for i in ROWS:
            y1=1
            crs.execute("select "+i+" from "+username_info)
            rec=crs.fetchall()
            for r in rec:
                products=Label(cartframedesign, text=r, font="Times 25", bg="gold").grid(row=y1, column=x1, pady=11)
                y1+=1
            x1+=1
        if rec==[]:
            containerframe.destroy()
            Label(screen9, text="Your Cart is Empty", fg="red", font= "TIMES 30", bg="gold").grid(row=1, column=0)
            removefromcart.config(state=DISABLED)
        else:
            product_headers(cartframedesign, "gold", "yes", "yes")
            canvasheight=(y1-1)*65
            if canvasheight>=400:
                canvasheight=400
            canvas.configure(height=285+canvasheight)
            Label(cartframedesign, text="AMOUNT", font="Times 28 bold", bg="gold").grid(row=0, column=5, padx=30)
            crs.execute("select SUM(ptotalamount) from "+username_info)
            totalprice=crs.fetchall()
            for i in totalprice:
                Label(cartframedesign, text=i, font="TIMES 25", bg="gold").grid(row=y1+1, column=2, columnspan=2)
            Label(cartframedesign, text="TOTAL PRICE:", font="Times 25", bg="gold").grid(row=y1+1, column=1, pady=20)
            Label(cartframedesign, text="Rs.", font="Times 25", bg="gold").grid(row=y1+1, column=2)
            Button(cartframedesign, text="Proceed to buy",command= buy_screen, font="TIMES 20", bg="#03AC13").grid(row=y1+2, column=2, columnspan=2, pady=10)
    except:
        containerframe.destroy()
        removefromcart.config(state=DISABLED)
        Label(screen9, text="Your Cart is Empty", fg="red", font= "TIMES 30", bg="gold").pack()
    Button(screen9, text="go back", height =2, width =15, command= screen9.destroy).place(x=5,y=5)
   
def shopping():
    global input_,screen2,yourcart
    screen2=Toplevel(screen)
    bg_photo(screen2)
    heading=Label(screen2, text="SONIC CART", bg="light green", width=900, height=1, font= "JOKERMAN 30").pack()
    space=Label(screen2, text="", height=1)
    space.pack()
    space.lower()
    screen2.title("Shopping site")
    screen2.attributes("-fullscreen", True)
    scroll_command(screen2, "no")
    frame3=Frame(canvas)
    canvas.create_window((0,0), window= frame3, anchor="nw")
    if screen.winfo_screenheight()<=800:
        shoppingframe=screen.winfo_screenheight()-30
        canvas.configure(height=shoppingframe, width=1250)
    else:
        canvas.configure(height=747, width=1250)
    framedesign=LabelFrame(frame3, width=1400, height=700, relief='ridge', bg='light green', bd=20)
    framedesign.grid(row=1,column=0)
    input_= StringVar()
    userinfo=Label(screen2, text="User: "+username_info, bg="light green", font= "TIMES 16")
    userinfo.place(x=5,y=5)
    photos=("groceries","homeappliances","games","clothes","toys","electronics")
    x1=0
    y1=0
    for i in photos:
        photo= PhotoImage(file = "Assets/"+i+".gif")
        lab = Label(framedesign, image=photo)
        lab.image = photo
        lab.grid(row=x1,column=y1,padx=20, pady=0)
        if y1==2:
            x1+=3
            y1=0
        else:
            y1+=1
    grocery= Button(framedesign, text="Groceries", width=22, height=1, command= groceries, font="garamond 20 bold", bg="pink").grid(row=1, column=0)
    space=Label(framedesign, text="", bg='light green').grid(row=2,column=1, pady=11)
    homeappliance= Button(framedesign, text="HomeApliances", width=24, height=1, command= home_appliances, font="garamond 19 bold", bg="white").grid(row=1, column=1)
    game= Button(framedesign, text="Games", width=20, height=1, command= games, font="garamond 20 bold", bg="light blue").grid(row=1, column=2)
    fashions= Button(framedesign, text="Fashion", width=24, height=1, command= fashion, font="garamond 19 bold", bg="purple").grid(row=4, column=0)
    toy= Button(framedesign, text="Toys", width=23, height=1, command= toys, font="garamond 20 bold", bg="orange").grid(row=4, column=1)
    electronic= Button(framedesign, text="Electronics", width=23, height=1, command= electronics, font="garamond 21 bold", bg="#03AC13").grid(row=4, column=2)
    Button(screen2, text="sign out", width=12, height=1, command= sign_out).place(x=windowwidth-100,y=5)
    Button(screen2, text="delete acoount", width=12, height=1, command= delete_account).place(x=windowwidth-100,y=37)
    myfile = open("Account Info/"+username_info+".bin","rb")
    try:
        pickle.load(myfile).splitlines()[1]
        userinfo.place(x=5,y=17)
    except:
        Button(screen2, text="Your Cart", width=9, height=1, command= shopping_cart, bg="yellow", font="TIMES 20").place(x=windowwidth-270,y=5)
        Button(screen2, text="Your Orders", width=12, height=1, command= your_orders).place(x=5,y=37)
    myfile.close()

def your_orders():
    global screen12
    screen12=Toplevel(screen)
    screen12.title("Your Orders")
    screen12.attributes("-fullscreen", True)
    bg_photo(screen12)
    Label(screen12, text="Your Orders", bg="light green", width=700, height=1, font= "TIMES 34").pack()
    space=Label(screen12, text="", height=2)
    space.pack()
    space.lower()
    scroll_command(screen12, "yes")
    frame17=Frame(canvas)
    canvas.create_window((0,0), window= frame17, anchor="nw")
    Button(screen12, text="go back", width=15, height=2, command=screen12.destroy).place(x=5,y=5)
    CLEAR=Button(screen12, text="Clear", width=15, height=2, command=clear_history)
    CLEAR.place(x=windowwidth-117,y=5)
    framedesign= LabelFrame(frame17, width=1400, height=700, relief='ridge', bg="light green", bd=20)
    framedesign.grid(row=1,column=0)
    try:
        ROWS=("pid","pname","pprice","pseller","pquantity","ptotalamount")
        x1=0
        for i in ROWS:
            y1=1
            crs.execute("select "+i+" from "+username_info+"orders")
            rec=crs.fetchall()
            for r in rec:
                products=Label(framedesign, text=r, font="Times 25", bg="light green").grid(row=y1, column=x1, pady=11)
                y1+=1
            x1+=1
        canvasheight=(y1-1)*65
        if canvasheight>=600:
            canvasheight=600
        canvas.configure(height=128+canvasheight)
        product_headers(framedesign, "light green", "yes")
        Label(framedesign, text="AMOUNT", font="Times 28 bold", bg="light green").grid(row=0, column=5, padx=30)
    except:
        containerframe.destroy()
        Label(screen12, text="NO ORDER HISTORY AVAILBLE", fg="red", bg="light green", font= "TIMES 30").pack()
        CLEAR.config(state=DISABLED)
    
def clear_history():
    try:
        crs.execute("drop table "+username_info+"orders")
        mc.commit()
        screen12.destroy()
    except:
        pass

def product_headers(framedesign, color, amount, tax="no"):
    if amount=="yes":
        spacing=35
    else:
        spacing=45
    Label(framedesign, text="ID", font="Times 28 bold", bg= color).grid(row=0, column=0, padx=spacing, pady=20)
    Label(framedesign, text="NAME", font="Times 28 bold", bg= color).grid(row=0, column=1, padx=spacing)
    if tax=="yes":
        Label(framedesign, text="PRICE \n (Tax Included)", font="Times 27 bold", bg= color).grid(row=0, column=2, padx=spacing)
    else:
        Label(framedesign, text="PRICE", font="Times 28 bold", bg= color).grid(row=0, column=2, padx=spacing)
    Label(framedesign, text="SELLER", font="Times 28 bold", bg= color).grid(row=0, column=3, padx=spacing)
    Label(framedesign, text="QUANTITY", font="Times 28 bold", bg= color).grid(row=0, column=4, padx=spacing)

def bg_photo(screen):
    photo= PhotoImage(file = "Assets/categoryselect.gif")
    lab = Label(screen, image=photo)
    lab.image = photo
    lab.place(x=-3,y=-3)

def start_addtocart():
    global screen7,productnamesearch,pnamesearch,searchquantity
    screen7= Toplevel(screen3)
    screen7.title("ADD QUANTITY")
    screen7.attributes("-fullscreen", True)
    bg_photo(screen7)
    Label(screen7, text="ADD TO CART", bg='dark orange', width="300", height="1", font= "TIMES 34").pack()
    frame9=Frame(screen7)
    frame9.pack(pady=20)
    framedesign= LabelFrame(frame9, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    framedesign.grid(row=1,column=0)
    pnamesearch= StringVar()
    Label(framedesign, text="Product Name:", font="TIMES 25", bg="dark orange").grid(row=1, column=0, padx=15, pady=20)
    productnamesearch=Entry(framedesign, textvariable=pnamesearch, font="TIMES 25")
    productnamesearch.grid(row=1, column=1, padx=20)
    searchquantity= Button(framedesign, text="Check Availbility", height=1, width=15, command=adding_to_cart, bg="light green", font= "TIMES 20")
    searchquantity.grid(row=2, column=1, columnspan=2, pady=10)
    Button(screen7,text="cancel", height=2 , width=14, command= screen7.destroy).place(x=5, y=5)

def start_delete_product():
    global screen6,deleteID,deleteproductID,deletesearch
    screen6=Toplevel(screen)
    screen6.attributes("-fullscreen", True)
    bg_photo(screen6)
    Label(screen6, text="Delete Product from "+categoryID, bg='dark orange', width="300", height="1", font= "TIMES 33").pack()
    space=Label(screen6, text="", height=2)
    space.pack()
    space.lower()
    deleteID= StringVar()
    frame5=Frame(screen6)
    frame5.pack()
    framedesign= LabelFrame(frame5, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    framedesign.grid(row=1,column=0)
    Label(framedesign, text="Enter ID:", font="Times 25", bg= "dark orange").grid(row=1, column=0, pady=10)
    deleteproductID = Entry(framedesign, textvariable=deleteID, font="Times 25")
    deleteproductID.grid(row=1, column=1, padx=20, pady=5)
    deletesearch=Button(framedesign, text="Search", width=10, height=1, command=delete_frame, font="Times 20", bg="light green")
    deletesearch.grid(row=2, column=0, pady=10, columnspan=2)
    Button(screen6, text="cancel", width=15, height=2, command=screen6.destroy).place(x=5,y=5)

def delete_frame():
    global frame6
    frame6=Frame(screen6)
    frame6.pack(pady=20)
    framedesign= LabelFrame(frame6, width=1400, height=700, relief='ridge', bg="dark orange", bd=20)
    framedesign.grid(row=1,column=0)
    ROWS=("pid","pname","pprice","pseller","pquantity")
    try:
        x1=0
        for i in ROWS:
            crs.execute("select "+i+" from "+categoryID+" where pid='"+deleteID.get()+"' and pseller='"+username_info+"'")
            rec=crs.fetchall()
            for r in rec:
                products=Label(framedesign, text=r, font="Times 25", bg="dark orange")
                products.grid(row=1, column=x1, padx=25, pady=11)
            x1+=1
        if rec==[]:
            notavailble=Label(framedesign, text="No Such Product Entered by You in "+categoryID, fg="red", bg="dark orange", font="Times 25")
            notavailble.pack()
            notavailble.after(1200, lambda: frame6.destroy())
        else:
            deletesearch.config(state=DISABLED)
            product_headers(framedesign, "dark orange", "no")
            Label(framedesign, text="Are You sure you want to delete this product?", font="Times 30", bg="dark orange").grid(row=2, column=0, columnspan=4)
            Button(framedesign, text="YES", width=10, height=1, command=delete_product, bg="light green", font="Times 20").grid(row=3, column=0, padx=15, pady=10, columnspan=2)
            Button(framedesign, text="NO", width=10, height=1, command=re_search_delete, bg= "red", font="Times 20").grid(row=3, column=2)
    except:
        notfound=Label(framedesign, text="No Such Product Availble", fg='red', bg='dark orange')
        notfound.pack()
        notfound.after(1200, lambda: frame6.destroy())

def re_search_delete():
    frame6.destroy()
    deleteproductID.delete(0, END)
    deletesearch.config(state=NORMAL)

def refresh(screen):
    screen.destroy()
    containerframe.destroy()
    categoryframe()

def sign_out():
    username_entry.delete (0, END)
    password_entry.delete (0, END)
    signin.config(state=NORMAL)
    Exit.config(state=NORMAL)
    signup.config(state=NORMAL)
    screen2.destroy()

def categories():
    global screen3,back,DELETEbtn,addproductbtn,addquantitybtn,buybtn
    screen3=Toplevel(screen)
    screen3.attributes("-fullscreen", True)
    screen3.title(categoryID.upper())
    bg_photo(screen3)
    Label(screen3, text=categoryID.upper(), bg=categoryclr, width="300", height="1", font= "jokerman 30").pack()
    if categoryID=="groceries":
        Label(screen3, text="(Note-all the prices of fruits and vegetables are per kg)", bg='cyan').pack()
    space=Label(screen3, text="", height=2)
    space.pack()
    space.lower()
    back=Button(screen3, text = "go back", width=14, height=1, command = screen3.destroy)
    back.place(x=5,y=5)
    myfile = open("Account Info/"+username_info+".bin","rb")
    try:
        pickle.load(myfile).splitlines()[1]
        DELETEbtn=Button(screen3, text="Delete product", height=1, width=14, command= start_delete_product)
        addproductbtn=Button(screen3, text="Add Product", width=14, height=1, command = add_product)
        addquantitybtn=Button(screen3, text="Add Quantity", width=14, height=1, command = add_quantity)
        DELETEbtn.place(x=5,y=36)
        addproductbtn.place(x=windowwidth-110,y=5)
        addquantitybtn.place(x=windowwidth-110,y=36)
    except:
        buybtn=Button(screen3, text="Buy Product", width=14, height=2, command = start_addtocart)
        buybtn.place(x=windowwidth-110,y=5)
        back.config(height=2)
    myfile.close()
    categoryframe()

def scroll_command(screen, amount):
    global containerframe, canvas
    containerframe=Frame(screen)
    containerframe.pack()
    if amount=="yes":
        canvas= Canvas(containerframe, width=1260, height=300)
    else:
        canvas= Canvas(containerframe, width=1110, height=300)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    framescroll=Frame(canvas)
    yscrollbar= ttk.Scrollbar(containerframe, orient="vertical", command=canvas.yview)
    yscrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=yscrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
   
def categoryframe():
    global noproductcat
    scroll_command(screen3, "no")
    frame4=Frame(canvas)
    canvas.create_window((0,0), window= frame4, anchor="nw")
    framedesign= LabelFrame(frame4, width=1400, height=700, relief='ridge', bg=categoryclr, bd=20)
    framedesign.grid(row=0,column=0)
    ROWS=("pid","pname","pprice","pseller","pquantity")
    x1=0
    for i in ROWS:
        y1=1
        crs.execute("select "+i+" from "+categoryID)
        rec=crs.fetchall()
        for r in rec:
            products=Label(framedesign, text=r, font="Times 25", bg=categoryclr)
            products.grid(row=y1, column=x1, padx=25, pady=11)
            y1+=1
        x1+=1
    if rec==[]:
        containerframe.destroy()
        noproductcat=Label(screen3, text="No Products Available", font="Times 25", fg="red", bg=categoryclr)
        noproductcat.pack()
        if categoryclr=="red":
            noproduct.config(fg="dark red")
        try:
            DELETEbtn.config(state=DISABLED)
            addquantitybtn.config(state=DISABLED)
        except:
            buybtn.config(state=DISABLED)
    else:
        canvasheight=(y1-1)*65
        if canvasheight>=580:
            canvasheight=580
        canvas.configure(height=128+canvasheight)
        product_headers(framedesign, categoryclr, "no")
        try:
            DELETEbtn.config(state=NORMAL)
            addquantitybtn.config(state=NORMAL)
        except:
            buybtn.config(state=NORMAL)

def register():
    global usernameregister,passwordregister,screen1,confirm,password_confirm,registerusername_entry,registerpassword_entry,password_confirm,usertype
    screen1=Toplevel(screen)
    screen1.title("Register")
    screen1.attributes("-fullscreen", True)
    photo= PhotoImage(file = "Assets/mainscreen.gif")
    lab1 = Label(screen1, image=photo)
    lab1.image = photo
    lab1.place(x=-3,y=-3)
    Title=Label(screen1, text="SONIC  CART", bg='dark BLUE', fg='gold', width="300", height="1", font= "JOKERMAN 36 bold italic")
    Title.pack()
    Label(screen1, text="").pack()
    Label(screen1, text="").pack()
    lab1.lift()
    Title.lift()    
    frame = Frame(screen1, bg='#10DAB1', bd=20)
    frame.pack()
    loginframe2= LabelFrame(frame, width=1400, height=700, relief='ridge', bg='#10DAB1', bd=20)
    loginframe2.grid(row=1,column=0)
    usernameregister = StringVar()
    passwordregister = StringVar()
    confirm = StringVar()
    usertype= StringVar()
    Register=Label(loginframe2, text="REGISTER YOUR ACCOUNT", bg='#10DAB1', font= "garamond 29 bold underline", fg="purple").grid(row=0, column=0, columnspan=3, pady=20)
    username_label= Label (loginframe2, text = "Username:", font= "garamond 32 bold", bg='#10DAB1').grid(row=1, column=0, pady=15)
    registerusername_entry = Entry (loginframe2, textvariable = usernameregister, width="31", font= "garamond 21 bold")
    registerusername_entry.grid(row=1, column=1, pady=15, columnspan=2)
    passwordlabel= Label (loginframe2, text = "Password \n (atleast 8 characters):", font= "garamond 32 bold", bg='#10DAB1').grid(row=2, column=0, pady=15)
    registerpassword_entry = Entry (loginframe2, textvariable = passwordregister, show="*", width="31", font= "garamond 21 bold")
    registerpassword_entry.grid(row=2, column=1, columnspan=2)
    confirmlabel= Label (loginframe2, text = "Confirm Password:", font= "garamond 32 bold", bg='#10DAB1').grid(row=3, column=0, pady=15)
    password_confirm = Entry (loginframe2, textvariable = confirm, show="*", width="31", font= "garamond 21 bold")
    password_confirm.grid(row=3, column=1, columnspan=2, padx=15)
    usertype.set("buyer")
    acctype= Label(loginframe2, text="Account Type:", font= "garamond 32 bold", bg='#10DAB1').grid(row=4, column=0,pady=15)
    userbutton= Radiobutton(loginframe2, text="User", variable=usertype, value="buyer", font= "garamond 30 bold", bg='#10DAB1')
    userbutton.grid(row=4, column=1)
    sellerbutton= Radiobutton(loginframe2, text="Seller", variable=usertype, value="seller", font= "garamond 30 bold", bg='#10DAB1')
    sellerbutton.grid(row=4, column=2)
    Button(loginframe2, text = "REGISTER", bg="#03AC13", height=1, width=18, font= "garamond 20 bold", command = register_user).grid(row=5, column=0, padx=30)
    Button(loginframe2, text="GO BACK", bg="red", height=1, width=18, font= "garamond 20 bold", command= screen1.destroy).grid(row=5, column=1, columnspan=2, padx=30, pady=10)
    
def register_user():
    passlength=0
    username_info2 = usernameregister.get()
    filename2="Account Info/"+username_info2+".bin"
    if username_info2=="":
        user_false=Label (screen1, text="Username cannot be Left Empty", fg="red")
        user_false.pack()
        user_false.after(1200, lambda: user_false.destroy())
    else:
        try:
            myfile = open(filename2,"rb")
            user_exists=Label (screen1, text="username already exists", fg="red", bg='#10DAB1', font="garamond 25 bold")
            user_exists.pack()
            user_exists.after(1200, lambda: user_exists.destroy())
        except:
            for i in passwordregister.get():
                 passlength+=1
            if passlength==8 or passlength>8:    
                if passwordregister.get()==confirm.get():
                    myfile= open(filename2,"wb")
                    if usertype.get()=="seller":
                        pickle.dump(passwordregister.get()+"\n"+usertype.get(),myfile)
                    else:
                        pickle.dump(passwordregister.get(),myfile)
                    myfile.close()
                    registerusername_entry.delete (0, END)
                    registerpassword_entry.delete (0, END)
                    password_confirm.delete (0, END)
                    Registrationsuccess=Label (screen1, text = "Registration Sucessful", bg='#10DAB1', fg = "green", font="garamond 25 bold")
                    Registrationsuccess.pack()
                    Registrationsuccess.after(1300, lambda: Registrationsuccess.destroy())
                else:
                    Label (screen1, text="").pack()
                    match=Label (screen1, text = "password and confirm password doesn't match", bg='#10DAB1', fg = "red", font="garamond 25 bold")
                    match.pack()
                    match.after(1200, lambda: match.destroy())
            else:
                short= Label (screen1, text = "Password less than 8 digits", bg='#10DAB1', fg="red", font="garamond 25 bold")
                short.pack()
                short.after(1200, lambda: short.destroy())

def login_user():
    global username_info,continuelogin,success,passkey
    username_info = username.get()
    password_info = password.get()
    filename="Account Info/"+username_info+".bin"
    try:
        myfile = open(filename,"rb")
        passkey=pickle.load(myfile).splitlines()[0]
        myfile.close()
        if password_info==passkey:
            signin.config(state=DISABLED)
            Exit.config(state=DISABLED)
            signup.config(state=DISABLED)
            success=Label(screen, text="Signing In...", fg="green", bg='#10DAB1', font="garamond 25 bold")
            success.pack()
            success.after(1200, lambda: shopping())
            success.after(1200, lambda: success.destroy())
        else:
            incorrect_password=Label(screen, text="Incorrect Password",bg='#10DAB1', fg="red", font="garamond 25 bold")
            incorrect_password.pack()
            incorrect_password.after(1200, lambda: incorrect_password.destroy())
    except:
        invalid_username=Label(screen, text="Invalid Username", bg='#10DAB1', fg='red', font="garamond 25 bold")
        invalid_username.pack()
        invalid_username.after(1200, lambda: invalid_username.destroy())

def login_screen():
    global Login,username,password,password_entry,username_entry,signin,signup,Exit
    progress.destroy()
    username=StringVar()
    password=StringVar()
    photo= PhotoImage(file = "Assets/mainscreen.gif")
    lab1 = Label(screen, image=photo)
    lab1.image = photo
    lab1.place(x=-3,y=-3)
    frame = Frame(screen, bg='#10DAB1')
    Title.lift()
    frame.pack()
    loginframe= LabelFrame(frame, width=1400, height=700, relief='ridge', bg='#10DAB1', bd=20)
    loginframe.grid(row=1,column=0)
    enterdetails = Label (loginframe, text = "LOGIN", fg="yellow", bg='#10DAB1', font= "garamond 29 bold underline").grid(row=0, column=0, columnspan=3, pady=20)
    usernamedetail = Label (loginframe, text = "Username:", font= "garamond 32 bold", bg='#10DAB1').grid(row=1, column=0, pady=15)
    username_entry = Entry (loginframe, textvariable = username, width="31", font= "garamond 21 bold")
    username_entry.grid(row=1, column=1, pady=15, columnspan=2)
    passworddetail = Label (loginframe, text = "Password:", font= "garamond 32 bold", bg='#10DAB1').grid(row=2, column=0)
    password_entry = Entry (loginframe, textvariable = password, show="*", width="31", font= "garamond 21 bold")
    password_entry.grid(row=2, column=1, columnspan=2)
    signin=Button(loginframe, text = "SIGN IN", bg="#03AC13", width = 12, height = 1, command = login_user, font= "garamond 20 bold")
    signin.grid(row=3, column=0, pady=15, padx=10)
    signup=Button(loginframe, text="SIGN UP", bg="#188CCD", height=1, width=12, command=register, font= "garamond 20 bold")
    signup.grid(row=3, column=1, pady=15, padx=10)
    Exit=Button(loginframe, text="EXIT", bg="red", height=1, width=12, command= screen.destroy, font= "garamond 20 bold")
    Exit.grid(row=3, column=2, pady=15, padx=10)

def start_up():
    global screen,Title,windowheight,windowwidth,progress
    screen=Tk()
    screen.attributes("-fullscreen", True)
    screen.title("Main Screen")
    Title=Label(screen, text="SONIC  CART", bg='dark BLUE', fg='gold', width="300", height="1", font= "JOKERMAN 36 bold italic")
    Title.pack()
    windowheight=screen.winfo_screenheight()
    windowwidth=screen.winfo_screenwidth()
    Label(screen,text="", height=2).pack()
    photo= PhotoImage(file = "Assets/loadscreen.gif")
    lab1 = Label(screen, image=photo)
    lab1.image = photo
    lab1.place(x=-2,y=-3)
    progress= ttk.Progressbar(screen, orient=HORIZONTAL, length= 500, mode= 'determinate', maximum=100)
    progress.pack(side= BOTTOM, pady=70)
    progress.start(40)
    lab1.after(4000, lambda: login_screen())
    screen.mainloop()
    
start_up()
