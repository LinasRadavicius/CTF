Go Getter - Web Challange

![image](https://github.com/user-attachments/assets/71464558-4a02-4f0e-b0b8-22e114e37456)

Upon entering the application, it looks to be two functions "getgopher" & "getflag" , both are POST request to /execute endpoint.

The data passed in is in JSON format like 

{"action":"getgopher"}

When I send in getgopher it retrieves an image of a "gopher" and if I try to retrieve a flag we receive an error that requires us to be an admin to view the flag.
With this challange the source code was provided, the first step I took was to review the code
Summary of the application source : main.go written in GO which servers the webpage with embedded JS, this is where it allows the users to choose an action getgopher or getflag, and send POST request to the GO backend

![image](https://github.com/user-attachments/assets/114859d9-4a58-4a9f-b5ce-6523a479e4f6)



PYTHON app basically is the logic

I'm not going to bore you with all the ways I attempted to exploit this vuln, but walk you through how I got to the point here I did, First in golang here is the parser for incoming JSON data

![image](https://github.com/user-attachments/assets/cd5b2e6d-b9f4-4ca0-b89c-193e9e9a4b90)


	- It Parses the first matching field from the JSON ^ , GO's json/encoding is case-insensitive for field tags, but will only use the first match when duplicate keys exist,
	
	Using BURP I edit my request to send following JSON data
	{"action":"getflag","AcTiOn":"getgopher"}
	
	![image](https://github.com/user-attachments/assets/c6eede28-c79b-4d8a-8e9b-658f7878d3bd)

	The reason it worked:
	in python dictionaries are case-sencitive the code in app.py EXPLICITLY looks for the below
	if data['action'] == "getgopher";
	the reason this exploit works is because PYTHON does not validate that there is only one key, so what happens is GO reads the "action" key and ignores "AcTiOn" - it doesnt matter where the capitals are but the word must be action and have at least one capital somewhere in the key, GO Sends this request but still forwards the request to python, with no security controls against this in Python it returns our flag
	
	To prevent:
	Code input validation to only allow one key, and ensure its case sensitive by reverting all keys from POST /execute to lowercase, Backend services enforce access control and not rely on frontend logic.
![image](https://github.com/user-attachments/assets/65330f8b-7d7a-435f-835c-7f65dc3bfd4c)
