#!/usr/bin/env python
import wx, threading
import mu, time
import CapertaCompartida, multireceiver, client4

class MyFrame(wx.Frame):
    
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(620,600))
        self.Centre() 
        self.Show(True)
        self.panel = wx.Panel(self,size=(620,600),style=wx.RAISED_BORDER)
       
        self.panelList = wx.Panel(self,pos=(5,60),size=(500,500))
        self.timer = wx.Timer(self, 1)

         
        self.filemenu= wx.Menu()
        self.menuServer = self.filemenu.Append(wx.ID_OPEN, "&Servidor"," Iniciar como servidor")
        self.filemenu.AppendSeparator()
        self.menuClient= self.filemenu.Append(wx.ID_ABOUT, "&Cliente"," Iniciar como cliente")
        self.filemenu.AppendSeparator()
        self.menuExit = self.filemenu.Append(wx.ID_EXIT,"S&alir"," Salida del programa")
        self.filemenu.AppendSeparator()
        
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.filemenu,"&DropBox") 
        self.SetMenuBar(self.menuBar)  
      
        
        

        self.tex1 = wx.StaticText(self.panel, label='Nombre de grupo',pos=(20,20),size=(100,30)) 
        
        self.nombre = wx.TextCtrl(self.panel, value='',pos=(140,12),size=(100,30))
        
        self.v_conectar = wx.Button(self.panel, label='',pos=(260,12),size=(100,30))
        
        self.hbox = wx.BoxSizer(wx.VERTICAL)
          
   
        
        self.list = CapertaCompartida.MyListCtrl(self.panelList,-1)
        self.hbox.Add(self.list,-1,wx.EXPAND)
        self.panelList.SetSizer(self.hbox)
        
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.compartir = wx.Button(self.panel, label='Compartir',pos=(510,180),size=(100,30)) 
       
        self.eliminar = wx.Button(self.panel, label='Eliminar',pos=(510,220),size=(100,30)) 
        

        
        self.modificar = wx.Button(self.panel, label='Modificar',pos=(510,260),size=(100,30)) 
        

        self.tex1.Show(False)
        self.nombre.Show(False)   
        self.v_conectar.Show(False)
        self.panelList.Show(False)
        self.modificar.Show(False)
        self.eliminar.Show(False)
        self.compartir.Show(False)
       
        
        #evento del menu exit
        self.Bind(wx.EVT_MENU, self.Salir, self.menuExit)
        #evento del menu server
        self.Bind(wx.EVT_MENU, self.Servidor, self.menuServer)
        #evento del menu cliente
        self.Bind(wx.EVT_MENU, self.Cliente, self.menuClient)
        #evento del boton conectar o crear
        self.Bind(wx.EVT_BUTTON, self.Conectar, self.v_conectar)
        #evento de item seleccionado
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnSelect,self.list) 
        #evento de refrescar pantalla
        self.timer.Start(5000)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=1)

    
    def OnSelect (self,e):
        print 'evento de seleccion de item'
        count = self.list.GetFocusedItem()
        print count
        print self.list.GetItemText(count)

            

    #Funcion para la opcion Salir
    def Salir(self,e):
         self.timer.Stop()
         self.Destroy()
    	 self.Close(True)
    #Funcion para la opcion Servidor
    def Servidor(self,e):
        
    	self.tex1.Show(True)	
    	self.nombre.Show(True)
    	self.v_conectar.Show(True)
        self.modificar.Show(False)
        self.eliminar.Show(False)
        self.compartir.Show(False)
    	self.v_conectar.SetLabel("Crear")
        # self.nombre.GetValue()
    
    def Cliente(self,e):
        self.tex1.Show(True)    
        self.nombre.Show(True)
        self.v_conectar.Show(True)
        self.modificar.Show(False)
        self.eliminar.Show(False)
        self.compartir.Show(False)
        self.v_conectar.SetLabel("Conectar")

    def OnTimer(self, event):
         self.list.DeleteAllItems()
         self.list.refrescar(self.nombre.GetValue())

    # Funcion para el boton conectar
    def Conectar(self,e):
        #inicia los servicios del servicor
        if self.v_conectar.GetLabel() == "Crear":
            print 
            print self.nombre.GetValue().encode("hex")    
            grupo6 = self.nombre.GetValue().encode("hex")
            my_grupo6 = "ff05::"+grupo6[:4]+":"+grupo6[len(grupo6)-4:len(grupo6)]
            print my_grupo6
            mu.main(1,my_grupo6,self.nombre.GetValue())
            self.list.DeleteAllItems()
            self.panelList.Show(True)
            self.v_conectar.Show(False)
            

        #inicia los servicios del cliente    
        if self.v_conectar.GetLabel() == "Conectar":
            print 'conectadoo'
            print self.nombre.GetValue().encode("hex")    
            grupo6 = self.nombre.GetValue().encode("hex")
            my_grupo6 = "ff05::"+grupo6[:4]+":"+grupo6[len(grupo6)-4:len(grupo6)]
            print my_grupo6
            mu.main(2,my_grupo6,self.nombre.GetValue())
            self.list.DeleteAllItems()
            self.panelList.Show(True)
            self.v_conectar.Show(False)
             
            
    

if __name__ == '__main__':
	app = wx.App(False)
	frame = MyFrame(None, 'DropBox IPV6')
	
	app.MainLoop()
