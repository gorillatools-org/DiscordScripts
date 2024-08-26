import json
import asyncio
import requests

# useragent cus why not (not necessary)
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 OPR/81.0.4196.31"

auth = input("[+] Your Discord Token -» ")
recipients = [
    "", # id 1
    "", # id 2 and so on...
]

async def gc_spam():
    gc_resp = await asyncio.to_thread(requests.post, "https://ptb.discord.com/api/v9/users/@me/channels", headers={
        "Authorization": auth,
        "Content-Type": "application/json",
        "Host": "ptb.discord.com",
        "User-Agent": str(ua)
    }, data=json.dumps({"recipients": recipients}))
    r = gc_resp.json()
    print(r)
    
    if gc_resp.status_code == 429:
        s = r["retry_after"]
        print("Got Limited, attempting to wait: " + str(s) + "s")
        await asyncio.sleep(s) # do not remove this fuck nigga
    else:
        gc_id = r["id"]
        await asyncio.to_thread(requests.delete, f"https://ptb.discord.com/api/v9/channels/{gc_id}?silent=true", headers={
            "Authorization": auth,
            "Content-Type": "application/json",
            "Host": "ptb.discord.com",
            "User-Agent": str(ua)
        })

async def main():
    while True:
        await gc_spam()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("\n[!] Safely Handled Ctrl+C :P\n")
        exit()
