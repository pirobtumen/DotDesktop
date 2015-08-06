from kivy.app import App

from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder

from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty

from kivy.uix.textinput import TextInput

from os.path import expanduser
import re

# Personalize widgets
TextInput.cursor_color = (0,0,0,1)

# No resizable window
Config.set('graphics', 'resizable', 0)
Config.write()

# Load dialogs gui
Builder.load_file("dialogs.kv")

# Window size
window_width = 540
window_height = 250

popup_width = 500
popup_height = 500

# Open file dialog
class OpenFileDialog( BoxLayout ):
	
	# Open button action
	open_file = ObjectProperty( None )
	
	# Close button action
	close_dialog = ObjectProperty( None )

# Main Screen
class DotDesktop(BoxLayout):
	
	def default_size(self, instance = ObjectProperty(None)):
		# Initial window size
		
		Window.size = (window_width,window_height);
	
	def close_popup(self):
		# Closes popup and restores size
	
		self.default_size()
		
		self.popup.dismiss()
	
	def show_popup(self, content):
		# Create a popup that contains the view
		self.popup = Popup(title="Open file", content=content,
		                    size_hint=(0.9, 0.9))
		
		# Get the user dir
		content.ids.open_file_chooser.path = expanduser('~')
		
		# If the user clicks out
		self.popup.bind( on_dismiss = self.default_size )
		
		# Show the popup
		self.popup.open()
		
		# Resize the window
		Window.size = (popup_height,popup_width)
	
	def open_file( self ):
		# Open file button action
		
		# Load the FileChooser inside a Popup
		content = OpenFileDialog( open_file=self.read_file ,close_dialog = self.close_popup )
		
		self.show_popup( content )
	
	def read_file( self, files ):
		# Read the .desktop file
		
		
		
		self.close_popup()
	
	def select_file(self, text_input ):
		# Open FileChooser and set TextInput text
		self.text_input = text_input
		
		# Load the FileChooser inside a Popup
		content = OpenFileDialog( open_file=self.set_textinput ,close_dialog = self.close_popup )
		
		self.show_popup( content )
	
	def set_textinput(self, files):
		# Set TextInput text from FileChooser
		self.text_input.text = files[0]
		self.close_popup()
		
# Main class
class DotDesktopApp(App):
	def build(self):		
		# Window size
		Window.size = (window_width, window_height)
		
		# Window background color
		Window.clearcolor = (0.20,0.20,0.20,1)
		
		# Run ScreenManager  
		return DotDesktop()


if __name__ == '__main__':
	
	# Run app
	DotDesktopApp().run()