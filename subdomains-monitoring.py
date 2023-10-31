import subprocess, time


def new_subs_alert(domain,domainPath, notifyId):

    print("Starting new subdomains checkup on {}\n".format(domain))
    subprocess.Popen("subfinder -d {} -o {}new-subdomains.txt -all -silent".format(domain, domainPath), shell=True)
    time.sleep(600)#10min
    subprocess.Popen("cat {}new-subdomains.txt | anew {}subdomains.txt | notify -p discord -id {} -silent".format(domainPath, domainPath,notifyId), shell=True)
    time.sleep(60)#1min
    subprocess.Popen("rm {}new-subdomains.txt".format(domainPath), shell=True)
    time.sleep(1)
    subprocess.Popen("cat {}subdomains.txt | httpx -sc -title -cl -wc -td | tee {}new-live-subdomains.txt".format(domainPath, domainPath), shell=True)
    time.sleep(1200)#20min
    subprocess.Popen("cat {}new-live-subdomains.txt | anew {}live-subdomains.txt | notify -p discord -id {} -silent".format(domainPath, domainPath,notifyId), shell=True)
    time.sleep(60)
    subprocess.Popen("rm {}new-live-subdomains.txt".format(domainPath), shell=True)
    time.sleep(1)
    subprocess.Popen("echo \"Finished the process of {} \" | notify -p discord -id {} -silent".format(domain, notifyId), shell=True)
    time.sleep(3)
    print ("-"*100+"\n")

while 1:
    new_subs_alert("domain.com","/your/Path/here/", "your-notify-id-here")
    time.sleep(14400)# 4 hours