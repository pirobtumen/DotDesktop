from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.config import Config

Builder.load_file("dialogs.kv")

# Open file dialog
class OpenFileDialog( BoxLayout ):
	open_file = ObjectProperty( None )
	close_dialog = ObjectProperty( None )

# Main Screen
class DotDesktop(BoxLayout):
	def close_popup(self):
		self._popup.dismiss()
	
	def open_file(self):
		content = OpenFileDialog( close_dialog = self.close_popup )
		self._popup = Popup(title="Open file", content=content,
		                    size_hint=(0.9, 0.9))
		self._popup.open()

# Main class
class DotDesktopApp(App):
	def build(self):		
		# Window size
		Window.size = (540, 200)
		
		# Window background color
		Window.clearcolor = (0.20,0.20,0.20,1)
		
		# Window config
		Config.set('graphics','resizable', 0 )
		
		# Update config
		Config.write()
		
		# Run ScreenManager  
		return DotDesktop()


if __name__ == '__main__':
	app = DotDesktopApp()
	app.run()