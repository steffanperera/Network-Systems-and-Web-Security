"""
NSW Lab 3
Telnet, SSH, Packet Sniffing, and Firewall / ACL
Department of Computer Science and IT
Assessment 1 Weekly Submission | Worth: 1.5%

Overview & Lab Objective
In this lab, you will learn how remote access and basic firewall rules work in Cisco Packet Tracer.
The main focus is comparing Telnet and SSH, then using packet sniffing to see why Telnet is unsafe and
why SSH is preferred. You will also configure Access Control Lists (ACLs) to control which devices can
access the router or server.

By the end of this lab, your Packet Tracer network should demonstrate:
1. Remote router access using Telnet
2. Secure remote router access using SSH
3. Packet sniffing to compare Telnet and SSH traffic
4. Firewall-style filtering using Standard and Extended ACLs

Real-World Analogy
Imagine a company network where administrators need to manage routers remotely. Telnet is like sending
your password on a postcard because anyone who captures the traffic can read it. SSH is like sending the
same information inside a locked envelope because the traffic is encrypted. ACLs are like security guards
that decide who is allowed to enter certain parts of the network.

Reference Videos
- Telnet: https://www.youtube.com/watch?v=h5YdirpB53o
- SSH: https://www.youtube.com/watch?v=Rkp3sR__rds
- Configuring SSH on a router: https://www.youtube.com/watch?v=qPoPAmHeB1M
- Firewall / ACL: https://www.youtube.com/watch?v=yLOYd87z2jg

Important: Plagiarism
All written explanations must be in your own words. You may use the lab guide and video references for
help, but your screenshots and reflection must be based on your own Packet Tracer work.

Part A: Configure Telnet
Telnet allows a user to remotely log in to a router and type commands. However, Telnet does not encrypt
traffic. This means usernames, passwords, and commands can be seen by a packet sniffer.

Analogy: Telnet is Like a Postcard
A postcard can be read by anyone who sees it. Telnet works in a similar way because the password is sent
in readable plain text.

Lab Setup
Use the following devices in Cisco Packet Tracer:
- 1 Router, such as 2620XM or similar
- 1 Switch, such as 2960-24TT
- 1 PC

Connections:
- PC0 FastEthernet0 to Switch Fa0/1
- Switch Fa0/0 to Router Fa0/0
- Use copper straight-through cables

Step A1: Configure the Router Interface and Enable Password
Open the Router CLI and enter:

Router> enable
Router# configure terminal
Router(config)# interface FastEthernet 0/0
Router(config-if)# ip address 10.0.0.1 255.0.0.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# enable password cisco
Router(config)# end
Router# write memory

Why this matters:
The router interface needs an IP address so the PC can communicate with it. The no shutdown command is
important because router interfaces are disabled by default. The enable password protects privileged mode.

Step A2: Enable Telnet on the VTY Lines
VTY lines are virtual terminal lines used for remote access. Enter:

Router# configure terminal
Router(config)# line vty 0 15
Router(config-line)# password cisco
Router(config-line)# login
Router(config-line)# transport input telnet
Router(config-line)# exit
Router(config)# end
Router# write memory

Step A3: Configure PC0
On PC0, go to Desktop > IP Configuration and set:
- IP Address: 10.0.0.2
- Subnet Mask: 255.0.0.0
- Default Gateway: 10.0.0.1

Then open Command Prompt and test:

C:\> ping 10.0.0.1

Expected result:
You should receive replies from 10.0.0.1. This confirms that the PC can reach the router.

Step A4: Connect Using Telnet
On PC0 Command Prompt, type:

C:\> telnet 10.0.0.1
Password: cisco
Router>
Router> enable
Password: cisco
Router#

Expected result:
The Router# prompt means you have successfully logged in remotely and entered privileged mode.

Reflection Point
Telnet works for remote access, but it is insecure because the password travels across the network in
plain text.

Part B: Configure SSH
SSH also allows remote login, but it encrypts the communication. SSH is the safer replacement for Telnet.
Cisco routers need a hostname, domain name, RSA keys, and a local user account before SSH can work.

Analogy: SSH is Like a Locked Envelope
Even if someone captures SSH packets, they cannot easily read the password or commands because the data is
encrypted.

Step B1: Set Hostname and Domain Name
On the router CLI, enter:

Router> enable
Router# configure terminal
Router(config)# hostname R1
R1(config)# ip domain-name lab.com

Step B2: Generate RSA Keys
Enter:

R1(config)# crypto key generate rsa

When asked for the key size, enter:

1024

Optional verification command:

R1# show crypto key mypubkey rsa

Why this matters:
RSA keys are needed for SSH encryption. A 1024-bit key is acceptable for the lab, but stronger keys such as
2048-bit are preferred in real networks.

Step B3: Create a Local User Account
Enter:

R1(config)# username admin secret 12345

Why this matters:
SSH uses the local username and password for authentication. The secret keyword stores the password more
securely than the older password keyword.

Step B4: Allow SSH Only on VTY Lines
Enter:

R1(config)# line vty 0 15
R1(config-line)# login local
R1(config-line)# transport input ssh
R1(config-line)# exit
R1(config)# ip ssh version 2
R1(config)# end
R1# write memory

Step B5: Verify SSH
Enter:

R1# show ip ssh
R1# show running-config | section vty

Expected result:
The router should show that SSH version 2 is enabled and that VTY lines allow SSH only.

Step B6: Connect Using SSH
On PC0 Command Prompt, type:

C:\> ssh -l admin 10.0.0.1
Password: 12345
R1>
R1> enable
R1#

Expected result:
You should successfully log in through SSH. If Telnet is attempted after SSH-only mode is enabled, the
connection should be refused.

Reflection Point
SSH is safer than Telnet because SSH encrypts traffic. A packet sniffer may still see that SSH traffic exists,
but it cannot read the password in plain text.

Part C: Packet Sniffer
A packet sniffer captures network traffic. In this lab, the sniffer is used to prove the difference between
Telnet and SSH.

Analogy: Packet Sniffer is Like a Security Camera
It watches the traffic passing through the network. If the traffic is unprotected, the sniffer can reveal
important information.

Lab Setup
Add a Sniffer device between the router and switch:
- Router Fa0/0 to Sniffer Eth0
- Sniffer Eth1 to Switch Fa0/3
- PC0 to Switch Fa0/1
- PC1 to Switch Fa0/2

Step C1: Configure the Sniffer
Open the Sniffer device:
1. Go to the GUI tab
2. Turn Port0 ON
3. Select Port0
4. Open Edit Filters
5. Enable Telnet and SSH filters
6. Close the filter window

Step C2: Capture Telnet
If SSH-only mode is already enabled, temporarily re-enable Telnet:

R1# configure terminal
R1(config)# line vty 0 15
R1(config-line)# transport input telnet
R1(config-line)# login
R1(config-line)# password cisco
R1(config-line)# end

From PC0:

C:\> telnet 10.0.0.1
Password: cisco
Router>

Now check the Sniffer GUI and inspect Telnet packets.

Expected result:
Telnet traffic should show readable information, including the password or typed characters. This proves that
Telnet is insecure.

Step C3: Capture SSH
Clear the sniffer capture, then lock the router back to SSH only:

R1(config)# line vty 0 15
R1(config-line)# transport input ssh
R1(config-line)# login local
R1(config-line)# end

From PC0:

C:\> ssh -l admin 10.0.0.1
Password: 12345
R1>

Now check the Sniffer GUI and inspect SSH packets.

Expected result:
SSH packets should not show readable passwords. The contents should look encrypted or unreadable.

Telnet vs SSH Comparison
- Telnet uses TCP port 23
- SSH uses TCP port 22
- Telnet sends passwords in plain text
- SSH encrypts passwords and commands
- Telnet is not safe for real networks
- SSH is recommended for secure remote administration

Part D: Firewall / ACL
A firewall controls which traffic is allowed or blocked. In Cisco Packet Tracer, router ACLs can be used to
create firewall-like rules.

Analogy: ACL is Like a Bouncer
The router checks each packet against a rule list. If a rule matches, the router permits or denies the packet.
If no rule matches, the invisible final rule denies everything.

Key ACL Ideas
- ACL rules are checked from top to bottom
- First matching rule is applied
- Every ACL has an invisible deny all at the end
- Standard ACLs filter by source IP only
- Extended ACLs can filter by source, destination, protocol, and port

Firewall Lab Setup
Use:
- 1 Router R1
- 1 Switch for PC0 and PC1
- 1 Server on the other side of the router

IP Addressing:
- R1 Fa0/0: 192.168.1.1 / 255.255.255.0
- R1 Fa1/0: 192.168.2.1 / 255.255.255.0
- PC0: 192.168.1.10 / 255.255.255.0, gateway 192.168.1.1
- PC1: 192.168.1.20 / 255.255.255.0, gateway 192.168.1.1
- Server: 192.168.2.10 / 255.255.255.0, gateway 192.168.2.1

Before ACLs:
Make sure all devices can ping each other before adding access control rules.

Step D1: Standard ACL to Restrict SSH Access
This allows only PC0 to SSH into the router. PC1 is blocked.

R1# configure terminal
R1(config)# hostname R1
R1(config)# ip domain-name cisco.com
R1(config)# crypto key generate rsa
R1(config)# ip ssh version 2
R1(config)# username admin secret cisco123
R1(config)# access-list 10 permit host 192.168.1.10
R1(config)# line vty 0 15
R1(config-line)# access-class 10 in
R1(config-line)# transport input ssh
R1(config-line)# login local
R1(config-line)# end
R1# write memory

Test from PC0:

C:\> ssh -l admin 192.168.1.1

Expected result:
PC0 should be allowed.

Test from PC1:

C:\> ssh -l admin 192.168.1.1

Expected result:
PC1 should be blocked.

Step D2: Extended ACL to Block PC1 from the Server
This blocks PC1 from reaching the server, while allowing other traffic.

R1# configure terminal
R1(config)# access-list 100 deny ip host 192.168.1.20 host 192.168.2.10
R1(config)# access-list 100 permit ip any any
R1(config)# interface fa0/0
R1(config-if)# ip access-group 100 in
R1(config-if)# end
R1# write memory

Test from PC0:

C:\> ping 192.168.2.10

Expected result:
PC0 should successfully ping the server.

Test from PC1:

C:\> ping 192.168.2.10

Expected result:
PC1 should be blocked or receive request timeouts.

Step D3: Verify ACLs
Use these commands:

R1# show access-lists
R1# show ip interface fa0/0

Expected result:
The ACL hit counters should show that packets from PC1 match the deny rule, while other packets match the
permit rule.

Screenshot Checklist
Take screenshots at the following stages:
1. Start: topology built and devices connected
2. Middle: SSH session active, showing R1# in the terminal
3. End: Sniffer GUI showing encrypted SSH packets or ACL results showing access control working

Written Explanation Requirements
Your explanation should be minimum one page and up to two pages. It should include:
1. What Telnet does and why it is insecure
2. What SSH does and why it is more secure
3. What the packet sniffer showed
4. How ACLs work as firewall rules
5. What you learned about real-world network security

Sample Written Explanation
In this lab, I configured remote access and firewall rules in Cisco Packet Tracer. First, I set up Telnet on a
router and connected from a PC using the router IP address. This showed that remote access can be useful
because the router can be managed without physically sitting in front of it. However, Telnet is not secure
because it sends the password in plain text. Next, I configured SSH by setting a hostname, domain name,
RSA keys, and a local user account. SSH was more secure because the traffic was encrypted and the password
was not readable in the packet sniffer.

The packet sniffer helped me clearly see the difference between Telnet and SSH. When I used Telnet, the
traffic could be inspected and the login information was visible. When I used SSH, the captured traffic was
not readable because it was encrypted. This showed why SSH should be used instead of Telnet in real
networks. I also configured ACLs to act like firewall rules. A standard ACL allowed only PC0 to access the
router using SSH, while PC1 was blocked. Then I used an extended ACL to block PC1 from reaching the
server while still allowing PC0. This lab taught me that secure remote access and access control are important
parts of protecting a network.

Final Submission Checklist
- Include start, middle, and end screenshots
- Explain the activity in your own words
- Mention Telnet, SSH, packet sniffing, and ACL/firewall configuration
- Include references if required by your LMS
- Submit via the Lab 03 LMS link before Week 6 Monday 23:59
"""


def get_lab_guide() -> str:
    """Return the full Lab 3 guide as a string."""
    return __doc__ or ""


if __name__ == "__main__":
    print(get_lab_guide())
