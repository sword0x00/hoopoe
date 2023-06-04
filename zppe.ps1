param(
    
    [parameter(Mandatory=$true)]
    $D,
    [parameter(Mandatory =$false)]
    $OutFile

)
###############################################################

function TurnToHackerone([string]$InputParameter) {
  # Remove the ".com" from the input parameter.
  $OutputParameter = $InputParameter.Replace(".com", "")

  # Return the output parameter.
  return $OutputParameter
}

#==================================you target will be here ===============================
$NewDir=TurnToHackerone($D)
mkdir -Path \Recon\$NewDir

$allsubs_txt=New-Item -Path \Recon\$NewDir\AllSubDomains.txt -ItemType File

#==================================subfinder===============================
$subfinder_txt=New-Item -Path \Recon\$NewDir\subfinder.txt -ItemType File
$OutFile=$subfinder_txt
subfinder.exe -d $D -o $OutFile

#==================================assetfinder===============================
$assetfinder_txt=New-Item -Path \Recon\$NewDir\assetfinder.txt -ItemType File
$OutFile=$assetfinder_txt
assetfinder.exe -subs-only $D |Out-File $OutFile 

#==================================amass===================================
$amass_txt=New-Item -Path \Recon\$NewDir\amass.txt -ItemType File
$OutFile=$amass_txt
amass enum -passive -norecursive -noalts -d $D -o $OutFile

#==================================findomain===============================
$findomain_txt=New-Item -Path \Recon\$NewDir\findomain.txt -ItemType File
$OutFile=$findomain_txt
findomain -t $D --external-subdomains -u $OutFile

#==================================chaos===================================
$chaos_txt=New-Item -Path \Recon\$NewDir\chaos.txt -ItemType File
$OutFile=$chaos_txt
chaos.exe -d $D -o $OutFile -key you_API_token 

#==================================final results==================================
type $subfinder_txt |anew.exe $allsubs_txt
type $assetfinder_txt | anew.exe $allsubs_txts
type $amass_txt | anew.exe $allsubs_txt
type $findomain_txt | anew.exe $allsubs_txt
type $chaos_txt | anew.exe $allsubs_txts

#subdomain_take_over_check__this func will output two files one-> statusservers_details.txt & another one-> cnames.txt
# if you opervede that the status code in statusservers_details is [500] unknown domain the try to go to check the CNAME in cnames
#reference https://infosecwriteups.com/fastly-subdomain-takeover-2000-217bb180730f
httpx.exe -l \Recon\$NewDir\AllSubDomains.txt -cname -o \Recon\$NewDir\Cnames.txt
httpx.exe -l \Recon\$NewDir\AllSubDomains.txt -p 80,443,8080,3000 -status-code -title -o \Recon\$NewDir\Servers_details.txt


