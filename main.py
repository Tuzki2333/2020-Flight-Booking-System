import sys
import log_in
import user_operation, log_in_error,sign_up,username_error,password_error
import booking,personal_info,email_update,tel_update,password_update,passenger,passenger_add,orders,flight_info
import admin_operation,flight_admin, flight_add,flight_edit,flight_delete,orders_management,user_management,user_delete
import visitor_operation
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog,QMessageBox
import pymysql
from PyQt5.QtCore import QStringListModel
import datetime;



def check(user,password):#根据用户名密码修改登录键的返回结果
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur=con.cursor()
    cur.execute("select UID,UPassword from User where UID='"+user+"' and UPassword='"+password+"'")
    if(cur.rowcount!=0):
        login_window.btn_login.clicked.connect(MainWindow_user.show)
        login_window.btn_login.clicked.connect(Dialog_login_error.close)
    else:
        login_window.btn_login.clicked.connect(Dialog_login_error.show)
        login_window.btn_login.clicked.connect(MainWindow_user.close)
    cur.close()
    login_window.btn_login.clicked.connect(lambda:user_window.statusbar.showMessage(login_window.user.text()))
def check_admin(user,password):#根据用户名密码修改管理员登录键的返回结果
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur=con.cursor()
    cur.execute("select AID,APassword from Admin where AID='"+user+"' and APassword='"+password+"'")
    if(cur.rowcount!=0):
        login_window.btn_admin.clicked.connect(Dialog_admin.show)
        login_window.btn_admin.clicked.connect(Dialog_login_error.close)
    else:
        login_window.btn_admin.clicked.connect(Dialog_login_error.show)
        login_window.btn_admin.clicked.connect(Dialog_admin.close)
    cur.close()
    login_window.btn_admin.clicked.connect(lambda: user_window.statusbar.showMessage(login_window.user.text()))

def check_booking():
    if (user_window.listView.selectedIndexes()):
        Dialog_booking.show()
        booking_dialog.output_FID.clear()
        booking_dialog.output_FID.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][0:6])
        booking_dialog.output_Airline.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][7:11])
        booking_dialog.output_Depart.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][12:16])
        booking_dialog.output_Arrive.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][17:21])
        booking_dialog.output_Dtime.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][22:27])
        booking_dialog.output_Atime.setText(user_window.qList[user_window.listView.selectedIndexes()[0].row()][28:33])
    UID=login_window.user.text()
    booking_dialog.output_nr.clear()
    booking_dialog.output_price.clear()
    booking_dialog.qList.clear()
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("select PID,PName,PSex from Passenger where UID='"+UID+"'")
    row=cur.fetchone()
    while row:
        booking_dialog.qList.append(row[0]+" "+row[1]+" "+row[2])
        row=cur.fetchone()
    slm = QStringListModel()
    slm.setStringList(booking_dialog.qList)
    booking_dialog.listView.setModel(slm)

def check_ticket():
    FID=booking_dialog.output_FID.text()
    date=booking_dialog.date_selected.text()
    class_selected=booking_dialog.class_selected.currentText()
    booking_dialog.output_price.clear()
    booking_dialog.output_nr.clear()
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    if(date):
        if(class_selected):
            cur.execute("select ClassPrice,SeatNum from Class where FID='"+FID+"' and ClassType='"+class_selected+"'")
            row=cur.fetchone()
            if row:
                booking_dialog.output_price.setText(row[0])
                cur.execute("SELECT COUNT(TID) FROM Ticket where FID ='"+FID+"' and FDate=str_to_date('"+date+"','%Y/%m/%d') and ClassType='"+class_selected+"'")
                count=cur.fetchone()
                booking_dialog.output_nr.setText(str((int(row[1])-count[0])))

            cur.close()

def confirm_booking():
    global ticket_nr
    UID=login_window.user.text()
    FID=booking_dialog.output_FID.text()
    PID=booking_dialog.qList[booking_dialog.listView.selectedIndexes()[0].row()][0:18]
    Fdate=booking_dialog.date_selected.text()
    Odate=datetime.date.today().strftime("%Y-%m-%d")
    ClassType=booking_dialog.class_selected.currentText()
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("select count(TID) from Ticket")
    ticket_nr=cur.fetchone()[0]+1
    TID=datetime.date.today().strftime("%Y%m%d")+'000000'+str(ticket_nr)
    sql="insert into Ticket (TID, TState,OrderDate,FDate,UID,PID,FID,ClassType) values ('"+TID+"','正常',str_to_date('"+Odate+"','%Y-%m-%d'),str_to_date('"+Fdate+"','%Y/%m/%d'),'"+UID+"','"+PID+"','"+FID+"','"+ClassType+"')"
    cur.execute(sql)
    QMessageBox.information(booking_dialog.listView,"成功","订购成功，您的订单编号：\n"+TID)
    con.commit()
    cur.close()
    Dialog_booking.close()

def check_personal():
    Dialog_personal.show()
    UID=login_window.user.text()
    personal_dialog.output_username.setText(UID)
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("select * from User where UID='"+UID+"'")
    row=cur.fetchone()
    Uemail=row[2]
    Utel=row[3]
    cur.close()
    personal_dialog.output_email.setText(Uemail)
    personal_dialog.output_tel.setText(Utel)
    email_dialog.output_email.setText(Uemail)
    tel_dialog.output_tel.setText(Utel)

def confirm_email():
    UID=login_window.user.text()
    newEmail=email_dialog.input_email.text()
    sql_update="update User set UEmail='"+newEmail+"' where UID='"+UID+"'"
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute(sql_update)
    con.commit()
    cur.close()
    Dialog_email.close()
    personal_dialog.output_email.setText(newEmail)
def confirm_tel():
    UID=login_window.user.text()
    newTel=tel_dialog.input_tel.text()
    sql_update="update User set UTel='"+newTel+"' where UID='"+UID+"'"
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute(sql_update)
    con.commit()
    cur.close()
    Dialog_tel.close()
    personal_dialog.output_tel.setText(newTel)

def confirm_password():
    UID = login_window.user.text()
    password=password_dialog.password.text()
    password2 = password_dialog.password2.text()
    if(password == password2):
        sql_update = "update User set UPassword='" + password + "' where UID='" + UID + "'"
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute(sql_update)
        con.commit()
        cur.close()
        Dialog_password.close()
    else:
        Dialog_password_error = QDialog()
        error_password = password_error.Ui_Dialog()
        error_password.setupUi(Dialog_password_error)
        Dialog_password_error.exec()

def check_passenger():
    Dialog_passenger.show()
    UID = login_window.user.text()
    passenger_dialog.qList.clear()
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("select PID,PName,PSex from Passenger where UID='" + UID + "'")
    row=cur.fetchone()
    while row:
        passenger_dialog.qList.append(row[0]+" "+row[1]+" "+row[2])
        row=cur.fetchone()
    slm = QStringListModel()
    slm.setStringList(passenger_dialog.qList)
    passenger_dialog.listView.setModel(slm)
    cur.close()

def confirm_add_pas():
    UID=login_window.user.text()
    PID=passenger_add_dialog.input_id.text()
    name=passenger_add_dialog.input_name.text()
    sex=passenger_add_dialog.sex_selected.currentText()
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("insert into Passenger (PID,UID,PName,PSex) values ('"+PID+"','"+UID+"','"+name+"','"+sex+"')")
    con.commit()
    cur.close()
    Dialog_passenger_add.close()
    check_passenger()
def confirm_delete_pas():
    UID = login_window.user.text()
    PID = passenger_dialog.qList[passenger_dialog.listView.selectedIndexes()[0].row()][0:18]
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("delete from Passenger where UID='"+UID+"' and PID='"+PID+"'")
    con.commit()
    cur.close()
    check_passenger()

def inquire_orders():
    UID = login_window.user.text()
    first = 1
    str_state=orders_dialog.input_state.text()
    str_name=orders_dialog.input_name.text()
    str_FID=orders_dialog.input_FID.text()
    str_TID=orders_dialog.input_TID.text()
    Odate1=orders_dialog.Odate1.text()
    Odate2 = orders_dialog.Odate2.text()
    Fdate1=orders_dialog.Fdate1.text()
    Fdate2=orders_dialog.Fdate2.text()
    sql_inquire = "select TID,TState,OrderDate,FID,FDate,ClassType,PID from Ticket where UID='" + UID + "' and (OrderDate between str_to_date('"+Odate1+"','%Y/%m/%d') and str_to_date('"+Odate2+"','%Y/%m/%d')) and (FDate between str_to_date('"+Fdate1+"','%Y/%m/%d') and str_to_date('"+Fdate2+"','%Y/%m/%d'))"
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()

    if str_state!='':
        sql_inquire+=" and TState='" + str_state + "'"
        first=0
    if str_FID!='':
        sql_inquire+=" and FID='" + str_FID + "'"
        first=0
    if str_TID!='':
        sql_inquire+=" and TID='" + str_TID + "'"
        first=0
    if str_name!='':
        cur.execute("select PID from Passenger where UID='"+UID+"' and PName= '"+str_name+"'")
        PID=cur.fetchone()[0]
        sql_inquire+=" and PID='" + PID + "'"
        first=0

    cur.execute(sql_inquire)
    row = cur.fetchone()
    orders_dialog.qList.clear()
    orders_dialog.qList.append("        订单编号\t     订单状态 订单日期    航班号    航班日期  舱位类型 乘客 \t   身份证号码")
    while row:
        cur2=con.cursor()
        cur2.execute("select PName from Passenger where PID ='"+row[6]+"'")
        name=cur2.fetchone()[0]
        orders_dialog.qList.append(row[0]+' '+row[1]+' '+row[2].strftime('%Y/%m/%d')+' '+row[3]+' '+row[4].strftime('%Y/%m/%d')+' '+row[5]+' '+name+' '+row[6])
        row=cur.fetchone()
    cur.close()
    slm = QStringListModel()
    slm.setStringList(orders_dialog.qList)
    orders_dialog.listView.setModel(slm)
def check_flight_info():
    TID=orders_dialog.qList[orders_dialog.listView.selectedIndexes()[0].row()][0:15]
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("select FID from Ticket where TID='"+TID+"'")
    FID=cur.fetchone()[0]
    cur.execute("select Airline,Depart,Arrive,Dtime,Atime from Flight where FID='"+FID+"'")
    row=cur.fetchone()
    flight_info_dialog.output_FID.setText(FID)
    flight_info_dialog.output_Airline.setText(row[0])
    flight_info_dialog.output_Depart.setText(row[1])
    flight_info_dialog.output_Arrive.setText(row[2])
    flight_info_dialog.output_Dtime.setText(row[3])
    flight_info_dialog.output_Atime.setText(row[4])
    Dialog_flight_info.show()

def cancel_ticket():
    TID = orders_dialog.qList[orders_dialog.listView.selectedIndexes()[0].row()][0:15]
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("update Ticket set TState='退票' where TID='"+TID+"'")
    con.commit()
    cur.close()
    inquire_orders()

def inquire():
    sql_inquire = "select FID,Airline,Depart,Arrive,Dtime,Atime from Flight "
    first = 1
    str_FID = admin_flight_window.input_FID.text()
    str_Airline = admin_flight_window.input_Airline.text()
    str_Depart = admin_flight_window.input_Depart.text()
    str_Arrive = admin_flight_window.input_Arrive.text()

    if str_FID != '':
        if first != 1:
            sql_inquire += " and "
        else:
            sql_inquire += " where "
        sql_inquire += "FID='" + str_FID + "'"
        first = 0
    if str_Airline != '':
        if first != 1:
            sql_inquire += " and "
        else:
            sql_inquire += " where "
        sql_inquire += "Airline like '%"+str_Airline+"%'"
        first = 0
    if str_Depart != '':
        if first != 1:
            sql_inquire += " and "
        else:
            sql_inquire += " where "
        sql_inquire += "Depart like '%"+str_Depart+"%'"
        first = 0
    if str_Arrive != '':
        if first != 1:
            sql_inquire += " and "
        else:
            sql_inquire += " where "
        sql_inquire += "Arrive like '%"+str_Arrive+"%'"
        first = 0

    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute(sql_inquire)
    row = cur.fetchone()
    admin_flight_window.qList.clear()
    while row:
        admin_flight_window.qList.append(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+row[5])
        row = cur.fetchone()
    cur.close()
    slm = QStringListModel()
    slm.setStringList(admin_flight_window.qList)
    admin_flight_window.listView.setModel(slm)
    admin_flight_window.statusbar.showMessage('查询成功', 1000)
def confirm_add_flight():
    FID=flight_add_dialog.input_FID.text()
    airline=flight_add_dialog.input_airline.text()
    depart=flight_add_dialog.input_depart.text()
    arrive=flight_add_dialog.input_arrive.text()
    dtime=flight_add_dialog.input_dtime.text()
    atime=flight_add_dialog.input_atime.text()
    class1=flight_add_dialog.input_type1.text()
    price1=flight_add_dialog.input_price1.text()
    num1=flight_add_dialog.input_nr1.text()
    class2 = flight_add_dialog.input_type2.text()
    price2 = flight_add_dialog.input_price2.text()
    num2 = flight_add_dialog.input_nr2.text()
    class3 = flight_add_dialog.input_type3.text()
    price3 = flight_add_dialog.input_price3.text()
    num3 = flight_add_dialog.input_nr3.text()

    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("insert into Flight (FID,Airline,Depart,Arrive,Dtime,Atime) values ('"+FID+"','"+airline+"','"+depart+"','"+arrive+"','"+dtime+"','"+atime+"')")
    sql_add_class="insert into Class (FID,ClassType,ClassPrice,SeatNum) values ('"+FID+"','"+class1+"','"+price1+"','"+num1+"')"
    if class2 != '':
        sql_add_class+=",('"+FID+"','"+class2+"','"+price2+"','"+num2+"')"
    if class3 !='':
        sql_add_class+=",('"+FID+"','"+class3+"','"+price3+"','"+num3+"')"
    cur.execute(sql_add_class)
    QMessageBox.information(flight_add_dialog.buttonBox,"成功","操作成功！")
    con.commit()
    cur.close()
    inquire()
    Dialog_flight_add.close()
def check_flight_edit():
    if (admin_flight_window.listView.selectedIndexes()):
        Dialog_flight_edit.show()
        flight_edit_dialog.output_FID.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][0:6])
        flight_edit_dialog.output_airline.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][7:11])
        flight_edit_dialog.input_depart.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][12:16])
        flight_edit_dialog.input_arrive.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][17:21])
        flight_edit_dialog.input_dtime.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][22:27])
        flight_edit_dialog.input_atime.setText(admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][28:33])
        FID=flight_edit_dialog.output_FID.text()
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("select ClassType,ClassPrice,Seatnum from Class where FID='"+FID+"'")
        row1=cur.fetchone()
        if row1:
            flight_edit_dialog.input_type1.setText(row1[0])
            flight_edit_dialog.input_price1.setText(row1[1])
            flight_edit_dialog.input_nr1.setText(row1[2])
            row2=cur.fetchone()
            if row2:
                flight_edit_dialog.input_type2.setText(row2[0])
                flight_edit_dialog.input_price2.setText(row2[1])
                flight_edit_dialog.input_nr2.setText(row2[2])
                row3 = cur.fetchone()
                if row3:
                    flight_edit_dialog.input_type3.setText(row3[0])
                    flight_edit_dialog.input_price3.setText(row3[1])
                    flight_edit_dialog.input_nr3.setText(row3[2])
                else:
                    flight_edit_dialog.input_type3.clear()
                    flight_edit_dialog.input_price3.clear()
                    flight_edit_dialog.input_nr3.clear()
            else:
                flight_edit_dialog.input_type2.clear()
                flight_edit_dialog.input_price2.clear()
                flight_edit_dialog.input_nr2.clear()
                flight_edit_dialog.input_type3.clear()
                flight_edit_dialog.input_price3.clear()
                flight_edit_dialog.input_nr3.clear()
        else:
            flight_edit_dialog.input_type1.clear()
            flight_edit_dialog.input_price1.clear()
            flight_edit_dialog.input_nr1.clear()
            flight_edit_dialog.input_type2.clear()
            flight_edit_dialog.input_price2.clear()
            flight_edit_dialog.input_nr2.clear()
            flight_edit_dialog.input_type3.clear()
            flight_edit_dialog.input_price3.clear()
            flight_edit_dialog.input_nr3.clear()

def confirm_edit_flight():
    FID = flight_edit_dialog.output_FID.text()
    depart = flight_edit_dialog.input_depart.text()
    arrive = flight_edit_dialog.input_arrive.text()
    dtime = flight_edit_dialog.input_dtime.text()
    atime = flight_edit_dialog.input_atime.text()
    class1 = flight_edit_dialog.input_type1.text()
    price1 = flight_edit_dialog.input_price1.text()
    num1 = flight_edit_dialog.input_nr1.text()
    class2 = flight_edit_dialog.input_type2.text()
    price2 = flight_edit_dialog.input_price2.text()
    num2 = flight_edit_dialog.input_nr2.text()
    class3 = flight_edit_dialog.input_type3.text()
    price3 = flight_edit_dialog.input_price3.text()
    num3 = flight_edit_dialog.input_nr3.text()

    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute("update Flight set Depart='"+depart+"',Arrive='"+arrive+"',Dtime='"+dtime+"',Atime='"+atime+"' where FID='"+FID+"'")
    if class1:
        cur.execute("select * from Class where FID='"+FID+"' and ClassType='"+class1+"'")
        if cur.fetchone():
            cur.execute("update Class set ClassPrice='"+price1+"',SeatNum='"+num1+"' where FID='"+FID+"' and ClassType='"+class1+"'")
        else:
            cur.execute("insert into Class (FID,ClassType,ClassPrice,SeatNum) values ('"+FID+"','"+class1+"','"+price1+"','"+num1+"')")
    if class2:
        cur.execute("select * from Class where FID='" + FID + "' and ClassType='" + class2 + "'")
        if cur.fetchone():
            cur.execute(
                "update Class set ClassPrice='" + price2 + "',SeatNum='" + num2 + "' where FID='" + FID + "' and ClassType='" + class2 + "'")
        else:
            cur.execute(
                "insert into Class (FID,ClassType,ClassPrice,SeatNum) values ('" + FID + "','" + class2 + "','" + price2 + "','" + num2 + "')")
    if class3:
        cur.execute("select * from Class where FID='" + FID + "' and ClassType='" + class3 + "'")
        if cur.fetchone():
            cur.execute(
                "update Class set ClassPrice='" + price3 + "',SeatNum='" + num3 + "' where FID='" + FID + "' and ClassType='" + class3 + "'")
        else:
            cur.execute(
                "insert into Class (FID,ClassType,ClassPrice,SeatNum) values ('" + FID + "','" + class3 + "','" + price3 + "','" + num3 + "')")

    QMessageBox.information(flight_edit_dialog.buttonBox, "成功", "操作成功！")
    con.commit()
    cur.close()
    inquire()
    Dialog_flight_edit.close()

def confirm_delete_flight():
    if (admin_flight_window.listView.selectedIndexes()):
        FID=admin_flight_window.qList[admin_flight_window.listView.selectedIndexes()[0].row()][0:6]
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("delete from Class where FID='"+FID+"'")
        cur.execute("delete from Flight where FID='" + FID + "'")
        cur.execute("update Ticket set TState='取消' where FID='" + FID + "' and TState='正常'")
        con.commit()
        cur.close()
    Dialog_flight_delete.close()
    inquire()
def inquire_orders_admin():
    first = 1
    str_state=admin_order_dialog.input_state.text()
    str_username=admin_order_dialog.input_username.text()
    str_FID=admin_order_dialog.input_FID.text()
    str_TID=admin_order_dialog.input_TID.text()
    Odate1=admin_order_dialog.Odate1.text()
    Odate2 = admin_order_dialog.Odate2.text()
    Fdate1=admin_order_dialog.Fdate1.text()
    Fdate2=admin_order_dialog.Fdate2.text()
    sql_inquire = "select TID,TState,OrderDate,FID,FDate,ClassType,PID,UID from Ticket where (OrderDate between str_to_date('"+Odate1+"','%Y/%m/%d') and str_to_date('"+Odate2+"','%Y/%m/%d')) and (FDate between str_to_date('"+Fdate1+"','%Y/%m/%d') and str_to_date('"+Fdate2+"','%Y/%m/%d'))"
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()

    if str_state!='':
        sql_inquire+=" and TState='" + str_state + "'"
        first=0
    if str_FID!='':
        sql_inquire+=" and FID='" + str_FID + "'"
        first=0
    if str_TID!='':
        sql_inquire+=" and TID='" + str_TID + "'"
        first=0
    if str_username!='':
        sql_inquire+=" and UID='" + str_username + "'"
        first=0

    cur.execute(sql_inquire)
    row = cur.fetchone()
    admin_order_dialog.qList.clear()
    admin_order_dialog.qList.append("        订单编号\t     订单状态 订单日期    航班号    航班日期  舱位类型 乘客 \t用户名")
    while row:
        cur2=con.cursor()
        cur2.execute("select PName from Passenger where PID ='"+row[6]+"' and UID='"+row[7]+"'")
        name=cur2.fetchone()[0]
        admin_order_dialog.qList.append(row[0]+' '+row[1]+' '+row[2].strftime('%Y/%m/%d')+' '+row[3]+' '+row[4].strftime('%Y/%m/%d')+' '+row[5]+' '+name+' '+row[7])
        row=cur.fetchone()
    cur.close()
    slm = QStringListModel()
    slm.setStringList(admin_order_dialog.qList)
    admin_order_dialog.listView.setModel(slm)
def confirm_normal():
    if (admin_order_dialog.listView.selectedIndexes()):
        TID=admin_order_dialog.qList[admin_order_dialog.listView.selectedIndexes()[0].row()][0:15]
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("update Ticket set TState='正常' where TID='"+TID+"'")
        QMessageBox.information(admin_order_dialog.btn_normal,"成功","操作成功！")
        con.commit()
        cur.close()
        inquire_orders_admin()
def confirm_cancel():
    if (admin_order_dialog.listView.selectedIndexes()):
        TID=admin_order_dialog.qList[admin_order_dialog.listView.selectedIndexes()[0].row()][0:15]
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("update Ticket set TState='退票' where TID='"+TID+"'")
        QMessageBox.information(admin_order_dialog.btn_normal,"成功","操作成功！")
        con.commit()
        cur.close()
        inquire_orders_admin()
def confirm_delete():
    if (admin_order_dialog.listView.selectedIndexes()):
        TID=admin_order_dialog.qList[admin_order_dialog.listView.selectedIndexes()[0].row()][0:15]
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("update Ticket set TState='取消' where TID='"+TID+"'")
        QMessageBox.information(admin_order_dialog.btn_normal,"成功","操作成功！")
        con.commit()
        cur.close()
        inquire_orders_admin()
def inquire_user():
    first=1
    UID=admin_user_dialog.input_username.text();
    email=admin_user_dialog.input_email.text()
    tel=admin_user_dialog.input_tel.text()
    sql_inquire="select UID, UEmail,UTel from User "
    if UID:
        if first==1:
            sql_inquire+="where "
        else:
            sql_inquire+="and "
        sql_inquire+="UID like '%"+UID+"%'"
    if email:
        if first==1:
            sql_inquire+="where "
        else:
            sql_inquire+="and "
        sql_inquire+="UEmail like '%"+email+"%'"
    if tel:
        if first==1:
            sql_inquire+="where "
        else:
            sql_inquire+="and "
        sql_inquire+="UTel like '%"+tel+"%'"
    con = pymysql.connect('localhost', 'root', '123456', 'mydb')
    cur = con.cursor()
    cur.execute(sql_inquire)
    row=cur.fetchone()
    admin_user_dialog.qList.clear()
    while row:
        admin_user_dialog.qList.append(row[0]+"\t"+row[1]+"\t"+row[2])
        row=cur.fetchone()
    cur.close()
    slm = QStringListModel()
    slm.setStringList(admin_user_dialog.qList)
    admin_user_dialog.listView.setModel(slm)
def confirm_delete_user():
    if (admin_user_dialog.listView.selectedIndexes()):
        UID = admin_user_dialog.qList[admin_user_dialog.listView.selectedIndexes()[0].row()][0:7]
        con = pymysql.connect('localhost', 'root', '123456', 'mydb')
        cur = con.cursor()
        cur.execute("delete from User where UID='"+UID+"'")
        cur.execute("delete from Passenger where UID='"+UID+"'")
        QMessageBox.information(user_delete_dialog.buttonBox, "成功", "操作成功！")
        con.commit()
        cur.close()
        Dialog_user_delete.close()
        inquire_user()

if __name__ == '__main__':
    global ticket_nr
    ticket_nr=1

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    login_window = log_in.Ui_MainWindow()
    login_window.setupUi(MainWindow)

    MainWindow.show()

    MainWindow_user = QMainWindow()
    user_window = user_operation.Ui_MainWindow()
    user_window.setupUi(MainWindow_user)

    Dialog_login_error=QDialog()
    error_login = log_in_error.Ui_Dialog()
    error_login.setupUi(Dialog_login_error)

    Dialog_signup=QDialog()
    signup_dialog=sign_up.Ui_Dialog()
    signup_dialog.setupUi(Dialog_signup)

    #检查用户名和密码
    #login_window.btn_login.clicked.connect(MainWindow.close)
    login_window.user.textEdited.connect(lambda:check(login_window.user.text(),login_window.password.text()))
    login_window.password.textEdited.connect(lambda: check(login_window.user.text(), login_window.password.text()))
    login_window.user.textEdited.connect(lambda: check_admin(login_window.user.text(), login_window.password.text()))
    login_window.password.textEdited.connect(lambda: check_admin(login_window.user.text(), login_window.password.text()))

    login_window.btn_signup.clicked.connect(Dialog_signup.show)
#订票页面
    Dialog_booking=QDialog()
    booking_dialog=booking.Ui_Dialog()
    booking_dialog.setupUi(Dialog_booking)
    user_window.btn_book.clicked.connect(check_booking)
    booking_dialog.btn_search.clicked.connect(check_ticket)
    booking_dialog.buttonBox.accepted.connect(confirm_booking)
#个人信息管理
    Dialog_personal=QDialog()
    personal_dialog=personal_info.Ui_Dialog()
    personal_dialog.setupUi(Dialog_personal)
    user_window.btn_info.clicked.connect(check_personal)
#修改邮箱
    Dialog_email=QDialog()
    email_dialog=email_update.Ui_Dialog()
    email_dialog.setupUi(Dialog_email)
    email_dialog.buttonBox.accepted.connect(confirm_email)
    personal_dialog.btn_email.clicked.connect(Dialog_email.show)
#修改电话
    Dialog_tel = QDialog()
    tel_dialog = tel_update.Ui_Dialog()
    tel_dialog.setupUi(Dialog_tel)
    tel_dialog.buttonBox.accepted.connect(confirm_tel)
    personal_dialog.btn_tel.clicked.connect(Dialog_tel.show)
# 修改密码
    Dialog_password = QDialog()
    password_dialog = password_update.Ui_Dialog()
    password_dialog.setupUi(Dialog_password)
    password_dialog.buttonBox.accepted.connect(confirm_password)
    personal_dialog.btn_password.clicked.connect(Dialog_password.show)
#乘机人管理
    Dialog_passenger=QDialog()
    passenger_dialog=passenger.Ui_Dialog()
    passenger_dialog.setupUi(Dialog_passenger)
    user_window.btn_passengers.clicked.connect(check_passenger)
#新增乘机人
    Dialog_passenger_add=QDialog()
    passenger_add_dialog=passenger_add.Ui_Dialog()
    passenger_add_dialog.setupUi(Dialog_passenger_add)
    passenger_dialog.btn_add.clicked.connect(Dialog_passenger_add.show)
    passenger_add_dialog.buttonBox.accepted.connect(confirm_add_pas)
#删除乘机人
    passenger_dialog.btn_delete.clicked.connect(confirm_delete_pas)
#订单管理
    Dialog_order=QDialog()
    orders_dialog=orders.Ui_Dialog()
    orders_dialog.setupUi(Dialog_order)
    user_window.btn_orders.clicked.connect(Dialog_order.show)
#订单查询
    orders_dialog.btn_search.clicked.connect(inquire_orders)
#航班信息
    Dialog_flight_info=QDialog()
    flight_info_dialog=flight_info.Ui_Dialog()
    flight_info_dialog.setupUi(Dialog_flight_info)
    orders_dialog.btn_flight_info.clicked.connect(check_flight_info)
#退票
    orders_dialog.btn_cancel.clicked.connect(cancel_ticket)

#管理员窗口
    Dialog_admin=QDialog()
    admin_dialog=admin_operation.Ui_Dialog()
    admin_dialog.setupUi(Dialog_admin)
#航班管理窗口
    MainWindow_flight=QMainWindow()
    admin_flight_window=flight_admin.Ui_MainWindow()
    admin_flight_window.setupUi(MainWindow_flight)
    admin_dialog.btn_flight.clicked.connect(MainWindow_flight.show)
#航班查询
    admin_flight_window.btn_search.clicked.connect(inquire)
#新增航班
    Dialog_flight_add=QDialog()
    flight_add_dialog=flight_add.Ui_Dialog()
    flight_add_dialog.setupUi(Dialog_flight_add)
    admin_flight_window.btn_add.clicked.connect(Dialog_flight_add.show)
    flight_add_dialog.buttonBox.accepted.connect(confirm_add_flight)
#编辑航班
    Dialog_flight_edit=QDialog()
    flight_edit_dialog=flight_edit.Ui_Dialog()
    flight_edit_dialog.setupUi(Dialog_flight_edit)
    admin_flight_window.btn_edit.clicked.connect(check_flight_edit)
    flight_edit_dialog.buttonBox.accepted.connect(confirm_edit_flight)
#删除航班
    Dialog_flight_delete=QDialog()
    flight_delete_dialog=flight_delete.Ui_Dialog()
    flight_delete_dialog.setupUi(Dialog_flight_delete)
    admin_flight_window.btn_delete.clicked.connect(Dialog_flight_delete.show)
    flight_delete_dialog.buttonBox.accepted.connect(confirm_delete_flight)
#订单管理
    Dialog_order_admin=QDialog()
    admin_order_dialog=orders_management.Ui_Dialog()
    admin_order_dialog.setupUi(Dialog_order_admin)
    admin_dialog.btn_order.clicked.connect(Dialog_order_admin.show)
    admin_order_dialog.btn_search.clicked.connect(inquire_orders_admin)
#置为xx状态
    admin_order_dialog.btn_normal.clicked.connect(confirm_normal)
    admin_order_dialog.btn_cancel.clicked.connect(confirm_cancel)
    admin_order_dialog.btn_delete.clicked.connect(confirm_delete)
#用户管理
    Dialog_user_admin=QDialog()
    admin_user_dialog=user_management.Ui_Dialog()
    admin_user_dialog.setupUi(Dialog_user_admin)
    admin_dialog.btn_user.clicked.connect(Dialog_user_admin.show)
    admin_user_dialog.btn_search.clicked.connect(inquire_user)
#删除用户
    Dialog_user_delete=QDialog()
    user_delete_dialog=user_delete.Ui_Dialog()
    user_delete_dialog.setupUi(Dialog_user_delete)
    admin_user_dialog.btn_delete.clicked.connect(Dialog_user_delete.show)
    user_delete_dialog.buttonBox.accepted.connect(confirm_delete_user)
#游客
    MainWindow_visitor=QMainWindow()
    visitor_window=visitor_operation.Ui_MainWindow()
    visitor_window.setupUi(MainWindow_visitor)
    login_window.btn_visitor.clicked.connect(MainWindow_visitor.show)
    sys.exit(app.exec_())