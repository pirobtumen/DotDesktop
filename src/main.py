from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.properties import ObjectProperty

from kivy.uix.textinput import TextInput

import os
from os.path import expanduser

import stat

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
popup_height = window_width

class AlertPopup(Popup):
	'''
		AlertPopup
		==============================================================
	
		This class shows a Popup.
		The Popup can display:
			
			- Alert. It only display a message and a cancel button.
			- Prompt. If you pass a function to "on_accept" it will
					  display a second button, "OK" that will execute
					  the callback.
		
			- Both can display an extra message if you pas a string
			  to "msg".
		
		@param string	title
		@param string	msg [ optional ]
		@param function	on_accept [ optional ]
	'''
	
	def __init__(self, title, msg = '', on_accept = None, **kwargs ):
		super(AlertPopup, self).__init__( **kwargs )
		
		# Define object vars
		self.title = title
		self.size_hint = (0.5,0.6)
		self.accept_callback = on_accept
		
		# On dismiss
		self.bind( on_dismiss = self.close )
		
		# Principal layout
		layout = BoxLayout(orientation='vertical', padding=1)
		
		# Close button
		btn_close = Button( text='Close' )
		btn_close.bind(on_release=self.close )
		
		# Check if there is a message
		if msg != '':
			label = Label(text=msg)
			layout.add_widget(label)
		else:
			layout.size_hint = (0.9, 0.9)
		
		# Check if it's a prompt
		if self.accept_callback != None:
			button_layout = BoxLayout(spacing=1)
			
			btn_accept = Button(text='Ok')
			btn_accept.bind(on_release=self.accept)
			
			button_layout.add_widget(btn_accept)
			button_layout.add_widget(btn_close)
			layout.add_widget(button_layout)
			
		else:
			layout.add_widget(btn_close)
		
		# Create Popup
		self.add_widget(layout)
		self.open()
		
	def close( self, instance ):
		'''
			Closes the popup.
		'''
		self.dismiss()
		
	def accept(self, instance):
		'''
			Closes the poppup and calls the callback.
		'''
		self.close(instance)
		self.accept_callback(instance)

class OpenFileDialog( BoxLayout ):
	'''
		Widget that contains a FileChooser where
		the user can select a file.
		
			- open_file: function callback when press the open button.
			- close_dialog: function callback that closes the popup.	
	'''
	
	# Open button action
	open_file = ObjectProperty( None )
	
	# Close button action
	close_dialog = ObjectProperty( None )

class DotDesktop(BoxLayout):
	'''
		//////////////////////////
		//						//
		//	Main Screen Widget  //
		//						//
		//////////////////////////	
	'''
	
	# Get TextInput widgets from .kv
	txt_input_name = ObjectProperty(None)
	txt_input_desc = ObjectProperty(None)
	txt_input_path = ObjectProperty(None)
	txt_input_exec = ObjectProperty(None)
	txt_input_icon = ObjectProperty(None)
	
	def default_size(self, instance = ObjectProperty(None)):
		# Initial window size
		
		Window.size = (window_width,window_height);
	
	def close_popup(self, instance = ObjectProperty(None)):
		# Closes popup and restores size
	
		self.default_size()
		self.popup.dismiss()
	
	def show_popup(self, title, content):
		# Create a popup that contains the view
		self.popup = Popup(title=title, content=content,
		                    size_hint=(0.9, 0.9))
		
		# On dismiss
		self.popup.bind( on_dismiss = self.default_size )
		
		# Show the popup
		self.popup.open()
		
		# Resize the window
		Window.size = (popup_height,popup_width)
	
	def open_file( self ):
		# Open file button action
		
		# Load the FileChooser inside a Popup
		content = OpenFileDialog( open_file=self.read_file ,close_dialog = self.close_popup )
		
		# Get the user dir
		content.ids.open_file_chooser.path = expanduser('~')
		
		self.show_popup( "Open file", content )
	
	def read_file( self, files ):
		# Read the .desktop file
		
		# Open file
		file_txt = open( files[0] )
		
		# Parse
		file_dic = {}
		
		for line in file_txt:
			
			# Get a new line and split
			line_part = line.split("=")
			
			# If there are two parts
			if len(line_part) == 2:
				
				# Add new key to the dict.
				# You can access every '.dektop' property with
				# its name in lowercase and no spaces.
				file_dic[ line_part[0].replace(" ", "").lower() ] = line_part[1]
		
		# Set TextInput text
		self.txt_input_path.text = files[0]
		self.txt_input_name.text = file_dic.get("name","")
		self.txt_input_comment.text = file_dic.get("comment","")
		self.txt_input_exec.text = file_dic.get("exec","")
		self.txt_input_icon.text = file_dic.get("icon","")
		
		# Close file and Popup
		file_txt.close()		
		self.close_popup()
	
	def select_file(self, text_input ):
		# Open FileChooser and set TextInput text
		self.text_input = text_input
		
		# Load the FileChooser inside a Popup
		content = OpenFileDialog( open_file=self.set_textinput, close_dialog = self.close_popup )
		
		# Get the user dir
		content.ids.open_file_chooser.path = expanduser('~')
		
		# Show Popup
		self.show_popup( "Select file", content )
	
	def set_textinput(self, files):
		# Set TextInput text from FileChooser
		self.text_input.text = files[0]
		self.close_popup()
		
	def check_before_save(self, instance):
		# Save the file

		# Set file path
		self.file_path = self.txt_input_path.text

		# Check if file path is empty
		if self.file_path == '':
			AlertPopup("File path empty!")
		
		# Check if file exists
		elif os.path.isfile( self.file_path ):
			AlertPopup("Caution","Overwrite file?", self.save_file )
		
		# Save file
		else:
			self.save_file( instance )
		
	def save_file( self, instance ):
			# Write file data
			try:
				output_file = open( self.file_path, 'w' )
				output_file.write("[Desktop Entry]\n")
				output_file.write("Type=Application\n")
				output_file.write("Name=" + self.txt_input_name.text.replace('\n', "") + '\n' )
				output_file.write("Comment=" + self.txt_input_comment.text.replace('\n', "") + '\n' )
				output_file.write("Icon=" + self.txt_input_icon.text.replace('\n', "") + '\n' )
				output_file.write("Exec=" + self.txt_input_exec.text.replace('\n', "") + '\n')
				output_file.close()
				
				# Set execute permissions
				file_mode = os.stat( self.file_path )
				os.chmod( self.file_path, file_mode.st_mode | stat.S_IEXEC )
				
				#self.show_popup( "File saved!", AlertPopup() )
				AlertPopup("File saved!")
			
			# Manage exceptions
			except IOError:
				AlertPopup("Error while saving", "File can't be saved.")				
				
		
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