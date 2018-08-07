from burp import IBurpExtender
from burp import ISessionHandlingAction
from burp import IParameter
from java.io import PrintWriter
from datetime import datetime
import hashlib
import hmac
import base64
import sys

class BurpExtender(IBurpExtender, ISessionHandlingAction):
    #
    # implement IBurpExtender
    #
	
    global key;
    def registerExtenderCallbacks(self, callbacks):
        stdout = PrintWriter(callbacks.getStdout(), True)
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("HMAC Header")
        stdout.println("HMAC Header register")
        callbacks.registerSessionHandlingAction(self)
        stdout.println("Session handling")
        return	

    def getActionName(self):
        return "HMAC Header"

    def performAction(self, currentRequest, macroItems):
        #update me: key need to represent the key used to hash the data
        key	= "cd6b1f94e9d043e099a82b9ea357f1e5";
        stdout = PrintWriter(self._callbacks.getStdout(), True)
        stdout.println("performAction")
        requestInfo = self._helpers.analyzeRequest(currentRequest)

		#acquire token and timestamp
        headers = requestInfo.getHeaders()
        for header in headers:
            if(header.split(" ")[0]=="Authorization:"):
                token=header.split(" ")[2]
            elif(header.split(" ")[0]=="HMAC-Timestamp:"):
                timestamp=header.split(" ")[1]
        
        #acquire body
        msgBody = currentRequest.getRequest()[requestInfo.getBodyOffset():]
        msg=(''.join(chr(i) for i in msgBody))
        msg=(((msg.replace(" ","")).replace("\n","")).replace("\r","")).replace(" ","")
        		
        hashstring = token +":"+ timestamp +":"+ msg
        #stdout.println("hashstring: " + hashstring)
		
        hashstring = bytes(hashstring).encode('utf-8')
        key=bytes(key).encode('utf-8')
        _hmac = base64.b64encode(hmac.new(key, hashstring, digestmod=hashlib.sha256).digest())
		
        #hmac_sting=createHmac(hashstring)
        #headers.add('HMAC-Signature: %s' % _hmac)
        #stdout.println('HMAC-Signature: '+ _hmac)
        i=0
        for header in headers:
            if(header.split(" ")[0]=="HMAC-Signature:"):
                headers[i]="HMAC-Signature: "+ _hmac
            i=i+1


        # Build new Http Message with the new Hash Header
        message = self._helpers.buildHttpMessage(headers, msgBody)
        # Print Header into UI
        #stdout.println(message)

        # Update Request with New Header
        currentRequest.setRequest(message)
        return 
