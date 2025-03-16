After downloading the CTF file and viewing it in details first we notice its an ELF, but when i ran
binwalk chal i noticed the following

![image](https://github.com/user-attachments/assets/40ab6ad2-9dc4-43ab-b5aa-32b00b411d50)

"Copyright the UPX Team" , which was a strong indicator it is compressed with UPX

upx -t chal  -- confirms the above is compressed and can be decompressed with upx

![image](https://github.com/user-attachments/assets/e160dbe6-a320-4abd-84eb-b0fb4befa912)


upx -d chal -o chal_de  -- to decompress


This time when I used ghidra I was able to view binary in full

Launch and analyze

Using ghidra I viewed all defined strings via Window > Defined strings
Which i found "Success!"

![image](https://github.com/user-attachments/assets/87b7e9a1-df62-49ad-b069-8d3648bf72c3)


Next I analysed the main function:

![image](https://github.com/user-attachments/assets/9df35b36-d0ba-46b7-92b9-16024a95f476)



From the main function we see:
puts(intro) - Prints "What is the Flag" for the user(us)
which then stores our input to variable "local_38"
checks if Ivar1 == 0 to print success (Meaning if our input local_38 matches local_68 (theFlag))

Next task - find how Local_68 is built

char local_68 [32] -- character array of 32 BYTES
we see the for loop which is used for in the main function

for (local_6c = 0; local_6c < 0x160; local_6c = local_6c + 0xb) {
  local_68[local_6c / 0xb] = arr_data[local_6c];
}

The above loop contains "arr_data", which itterates through arr_data, but only every 11th char(0xb in hex), and ensures it is placed sequentially in local_68

To find our flag we need to A. find arr_data and copy its character array B. Use python to store the array of arr_data and complete the same loop as above, but translate hex to us.


using Shift + E within Ghidra look for arr_data OR from Symbol Tree > Labels > select arr_data
and right click "make selection"

![image](https://github.com/user-attachments/assets/5d2e7daf-1087-4a68-b258-e28c5b8890f9)


Next in the arr_data in binary right click and select "Copy Special" >  C Array 

![image](https://github.com/user-attachments/assets/007357ea-8e26-4cdb-8d46-e9e97b9298b6)


Lastly, we need to create python script (reverse.py), I have this uploaded in this repo feel free to analyse and use it

And run your script!
