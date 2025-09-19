# Search for CVE PoC

## **Intro**

*“Search by CVE-ID and open* https://nvd.nist.gov/ *then see the metric  cvss.0×3. if it is from network and no privilege required && after that go description and see if you can exploit (normally) or you need to access something in local network(hard) .. if all clear? .. then search for your poc.”*

## Check list

- [X] Google  —> search by "Technology" "Version" vulnerabilities.
   - Ex: Tomcat 3.4.3 vulnerabilites
   - Ex: Tomcat 3.6.6 CVEs
   - EX: Tomcat 3.5.3 publicly available exploits
   - Ex: Apache 9.1.1 proof of concepts (PoCs)
   - Ex: Apache 9.1.3 exploits
- [ ] https://cvexploits.io/ —> search by CVE-ID  or by technology.
- [ ] https://exploit-db.com —> search by your Technology or by CVE-ID or anything.
- [ ] Google —> search by “CVE-ID  GitHub”
    - Ex1: CVE-2024-22245 GitHub
    - Ex2: CVE-2024-22245 github.com
    - Ex3: Apache 3.9.6 exploit metasploit github
- [ ] Twitter —> search by CVE-ID
- [ ] Searchsploit tool on Kali Linux by :
    
  ```jsx
    > searchsploit nginx
    > searchsploit tomcat
    > searchsploit -p 12345
    > cat path.txt
    > searchsploit -update
  ```
- [ ] search on Metasploit tool by:
    
    ```jsx
    msf> search nginx 
    or 
    msf> search tomcat
    ```
    
- [ ] look for commits random ids and see the green and red lines of code in GitHub

## References:

- Exploitation playbook book by Alex Thomas.
- https://www.youtube.com/watch?v=t4KE-p2eCbY
