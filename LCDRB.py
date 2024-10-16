import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from i2clcd import i2clcd

class LCDRB(Gtk.Window):
    def __init__(self):
        super().__init__(title="lcd...rb")
        self.set_size_request(270, 150)

        #Creamos un objeto lcd
        self.lcd = i2clcd(1,0x27,20) 

        # Crear un VBox para organizar widgets verticalmente
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.add(vbox)

        # Crear un TextView para ingresar texto multilinea
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.CHAR)

        #Ajustamos el tamano de la textview para que parezc un LCD
        self.textview.set_size_request(220,100) 
        # Ajustar la fuente que se va a ver en el textview
        font_desc = Pango.FontDescription("Monospace 16")
        self.textview.modify_font(font_desc)
        #almacenamos lo que va a poner el usuario en el textview
        self.textview.get_buffer().create_tag("font_tag", font=font_desc.to_string())

        vbox.pack_start(self.textview, True, True, 0)

        # Boton para enviar el texto al LCD
        self.button = Gtk.Button(label="Display")
        self.button.set_size_request(40, 20)  
        self.button.connect("clicked", self.on_button_clicked)
        
        frame= Gtk.Frame()
        frame.set_label("")
        frame.set_border_width(5)
        frame.add(self.button)
  

        vbox.pack_start(frame, True, True, 0)

        # Conectar la senal de cierre de la ventana
        self.connect("destroy", Gtk.main_quit)

    def on_button_clicked(self, widget):
        buffer = self.textview.get_buffer()  
        text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True) 

        lines = text.splitlines() 
        for line_num, line in enumerate(lines):
            if line_num < 4: 
                line = line[:20] 
                self.lcd.print_line(line, line_num)  

        buffer.set_text("") 

# Ejecutar la aplicacion
if __name__ == "__main__":
    app = LCDRB()
    app.show_all()
    Gtk.main()