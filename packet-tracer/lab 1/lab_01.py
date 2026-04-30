"""
NSW Lab 1
Web Server, DNS, Ping, and Packet Sniffer
Department of Computer Science and IT
Assessment 1 Weekly Submission | Worth: 1.5%

Overview & Lab Objective
In this lab, you will learn basic cybersecurity and networking concepts using Cisco Packet Tracer.
The main focus is configuring a web server, DNS server, ping testing, and packet sniffing. These are
important skills for understanding how devices communicate and how network traffic can be observed.

By the end of this lab, your Packet Tracer work should demonstrate:
1. A working HTTP web server
2. DNS name resolution from a domain name to an IP address
3. Ping testing between devices
4. A packet sniffer setup to observe network traffic

Real-World Analogy
Imagine a small company network. The web server is like the company website, the DNS server is like a
phone book that changes website names into IP addresses, ping is like checking whether another device is
awake and reachable, and a sniffer is like a security camera watching network traffic.

Reference Material
- Configure Web and DNS servers and ping video:
  https://www.youtube.com/watch?v=tI1r-suDOEA
- Sniffer setup video: available through LMS
- Cisco Packet Tracer is required for this lab.

Important: Plagiarism
All written explanations must be in your own words. You can use the lab guide and video references for help,
but your screenshots and explanation should be based on your own Packet Tracer work.

Part 1: Configure Web and DNS Servers
In this part, you will build a simple network with client PCs, a router, switches, a web server, and a DNS server.
The goal is to access a website first using an IP address, then using a domain name.

What is an HTTP Server?
An HTTP server hosts web pages. In Packet Tracer, a server can run the HTTP service and allow a PC to open
that web page using the Web Browser tool.

What is a DNS Server?
DNS stands for Domain Name System. It translates a domain name, such as networking.com, into an IP address,
such as 10.10.10.10. This makes it easier for users because they do not need to remember numbers.

Lab Setup
Use the following devices in Cisco Packet Tracer:
- 1 Router
- 2 Switches
- 2 PCs
- 1 HTTP Server
- 1 DNS Server

Connections:
- PC0 to Switch 1
- PC1 to Switch 1
- DNS Server to Switch 1
- HTTP Server to Switch 2
- Switch 1 to Router interface G0/0
- Switch 2 to Router interface G0/1
- Use copper straight-through cables

Step 1: Configure Router Interfaces
Open the router CLI and configure the two networks:

Router> enable
Router# configure terminal
Router(config)# interface gigabitEthernet 0/0
Router(config-if)# ip address 192.168.10.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# interface gigabitEthernet 0/1
Router(config-if)# ip address 10.10.10.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# end
Router# write memory

Why this matters:
The router connects the client network to the server network. Without router IP addresses and no shutdown,
the PCs will not be able to reach the HTTP server on the other network.

Step 2: Configure PC and Server IP Addresses
Set these values using Desktop > IP Configuration on each device:

PC0:
- IP Address: 192.168.10.2
- Subnet Mask: 255.255.255.0
- Default Gateway: 192.168.10.1
- DNS Server: 192.168.10.11

PC1:
- IP Address: 192.168.10.3
- Subnet Mask: 255.255.255.0
- Default Gateway: 192.168.10.1
- DNS Server: 192.168.10.11

DNS Server:
- IP Address: 192.168.10.11
- Subnet Mask: 255.255.255.0
- Default Gateway: 192.168.10.1

HTTP Server:
- IP Address: 10.10.10.10
- Subnet Mask: 255.255.255.0
- Default Gateway: 10.10.10.1

Step 3: Enable the HTTP Service
On the HTTP Server:
1. Click the server.
2. Go to Services > HTTP.
3. Turn HTTP On.
4. Edit index.html if required.
5. Save the page.

Screenshot Tip - Starting Point
Take a screenshot showing the topology built with the PCs, switches, router, HTTP server, and DNS server.

Step 4: Test Web Access Using the IP Address
On PC0:
1. Go to Desktop > Web Browser.
2. Type: http://10.10.10.10
3. Click Go.

Expected result:
The web page from the HTTP server should load successfully.

Step 5: Enable DNS and Create a DNS Record
On the DNS Server:
1. Go to Services > DNS.
2. Turn DNS On.
3. Add this record:
   - Name: networking.com
   - Address: 10.10.10.10
4. Click Add.

Step 6: Test Web Access Using the Domain Name
On PC0:
1. Go to Desktop > Web Browser.
2. Type: http://networking.com
3. Click Go.

Expected result:
The same web page should load using the domain name instead of the IP address.

Screenshot Tip - Middle Point
Take a screenshot showing the domain name networking.com loading in the browser, or the DNS record mapping
networking.com to 10.10.10.10.

Reflection Question
Why can the PC open networking.com after DNS is configured?

Suggested Answer:
The PC can open networking.com because the DNS server translates the domain name into the HTTP server IP
address. Before DNS is configured, the PC does not know which IP address belongs to that name.

Part 2: Ping Testing
Ping is used to test whether one device can reach another device on the network. It uses ICMP packets.

Step 1: Test from PC0 to the HTTP Server
On PC0 > Desktop > Command Prompt, type:

C:\> ping 10.10.10.10

Expected result:
You should receive replies from 10.10.10.10.

Step 2: Test from PC0 to the DNS Server
On PC0 > Desktop > Command Prompt, type:

C:\> ping 192.168.10.11

Expected result:
You should receive replies from 192.168.10.11.

Why this matters:
Ping confirms that the IP addressing, cables, router interfaces, and gateway settings are working correctly.
If ping fails, the web and DNS services may also fail because the devices cannot communicate.

Part 3: Set Up a Packet Sniffer
In this part, you will set up a sniffer to observe traffic. A sniffer is used to capture and inspect packets moving
across a network.

What is a Packet Sniffer?
A packet sniffer is a tool that monitors network traffic. Security engineers can use sniffers to troubleshoot
network problems, but attackers can also use them to capture sensitive traffic if the network is not protected.

Lab Setup for Sniffer
Use the following devices:
- Router0
- Router1
- Hub0
- Sniffer0

Connections:
- Router0 Gig0/0/0 to Hub Fa0
- Router1 Gig0/0/0 to Hub Fa1
- Sniffer0 Eth0 to Hub Fa2

Why use a hub?
A hub broadcasts traffic to all ports. This allows the sniffer to see the traffic between Router0 and Router1.
A switch usually sends traffic only to the destination port, so the sniffer would not see everything unless port
mirroring was used.

Step 1: Configure Router0
Open Router0 CLI and enter:

Router> enable
Router# configure terminal
Router(config)# interface gigabitEthernet 0/0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# end
Router# write memory

Step 2: Configure Router1
Open Router1 CLI and enter:

Router> enable
Router# configure terminal
Router(config)# interface gigabitEthernet 0/0/0
Router(config-if)# ip address 192.168.1.2 255.255.255.0
Router(config-if)# no shutdown
Router(config-if)# exit
Router(config)# end
Router# write memory

Step 3: Test Connectivity
On Router0 CLI, type:

Router# ping 192.168.1.2

Expected result:
Router0 should receive replies from Router1.

Step 4: Use Simulation Mode
1. Switch Packet Tracer from Realtime mode to Simulation mode.
2. Click Edit Filters.
3. Select ICMP.
4. Run the ping again.
5. Use Capture/Forward to watch packets move through the network.
6. Click packets in the event list to inspect the PDU details.

Screenshot Tip - Ending Point
Take a screenshot showing Simulation Mode with ICMP packets visible, or the PDU details showing the captured
ping traffic.

Reflection Question
What did the sniffer activity show?

Suggested Answer:
The sniffer activity showed that network traffic can be observed as packets move between devices. By using
Simulation Mode, I could see ICMP packets being sent and received during the ping test. This helped me
understand how packet analysis can be used for troubleshooting and cybersecurity learning.

Sample Written Explanation
In this lab, I used Cisco Packet Tracer to configure a basic network with a web server, DNS server, PCs, switches,
and a router. First, I assigned IP addresses to the router interfaces, PCs, DNS server, and HTTP server. Then I
enabled the HTTP service and tested access to the web server using its IP address. After that, I configured DNS
so the PC could access the same website using the domain name networking.com. I also used ping to confirm
that the devices were reachable across the network. In the second part, I set up a sniffer with two routers and a
hub, then used Simulation Mode to observe ICMP packet movement during a ping test. This lab helped me
understand how web servers, DNS, ping, and packet sniffing are used in real network and cybersecurity work.

Final Submission Checklist
- Include start, middle, and end screenshots
- Explain the activity in your own words
- Mention HTTP, DNS, ping, and sniffer setup
- Include references if required by your LMS
- Submit via the Lab 01 LMS link before Week 4 Monday 23:59
"""


def get_lab_guide() -> str:
    """Return the full Lab 1 guide as a string."""
    return __doc__ or ""


if __name__ == "__main__":
    print(get_lab_guide())
