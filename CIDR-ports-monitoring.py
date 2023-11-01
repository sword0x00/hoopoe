import subprocess
import time


def CIDR_alert(domain, CIDRi, CIDR_dirPath, notifyId):
    try:
        # Replace / with _ in the CIDR range for the file name
        output_file = "{}new-CIDR({}).txt".format(CIDR_dirPath,
                                                  CIDRi.replace('/', '_'))

        print("Starting new CIDR Ports checkup on {}\n".format(domain))
        subprocess.run([
            "masscan",
            "-p", "8080,8001,8009,1311,2480,4444,4445,3333,4567,5000,5001,5104,5800,7000,7001,7002,8008,8042,8088,8222,8243,8280,8281,8333,8530,8531,8887,8888,8443,8834,9080,9443,9981,12043,12046,16080,18091,10443,18092,1010,1311,2082,2087,2095,2096,3000,3128,4243,4711,4712,4993,5108,6543,7396,7474,8000,8001,8008,8014,8069,8080,8081,8090,8091,8118,8088,8123,8172,8500,8880,8800,8983,9000,9043,9060,9090,9091,9200,9800,12443,20720,28017,0-1024",
            CIDRi,
            "--exclude", "255.255.255.255",
            "--banners",
            "-oX", output_file
        ])
        time.sleep(1800)  # Sleep for 30 minutes

        subprocess.run([
            "cat",
            output_file,
            "|",
            "anew",
            "{}CIDR({}).txt".format(CIDR_dirPath, CIDRi.replace('/', '_')),
            "|",
            "notify",
            "-p", "discord",
            "-id", notifyId,
            "-silent"
        ])
        time.sleep(182)  # Sleep for 3 minutes

        subprocess.run([
            "rm",
            output_file
        ])
        time.sleep(3)
        print("-" * 100 + "\n")
    except Exception as e:
        print("Error in CIDR_alert: {}".format(e))


def loop_on_CIDR_alert(domain, CIDR_dirPath, listOfCIDRs_filePath, notifyId):
    with open(listOfCIDRs_filePath, "r") as f:
        listOfCIDRs = f.readlines()

    for CIDRi in listOfCIDRs:
        CIDR_alert(domain, CIDRi.strip(), CIDR_dirPath, notifyId)


while True:  # This loop will run indefinitely until manually stopped
    loop_on_CIDR_alert("domain.com", "/path/Recon/domain/CIDR/",
                       "/path/Recon/domain/CIDR/list_OfCIDRs.txt", "your-notifyId")
    time.sleep(43200)  # Sleep for 12 hours
