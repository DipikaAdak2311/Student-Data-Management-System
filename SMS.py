from tkinter import *
from sqlite3 import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import requests
import bs4

def open_add():
	add_st.deiconify()
	root.withdraw()

def close_add():
	root.deiconify()
	add_st.withdraw()

def open_updt():
	updt_st.deiconify()
	root.withdraw()

def close_updt():
	root.deiconify()
	updt_st.withdraw()

def open_dlt():
	dlt_st.deiconify()
	root.withdraw()

def close_dlt():
	root.deiconify()
	dlt_st.withdraw()

def open_chrt():
	st_chrt.deiconify()
	root.withdraw()
	chrt_ent_sub.current(0)

def close_chrt():
	root.deiconify()
	st_chrt.withdraw()

def open_view():
	view_st.deiconify()
	root.withdraw()
	view_ent_sub.current(0)
	con = None
	try:
		con = connect("SMS.db")
		cursor = con.cursor()
		view_scroll.configure(state=NORMAL)
		view_scroll.delete(1.0,END)
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = "rno:"+str(d[0])+", name:"+str(d[1])+", marks:"+str(d[2])+", subj:"+str(d[3])+"\n"
			view_scroll.insert(INSERT,info)
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
	finally:
		view_scroll.configure(state=DISABLED)
		if con is not None:
			con.close()

def close_view():
	root.deiconify()
	view_st.withdraw()

def add_data():
	con = None
	roll = add_ent_roll.get()
	name = add_ent_nm.get()
	marks = add_ent_mrks.get()
	#outof = add_ent_outof.get()
	#score = marks + "/" + outof
	sub = add_ent_sub.get()
	if roll=="" or name=="" or marks=="" or sub=="":
                showerror("ERROR","Fields should not be empty.")
	elif roll.isdigit()==False:
		showerror("ERROR","Roll no. should contain only positive integers")
	elif name.isalpha()==False:
		showerror("ERROR","Name should contain only alphabets.")
	elif len(name)<2:
		showerror("ERROR","Name should contain atleast 2 characters.")
	elif marks.isdigit()==False:
		showerror("ERROR","Marks should contain only positive integers.")
	elif int(marks)<0 or int(marks)>100:
		showerror("ERROR","Marks should be in range of 0 and 100.")
	else:
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql1 = "select * from student where rollno='%d'"
			cursor.execute(sql1 % (int(roll)))
			data = cursor.fetchall()
			if len(data)>0:
				showerror("INVALID","Roll no. already exist")
			else:
				sql = "insert into student values('%d','%s','%d','%s')"
				cursor.execute(sql % (int(roll),name,int(marks),sub))
				con.commit()
				showinfo("Added", "Student details added successfully")
		except Exception as e:
			con.rollback()
			showerror("Issue",e)
		finally:
			if con is not None:
				con.close()
	add_ent_roll.delete(0,END)
	add_ent_nm.delete(0,END)
	add_ent_mrks.delete(0,END)
	add_ent_sub.delete(0,END)

def updt_data():
	con = None
	roll = updt_ent_roll.get()
	name = updt_ent_nm.get()
	marks = updt_ent_mrks.get()
	sub = updt_ent_sub.get()
	if roll=="" or name=="" or marks=="" or sub=="":
                showerror("ERROR","Fields should not be empty.")
	elif roll.isdigit()==False:
		showerror("ERROR","Roll no. should contain only positive integers")
	elif name.isalpha()==False:
		showerror("ERROR","Name should contain only alphabets.")
	elif len(name)<2:
		showerror("ERROR","Name should contain atleast 2 characters.")
	elif marks.isdigit()==False:
		showerror("ERROR","Marks should contain only positive integers.")
	elif int(marks)<0 or int(marks)>100:
		showerror("ERROR","Marks should be in range of 0 and 100.")
	else:
		try:
			con = connect("SMS.db")
			cursor = con.cursor()
			sql1 = "select * from student where rollno='%d'"
			cursor.execute(sql1 % (int(roll)))
			data = cursor.fetchall()
			if len(data)<1:
				showerror("INVALID","Roll no. "+roll+" doesn't exist")
			else:
				sql = "update student set name='%s', marks='%d', sub='%s' where rollno='%d'"
				cursor.execute(sql % (name,int(marks),sub,int(roll)))
				con.commit()
				showinfo("Updated", "Student details updated successfully")
		except Exception as e:
			con.rollback()
			showerror("Issue",e)
		finally:
			if con is not None:
				con.close()
	updt_ent_roll.delete(0,END)
	updt_ent_nm.delete(0,END)
	updt_ent_mrks.delete(0,END)
	updt_ent_sub.delete(0,END)

def chck_data():
	con = None
	roll = dlt_ent_roll.get()
	if roll=="":
                showerror("ERROR","Fields should not be empty.")
	elif roll.isdigit()==False:
		showerror("ERROR","Roll no. should contain only positive integers")
	else:
		try:
			con = connect("SMS.db")
			cursor = con.cursor() 
			sql1 = "select * from student where rollno='%d'"
			cursor.execute(sql1 % (int(roll)))
			data = cursor.fetchall()
			if len(data)<1:
				showerror("INVALID","Roll no. "+str(roll)+" doesn't exist")
				sname.set(" ")
				smarks.set(" ")
				ssub.set(" ")
			else:
				sql = "select name, marks, sub from student where rollno='%d'"
				cursor.execute(sql % (int(roll)))
				data = cursor.fetchall()
				for d in data:
					name=str(d[0])
					marks=str(d[1])
					sub=str(d[2])
				sname.set(name)
				smarks.set(marks)
				ssub.set(sub)
		except Exception as e:
			con.rollback()
			showerror("Issue",e)
		finally:
			if con is not None:
				con.close()

def dlt_data():
	con = None
	roll = dlt_ent_roll.get()
	if roll=="":
                showerror("ERROR","Fields should not be empty.")
	elif roll.isdigit()==False:
		showerror("ERROR","Roll no. should contain only positive integers")
	else:
		try:
			con = connect("SMS.db")
			cursor = con.cursor() 
			sql1 = "select * from student where rollno='%d'"
			cursor.execute(sql1 % (int(roll)))
			data = cursor.fetchall()
			if len(data)<1:
				showerror("INVALID","Roll no. "+str(roll)+" doesn't exist")
			else:
				sql = "delete from student where rollno='%d'"
				cursor.execute(sql % (int(roll)))
				con.commit()
				showinfo("Deleted","Data deleted successfully")
		except Exception as e:
			con.rollback()
			showerror("Issue",e)
		finally:
			if con is not None:
				con.close()
	dlt_ent_roll.delete(0,END)
	sname.set(" ")
	smarks.set(" ")
	ssub.set(" ")

def view_chrt():
	con = None
	subj = chrt_ent_sub.get()
	lname = []
	lmrks = []
	try:
		con = connect("SMS.db")
		cursor = con.cursor() 
		sql = "select name from student where sub='%s'"
		cursor.execute(sql % (subj))
		sname = cursor.fetchall()
		for i in sname:
			lname.append(i[0])
		sql1 = "select marks from student where sub='%s'"
		cursor.execute(sql1 % (subj))
		smarks = cursor.fetchall()
		for j in smarks:
			lmrks.append(j[0])
		colors = ["red","green","orange","purple","gold","blue","yellow","violet","pink"]
		plt.bar(lname, lmrks, color=colors)
		plt.title("Student's Performance in "+subj)
		plt.xlabel("STUDENT")
		plt.ylabel("MARKS")
		plt.show()
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
	finally:
		if con is not None:
			con.close()

def on_select(event):
	subj = event.widget.get()
	info=" "
	con = None
	try:
		con = connect("SMS.db")
		cursor = con.cursor()
		view_scroll.configure(state=NORMAL)
		view_scroll.delete(1.0,END)
		if subj=="ALL":
			sql = "select * from student"
			cursor.execute(sql)
			data = cursor.fetchall()
			for d in data:
				info = "rno:"+str(d[0])+", name:"+str(d[1])+", marks:"+str(d[2])+", subj:"+str(d[3])+"\n"
				view_scroll.insert(INSERT,info)
		else:
			sql = "select rollno, name, marks from student where sub='%s'"
			cursor.execute(sql % (subj))
			data = cursor.fetchall()
			for d in data:
				info = "rno:"+str(d[0])+", name:"+str(d[1])+", marks:"+str(d[2])+"\n"
				view_scroll.insert(INSERT,info)
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
	finally:
		view_scroll.configure(state=DISABLED)
		if con is not None:
			con.close()

def QOTD():
	try:
		weblink = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(weblink)
		#print(res)

		data = bs4.BeautifulSoup(res.text, "html.parser")
		#print(data)

		info = data.find("img",{"class":"p-qotd"})
		#print(info)

		qoute = info['alt']
		qotd_id.insert(INSERT, qoute)
	except Exception as e:
		print("Issue",e)

def locatn():
	try:
		# weblink = "https://ipgeolocation.io/"
		#weblink = "https://db-ip.com/"
		#weblink = "https://www.ip2location.com/"

		weblink = "https://ipinfo.io/"
		res = requests.get(weblink)
		#print(res)
		
		data = res.json()
		#data = bs4.BeautifulSoup(res.text, "html.parser")
		#print(data)
		
		city = data['city']
		state = data['region']
		C.itemconfig(location_id, text=city+", "+state[0:4])
		
		#info = data.find("div",{"class":"col-md-4"})
		#print(info)
	except Exception as e:
		print("Issue",e)

def temp():
	try:
		w1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
		w2 = "&q=" + "navi mumbai"
		w3= "&appid=" + "b4b64e214d358cdf316ebd6e61aea66c"
		weblink = w1 + w2 + w3
		res = requests.get(weblink)
		#print(res)
		data = res.json()
		#print(data)
		temp = data['main']['temp']
		C.itemconfig(temp_id, text=str(temp)+"\u00B0"+"C")
	except Exception as e:
		print("Issue",e)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ root ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk()
root.title("S.M.S")
root.geometry("550x550+400+80")

bg = PhotoImage(file="root_bg.png")
add = PhotoImage(file="add.png")
view = PhotoImage(file="view.png")
updt = PhotoImage(file="update.png")
dlt = PhotoImage(file="delete.png")
chrt = PhotoImage(file="charts.png")

C= Canvas(root, width=550, height=550, bg="powder blue")
C.create_image(275, 275, image=bg)
C.create_text(275, 50, text="STUDENT MANAGEMENT SYSTEM", font=("Calibri",17,"bold"))
C.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

C.create_image(90, 116, image=add)
add_btn = Button(root, text="ADD", font=("Arial",14,"bold"), width=12, command=open_add)
add_btn.place(x=125, y=100)

C.create_image(285, 180, image=view)
view_btn = Button(root, text="VIEW", font=("Arial",14,"bold"), width=12, command=open_view)
view_btn.place(x=320, y=165)

C.create_image(90, 248, image=updt)
updt_btn = Button(root, text="UPDATE", font=("Arial",14,"bold"), width=12, command=open_updt)
updt_btn.place(x=125, y=230)

C.create_image(285, 312, image=dlt)
dlt_btn = Button(root, text="DELETE", font=("Arial",14,"bold"), width=12, command=open_dlt)
dlt_btn.place(x=320, y=295)

C.create_image(90, 376, image=chrt)
chrts_btn = Button(root, text="CHARTS", font=("Arial",14,"bold"), width=12, command=open_chrt)
chrts_btn.place(x=125, y=360)

C.create_text(275, 410, text="________________________________________", font=("Calibri",17,"bold"))

C.create_text(90, 445, text="Location : ", font=("Calibri",16,"bold"))
location_id = C.create_text(140, 445, font=("Calibri",14,"italic"), anchor="w")

C.create_text(350, 445, text="Temp : ", font=("Calibri",16,"bold"))
temp_id = C.create_text(385, 445, font=("Calibri",14,"italic"), anchor="w")

C.create_text(100, 479, text="QOTD : ", font=("Calibri",16,"bold"))
qotd_id = Text(root, height=3, width=35, font=("Calibri",14,"italic"), bd=0,wrap=WORD,background="#d1f6ff")
qotd_id.place(x=135,y=466)

QOTD()
locatn()
temp()
C.pack()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Add_page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

add_st=Toplevel(root)
add_st.title("Add_Student")
add_st.geometry("550x550+400+80")
#a0e6fa
C1= Canvas(add_st, width=550, height=550,bg="#bfe6ff")
#C1.create_image(275, 275, image=bg)
C1.create_text(275, 50, text="ADD STUDENT", font=("Calibri",17,"bold"))
C1.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

options = ["PYTHON","JAVA","C++","RUBY"]

add_lbl_roll = Label(add_st, text="Enter Roll no.:", font=("Arial",15,"normal"), background="#bfe6ff")
add_lbl_roll.place(x=210, y=100)
add_ent_roll = Entry(add_st, font=("Arial",15,"normal"),justify='center',width=35)
add_ent_roll.place(x=80, y=130)

add_lbl_nm = Label(add_st, text="Enter Name :", font=("Arial",15,"normal"), background="#bfe6ff")
add_lbl_nm.place(x=212, y=175)
add_ent_nm = Entry(add_st, font=("Arial",15,"normal"),justify='center',width=35)
add_ent_nm.place(x=80, y=205)

add_lbl_sub = Label(add_st, text="Select subject:", font=("Arial",15,"normal"), background="#bfe6ff")
add_lbl_sub.place(x=205, y=250)
add_ent_sub = ttk.Combobox(add_st, font=("Arial",15,"normal"),justify='center',width=34, values=options, state='readonly')
add_ent_sub.place(x=80, y=280)

add_lbl_mrks = Label(add_st, text="Enter marks(outof 100)", font=("Arial",15,"normal"), background="#bfe6ff")
add_lbl_mrks.place(x=170, y=325)
add_ent_mrks = Entry(add_st, font=("Arial",15,"normal"),justify='center',width=35)
add_ent_mrks.place(x=80, y=355)

C1.create_text(275, 415, text="________________________________________", font=("Calibri",17,"bold"))
add_st_btn = Button(add_st, text="ADD", font=("Arial",14,"bold"), width=10, command=add_data)
add_st_btn.place(x=80,y=450)
bck_st_btn = Button(add_st, text="BACK", font=("Arial",14,"bold"), width=10, command=close_add)
bck_st_btn.place(x=320,y=450)

C1.pack()
add_st.withdraw()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Update_page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

updt_st=Toplevel(root)
updt_st.title("Update_Student")
updt_st.geometry("550x550+400+80")
#a4fce5
#b9fae9
C2= Canvas(updt_st, width=550, height=550,bg="#b9fae9")
#C1.create_image(275, 275, image=bg)
C2.create_text(275, 50, text="UPDATE STUDENT DETAILS", font=("Calibri",17,"bold"))
C2.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

updt_lbl_roll = Label(updt_st, text="Enter Roll no.:", font=("Arial",15,"normal"), background="#b9fae9")
updt_lbl_roll.place(x=210, y=100)
updt_ent_roll = Entry(updt_st, font=("Arial",15,"normal"),justify='center',width=35)
updt_ent_roll.place(x=80, y=130)

updt_lbl_nm = Label(updt_st, text="Enter Name :", font=("Arial",15,"normal"), background="#b9fae9")
updt_lbl_nm.place(x=212, y=175)
updt_ent_nm = Entry(updt_st, font=("Arial",15,"normal"),justify='center', width=35)
updt_ent_nm.place(x=80, y=205)

updt_lbl_sub = Label(updt_st, text="Select subject:", font=("Arial",15,"normal"), background="#b9fae9")
updt_lbl_sub.place(x=205, y=250)
updt_ent_sub = ttk.Combobox(updt_st, font=("Arial",15,"normal"),justify='center',width=34, values=options, state='readonly')
updt_ent_sub.place(x=80, y=280)

updt_lbl_mrks = Label(updt_st, text="Enter marks(outof 100)", font=("Arial",15,"normal"), background="#b9fae9")
updt_lbl_mrks.place(x=170, y=325)
updt_ent_mrks = Entry(updt_st, font=("Arial",15,"normal"),justify='center',width=35)
updt_ent_mrks.place(x=80, y=355)

C2.create_text(275, 415, text="________________________________________", font=("Calibri",17,"bold"))
updt_st_btn = Button(updt_st, text="UPDATE", font=("Arial",14,"bold"), width=10, command=updt_data)
updt_st_btn.place(x=80,y=450)
bck_st_btn = Button(updt_st, text="BACK", font=("Arial",14,"bold"), width=10, command=close_updt)
bck_st_btn.place(x=320,y=450)

C2.pack()
updt_st.withdraw()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Delete_page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

dlt_st=Toplevel(root)
dlt_st.title("Delete_Student")
dlt_st.geometry("550x550+400+80")

sname = StringVar()
smarks = StringVar()
ssub = StringVar()

C3= Canvas(dlt_st, width=550, height=550,bg="#efc2ff")
#C1.create_image(275, 275, image=bg)
C3.create_text(275, 50, text="DELETE STUDENT DETAILS", font=("Calibri",17,"bold"))
C3.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

dlt_lbl_roll = Label(dlt_st, text="Enter Student roll no.:", font=("Arial",15,"normal"), background="#efc2ff")
dlt_lbl_roll.place(x=70, y=100)
dlt_ent_roll = Entry(dlt_st, font=("Arial",15,"normal"),width=26,borderwidth=2)
dlt_ent_roll.place(x=70, y=130)

dlt_chck_btn = Button(dlt_st, text="check", font=("Arial",10,"bold"),background="white",width=10,command=chck_data)
dlt_chck_btn.place(x=390, y=130)

C3.create_text(275, 200, text="~ STUDENT DETAILS ~", font=("Calibri",16,"bold"))
#C3.create_text(275, 202, text="_____________________", font=("Calibri",16,"bold"), fill="#d37aff")

dlt_lbl_nm = Label(dlt_st, text="Name :", font=("Arial",15,"normal"), background="#efc2ff")
dlt_lbl_nm.place(x=70, y=230)
dlt_ent_nm = Label(dlt_st, textvariable=sname, font=("Arial",15,"normal"),width=26, background="white", borderwidth=1 ,relief="sunken")
dlt_ent_nm.place(x=180, y=230)

dlt_lbl_sub = Label(dlt_st, text="Subject:", font=("Arial",15,"normal"), background="#efc2ff")
dlt_lbl_sub.place(x=70, y=275)
dlt_ent_sub = Label(dlt_st, textvariable=ssub, font=("Arial",15,"normal"),width=26, background="white", borderwidth=1 ,relief="sunken",height=2)
dlt_ent_sub.place(x=180, y=275)

dlt_lbl_entr = Label(dlt_st, text="Marks:", font=("Arial",15,"normal"), background="#efc2ff")
dlt_lbl_entr.place(x=70, y=340)
dlt_lbl_mrks = Label(dlt_st, textvariable=smarks, font=("Arial",15,"normal"),width=26, background="white", borderwidth=1 ,relief="sunken")
dlt_lbl_mrks.place(x=180, y=340)

C3.create_text(275, 415, text="________________________________________", font=("Calibri",17,"bold"))
dlt_st_btn = Button(dlt_st, text="DELETE", font=("Arial",14,"bold"), width=10, command=dlt_data)
dlt_st_btn.place(x=80,y=450)
bck_st_btn = Button(dlt_st, text="BACK", font=("Arial",14,"bold"), width=10, command=close_dlt)
bck_st_btn.place(x=320,y=450)

C3.pack()
dlt_st.withdraw()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Chart_page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

st_chrt =Toplevel(root)
st_chrt.title("Charts")
st_chrt.geometry("550x550+400+80")

C4= Canvas(st_chrt, width=550, height=550,bg="#c7ffd4")
#C1.create_image(275, 275, image=bg)
C4.create_text(275, 50, text="STUDENT CHART", font=("Calibri",17,"bold"))
C4.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

chrt_lbl_sub = Label(st_chrt, text="Select Subject:", font=("Arial",15,"normal"), background="#c7ffd4")
chrt_lbl_sub.place(x=205, y=100)
chrt_ent_sub = ttk.Combobox(st_chrt, font=("Arial",15,"normal"),justify='center',width=33, values=options, state='readonly')
chrt_ent_sub.place(x=80, y=135)

chck_chrt_btn = Button(st_chrt, text="VIEW CHART", font=("Arial",13,"bold"),width=18,background="white",command=view_chrt)
chck_chrt_btn.place(x=180, y=200)
chrt_bck_btn = Button(st_chrt, text="BACK", font=("Arial",13,"bold"),width=13,command=close_chrt)
chrt_bck_btn.place(x=205, y=260)

C4.pack()
st_chrt.withdraw()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ View_page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

view_st =Toplevel(root)
view_st.title("Charts")
view_st.geometry("550x550+400+80")

choices = ["ALL","PYTHON","JAVA","C++","RUBY"]

C5= Canvas(view_st, width=550, height=550,bg="#bfcfff")
C5.create_text(275, 50, text="VIEW STUDENT DETAILS", font=("Calibri",17,"bold"))
C5.create_text(275, 65, text="________________________________________", font=("Calibri",17,"bold"))

view_lbl_sub = Label(view_st, text="Select Subject:", font=("Arial",15,"normal"), background="#bfcfff")
view_lbl_sub.place(x=70, y=100)

view_ent_sub = ttk.Combobox(view_st,font=("Arial",15,"normal"),justify='center',width=35, values=choices, state='readonly')
view_ent_sub.place(x=70, y=130)
view_ent_sub.bind('<<ComboboxSelected>>', on_select)

view_scroll = ScrolledText(view_st,width=35,height=11,font=("Arial",15,"normal"),wrap=WORD,state=NORMAL)
view_scroll.place(x=70, y=180)

view_bck_btn = Button(view_st, text="BACK", font=("Arial",13,"bold"),width=10,command=close_view)
view_bck_btn.place(x=215, y=470)

C5.pack()
view_st.withdraw()

root.mainloop()
