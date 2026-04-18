"""
Cisco Packet Tracer Lab
Creating a Cyber World
NSW Lab 2 | Department of Computer Science and IT
Assessment 1 Weekly Submission | Worth: 1.5%

Overview & Lab Objective
In this lab, you will build and configure a simulated corporate network using Cisco Packet Tracer (CPT). Think of it like setting up a real company's IT infrastructure from scratch. You will install and configure six essential services across three servers, then verify everything works as expected.

By the end, your virtual network will support:
1. File sharing via FTP
2. A working company website via HTTP/HTTPS
3. Domain name resolution via DNS
4. Internal company email via SMTP/POP3
5. Synchronised network clocks via NTP
6. Centralised user authentication via AAA

Real-World Analogy
Imagine you are the IT manager for Metropolis Bank. The bank has just moved into a new building and you need to set up all the digital infrastructure from scratch: file servers, a website, email, and security systems. That is exactly what this lab simulates.

Video Reference:
https://www.youtube.com/watch?v=t34Ku3fdU14

Addressing Table
- FTP/Web Server: 10.44.1.254 / 255.255.255.0 / Metropolis Bank HQ
- Email/DNS Server: 10.44.1.253 / 255.255.255.0 / Metropolis Bank HQ
- NTP/AAA Server: 10.44.1.252 / 255.255.255.0 / Metropolis Bank HQ
- File Backup Server: 10.44.2.254 / 255.255.255.0 / Gotham Healthcare Branch

What is an IP Address?
An IP address is like a street address for a device on a network. Just as 123 Main Street tells the mail carrier exactly where to deliver a package, the IP address 10.44.1.254 tells the network exactly where to send data for the FTP/Web Server.

Lab Preparation Checklist
1. Ensure Cisco Packet Tracer is installed and you are logged into your Cisco Networking Academy account.
2. Open the provided .pka file (Creating_a_Cyber_World.pka) in Packet Tracer.
3. Work in a group for the first 30 minutes, then follow the video guide if needed.
4. Take screenshots at three key moments: start, midway, and end of your lab.

Important: Plagiarism
All written explanations must be in your own words. Do not copy from the video transcript or other students. You are welcome to reference the lab video for guidance on steps, but the written analysis must be original.

Part 1: Configure the FTP Server
FTP (File Transfer Protocol) is one of the oldest and most commonly used methods for transferring files across a network. In this part, you will activate FTP on the server and create user accounts that allow controlled access.

Analogy: FTP is Like a Shared USB Drive
Imagine the FTP server as a shared USB drive plugged into the company network. Instead of physically passing a USB stick around, employees can log in remotely and upload or download files. The user accounts you create control who is allowed to access that drive and what they can do with it.

Step 1: Activate the FTP Service
1. Click on the Metropolis Bank HQ building in Packet Tracer.
2. Click on the FTP/Web Server device.
3. Click the Services tab at the top of the server window.
4. Click FTP from the left-side menu.
5. Click the On radio button to activate the FTP service.

Screenshot Tip - Starting Point
Take your first screenshot here after enabling FTP. Your screenshot should clearly show the Services tab open on FTP, with the service toggled ON.

Step 2: Create User Accounts with Full Permissions
1. In the FTP configuration window, find the user account section.
2. Create the following accounts, each with password cisco123:
   - bob
   - mary
   - mike
3. For each user, make sure all permission boxes are checked:
   - R (Read)
   - W (Write)
   - D (Delete)
   - Rename
   - N (Navigate)
   - L (List)
4. Click Add after entering each user.

What Does RWDNL Mean?
Think of RWDNL as the keys you give an employee for the filing room. Read means they can look at files. Write means they can add new ones. Delete means they can throw old ones away. Navigate means they can browse folders. List means they can see what is in each folder. Giving someone all five keys means total access.

Screenshot Tip - Midway
After creating all three users with full permissions, take a screenshot showing the complete user list on the FTP server.

Part 2: Configure the Web Server
The same physical server that hosts FTP also hosts the company website. In this section, you will enable HTTP and HTTPS so employees and customers can browse the bank's internal web page. You will also test what happens when DNS is not yet configured.

Analogy: HTTP vs HTTPS is Like a Postcard vs a Sealed Envelope
HTTP sends data across the network in plain text, like writing your message on a postcard that anyone can read. HTTPS encrypts that data first, like sealing the message in an envelope.

Step 1: Activate HTTP and HTTPS
1. With the FTP/Web Server still open, click HTTP from the left-side Services menu.
2. Turn ON both HTTP and HTTPS using their respective radio buttons.

Step 2: Verify Sally's IP Configuration
1. Click on PC Sally, then click the Desktop tab, then open IP Configuration.
2. Check the current IP address shown. It should be 10.44.1.4 with subnet mask 255.255.255.0.
3. If it is different, correct it now.
4. Enter the following values:
   - IP Address: 10.44.1.4
   - Subnet Mask: 255.255.255.0
   - Default Gateway: 10.44.1.1
5. Close the IP Configuration window once the settings are saved.

Why This Matters
Sally's PC must be on the same subnet as the servers to communicate with them. The default gateway tells her PC how to reach devices outside the local network, and the DNS server will later help resolve names to IP addresses.

Step 3: Test Web Access Before DNS
1. Click on the PC named Sally in the network.
2. Click the Desktop tab, then click Web Browser.
3. Try browsing to: www.cisco.corp. This will fail.
4. Now try browsing to: 10.44.1.254. This will succeed.

Reflection Question
Why can Sally browse to the IP address 10.44.1.254 but not to the name www.cisco.corp?

Screenshot Tip
Take two screenshots:
- one showing the failed attempt to load www.cisco.corp
- one showing the successful load using the IP address

Part 3: Configure the DNS Server
DNS allows humans to use easy-to-remember names instead of IP addresses.

Analogy: DNS is the Internet's Phone Book
When you type www.cisco.corp, your computer asks the DNS server what IP address belongs to this name.

Step 1: Activate the DNS Service
1. Click on the Email/DNS Server in Metropolis Bank HQ.
2. Go to Services > DNS.
3. Turn on the DNS service.

Step 2: Create DNS A Records
1. Create the first A record:
   - Name = email.cisco.corp
   - IP = 10.44.1.253
2. Create the second A record:
   - Name = www.cisco.corp
   - IP = 10.44.1.254

What is an A Record?
An A Record maps a hostname directly to an IPv4 address.

Step 3: Verify DNS is Working
1. Return to PC Sally > Desktop > IP Configuration.
2. Set DNS Server: 10.44.1.253
3. Return to PC Sally > Desktop > Web Browser.
4. Browse to www.cisco.corp.
5. This time it should load successfully.

Reflection Question
Why is Sally now able to browse to www.cisco.corp when she could not before?

Screenshot Tip
Take a screenshot showing www.cisco.corp loading successfully in the web browser. Include the DNS A records in another screenshot if possible.

Part 4: Configure the Email Server
Email relies on SMTP for sending and POP3 for receiving.

Analogy: SMTP and POP3 are Like a Post Office and a Mailbox
SMTP is like the postal worker who sends the letter. POP3 is like the mailbox where users retrieve delivered mail.

Step 1: Activate SMTP and POP3
1. Click the Email/DNS Server > Services > EMAIL.
2. Turn ON SMTP.
3. Turn ON POP3.

Reflection Question
Why does the email service require both SMTP and POP3 to be activated?

Step 2: Create the Email Domain and User Accounts
1. In the EMAIL configuration, set the domain name to: cisco.corp
2. Create the following user accounts, all with password cisco123:
   - phil
   - sally
   - bob
   - dave
   - mary
   - tim
   - mike

Step 3: Configure Email Clients on PCs

For PC Sally:
- Name: Sally
- Email Address: sally@cisco.corp
- Incoming Mail Server: email.cisco.corp
- Outgoing Mail Server: email.cisco.corp
- Username: sally
- Password: cisco123

For PC Bob:
- Name: Bob
- Email Address: bob@cisco.corp
- Incoming Mail Server: email.cisco.corp
- Outgoing Mail Server: email.cisco.corp
- Username: bob
- Password: cisco123

Screenshot Tip
Take a screenshot of the completed email configuration on Sally's PC. If time allows, send a test email from Sally to Bob and take a screenshot of Bob receiving it.

Part 5: Configure the NTP Server
NTP keeps all devices on the network synchronised to the same clock.

Analogy: NTP is Like Setting All the Clocks in a Building
Accurate time is critical for security logs, authentication tokens, digital certificates, and troubleshooting.

Step 1: Activate the NTP Service
1. Click the NTP/AAA Server > Services > NTP.
2. Turn on the NTP service.

Step 2: Secure NTP with Authentication
1. Enable the NTP Authentication feature.
2. Set Key 1 with a password of cisco123.

Why Authenticate NTP?
Without authentication, any rogue device on the network could pretend to be the NTP server and feed incorrect times to all devices.

Screenshot Tip
Capture the NTP configuration screen showing both the service is ON and the authentication key is configured.

Part 6: Configure the AAA Server
AAA stands for Authentication, Authorisation, and Accounting.

Analogy: AAA is Like a Security Guard at a Bank
- Authentication = Who are you?
- Authorisation = What are you allowed to do?
- Accounting = What did you do and when?

Step 1: Activate the AAA Service
1. Click the NTP/AAA Server > Services > AAA.
2. Turn on the AAA service.

Step 2: Configure AAA Network Client
Enter:
- Client Name: HQ_Router
- Client IP: 10.44.1.1
- Secret: cisco123

Step 3: Create an AAA User Account
Create:
- Username: admin
- Password: cisco123

The Shared Secret Explained
The secret is like a private password known only to the router and the AAA server.

Screenshot Tip - End Point
Take your final screenshot here. The AAA configuration screen should show both the HQ_Router client and the admin user account configured.

Final Submission Checklist
1. Screenshot 1: Starting Point - initial server layout visible
2. Screenshot 2: Midway Point - at least two or three services configured
3. Screenshot 3: Ending Point - all six services configured and the AAA screen visible

Written explanation must include:
1. A brief summary of what each service does and why it matters.
2. Answers to the three reflection questions in Parts 2, 3, and 4.
3. A description of what the lab taught you about real-world network infrastructure.

Submission Reminder
Submit your screenshots and written explanation via the LMS Lab 02 submission link before Week 5 Monday at 23:59. This assessment is worth 1.5%. Ensure all work is in your own words.
"""

def get_lab_guide() -> str:
    """Return the full lab guide as a string."""
    return __doc__ or ""

if __name__ == "__main__":
    print(get_lab_guide())
