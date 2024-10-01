from flet import *
import mysql.connector as msqlC



#Connection a la DB
mydb = msqlC.connect(
    host = "localhost",
    user="root",
    password = "",
    database = "flet_login_register"
)
cursor = mydb.cursor()



    
    
def main(page: Page):
    
    page.adaptive = True
    
    nomTxt = TextField(label="Nom")
    ageTxt = TextField(label="Age")
    
    mydt = DataTable(
                    columns=[
                        DataColumn(Text("Id")),
                        DataColumn(Text("Nom")),
                        DataColumn(Text("Âge")),
                        DataColumn(Text("Actions", size=18))
                        ],
                    rows=[]
                    )
    
    
    
    def delete(e):
        row = e.control.data
        try:
            sql = "DELETE FROM mainan WHERE id = %s"
            val = (row['id'],)
            cursor.execute(sql, val)
            mydb.commit()
            print(cursor.rowcount, "Suppression réussie!!!")

            mydt.rows.clear()
            load_data()

            page.snack_bar = SnackBar(
                Text("Suppression réussie🎉🎉", size=30, color="white"),
                bgcolor="black"
            )
            page.snack_bar.open = True
            page.update()
            
        except Exception as e:
            print(e)
            print("Erreur de suppression")
         
    
    def editbtn(e):
        row = e.control.data
        nomTxt.value = row['nom']
        ageTxt.value = row['age']
        page.update()
    
    
    
    
    
    def load_data():
        query = "SELECT * FROM mainan"
        cursor.execute(query)
        result = cursor.fetchall()
        
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]
        
        
        
        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells = [
                        DataCell(Text(row['id'])),
                        DataCell(Text(row['nom'])),
                        DataCell(Text(row['age'])),
                        DataCell(
                                Row(
                                    controls=[
                                        IconButton("delete", icon_color="red",
                                               data=row,
                                               on_click=delete
                                               ),
                                        IconButton("create", icon_color="blue",
                                               data=row,
                                               on_click=editbtn
                                               )
                                    ]
                                )
                            ),
                    ]
                )
            )
        
        page.update()
    
    
    load_data()
    
    def addUser(e):
                try:
                    if nomTxt == "":
                        page.snack_bar = SnackBar(
                            Text("Veuillez remplir tous les champs Svp", size=30, color="red")
                        )
                        print("remplir tous les champs")
                        page.snack_bar.open = True
                        page.update()
                    
                    
                    
                    else:
                        sql = "INSERT INTO mainan (nom, age) VALUE (%s, %s)"
                        val = (nomTxt.value, ageTxt.value)
                        cursor.execute(sql, val)
                        mydb.commit()
                        print(cursor.rowcount, "Insertion réussie!!!")
                        
                        mydt.rows.clear()
                        
                        page.snack_bar = SnackBar(
                            Text("Ajout Réussi🎉🎉", size=30, bgcolor="green")
                        )
                        page.snack_bar.open = True 
                        page.update()
                        load_data() 
                    

                    
                    
                    
                except Exception as e:
                    print(e)
                    print("Erreur de code")
                
                nomTxt.value = ""
                ageTxt.value = ""
                page.update()
                
                
               
    page.add(
        Column([
            
            nomTxt,
            ageTxt,
            FloatingActionButton(icon=icons.ADD, on_click=addUser),
            mydt
        ]
               )
        
    )
    


   


app(target=main)