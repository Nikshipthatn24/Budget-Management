import pymysql
from tabulate import tabulate
import re
from datetime import datetime

class Buget:
    inexp, inamo = '', ''
    exps, amo = [], []
    total = 0
    totsum = 0
    amount=[]
    earcop = 0
    earned=0
    exceed = 0
    l=0

    def connect_database(self):
        try:
            connection = pymysql.connect(host='localhost', user='root', password='Tiger@123')
            cursor = connection.cursor()
        except Exception as e:
            print(f'{e}')
            return None, None
        return cursor, connection

    def expense(self):

        cursor, connection = self.connect_database()
        cursor.execute('CREATE DATABASE IF NOT EXISTS View_buget_management')
        cursor.execute('USE View_buget_management')

        cursor.execute(

            'CREATE TABLE IF NOT EXISTS Budget_Management(SL_NO INT PRIMARY KEY AUTO_INCREMENT ,SALARY VARCHAR(30),EXPENSE_DESCRIPTION VARCHAR(30), EXPENSE_AMOUNT VARCHAR(30),PROFIT VARCHAR(30),LOSS VARCHAR(30),STATUS VARCHAR(30),DATE DATE,SUM_EXPENSES_AMOUNT varchar(30))')

    def manage(self):
            print('*************************************')
            while True:

                print('*************************************')
                print(''
                      '1.To Deposit  the amount\n'
                      '2.Add expenses \n'
                      '3.To save the data \n'
                      '4.Review the details \n'
                      '5.Get the details by entering the Date \n'
                      '6.Exit\n'
                      )
                print('*************************************')

                a = input('Enter the Number which you preferred ')

                print('*************************************')
                if a == '1':
                    if self.l == 0:
                            print(
                            'Note: 1.once you add the Total amount you cannot modify \n'
                            'But you can add it again once you save the previous deposit amount.\n'
                            )
                            while True:
                                a = int(input('Enter the total amount  '))
                                if a > 0:
                                    break
                                else:
                                    print('Do not add Negative or Zero value')
                            self.amount.append(a)
                            if len(self.amount) == 1:
                                print('the data is added')
                                print('Now you can add the expenses')
                            self.earned = int(self.amount[0])  # Convert the value to an integer
                            self.earcop = self.earned
                            self.l = 1
                            obj.manage()
                    elif self.l == 1:
                                print('*************************************')
                                print('The total amount is present u cannot add it again')
                                print('*************************************')
                elif a=='2':
                    if not self.earned:
                        print('First Deposit the amount ')
                    else:

                        while True:
                            try:
                                entries = int(input('How many entries need to add '))
                                break
                            except Exception as e:
                                print(f"{e}Invalid input. Please enter a valid integer.")
                        for i in range(entries):
                            while True:
                                # obj.data()
                                expense = input('Enter the expenses description')
                                if re.match(r'^[a-zA-Z][a-zA-Z\s]*$', expense):
                                    while True:
                                        try:
                                            amount_spend = int(input('Enter the expenses amount: '))
                                            break
                                        except Exception as e:
                                            print(f"{e}Invalid input. Please enter a valid integer.")
                                    if amount_spend <= self.earned:
                                        self.exps.append(expense)
                                        self.amo.append(amount_spend)
                                        self.earned -= amount_spend
                                        print('The data is added \n')
                                        print('*************************************')
                                        # print(self.amo, self.exps)
                                        # print('\n')
                                        self.total = sum(self.amo)
                                        self.totsum = self.earcop - self.total
                                        print(f'The remaining amount is {self.totsum} \n')
                                    else:
                                        print('amount your are updating is exceed to earned value')
                                        exceed = input('Do you want to update the same amount (y/n): ').lower()
                                        if exceed == 'y':
                                            self.exps.append(expense)
                                            self.amo.append(amount_spend)
                                            self.totsum = self.earned - amount_spend
                                            self.earned = self.totsum
                                            self.exceed = abs(self.totsum)
                                            print('Data is added ')
                                            print('*************************************')
                                            # print(f'earned amount: {self.totsum}')
                                            print(f'exceed amount: {self.exceed}\n')
                                            print('*************************************')

                                        elif exceed == 'n':
                                            obj.manage()
                                        else:
                                            print('plz enter (y/n)')
                                    break
                                else:
                                    print('Only character are allowed')

                        self.inexp = ','.join(self.exps)
                        self.inamo = ','.join(map(str, self.amo))
                        inamo_list = [x for x in self.inamo.split(',') if x.strip()]
                        self.sum_expamo = sum(map(int, inamo_list))
                        self.grand_total = self.earcop - self.sum_expamo
                elif a == '3':
                    if not self.amo and not self.exps and not self.totsum:
                        print('Go and fill expenses description  ')
                    else:
                        print('*************************************')
                        print(f'salary : {self.earcop} ')
                        print(f'The expenses description : {self.inexp}')
                        print(f'The expenses amount : {self.inamo}')
                        if self.totsum<0:
                            self.totsum=0
                            print(f'Saving amount : {self.totsum}')
                        else:
                            print(f'Saving amount : {self.totsum}')
                        print(f'Loss amount : {self.exceed}')
                        print('*************************************')

                        print('NOTE: Confirm the data before submission once you submit the data you cannot modify')

                        print('*************************************')

                        while True:
                            a = input('Say (y/n) to save the data  ')
                            if a == 'y':
                                while True:
                                    try:
                                        cursor, connection = self.connect_database()
                                        cursor.execute('USE View_buget_management')
                                        input_date = input('Enter the date (dd-mm-yyyy): ')
                                        date_object = datetime.strptime(input_date, '%d-%m-%Y')
                                        self.formatted_date = date_object.strftime('%Y-%m-%d')
                                        cursor.execute(
                                            'INSERT INTO Budget_Management (SALARY, EXPENSE_DESCRIPTION, EXPENSE_AMOUNT,DATE,SUM_EXPENSES_AMOUNT) VALUES (%s, %s, %s, %s,%s)',
                                            (self.earcop, self.inexp, self.inamo, self.formatted_date, self.sum_expamo)
                                        )
                                        cursor.execute(
                                            'SELECT SL_NO,SALARY,SUM_EXPENSES_AMOUNT FROM Budget_Management ')
                                        rows = cursor.fetchall()
                                        for row in rows:
                                            sl_no = row[0]
                                            s1 = row[1]
                                            s2 = row[2]
                                        self.total = int(s1) - int(s2)
                                        query = """
                                                                                     UPDATE Budget_Management
                                                                                     SET 
                                                                                         PROFIT = CASE
                                                                                             WHEN %s > 0 THEN %s
                                                                                             WHEN %s < 0 THEN 0
                                                                                             WHEN %s = 0 THEN 0
                                                                                         END,
                                                                                         LOSS = CASE
                                                                                             WHEN %s > 0 THEN 0
                                                                                             WHEN %s < 0 THEN ABS(%s)
                                                                                             WHEN %s = 0 THEN 0
                                                                                         END,
                                                                                         STATUS = CASE
                                                                                             WHEN %s > 0 THEN 'EARNED PROFIT'
                                                                                             WHEN %s < 0 THEN 'LOSS'
                                                                                             WHEN %s = 0 THEN 'NO PROFIT OR LOSS'
                                                                                         END
                                                                                          WHERE SL_NO = %s
                                                                                     """
                                        values = (
                                            self.total, self.total, self.total, self.total,  # For PROFIT
                                            self.total, self.total, self.total, self.total,  # For LOSS
                                            self.total, self.total, self.total,  # For STATUS
                                            sl_no

                                        )
                                        cursor.execute(query, values)
                                        connection.commit()
                                        print('*************************************')

                                        print('The record is Added \n')
                                        print('*************************************')
                                        self.l = 0
                                        self.amount=[]
                                        self.inexp, self.inamo = '', ''
                                        self.exps, self.amo = [], []
                                        self.total = 0
                                        self.totsum = 0
                                        self.earcop = 0
                                        self.exceed = 0
                                        self.earned=0
                                        print('Now you can Deposit the amount and repeat the process')
                                        break

                                    except Exception as e:
                                        print(f"{e}.")
                                break


                            elif a == 'n':
                                    obj.manage()
                            else:
                                    print('enter correctly(y/n) ')

                elif a == '4':

                    cursor, connection = self.connect_database()
                    cursor.execute('USE View_buget_management')
                    cursor.execute('select * from Budget_Management')
                    result = cursor.fetchall()
                    print('*************************************')
                    print("************** BUDGET MANAGEMENT **************")
                    headers = ['SL_NO', 'SALARY', 'EXPENSE_DESCRIPTION', 'EXPENSE_AMOUNT', 'SAVING', 'LOSS',
                               'STATUS', 'DATE',
                               'SUM_EXPENSES_AMOUNT']
                    print(tabulate(result, headers, tablefmt="psql"))
                elif a == '5':
                    cursor, connection = self.connect_database()
                    cursor.execute('USE View_buget_management')
                    cursor.execute('select * from Budget_Management')
                    result = cursor.fetchall()
                    headers = ['SL_NO', 'SALARY', 'EXPENSE_DESCRIPTION', 'EXPENSE_AMOUNT', 'SAVING', 'LOSS',
                               'STATUS', 'DATE',
                               'SUM_EXPENSES_AMOUNT']
                    print(tabulate(result, headers, tablefmt="psql"))
                    while True:
                        try:

                            input_date = input('Enter the date (dd-mm-yyyy): ')
                            date_object = datetime.strptime(input_date, '%d-%m-%Y')
                            self.formatted_date = date_object.strftime('%Y-%m-%d')
                            cursor.execute('select * from Budget_Management where DATE=%s',(self.formatted_date))
                            result = cursor.fetchone()
                            print('*************************************')
                            print(f''
                                  f'The amount deposited is {result[1]}\n'
                                  f'The expenses description is {result[2]} \n'
                                  f'The total expenses amount is {result[3]} \n'
                                  f'The saving amount is {result[4]} \n'
                                  f'The loss amount is {result[5]} \n'
                                  f'The status is {result[6]}')
                            print('*************************************')
                            break



                        except Exception as e:
                            print(f'{e}')
                elif a == '6':
                    exit()
                else:
                    print('Enter above number properly')




obj = Buget()
print("************** BUDGET MANAGEMENT **************")
obj.expense()
obj.manage()


