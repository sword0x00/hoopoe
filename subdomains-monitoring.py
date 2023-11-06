import subprocess
import time


def new_subs_alert(domain, domainPath, notifyId):
    # current_day, current_time=get_current_day_time()

    print("Starting new subdomains checkup on {}\n".format(domain))
    subfinder = subprocess.Popen(
        "subfinder -d {} -o {}new-subdomains.txt -all -silent".format(domain, domainPath), shell=True)
    subfinder.wait()  # 10min
    subprocess.Popen("cat {}new-subdomains.txt | anew {}subdomains.txt | notify -p discord -id {} -silent".format(
        domainPath, domainPath, notifyId), shell=True)
    time.sleep(60)
    subprocess.Popen("rm {}new-subdomains.txt".format(domainPath), shell=True)
    time.sleep(1)
    httpx = subprocess.Popen(
        "cat {}subdomains.txt | httpx -sc -title -cl -wc -td | tee {}new-live-subdomains.txt".format(domainPath, domainPath), shell=True)
    httpx.wait()
    subprocess.Popen("cat {}new-live-subdomains.txt | anew {}live-subdomains.txt | notify -p discord -id {} -silent".format(
        domainPath, domainPath, notifyId), shell=True)
    time.sleep(60)
    subprocess.Popen(
        "rm {}new-live-subdomains.txt".format(domainPath), shell=True)
    time.sleep(1)
    subprocess.Popen(
        "echo \"Finished the process of {} \" | notify -p discord -id {} -silent".format(domain, notifyId), shell=True)
    time.sleep(3)
    print("-"*100+"\n")


while 1:
    new_subs_alert("domain.com", "/yourPath/Recon/domain/",
                   "your-notifyId-belong-to-discord-here")
    time.sleep(43200)  # 12 hours


# to run this script on your "VPS background", use this command: nohup python3 subdomains-monitoring.py &
