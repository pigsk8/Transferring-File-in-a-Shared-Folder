import wx
import os
import time


ID_BUTTON=100
ID_EXIT=200
ID_SPLITTER=300

class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.files = os.listdir('.')

        #path = "/home/jose/graficopiton/"
        #self.files = os.listdir(path)
        

        self.InsertColumn(0, 'Nombre')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Dimension', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modificado')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

       

       # j = 1
        self.InsertStringItem(0, '..')
        self.SetItemImage(0, 5)
         
        self.j = 1
        for self.i in self.files:
            (self.name, self.ext) = os.path.splitext(self.i)
            self.ex = self.ext[1:]
            self.size = os.path.getsize(self.i)
            self.sec = os.path.getmtime(self.i)
            self.InsertStringItem(self.j, self.name)
            self.SetStringItem(self.j, 1, self.ex)
            self.SetStringItem(self.j, 2, str(self.size) + ' B')
            self.SetStringItem(self.j, 3, time.strftime('%Y-%m-%d %H:%M', time.localtime(self.sec)))

            

            if (self.j % 2) == 0:
                self.SetItemBackgroundColour(self.j, '#e6f1f5')
            self.j = self.j + 1


    
    def refrescar(self,directorio):
        #cambiar ruta para mostrar la carpeta
        self.nuevacarpeta = str(os.getcwd())
        count = 0
    
        if count == 0:
            self.files = os.listdir(self.nuevacarpeta)
        
      
            self.InsertColumn(0, 'Nombre')
            self.InsertColumn(1, 'Ext')
            self.InsertColumn(2, 'Dimension', wx.LIST_FORMAT_RIGHT)
            self.InsertColumn(3, 'Modificado')

            self.SetColumnWidth(0, 220)
            self.SetColumnWidth(1, 70)
            self.SetColumnWidth(2, 100)
            self.SetColumnWidth(3, 420)

       
       # j = 1
            self.InsertStringItem(0, '..')
            self.SetItemImage(0, 5)
            self.j = 1
            self.files = 1        
            self.files = os.listdir('.')
        
            for self.i in self.files:
                (self.name, self.ext) = os.path.splitext(self.i)
                self.ex = self.ext[1:]
                self.size = os.path.getsize(self.i)
                self.sec = os.path.getmtime(self.i)
                self.InsertStringItem(self.j, self.name)
                self.SetStringItem(self.j, 1, self.ex)
                self.SetStringItem(self.j, 2, str(self.size) + ' B')
                self.SetStringItem(self.j, 3, time.strftime('%Y-%m-%d %H:%M',time.localtime(self.sec)))

            

                if (self.j % 2) == 0:
                    self.SetItemBackgroundColour(self.j, '#e6f1f5')
                self.j = self.j + 1
