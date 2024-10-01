from flet import *
import mysql.connector as msqlC


class Register_and_Login:
    
    def __init__(self, page: Page):
        self.page = page
        self.page.adaptive=True
        
        
        #Db Connnection
        self.DataBase = msqlC.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "Formulaire1_flet"
        )
        self.cursor = self.DataBase.cursor()
        
        
        #TextField
        self.nomTxt = TextField(label="Nom")
        self.PreNomTxt = TextField(label="Prénom")
        self.AgeTxt = TextField(label="Age")
        self.SexeTxt = TextField(label="Sexe")
        self.ProfessionTxt = TextField(label="Profession")
        
        
        
        
        self.MyDataTable = DataTable(
                                columns=[
                                        DataColumn(Text("Id")),
                                        DataColumn(Text("Nom")),
                                        DataColumn(Text("Prénom")),
                                        DataColumn(Text("Age")),
                                        DataColumn(Text("Sexe")),
                                        DataColumn(Text("Profession")),
                                        DataColumn(Text("Actions", size=18)),
                                    ],
                                    rows=[]
            )
        
        
        self.container = self.container_All()
        self.load_data()
    
    
    def container_All(self):
        return Column(scroll="auto",
                        controls=[
                                self.Formulaire(),
                                
                        ]
            
        )
        
    
    
    def Formulaire(self):
       
      
        
        return Column(
                    controls=[
                                Row(alignment="center",controls=[self.nomTxt]),
                                Row(alignment="center",controls=[self.PreNomTxt]),
                                Row(alignment="center",controls=[self.AgeTxt]),
                                Row(alignment="center",controls=[self.SexeTxt]),
                                Row(alignment="center",controls=[self.ProfessionTxt]),
                                
                                Column(
                                        controls=[
                                                    Row(
                                                        controls=[
                                                                FloatingActionButton(
                                                                                    icon=icons.ADD, 
                                                                                    on_click=self.addUser
                                                    ),
                                                ]
                                            )                                            
                                        ]
                                    ),
                            
                                Container(          
                                        width=800,
                                        height=400,
                                        content=Column(
                                                        controls=[
                                                                self.MyDataTable,
                                                        ],
                                                        scroll="auto",                                      
                                            ),
                                )
                                
            ]
        )
    
    
    def load_data(self):
        query = "SELECT * FROM User"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        columns = [self.column[0] for self.column in self.cursor.description]
        self.rows = [dict(zip(columns, row)) for row in result]
         
        self.MyDataTable.rows.clear()
        for row in self.rows:
            self.MyDataTable.rows.append(
                DataRow(
                    cells=[
                            DataCell(
                                    Text(
                                        row[
                                            'Id'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Text(
                                        row[
                                            'nom'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Text(
                                        row[
                                            'prenom'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Text(
                                        row[
                                            'age'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Text(
                                        row[
                                            'sexe'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Text(
                                        row[
                                            'profession'
                                            ]
                                        )
                                    ),
                            DataCell(
                                    Row(
                                        controls=[
                                                IconButton("delete", 
                                                           icon_color="red", 
                                                           data=row, on_click=self.Suppresion
                                                           ),
                                                
                                                IconButton("edit", 
                                                           icon_color="blue", 
                                                           data=row, on_click=self.Modifier
                                                           ),
                                        ] 
                                    )
                                ),
                    ]
                )
                
            )
        
        self.page.update()
    
    
    
    
    def addUser(self, e):
        
        try:
            query = "INSERT INTO User (nom, prenom, age, sexe, profession) VALUE (%s, %s, %s, %s, %s)"
            value = (self.nomTxt.value, 
                     self.PreNomTxt.value, 
                     self.AgeTxt.value, 
                     self.SexeTxt.value,
                     self.ProfessionTxt.value)
            self.cursor.execute(query, value)
            self.DataBase.commit()
            
            self.MyDataTable.rows.clear()
            
            snack_bar = SnackBar(
                Text("Inscription Réussie", size=20, color="green")
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            
            self.load_data()
            self.page.update()
        
        
        
        except Exception as e:
            snack_bar = SnackBar(
                Text("Erreur d'enregistrement", size=20, color="red"))
            
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            
        self.nomTxt.value = ""
        self.PreNomTxt.value = ""
        self.AgeTxt.value = ""
        self.SexeTxt.value = ""
        self.ProfessionTxt.value = ""
        
        self.page.update()
            
    
    def Suppresion(self, e):
        row = e.control.data
        
        try:
            query = "DELETE FROM User WHERE Id=%s"
            value = (row['Id'],)
            self.cursor.execute(query, value)
            self.DataBase.commit()
            print(self.cursor.rowcount, "Suppression Réussie!")
            
            self.MyDataTable.rows.clear()
            
            snack_bar = SnackBar(
                Text( "Suppression Réussie!", size=20, color="green")
            )
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
            
            self.load_data()
            self.page.update()
            
            
        
        
        except Exception as e:
            print(f"Erreur de lors de la suppression {e}")
            
            snack_bar = SnackBar(
                Text("Erreur de lors de la suppression", size=20, color="red"))
            
            self.page.overlay.append(snack_bar)
            snack_bar.open = True
    
        self.page.update()
    
    
    
    
    def Modifier(self):
        pass
    
    
    
    def run(self):
        self.page.add(self.container)
        
    
    
def main(page: Page):
    app = Register_and_Login(page)
    app.run()
    
app(target=main)