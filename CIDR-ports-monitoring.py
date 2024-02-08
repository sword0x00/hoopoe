# This is a python script to run masscan tool on a list of CIDR ranges and check for open ports every 12 hours.
import subprocess
import time


# Define the func that take input and output file names and then remove the last column from the output file and save it to the output_afterfilter.txt file
def filter_output(input_file, output_file):

    # Open the input and output files
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Loop through each line in the input file
        for line in infile:
            # Split the line into columns using space as the delimiter
            columns = line.strip().split(' ')
            # Join the first (n-1) columns and write them to the output file
            outfile.write(' '.join(columns[:-1]) + '\n')

    # Close the files
    infile.close()
    outfile.close()


def CIDR_alert(domain, CIDRi, CIDR_dirPath, notifyId):
    try:
        # Replace / with _ in the CIDR range for the file name
        output_file = "{}new-CIDR_{}.txt".format(CIDR_dirPath,
                                                 CIDRi.replace('/', '_'))
        output_file_butAfterFiltering = "{}new-CIDR_afterFiltering_{}.txt".format(
            CIDR_dirPath, CIDRi.replace('/', '_'))
        print("Starting new CIDR Ports checkup on {}\n".format(domain))

        masscan_process = subprocess.Popen("masscan -p 8080,8001,3389,8009,1311,2480,4444,4445,3333,4567,5000,5001,5104,5800,7000,7001,7002,8008,8042,8088,8222,8243,8280,8281,8333,8530,8531,8887,8888,8443,8834,9080,9443,9981,12043,12046,16080,18091,10443,18092,1010,1311,2082,2087,2095,2096,3000,3128,4243,4711,4712,4993,5108,6543,7396,7474,8000,8001,8008,8014,8069,8080,8081,8090,8091,8118,8088,8123,8172,8500,8880,8800,8983,9000,9043,9060,9090,9091,9200,9800,12443,20720,28017,2375,10250,0-1024 {} --exclude 255.255.255.255 --banners -oL {}".format(CIDRi, output_file), shell=True)
        masscan_process.wait()  # Wait for the masscan process to finish

        subprocess.Popen("touch {}".format(
            output_file_butAfterFiltering), shell=True)
        time.sleep(1)  # Sleep for 2 second
        # Filter the output file to remove the last column
        filter_output(output_file, output_file_butAfterFiltering)
        subprocess.Popen("cat {} | anew {}CIDR_{}.txt | notify -p discord -id {} -silent".format(
            output_file_butAfterFiltering, CIDR_dirPath, CIDRi.replace('/', '_'), notifyId), shell=True)

        time.sleep(20)  # Sleep for 20 seconds
        if output_file or output_file_butAfterFiltering:
            command = ["rm", output_file]
            command2 = ["rm", output_file_butAfterFiltering]
            try:
                # Wait for the process to complete and check for errors
                subprocess.run(command, check=True)
                subprocess.run(command2, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error while deleting {output_file}: {e}")
        else:
            print("output_file is empty or invalid, so it cannot be deleted.")

        # return output_file_butAfterFiltering
        print("-" * 100 + "\n")
    except Exception as e:
        print("Error in CIDR_alert: {}".format(e))
        return None  # Handle errors and return None


def loop_on_CIDR_alert(domain, CIDR_dirPath, listOfCIDRs_filePath, notifyId):
    with open(listOfCIDRs_filePath, "r") as f:
        listOfCIDRs = f.readlines()

    for CIDRi in listOfCIDRs:
        CIDR_alert(domain, CIDRi.strip(), CIDR_dirPath, notifyId)


while True:  # This loop will run indefinitely until manually stopped
    loop_on_CIDR_alert("domain.com", "/yourPath/Recon/domain/CIDR/",
                       "/yourPath/Recon/domain/CIDR/list_OfCIDRs.txt", "your-notifyId-belong-to-discord-here")
    time.sleep(43200)  # Sleep for 12 hours


# to run this script on your "VPS background", use this command: nohup python3 CIDR-ports-monitoring.py &
