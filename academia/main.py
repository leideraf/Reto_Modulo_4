#from view.menu import menu_principal
from view.viewTkinter.menuPrincipal import MenuPrincipal
from config.database import Database

if __name__ == "__main__":
    db = Database()
    try:
        menu_principal = MenuPrincipal(db = db)
        menu_principal.root.mainloop()
    finally:
        db.close()