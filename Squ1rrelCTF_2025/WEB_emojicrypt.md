**Emoji encrypt:**

![1](https://github.com/user-attachments/assets/9dbd240b-eb5a-4282-8165-3e3ff22cade0)

The web application when we enter seems to be quite simple, registration form and login, what I found strange is the registration involves email and username and login is Username and password fields. 
Manually interacting with the application the furthest you can get is registering a new account.

![2](https://github.com/user-attachments/assets/1cd14cc9-313c-42a5-b953-52e40f2d0367)



And of course there will be no email sent, with this challenge we are also given the source , **index.html & app.py**

So let's review app.py

![3](https://github.com/user-attachments/assets/6c9a00c6-e17e-4b29-92e2-e88c1e84340e)


salt is generated using the **EMOJIS** array, picking 12 random emojis from the array and joining them together with the string "aa" in between them

![4](https://github.com/user-attachments/assets/faa33dd7-2ed2-4e57-a92b-deb6b0f592e0)



Register takes in email and username from the applicatiosn form,
salt is generated with the original function we looked at, random password is generated with 32 random numbers from the array above which is simply 0-9
and our password hash is
hashed using bcrypt.hashpw the function runs on salt + random_password, then if is encoded by UTF-8 because we are combining emojis and numeric password into a single string > encoding to UTF-8 so bcrypt can hash this (emojis and other non-ASCII ch. need to be encoded)

hashpw returns a BYTE string, in order to store this in a DB column it needs to be regular string(like text), 

![5](https://github.com/user-attachments/assets/9cbd0fd2-96eb-46e8-b1da-9ec091c538dd)



Login function essentially takes in the password does same hashing and compares with db stored details if its matched we get our flag

So we need to guess the password.. but a random 32 character password made up of numbers, is an insane amount of options, hence it's not an option here really..

I went to research mode about how I can exploit the process of password generation, and what I found that the pythons random module is not actually all that secure and random and if its undefined it is seeded with system time by default, which from research I found is very common to be used in CTF style challenge, the second I read this sentence I knew I stumbled upon my answer here.

Now the exciting part for me was more python, i have been really trying to improve my scripting without just using AI, after watching some videos online and other walkthroughs of somewhat similar challenge, I had the logic in place.

Reverse the function in original script > reconstruct seed/state used by server(timestamp as no seed provided) > use random.seed() with my own script using the known seed(timestamp) and generate the pass

**Register account with date and time:**
I used curl so I can use -i to grab the time of the server

curl -i -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "email=linax001@linax.com&username=linax001" http://52.188.82.43:8060/register

![6](https://github.com/user-attachments/assets/877b9e1e-42b7-407d-a5cd-71fd518b268d)


The response tells me the redirection is to /?registered=true

next was to replicate the password generation with the timestamp (https://github.com/LinasRadavicius/CTF/tree/main/Squ1rrelCTF_2025) I used my first script **passTime.py** in which I had the exact timestamp of when the account was created, however after multiple attempts I was unable to get passed this,

 So I ended up coding an offset, to generate 60 password using 60 different timestamps, 30seconds before and after creation, just in case the time is slightly off, script it using python called it timeOffset.py, this generated 60 passwords and output to wordlist timestamps.txt

Last step is to try authenticate with the passwords that the above script made, if you have burp pro use intruder is the fastest option, but you can also use ffuf and curl with a bash script, I used intruder, but I'll show how it could be done using ffuf.

ffuf -u http://52.188.82.43:8060/login -X POST -d "username=linax99&password=FUZZ" -H "Content-Type: application/x-www-form-urlencoded" -w timestamp.txt -fc 302

I filtered out 302 redirect, but many other filtering options to get the same result.

Also advice run the code on online IDE, my local time settings or python version were the reason the generated passwords were different to the one the IDE generated, and the correct answer was in the list of generated passwords by the IDE https://www.online-python.com/


![7](https://github.com/user-attachments/assets/c03a0d94-6237-4f9f-b268-d3e29a4323f0)
![8](https://github.com/user-attachments/assets/20e53ace-80f0-4781-964f-38f08798f967)




**Preventing this vulnerability:**
	- AVOID pythons module random it is not suitable for crypto apps as its predictable, use pythons secrets module
VALIDATE RANDOMNESS![image](https://github.com/user-attachments/assets/5b5bff48-3788-42f5-827d-f85ed422d3c3)
