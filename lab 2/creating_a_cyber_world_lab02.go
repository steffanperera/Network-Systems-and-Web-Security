// creating_a_cyber_world_lab02.go
//
// Cisco Packet Tracer Lab — Creating a Cyber World
// NSW Lab 2 | Department of Computer Science and IT
// Assessment 1 Weekly Submission | Worth: 1.5%
//
// This file models all six services configured in the lab:
//   Part 1 — FTP Server
//   Part 2 — Web Server (HTTP/HTTPS)
//   Part 3 — DNS Server
//   Part 4 — Email Server (SMTP/POP3)
//   Part 5 — NTP Server
//   Part 6 — AAA Server

package main

import (
	"fmt"
	"strings"
	"time"
)

// ─────────────────────────────────────────────────────────────
// ADDRESSING TABLE
// ─────────────────────────────────────────────────────────────

// ServerInfo holds the static IP configuration for each server in the lab.
type ServerInfo struct {
	Name       string
	IP         string
	SubnetMask string
	Site       string
}

var addressingTable = []ServerInfo{
	{"FTP/Web Server", "10.44.1.254", "255.255.255.0", "Metropolis Bank HQ"},
	{"Email/DNS Server", "10.44.1.253", "255.255.255.0", "Metropolis Bank HQ"},
	{"NTP/AAA Server", "10.44.1.252", "255.255.255.0", "Metropolis Bank HQ"},
	{"File Backup Server", "10.44.2.254", "255.255.255.0", "Gotham Healthcare Branch"},
}

func printAddressingTable() {
	fmt.Println("=== Addressing Table ===")
	fmt.Printf("%-22s %-15s %-16s %s\n", "Device", "IP Address", "Subnet Mask", "Site")
	fmt.Println(strings.Repeat("-", 75))
	for _, s := range addressingTable {
		fmt.Printf("%-22s %-15s %-16s %s\n", s.Name, s.IP, s.SubnetMask, s.Site)
	}
	fmt.Println()
}

// ─────────────────────────────────────────────────────────────
// PART 1 — FTP SERVER
// ─────────────────────────────────────────────────────────────

// FTPPermissions represents the RWDNL access flags for an FTP user.
type FTPPermissions struct {
	Read    bool
	Write   bool
	Delete  bool
	Rename  bool
	List    bool
}

// FullPermissions returns a permissions set with all flags enabled.
func FullPermissions() FTPPermissions {
	return FTPPermissions{Read: true, Write: true, Delete: true, Rename: true, List: true}
}

func (p FTPPermissions) String() string {
	flag := func(b bool, c string) string {
		if b {
			return c
		}
		return "-"
	}
	return flag(p.Read, "R") + flag(p.Write, "W") + flag(p.Delete, "D") +
		flag(p.Rename, "N") + flag(p.List, "L")
}

// FTPUser represents a user account on the FTP server.
type FTPUser struct {
	Username    string
	Password    string
	Permissions FTPPermissions
}

// FTPServer models the FTP service running on the FTP/Web Server.
type FTPServer struct {
	IP      string
	Enabled bool
	Users   []FTPUser
}

// NewFTPServer creates the FTP server pre-configured with the lab IP.
func NewFTPServer() *FTPServer {
	return &FTPServer{IP: "10.44.1.254"}
}

// Enable activates the FTP service.
func (f *FTPServer) Enable() {
	f.Enabled = true
	fmt.Printf("[FTP] Service ON — listening at %s:21\n", f.IP)
}

// AddUser creates a new FTP user account.
func (f *FTPServer) AddUser(username, password string, perms FTPPermissions) {
	f.Users = append(f.Users, FTPUser{username, password, perms})
	fmt.Printf("[FTP] User added: %-6s | Password: %s | Permissions: %s\n",
		username, password, perms)
}

// ShowUsers prints all configured FTP user accounts.
func (f *FTPServer) ShowUsers() {
	fmt.Println("\n[FTP] User Account List:")
	fmt.Printf("  %-10s %-12s %s\n", "Username", "Password", "Permissions")
	fmt.Println("  " + strings.Repeat("-", 35))
	for _, u := range f.Users {
		fmt.Printf("  %-10s %-12s %s\n", u.Username, u.Password, u.Permissions)
	}
}

// ─────────────────────────────────────────────────────────────
// PART 2 — WEB SERVER (HTTP / HTTPS)
// ─────────────────────────────────────────────────────────────

// WebServer models the HTTP/HTTPS service on the FTP/Web Server.
type WebServer struct {
	IP          string
	HTTPEnabled bool
	HTTPSEnabled bool
}

func NewWebServer() *WebServer {
	return &WebServer{IP: "10.44.1.254"}
}

func (w *WebServer) EnableHTTP() {
	w.HTTPEnabled = true
	fmt.Printf("[WEB] HTTP  ON  — listening at http://%s:80\n", w.IP)
}

func (w *WebServer) EnableHTTPS() {
	w.HTTPSEnabled = true
	fmt.Printf("[WEB] HTTPS ON  — listening at https://%s:443\n", w.IP)
}

// PCConfig represents a PC's IP configuration (Sally's PC in the lab).
type PCConfig struct {
	Name           string
	IPAddress      string
	SubnetMask     string
	DefaultGateway string
	DNSServer      string
}

// BrowseTo simulates a web browser request from a PC.
// Without a DNS server configured, domain names will fail; IPs succeed.
func (pc *PCConfig) BrowseTo(target string, dnsServer *DNSServer) {
	isIP := !strings.Contains(target, ".")
	// crude check: treat targets without letters as IPs (simplified)
	allDigitsOrDot := true
	for _, c := range target {
		if !(c >= '0' && c <= '9') && c != '.' {
			allDigitsOrDot = false
			break
		}
	}

	if allDigitsOrDot || isIP {
		// Direct IP browse — always works
		fmt.Printf("[BROWSER] %s browsing to %s ... SUCCESS (direct IP)\n", pc.Name, target)
		return
	}

	// Domain name — requires DNS resolution
	if dnsServer == nil || !dnsServer.Enabled {
		fmt.Printf("[BROWSER] %s browsing to %s ... FAILED (no DNS server configured)\n", pc.Name, target)
		return
	}
	resolved, ok := dnsServer.Resolve(target)
	if !ok {
		fmt.Printf("[BROWSER] %s browsing to %s ... FAILED (no DNS record found)\n", pc.Name, target)
		return
	}
	fmt.Printf("[BROWSER] %s browsing to %s ... resolved to %s ... SUCCESS\n", pc.Name, target, resolved)
}

// ─────────────────────────────────────────────────────────────
// PART 3 — DNS SERVER
// ─────────────────────────────────────────────────────────────

// DNSRecord represents a single DNS A record mapping a hostname to an IP.
type DNSRecord struct {
	Name string
	IP   string
}

// DNSServer models the DNS service on the Email/DNS Server.
type DNSServer struct {
	IP      string
	Enabled bool
	Records []DNSRecord
}

func NewDNSServer() *DNSServer {
	return &DNSServer{IP: "10.44.1.253"}
}

func (d *DNSServer) Enable() {
	d.Enabled = true
	fmt.Printf("[DNS] Service ON — listening at %s:53\n", d.IP)
}

// AddARecord creates a new DNS A (Address) record.
func (d *DNSServer) AddARecord(name, ip string) {
	d.Records = append(d.Records, DNSRecord{name, ip})
	fmt.Printf("[DNS] A Record added: %-25s -> %s\n", name, ip)
}

// Resolve performs a DNS lookup and returns the IP if a record exists.
func (d *DNSServer) Resolve(name string) (string, bool) {
	for _, r := range d.Records {
		if r.Name == name {
			return r.IP, true
		}
	}
	return "", false
}

func (d *DNSServer) ShowRecords() {
	fmt.Println("\n[DNS] A Record Table:")
	fmt.Printf("  %-28s %s\n", "Name", "IP Address")
	fmt.Println("  " + strings.Repeat("-", 40))
	for _, r := range d.Records {
		fmt.Printf("  %-28s %s\n", r.Name, r.IP)
	}
}

// ─────────────────────────────────────────────────────────────
// PART 4 — EMAIL SERVER (SMTP / POP3)
// ─────────────────────────────────────────────────────────────

// EmailUser represents a mailbox account on the email server.
type EmailUser struct {
	Username string
	Password string
	Inbox    []EmailMessage
}

// EmailMessage represents a sent or received email.
type EmailMessage struct {
	From    string
	To      string
	Subject string
	Body    string
}

// EmailServer models the SMTP/POP3 service on the Email/DNS Server.
type EmailServer struct {
	IP           string
	Domain       string
	SMTPEnabled  bool
	POP3Enabled  bool
	Users        map[string]*EmailUser
}

func NewEmailServer() *EmailServer {
	return &EmailServer{
		IP:    "10.44.1.253",
		Users: make(map[string]*EmailUser),
	}
}

func (e *EmailServer) EnableSMTP() {
	e.SMTPEnabled = true
	fmt.Printf("[EMAIL] SMTP ON — listening at %s:25\n", e.IP)
}

func (e *EmailServer) EnablePOP3() {
	e.POP3Enabled = true
	fmt.Printf("[EMAIL] POP3 ON — listening at %s:110\n", e.IP)
}

func (e *EmailServer) SetDomain(domain string) {
	e.Domain = domain
	fmt.Printf("[EMAIL] Domain set to: %s\n", domain)
}

func (e *EmailServer) AddUser(username, password string) {
	e.Users[username] = &EmailUser{Username: username, Password: password}
	fmt.Printf("[EMAIL] User added: %s@%s\n", username, e.Domain)
}

// SendEmail simulates sending an email via SMTP.
func (e *EmailServer) SendEmail(fromUser, toUser, subject, body string) error {
	if !e.SMTPEnabled {
		return fmt.Errorf("SMTP not enabled")
	}
	recipient, ok := e.Users[toUser]
	if !ok {
		return fmt.Errorf("user %s not found on domain %s", toUser, e.Domain)
	}
	msg := EmailMessage{
		From:    fromUser + "@" + e.Domain,
		To:      toUser + "@" + e.Domain,
		Subject: subject,
		Body:    body,
	}
	recipient.Inbox = append(recipient.Inbox, msg)
	fmt.Printf("[SMTP] Email sent: %s -> %s | Subject: %s\n", msg.From, msg.To, subject)
	return nil
}

// CheckInbox simulates retrieving email via POP3.
func (e *EmailServer) CheckInbox(username string) {
	if !e.POP3Enabled {
		fmt.Println("[POP3] POP3 not enabled — cannot retrieve mail")
		return
	}
	user, ok := e.Users[username]
	if !ok {
		fmt.Printf("[POP3] User %s not found\n", username)
		return
	}
	fmt.Printf("[POP3] Inbox for %s@%s (%d message(s)):\n", username, e.Domain, len(user.Inbox))
	for i, msg := range user.Inbox {
		fmt.Printf("  [%d] From: %-30s Subject: %s\n", i+1, msg.From, msg.Subject)
	}
}

// EmailClientConfig represents a PC's email client configuration.
type EmailClientConfig struct {
	PCName              string
	DisplayName         string
	EmailAddress        string
	IncomingMailServer  string
	OutgoingMailServer  string
	Username            string
	Password            string
}

func (c EmailClientConfig) Print() {
	fmt.Printf("[EMAIL CLIENT] %s configured:\n", c.PCName)
	fmt.Printf("  Name:             %s\n", c.DisplayName)
	fmt.Printf("  Email:            %s\n", c.EmailAddress)
	fmt.Printf("  Incoming (POP3):  %s\n", c.IncomingMailServer)
	fmt.Printf("  Outgoing (SMTP):  %s\n", c.OutgoingMailServer)
	fmt.Printf("  Username:         %s\n", c.Username)
}

// ─────────────────────────────────────────────────────────────
// PART 5 — NTP SERVER
// ─────────────────────────────────────────────────────────────

// NTPKey represents an NTP authentication key.
type NTPKey struct {
	KeyID    int
	Password string
}

// NTPServer models the NTP service on the NTP/AAA Server.
type NTPServer struct {
	IP             string
	Enabled        bool
	AuthEnabled    bool
	Keys           []NTPKey
	SyncedClients  []string
}

func NewNTPServer() *NTPServer {
	return &NTPServer{IP: "10.44.1.252"}
}

func (n *NTPServer) Enable() {
	n.Enabled = true
	fmt.Printf("[NTP] Service ON — listening at %s:123\n", n.IP)
}

func (n *NTPServer) EnableAuthentication() {
	n.AuthEnabled = true
	fmt.Println("[NTP] Authentication ENABLED")
}

func (n *NTPServer) AddKey(keyID int, password string) {
	n.Keys = append(n.Keys, NTPKey{keyID, password})
	fmt.Printf("[NTP] Auth Key %d set: %s\n", keyID, password)
}

// SyncClient simulates a network device syncing its clock to the NTP server.
// The client must present a valid key to authenticate.
func (n *NTPServer) SyncClient(clientName string, keyID int, keyPassword string) {
	if !n.Enabled {
		fmt.Printf("[NTP] SYNC FAILED for %s — service not running\n", clientName)
		return
	}
	if n.AuthEnabled {
		authenticated := false
		for _, k := range n.Keys {
			if k.KeyID == keyID && k.Password == keyPassword {
				authenticated = true
				break
			}
		}
		if !authenticated {
			fmt.Printf("[NTP] SYNC FAILED for %s — authentication key mismatch\n", clientName)
			return
		}
	}
	n.SyncedClients = append(n.SyncedClients, clientName)
	fmt.Printf("[NTP] SYNC OK — %s synchronised to %s at %s\n",
		clientName, n.IP, time.Now().UTC().Format("2006-01-02 15:04:05 UTC"))
}

// ─────────────────────────────────────────────────────────────
// PART 6 — AAA SERVER
// ─────────────────────────────────────────────────────────────

// AAAClient represents a network device registered as a trusted AAA client.
type AAAClient struct {
	ClientName string
	ClientIP   string
	Secret     string
}

// AAAUser represents an administrator account managed by the AAA server.
type AAAUser struct {
	Username string
	Password string
}

// AAAServer models the AAA service on the NTP/AAA Server.
// AAA = Authentication, Authorisation, Accounting
type AAAServer struct {
	IP      string
	Enabled bool
	Clients []AAAClient
	Users   []AAAUser
	Log     []string
}

func NewAAAServer() *AAAServer {
	return &AAAServer{IP: "10.44.1.252"}
}

func (a *AAAServer) Enable() {
	a.Enabled = true
	fmt.Printf("[AAA] Service ON — listening at %s\n", a.IP)
}

// AddNetworkClient registers a router/switch as a trusted AAA client.
func (a *AAAServer) AddNetworkClient(name, ip, secret string) {
	a.Clients = append(a.Clients, AAAClient{name, ip, secret})
	fmt.Printf("[AAA] Network client added: %-12s IP: %-15s Secret: %s\n", name, ip, secret)
}

// AddUser creates an administrator user account.
func (a *AAAServer) AddUser(username, password string) {
	a.Users = append(a.Users, AAAUser{username, password})
	fmt.Printf("[AAA] Admin user added: %s\n", username)
}

// Authenticate simulates a login attempt forwarded from a network client.
// The client must be registered and present the correct shared secret.
func (a *AAAServer) Authenticate(clientName, clientSecret, username, password string) bool {
	// Step 1 — verify the requesting client is trusted
	clientTrusted := false
	for _, c := range a.Clients {
		if c.ClientName == clientName && c.Secret == clientSecret {
			clientTrusted = true
			break
		}
	}
	if !clientTrusted {
		entry := fmt.Sprintf("[AAA] DENIED — unknown client: %s", clientName)
		a.Log = append(a.Log, entry)
		fmt.Println(entry)
		return false
	}

	// Step 2 — verify the user credentials
	for _, u := range a.Users {
		if u.Username == username && u.Password == password {
			entry := fmt.Sprintf("[AAA] PERMIT — user '%s' authenticated via %s", username, clientName)
			a.Log = append(a.Log, entry)
			fmt.Println(entry)
			return true
		}
	}

	entry := fmt.Sprintf("[AAA] DENIED — invalid credentials for user '%s' via %s", username, clientName)
	a.Log = append(a.Log, entry)
	fmt.Println(entry)
	return false
}

// ShowAccountingLog prints the full AAA accounting log.
func (a *AAAServer) ShowAccountingLog() {
	fmt.Println("\n[AAA] Accounting Log:")
	for i, entry := range a.Log {
		fmt.Printf("  [%d] %s\n", i+1, entry)
	}
}

// ─────────────────────────────────────────────────────────────
// MAIN — Build the Cyber World
// ─────────────────────────────────────────────────────────────

func main() {
	banner := strings.Repeat("=", 55)
	fmt.Println(banner)
	fmt.Println("  Creating a Cyber World — Lab 02 Simulation (Go)")
	fmt.Println("  NSW Lab 2 | Dept. of Computer Science and IT")
	fmt.Println(banner)
	fmt.Println()

	printAddressingTable()

	// ── PART 1: FTP ──────────────────────────────────────────
	fmt.Println(">>> PART 1: FTP Server")
	fmt.Println()
	ftp := NewFTPServer()
	ftp.Enable()
	// Lab step 11: create bob, mary, mike with full RWDNL permissions
	for _, user := range []string{"bob", "mary", "mike"} {
		ftp.AddUser(user, "cisco123", FullPermissions())
	}
	ftp.ShowUsers()
	fmt.Println()

	// ── PART 2: WEB SERVER ───────────────────────────────────
	fmt.Println(">>> PART 2: Web Server (HTTP/HTTPS)")
	fmt.Println()
	web := NewWebServer()
	web.EnableHTTP()
	web.EnableHTTPS()

	// Sally's PC configuration (lab step 16-18)
	sally := &PCConfig{
		Name:           "PC Sally",
		IPAddress:      "10.44.1.4",
		SubnetMask:     "255.255.255.0",
		DefaultGateway: "10.44.1.1",
		DNSServer:      "10.44.1.253",
	}
	fmt.Printf("\n[PC] %s configured — IP: %s | GW: %s\n",
		sally.Name, sally.IPAddress, sally.DefaultGateway)

	// Lab step 22-23: DNS not configured yet — name fails, IP succeeds
	fmt.Println("\n[TEST] Pre-DNS browsing:")
	sally.BrowseTo("www.cisco.corp", nil)    // FAIL — no DNS
	sally.BrowseTo("10.44.1.254", nil)       // SUCCESS — direct IP
	fmt.Println()

	// ── PART 3: DNS ──────────────────────────────────────────
	fmt.Println(">>> PART 3: DNS Server")
	fmt.Println()
	dns := NewDNSServer()
	dns.Enable()
	// Lab step 27-28: add A records
	dns.AddARecord("email.cisco.corp", "10.44.1.253")
	dns.AddARecord("www.cisco.corp", "10.44.1.254")
	dns.ShowRecords()

	// Lab step 32: re-test after DNS configured — should now succeed
	fmt.Println("\n[TEST] Post-DNS browsing:")
	sally.BrowseTo("www.cisco.corp", dns)    // SUCCESS — DNS resolves it
	fmt.Println()

	// ── PART 4: EMAIL ────────────────────────────────────────
	fmt.Println(">>> PART 4: Email Server (SMTP / POP3)")
	fmt.Println()
	email := NewEmailServer()
	email.EnableSMTP()
	email.EnablePOP3()
	// Lab step 37: set domain
	email.SetDomain("cisco.corp")
	// Lab step 38: create all user accounts
	for _, user := range []string{"phil", "sally", "bob", "dave", "mary", "tim", "mike"} {
		email.AddUser(user, "cisco123")
	}

	// Lab step 40-44: configure email clients on Sally and Bob's PCs
	sallyEmail := EmailClientConfig{
		PCName:             "PC Sally",
		DisplayName:        "Sally",
		EmailAddress:       "sally@cisco.corp",
		IncomingMailServer: "email.cisco.corp",
		OutgoingMailServer: "email.cisco.corp",
		Username:           "sally",
		Password:           "cisco123",
	}
	bobEmail := EmailClientConfig{
		PCName:             "PC Bob",
		DisplayName:        "Bob",
		EmailAddress:       "bob@cisco.corp",
		IncomingMailServer: "email.cisco.corp",
		OutgoingMailServer: "email.cisco.corp",
		Username:           "bob",
		Password:           "cisco123",
	}
	fmt.Println()
	sallyEmail.Print()
	fmt.Println()
	bobEmail.Print()

	// Send a test email from Sally to Bob
	fmt.Println()
	err := email.SendEmail("sally", "bob", "Hello from Sally!", "Hi Bob, the lab is working!")
	if err != nil {
		fmt.Println("[EMAIL ERROR]", err)
	}
	email.CheckInbox("bob")
	fmt.Println()

	// ── PART 5: NTP ──────────────────────────────────────────
	fmt.Println(">>> PART 5: NTP Server")
	fmt.Println()
	ntp := NewNTPServer()
	ntp.Enable()
	// Lab step 47-48: enable authentication, key 1 = cisco123
	ntp.EnableAuthentication()
	ntp.AddKey(1, "cisco123")

	// Simulate HQ_Router syncing with correct key
	ntp.SyncClient("HQ_Router", 1, "cisco123")
	// Simulate a rogue device trying to sync without the key
	ntp.SyncClient("RogueDevice", 1, "wrongpassword")
	fmt.Println()

	// ── PART 6: AAA ──────────────────────────────────────────
	fmt.Println(">>> PART 6: AAA Server")
	fmt.Println()
	aaa := NewAAAServer()
	aaa.Enable()
	// Lab step 51-52: register HQ_Router as a trusted client
	aaa.AddNetworkClient("HQ_Router", "10.44.1.1", "cisco123")
	// Lab step 53-54: create admin user
	aaa.AddUser("admin", "cisco123")

	// Simulate login attempts
	fmt.Println()
	aaa.Authenticate("HQ_Router", "cisco123", "admin", "cisco123")   // should PERMIT
	aaa.Authenticate("HQ_Router", "cisco123", "admin", "wrongpass")  // should DENY
	aaa.Authenticate("UnknownRouter", "cisco123", "admin", "cisco123") // should DENY (unknown client)
	aaa.ShowAccountingLog()

	// ── SUMMARY ──────────────────────────────────────────────
	fmt.Println()
	fmt.Println(banner)
	fmt.Println("  Lab Complete — All 6 Services Configured")
	fmt.Printf("  %-20s %s\n", "FTP Server:",   ftp.IP)
	fmt.Printf("  %-20s %s\n", "Web Server:",   web.IP)
	fmt.Printf("  %-20s %s\n", "DNS Server:",   dns.IP)
	fmt.Printf("  %-20s %s\n", "Email Server:", email.IP)
	fmt.Printf("  %-20s %s\n", "NTP Server:",   ntp.IP)
	fmt.Printf("  %-20s %s\n", "AAA Server:",   aaa.IP)
	fmt.Println(banner)
}
