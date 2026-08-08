# Roblox-Scanner-Python-Tool
This is a tool developed by me with the help of **AI** to scan Roblox accounts information like friends, followers, etc etc by only entering the accounts username/ID, using Roblox's Public APIs.

## Features
* Easy Search: Search by Username or ID.
* Status: Check if the user is online, offline, or in Studio.
* Dynamic Installer: Automatically installs dependencies like Rich, Fade, etc.
* Clean interface: Simple and optimized ASCII design for all Windows terminals.

## AI Disclosure
I made this fully with AI no mercy

## Posible Errors:
### User appears offline while playing:
This usually happens because the user has their "Who can see my presence" setting is set to "No One" or "Friends". The Public API will return "Offline" This is a restriction from Roblox's side to protect user privacy.

### "ModuleNotFoundError" or "Library missing":
Even though the script has a auto-installer, some environments (like restricted folders) might block it.
Fix: Manually install the dependencies/librarys.
<pre>
  not today
&gt; pip install rich fade requests
</pre>
### 3. "User Not Found"
* **Reason:** You might be using a **Display Name** instead of a **Username**, or the user has been recently banned.
* **Fix:** Try searching by the **User ID** (the numbers in their profile URL). It is the most accurate way to find an account.

### 4. Strange symbols in the terminal
* **Reason:** Old versions of CMD or PowerShell might not support certain ASCII characters.
* **Fix:** I recommend using **Windows Terminal** or ensuring your console is set to use a modern font like *Consolas* or *Lucida Console*.
