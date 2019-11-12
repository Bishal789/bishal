from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import mysql.connector as mc
from tkinter import messagebox as mb


try:
    connector = mc.connect(user='root', passwd='admin', host='localhost', database='Softwarica')
    db_cursor = connector.cursor()



except mc.Error:
    mb.showerror("Error!", "Couldn't connect to database.")



# -------------Function-----------


def add():
    try:
        data_id = entryid.get()
        data_fname = entryfname.get().title()
        data_lname = entrylname.get().title()
        data_address = entryaddress.get().title()
        data_age = entryage.get()
        data_gender = entrygender.get().title()
        data_contact = entrycontact.get()

        query = 'Insert into table_go values(%s, %s, %s, %s, %s, %s,%s)'

        values = (data_id,data_fname,data_lname,data_age,data_gender,data_contact,data_address)
        db_cursor.execute(query, values)
        connector.commit()
        mb.showinfo('Complete',"Data inserted successfully.")
        connector.commit()
        clear()
        show()

    except ValueError:
        mb.showerror('Error!',"Please fill the data properly.")
    except mc.errors.DatabaseError:
        mb.showwarning('Warning!',"ID Already Taken!")



def clear():
    entryid.delete(0,'end')
    entryfname.delete(0, 'end')
    entrylname.delete(0, 'end')
    entryage.delete(0, 'end')
    entrygender.delete(0,'end')
    entryaddress.delete(0,'end')
    entrycontact.delete(0, 'end')


def delete():
    if callback():
        answer = mb.askyesno("Confirm ?", "Do you want to delete?")
        if answer:
            query = 'delete from table_go where id=%s'
            values = (callback(),)
            db_cursor.execute(query, values)

            connector.commit()
            show()

    else:
        mb.showerror('Error!',"Please select your data.")


def callback():
    item_id = treeview.selection()
    candidate_name = []
    for i in item_id:
        candidate_name.append(treeview.item(i)['values'])
    for i in candidate_name:
        return i[0]


def show():

    records = treeview.get_children()

    for element in records:
        treeview.delete(element)

    query = 'select * from table_go'
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    for row in results:
        treeview.insert('', 'end', values=row)


def update():
    try:

        upd_id = entryid.get()
        upd_fname = entryfname.get()
        upd_lname = entrylname.get()
        upd_age = entryage.get()
        upd_gender = entrygender.get()
        upd_contact = entrycontact.get()
        upd_address = entryaddress.get()
        query = 'Update table_go set fname=%s,lname=%s, age=%s, gender=%s ,contact=%s, address=%s where id=%s'
        values = ( upd_fname, upd_lname, int(upd_age), upd_gender, upd_contact, upd_address, int(upd_id))
        db_cursor.execute(query, values)
        connector.commit()
        show()
        clear()
        mb.showinfo('Updated', 'Data updated successfully')
        return
    except mc.DatabaseError:
        mb.showerror('Error!', 'Check Connection')
    except ValueError:
        mb.showerror('Error', 'Update Unsuccesful')
        return


def pointer(event):
    try:
        point= treeview.focus()
        content= treeview.item(point)
        row= content['values']
        clear()
        entryid.insert(0, row[0])
        entryfname.insert(0, row[1])
        entrylname.insert(0, row[2])
        entryage.insert(0, row[3])
        entrygender.insert(0, row[4])
        entrycontact.insert(0, row[5])
        entryaddress.insert(0, row[6])
        # entryid.config(state='disabled')

    except IndexError:
        pass


def search():
    query="select * from table_go"
    db_cursor.execute(query)
    output_fetch=db_cursor.fetchall()

    entry_get=entrybox_search.get().title()
    combo_get=scrh.get()

    if combo_get == 'ID':
        go_column=0
        entry_get=int(entrybox_search.get())
    elif combo_get == "First Name":
        go_column=1
    elif combo_get == "Last Name":
        go_column =2
    elif combo_get == "Age":
        go_column = 3
        entry_get=int(entrybox_search.get())
    elif combo_get == "Gender":
        go_column = 4
    elif combo_get == "Contact":
        go_column = 5
        entry_get=int(entrybox_search.get())
    elif combo_get == "Address":
        go_column = 6
    else:
        mb.showwarning("Warning!","Data Not Found !")
        return

    list=[]
    for i in output_fetch:

        if entry_get == i[go_column]:
            list.append(i)

        if len(list) != 0:
            treeview.delete(*treeview.get_children())


        for i in list:
            treeview.insert("",'end', values=i)
            connector.commit()

    if not list:
        mb.showwarning("info","No data")


# def bubble_sort():
#     thelist = 'select * from table_go '
#     db_cursor.execute(thelist)
#     result = db_cursor.fetchall()
#     for i in range(0,len(result)-1):
#         for j in range(0,len(result)-1-i):
#             if result[j]>result[j+1]:
#                 result[j],result[j+1]=result[j+1],result[j]
#                 if len(result) != 0:
#                     treeview.delete(*treeview.get_children())
#                     for row in result:
#                         treeview.insert('', END, values=row)
#                         connector.commit()
#     return result
def sort(list,low,high):
    ent_sort=srt.get()

    if ent_sort=="ID":
        show_column=0
    elif ent_sort=="First Name":
        show_column=1
    elif ent_sort=="Last Name":
        show_column=2
    elif ent_sort=="Age":
        show_column=3
    elif ent_sort=="Gender":
        show_column=4
    elif ent_sort=="Address":
         show_column=5
    else:
        pass

    num_sort=low-1
    pivot=list[high][show_column]

    for var in range(low,high):
        if list[var][show_column] <= pivot:
            num_sort=num_sort+1
            list[num_sort],list[var]=list[var],list[num_sort]

    list[num_sort + 1], list[high] = list[high], list[num_sort + 1]
    return (num_sort + 1)

def quick_sort(list, low, high):

    if low < high:
        part=sort(list,low,high)
        quick_sort(list,low, part-1)
        quick_sort(list, part+1, high)


def final_sort():
    ent_sort=srt.get()

    if ent_sort:
        querys="select * from table_go"
        db_cursor.execute(querys)
        output_list = db_cursor.fetchall()

        quick_sort(output_list, 0, (len(output_list)-1))

        treeview.delete(*treeview.get_children())
        for value in output_list:
            treeview.insert("", 'end', values=value)
            connector.commit()
    else:
        mb.showerror("info","No value selected.")
#FOR COMBOBOX


gen = ['Male','Female',]
searchby = ['ID','First Name','Last Name','Age','Gender','Contact','Address']
sortby = ['ID','First Name','Last Name','Age','Gender','Address']




root = Tk()
root.title("Entry Form")
root.geometry('1350x425')
root.configure()
labl = Label(root,text='Data Entry Form',font='Timesroman 32',fg='red',bg="Orange")
labl.place(x=900,y=51,width=450)






#Frame

firstframe = LabelFrame(root,bg='skyblue',)
firstframe.configure()
firstframe.place(x=3,y=51,anchor=NW)

secondframe = LabelFrame(root,bg='skyblue')
secondframe.configure()
secondframe.place(x=363,y=51,anchor=NW)

thirdframe = LabelFrame(root,bg='skyblue')
thirdframe.configure()
thirdframe.place(x=363,y=106,anchor=NW,)



#label

id = Label(firstframe,text='ID',font='Timesroman 10',bg='skyblue')
id.grid(row=0,column=0)
fname = Label(firstframe,text='First Name',font='Timesroman 10',bg='skyblue')
fname.grid(row=1,column=0)
lname = Label(firstframe,text='Last Name',font='Timesroman 10',bg='skyblue')
lname.grid(row=2,column=0)
age = Label(firstframe,text='Age',font='Timesroman 10',bg='skyblue')
age.grid(row=3,column=0)
gender = Label(firstframe,text='Gender',font='Timesroman 10',bg='skyblue')
gender.grid(row=4,column=0)
contact = Label(firstframe,text='Contact',font='Timesroman 10',bg='skyblue')
contact.grid(row=5,column=0)
address = Label(firstframe,text='Address',font='Timesroman 10',bg='skyblue')
address.grid(row=6,column=0)


#---------Entry box and Radio Button---------

entryid = Entry(firstframe,width='28',font='Arial 12')
entryid.grid(row=0,column=1,padx=15,pady=15)
entryfname = Entry(firstframe,width='28',font='Arial 12')
entryfname.grid(row=1,column=1,padx=15,pady=15)
entrylname = Entry(firstframe,width='28',font='Arial 12')
entrylname.grid(row=2,column=1,padx=15,pady=15)
entryage = Entry(firstframe,width='28',font='Arial 12')
entryage.grid(row=3,column=1,padx=15,pady=15)
entrygender=Combobox(firstframe,value=gen,width=40)
entrygender.grid(row=4,column=1,padx=15,pady=15)
entrycontact = Entry(firstframe,width='28',font='Arial 12')
entrycontact.grid(row=5,column=1,padx=15,pady=15)
entryaddress = Entry(firstframe,width='28',font='Arial 12')
entryaddress.grid(row=6,column=1,padx=15,pady=15)


#-----------Treeview---------

treeview = ttk.Treeview(thirdframe)
treeview.grid()
treeview['columns'] = ('id', 'fname', 'lname', 'age','gender','contact','address')

treeview.column('id', width=80)
treeview.column('fname', width=150)
treeview.column('lname', width=150)
treeview.column('age', width=150)
treeview.column('gender',width=150)
treeview.column('contact',width=150)
treeview.column('address', width=150)
treeview['show'] = 'headings'

treeview.heading('id', text='ID', anchor=W)
treeview.heading('fname', text='First Name', anchor=W)
treeview.heading('lname', text='Last Name', anchor=W)
treeview.heading('age', text='Age', anchor=W)
treeview.heading('gender',text='Gender',anchor=W)
treeview.heading('contact',text='Contact',anchor=W)
treeview.heading('address', text='Address', anchor=W)
treeview.bind('<ButtonRelease-1>', pointer)
show()

#------Button---------#

btnadd = ttk.Button(secondframe,text= 'ADD',command=add)
btnadd.grid(row=1,column=0,padx=15,pady=15)
btndel = ttk.Button(secondframe,text= 'DELETE',command=delete)
btndel.grid(row=1,column=1,padx=15,pady=15)
btnshow = ttk.Button(secondframe,text= 'SHOW DATA',command=show)
btnshow.grid(row=1,column=2,padx=15,pady=15)
btnupdt = ttk.Button(secondframe,text= 'UPDATE',command=update)
btnupdt.grid(row=1,column=3,padx=15,pady=15)
btnclear = ttk.Button(secondframe,text= 'CLEAR',command=clear)
btnclear.grid(row=1,column=4,padx=15,pady=15)




#----------Searchbtn--------
lblsearchby=Label(thirdframe,text='Search By ',font='Timesroman 12 ',bg='skyblue')
lblsearchby.grid(padx=15,pady=16)
llbsearch=Label(thirdframe,text='Search',font='Timesroman 12',bg='skyblue')
llbsearch.grid(row=13,column=0)
scrh = Combobox(thirdframe,value=searchby,width=40)
scrh.place(x=100,y=245)
entrybox_search = Entry(thirdframe,width='29',font='Arial 12 ',)
entrybox_search.place(x=100,y=280)
btnsearch = ttk.Button(thirdframe,text= 'Search', command=search)
btnsearch.place(x=1,y=244,width=80,height=59)


#---------SortBtn---------
btnsort = ttk.Button(thirdframe,text='Sort',command=final_sort)
btnsort.place(x=580,y=245,width=80,height=59)
srt=Combobox(thirdframe,value=sortby,width = 40)
srt.place(x=700,y=260, )





mainloop()