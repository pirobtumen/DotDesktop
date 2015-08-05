from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty


# Load the views
Builder.load_file("dotdesktop.kv")

# Dialogs
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

# Views interfaces
class DotDesktop(Screen):
	pass

class MenuScreen(Screen):
	def dismiss_popup(self):
		self._popup.dismiss()
	
	def show_open(self):
		content = LoadDialog(cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
		                    size_hint=(0.9, 0.9))
		self._popup.open()
		
	


# Create the screen manager
sm = ScreenManager()

# Add views
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(DotDesktop(name='dotdesktop'))

# Main class
class DotDesktopApp(App):
	def build(self):
		
		# Window config
		Window.size = (300, 200)
		
		# Run ScreenManager  
		return sm

if __name__ == '__main__':
	app = DotDesktopApp()
	app.run()