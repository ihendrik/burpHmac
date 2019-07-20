# just creating the gui not the session handling yet.
# will create session handling, tab in the proxy, maybe send a request to the GUI.
# hopefully can manage to spare time to create the project
from burp import IBurpExtender, ITab, ISessionHandlingAction
from javax import swing
from java.io import PrintWriter
from java.awt import BorderLayout
from javax.swing import ButtonGroup
import sys
try:
    from exceptions_fix import FixBurpExceptions
except ImportError:
    pass

class BurpExtender(IBurpExtender, ITab, ISessionHandlingAction):
    @staticmethod
    def tabDesign(self,callbacks):
        topPanel=swing.JPanel(BorderLayout())
	
		#create HMAC Key Text Area:
        keyPanel=swing.JPanel(BorderLayout())
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("HMAC Key")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        keyText = swing.JTextField(512)
        keyText.setText("secretkey")
        boxHorizontal.add(keyText)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        keyPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        topPanel.add(keyPanel, BorderLayout.NORTH) 
		
		#create HMAC Key Text Area:
        hsPanel=swing.JPanel(BorderLayout())
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("HashString")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        hsText = swing.JTextField(512)
        hsText.setText("<header>:<body>:<header:timestamp>")
        boxHorizontal.add(hsText)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        hsPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        topPanel.add(hsPanel, BorderLayout.CENTER) 
        
        bTopPanel= swing.JPanel()
		
        #create HMAC Key Text Area:
        slPanel=swing.JPanel(BorderLayout())
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("Signature Location")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        hsText = swing.JTextField(75)
        hsText.setText("<header:signature>")
        boxHorizontal.add(hsText)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        slPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        bTopPanel.add(slPanel, BorderLayout.NORTH) 

		#create HMAC Key Text Area:
        haPanel=swing.JPanel()
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("Hash Algorithm")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        rbPanel = swing.JPanel()
        radio1=swing.JRadioButton("SHA-1")
        radio2=swing.JRadioButton("SHA-256",True)
        radio3=swing.JRadioButton("SHA-512")
        group = swing.ButtonGroup()
        group.add(radio1)
        group.add(radio2)
        group.add(radio3)
        rbPanel.add(radio1)
        rbPanel.add(radio2)
        rbPanel.add(radio3)
        boxHorizontal.add(rbPanel)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        haPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        bTopPanel.add(haPanel, BorderLayout.CENTER)
		
		#create HMAC Key Text Area:
        sPanel=swing.JPanel()
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("Signature")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        rbPanel = swing.JPanel()
        radio1=swing.JRadioButton("HEX",True)
        radio2=swing.JRadioButton("BASE64")
        group = swing.ButtonGroup()
        group.add(radio1)
        group.add(radio2)
        rbPanel.add(radio1)
        rbPanel.add(radio2)
        boxHorizontal.add(rbPanel)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        sPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        bTopPanel.add(sPanel, BorderLayout.SOUTH)

        topPanel.add(bTopPanel, BorderLayout.SOUTH)
		
        self.tab.add(topPanel, BorderLayout.NORTH) 
		
		#create HMAC Key Text Area:
        logPanel=swing.JPanel(BorderLayout())
		# Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("Logs")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)
        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        logText = swing.JTextArea("",10,100)
        boxHorizontal.add(logText)
        boxVertical.add(boxHorizontal)
        # Add the text label and area to the text panel
        logPanel.add(boxVertical)
        # Add the text panel to the top of the main tab
        self.tab.add(logPanel, BorderLayout.SOUTH) 
		
		
        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        #return self
		
    def registerExtenderCallbacks(self, callbacks):
        
        # Required for easier debugging: 
        # https://github.com/securityMB/burp-exceptions
        stdout = PrintWriter(callbacks.getStdout(), True)

        # Keep a reference to our callbacks object
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        # Set our extension name
        callbacks.setExtensionName("HMAC Module")
		#set the session handling
        callbacks.registerSessionHandlingAction(self)

        # Create the tab
        self.tab = swing.JPanel(BorderLayout())
        self.tabDesign(self,callbacks)
        return
		

		
    #implement session handling
    def getActionName(self):
        #stdout.println("getActionName")
        return "HMAC Header"
		
    # Implement ITab
    def getTabCaption(self):
        """Return the text to be displayed on the tab"""
        return "HMAC Module"
    
    def getUiComponent(self):
        """Passes the UI to burp"""
        return self.tab

try:
    FixBurpExceptions()
except:
    pass
