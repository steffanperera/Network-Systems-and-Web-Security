use chrono::Utc;
use std::collections::HashMap;

struct ServerInfo {
    name: &'static str,
    ip: &'static str,
    subnet_mask: &'static str,
    site: &'static str,
}

fn print_addressing_table() {
    let table = vec![
        ServerInfo { name: "FTP/Web Server", ip: "10.44.1.254", subnet_mask: "255.255.255.0", site: "Metropolis Bank HQ" },
        ServerInfo { name: "Email/DNS Server", ip: "10.44.1.253", subnet_mask: "255.255.255.0", site: "Metropolis Bank HQ" },
        ServerInfo { name: "NTP/AAA Server", ip: "10.44.1.252", subnet_mask: "255.255.255.0", site: "Metropolis Bank HQ" },
        ServerInfo { name: "File Backup Server", ip: "10.44.2.254", subnet_mask: "255.255.255.0", site: "Gotham Healthcare Branch" },
    ];

    println!("=== Addressing Table ===");
    println!("{:<22} {:<15} {:<16} {}", "Device", "IP Address", "Subnet Mask", "Site");
    println!("{:-<75}", "");

    for s in table {
        println!("{:<22} {:<15} {:<16} {}", s.name, s.ip, s.subnet_mask, s.site);
    }
    println!();
}

#[derive(Clone, Copy)]
struct FTPPermissions {
    read: bool,
    write: bool,
    delete: bool,
    rename: bool,
    list: bool,
}

impl FTPPermissions {
    fn full() -> Self {
        FTPPermissions { read: true, write: true, delete: true, rename: true, list: true }
    }
}

impl std::fmt::Display for FTPPermissions {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let flag = |b, c| if b { c } else { "-" };
        write!(f, "{}{}{}{}{}", flag(self.read, "R"), flag(self.write, "W"), flag(self.delete, "D"), flag(self.rename, "N"), flag(self.list, "L"))
    }
}

struct FTPUser {
    username: String,
    password: String,
    permissions: FTPPermissions,
}

struct FTPServer {
    ip: String,
    enabled: bool,
    users: Vec<FTPUser>,
}

impl FTPServer {
    fn new() -> Self {
        FTPServer { ip: "10.44.1.254".into(), enabled: false, users: vec![] }
    }

    fn enable(&mut self) {
        self.enabled = true;
        println!("[FTP] Service ON — listening at {}:21", self.ip);
    }

    fn add_user(&mut self, username: &str, password: &str, perms: FTPPermissions) {
        self.users.push(FTPUser { username: username.into(), password: password.into(), permissions: perms });
        println!("[FTP] User added: {:<6} | Password: {} | Permissions: {}", username, password, perms);
    }

    fn show_users(&self) {
        println!("\n[FTP] User Account List:");
        println!("  {:<10} {:<12} {}", "Username", "Password", "Permissions");
        println!("  {:-<35}", "");
        for u in &self.users {
            println!("  {:<10} {:<12} {}", u.username, u.password, u.permissions);
        }
    }
}

struct WebServer {
    ip: String,
    http_enabled: bool,
    https_enabled: bool,
}

impl WebServer {
    fn new() -> Self {
        WebServer { ip: "10.44.1.254".into(), http_enabled: false, https_enabled: false }
    }

    fn enable_http(&mut self) {
        self.http_enabled = true;
        println!("[WEB] HTTP  ON  — listening at http://{}:80", self.ip);
    }

    fn enable_https(&mut self) {
        self.https_enabled = true;
        println!("[WEB] HTTPS ON  — listening at https://{}:443", self.ip);
    }
}

struct PCConfig {
    name: String,
    ip_address: String,
    subnet_mask: String,
    default_gateway: String,
    dns_server: String,
}

struct DNSRecord {
    name: String,
    ip: String,
}

struct DNSServer {
    ip: String,
    enabled: bool,
    records: Vec<DNSRecord>,
}

impl DNSServer {
    fn new() -> Self {
        DNSServer { ip: "10.44.1.253".into(), enabled: false, records: vec![] }
    }

    fn enable(&mut self) {
        self.enabled = true;
        println!("[DNS] Service ON — listening at {}:53", self.ip);
    }

    fn add_a_record(&mut self, name: &str, ip: &str) {
        self.records.push(DNSRecord { name: name.into(), ip: ip.into() });
        println!("[DNS] A Record added: {:<25} -> {}", name, ip);
    }

    fn resolve(&self, name: &str) -> Option<&str> {
        self.records.iter().find_map(|r| (r.name == name).then(|| r.ip.as_str()))
    }

    fn show_records(&self) {
        println!("\n[DNS] A Record Table:");
        println!("  {:<28} {}", "Name", "IP Address");
        println!("  {:-<40}", "");
        for r in &self.records {
            println!("  {:<28} {}", r.name, r.ip);
        }
    }
}

impl PCConfig {
    fn browse_to(&self, target: &str, dns_server: Option<&DNSServer>) {
        let all_digits_or_dot = target.chars().all(|c| c.is_ascii_digit() || c == '.');
        let is_ip = !target.contains('.') || all_digits_or_dot;

        if is_ip {
            println!("[BROWSER] {} browsing to {} ... SUCCESS (direct IP)", self.name, target);
            return;
        }

        match dns_server {
            Some(dns) if dns.enabled => match dns.resolve(target) {
                Some(resolved) => println!("[BROWSER] {} browsing to {} ... resolved to {} ... SUCCESS", self.name, target, resolved),
                None => println!("[BROWSER] {} browsing to {} ... FAILED (no DNS record found)", self.name, target),
            },
            _ => println!("[BROWSER] {} browsing to {} ... FAILED (no DNS server configured)", self.name, target),
        }
    }
}

struct EmailMessage {
    from: String,
    to: String,
    subject: String,
    body: String,
}

struct EmailUser {
    username: String,
    password: String,
    inbox: Vec<EmailMessage>,
}

struct EmailServer {
    ip: String,
    domain: String,
    smtp_enabled: bool,
    pop3_enabled: bool,
    users: HashMap<String, EmailUser>,
}

impl EmailServer {
    fn new() -> Self {
        EmailServer { ip: "10.44.1.253".into(), domain: String::new(), smtp_enabled: false, pop3_enabled: false, users: HashMap::new() }
    }

    fn enable_smtp(&mut self) {
        self.smtp_enabled = true;
        println!("[EMAIL] SMTP ON — listening at {}:25", self.ip);
    }

    fn enable_pop3(&mut self) {
        self.pop3_enabled = true;
        println!("[EMAIL] POP3 ON — listening at {}:110", self.ip);
    }

    fn set_domain(&mut self, domain: &str) {
        self.domain = domain.into();
        println!("[EMAIL] Domain set to: {}", self.domain);
    }

    fn add_user(&mut self, username: &str, password: &str) {
        self.users.insert(username.into(), EmailUser { username: username.into(), password: password.into(), inbox: vec![] });
        println!("[EMAIL] User added: {}@{}", username, self.domain);
    }

    fn send_email(&mut self, from_user: &str, to_user: &str, subject: &str, body: &str) -> Result<(), String> {
        if !self.smtp_enabled {
            return Err("SMTP not enabled".into());
        }
        if let Some(recipient) = self.users.get_mut(to_user) {
            let msg = EmailMessage {
                from: format!("{}@{}", from_user, self.domain),
                to: format!("{}@{}", to_user, self.domain),
                subject: subject.into(),
                body: body.into(),
            };
            recipient.inbox.push(msg);
            println!("[SMTP] Email sent: {} -> {} | Subject: {}", format!("{}@{}", from_user, self.domain), format!("{}@{}", to_user, self.domain), subject);
            Ok(())
        } else {
            Err(format!("user {} not found on domain {}", to_user, self.domain))
        }
    }

    fn check_inbox(&self, username: &str) {
        if !self.pop3_enabled {
            println!("[POP3] POP3 not enabled — cannot retrieve mail");
            return;
        }
        match self.users.get(username) {
            Some(user) => {
                println!("[POP3] Inbox for {}@{} ({} message(s)):", username, self.domain, user.inbox.len());
                for (i, msg) in user.inbox.iter().enumerate() {
                    println!("  [{}] From: {:<30} Subject: {}", i + 1, msg.from, msg.subject);
                }
            }
            None => println!("[POP3] User {} not found", username),
        }
    }
}

struct EmailClientConfig {
    pc_name: String,
    display_name: String,
    email_address: String,
    incoming_mail_server: String,
    outgoing_mail_server: String,
    username: String,
    password: String,
}

impl EmailClientConfig {
    fn print(&self) {
        println!("[EMAIL CLIENT] {} configured:", self.pc_name);
        println!("  Name:             {}", self.display_name);
        println!("  Email:            {}", self.email_address);
        println!("  Incoming (POP3):  {}", self.incoming_mail_server);
        println!("  Outgoing (SMTP):  {}", self.outgoing_mail_server);
        println!("  Username:         {}", self.username);
    }
}

struct NTPKey {
    key_id: i32,
    password: String,
}

struct NTPServer {
    ip: String,
    enabled: bool,
    auth_enabled: bool,
    keys: Vec<NTPKey>,
    synced_clients: Vec<String>,
}

impl NTPServer {
    fn new() -> Self {
        NTPServer { ip: "10.44.1.252".into(), enabled: false, auth_enabled: false, keys: vec![], synced_clients: vec![] }
    }

    fn enable(&mut self) {
        self.enabled = true;
        println!("[NTP] Service ON — listening at {}:123", self.ip);
    }

    fn enable_authentication(&mut self) {
        self.auth_enabled = true;
        println!("[NTP] Authentication ENABLED");
    }

    fn add_key(&mut self, key_id: i32, password: &str) {
        self.keys.push(NTPKey { key_id, password: password.into() });
        println!("[NTP] Auth Key {} set: {}", key_id, password);
    }

    fn sync_client(&mut self, client_name: &str, key_id: i32, key_password: &str) {
        if !self.enabled {
            println!("[NTP] SYNC FAILED for {} — service not running", client_name);
            return;
        }
        if self.auth_enabled {
            let authenticated = self.keys.iter().any(|k| k.key_id == key_id && k.password == key_password);
            if !authenticated {
                println!("[NTP] SYNC FAILED for {} — authentication key mismatch", client_name);
                return;
            }
        }
        self.synced_clients.push(client_name.into());
        println!("[NTP] SYNC OK — {} synchronised to {} at {}", client_name, self.ip, Utc::now().format("%Y-%m-%d %H:%M:%S UTC"));
    }
}

struct AAAClient {
    client_name: String,
    client_ip: String,
    secret: String,
}

struct AAAUser {
    username: String,
    password: String,
}

struct AAAServer {
    ip: String,
    enabled: bool,
    clients: Vec<AAAClient>,
    users: Vec<AAAUser>,
    log: Vec<String>,
}

impl AAAServer {
    fn new() -> Self {
        AAAServer { ip: "10.44.1.252".into(), enabled: false, clients: vec![], users: vec![], log: vec![] }
    }

    fn enable(&mut self) {
        self.enabled = true;
        println!("[AAA] Service ON — listening at {}", self.ip);
    }

    fn add_network_client(&mut self, name: &str, ip: &str, secret: &str) {
        self.clients.push(AAAClient { client_name: name.into(), client_ip: ip.into(), secret: secret.into() });
        println!("[AAA] Network client added: {:<12} IP: {:<15} Secret: {}", name, ip, secret);
    }

    fn add_user(&mut self, username: &str, password: &str) {
        self.users.push(AAAUser { username: username.into(), password: password.into() });
        println!("[AAA] Admin user added: {}", username);
    }

    fn authenticate(&mut self, client_name: &str, client_secret: &str, username: &str, password: &str) -> bool {
        let client_trusted = self.clients.iter().any(|c| c.client_name == client_name && c.secret == client_secret);

        if !client_trusted {
            let entry = format!("[AAA] DENIED — unknown client: {}", client_name);
            println!("{}", entry);
            self.log.push(entry);
            return false;
        }

        if self.users.iter().any(|u| u.username == username && u.password == password) {
            let entry = format!("[AAA] PERMIT — user '{}' authenticated via {}", username, client_name);
            println!("{}", entry);
            self.log.push(entry);
            true
        } else {
            let entry = format!("[AAA] DENIED — invalid credentials for user '{}' via {}", username, client_name);
            println!("{}", entry);
            self.log.push(entry);
            false
        }
    }

    fn show_accounting_log(&self) {
        println!("\n[AAA] Accounting Log:");
        for (i, line) in self.log.iter().enumerate() {
            println!("  [{}] {}", i + 1, line);
        }
    }
}

fn main() {
    let banner = "=".repeat(55);
    println!("{}", banner);
    println!("  Creating a Cyber World — Lab 02 Simulation (Rust)");
    println!("  NSW Lab 2 | Dept. of Computer Science and IT");
    println!("{}", banner);
    println!();

    print_addressing_table();

    println!(">>> PART 1: FTP Server\n");
    let mut ftp = FTPServer::new();
    ftp.enable();
    for user in &["bob", "mary", "mike"] {
        ftp.add_user(user, "cisco123", FTPPermissions::full());
    }
    ftp.show_users();
    println!();

    println!(">>> PART 2: Web Server (HTTP/HTTPS)\n");
    let mut web = WebServer::new();
    web.enable_http();
    web.enable_https();

    let sally = PCConfig {
        name: "PC Sally".into(),
        ip_address: "10.44.1.4".into(),
        subnet_mask: "255.255.255.0".into(),
        default_gateway: "10.44.1.1".into(),
        dns_server: "10.44.1.253".into(),
    };

    println!("\n[PC] {} configured — IP: {} | GW: {}", sally.name, sally.ip_address, sally.default_gateway);

    println!("\n[TEST] Pre-DNS browsing:");
    sally.browse_to("www.cisco.corp", None);
    sally.browse_to("10.44.1.254", None);
    println!();

    println!(">>> PART 3: DNS Server\n");
    let mut dns = DNSServer::new();
    dns.enable();
    dns.add_a_record("email.cisco.corp", "10.44.1.253");
    dns.add_a_record("www.cisco.corp", "10.44.1.254");
    dns.show_records();

    println!("\n[TEST] Post-DNS browsing:");
    sally.browse_to("www.cisco.corp", Some(&dns));
    println!();

    println!(">>> PART 4: Email Server (SMTP / POP3)\n");
    let mut email = EmailServer::new();
    email.enable_smtp();
    email.enable_pop3();
    email.set_domain("cisco.corp");

    for user in &["phil", "sally", "bob", "dave", "mary", "tim", "mike"] {
        email.add_user(user, "cisco123");
    }

    let sally_email = EmailClientConfig {
        pc_name: "PC Sally".into(),
        display_name: "Sally".into(),
        email_address: "sally@cisco.corp".into(),
        incoming_mail_server: "email.cisco.corp".into(),
        outgoing_mail_server: "email.cisco.corp".into(),
        username: "sally".into(),
        password: "cisco123".into(),
    };

    let bob_email = EmailClientConfig {
        pc_name: "PC Bob".into(),
        display_name: "Bob".into(),
        email_address: "bob@cisco.corp".into(),
        incoming_mail_server: "email.cisco.corp".into(),
        outgoing_mail_server: "email.cisco.corp".into(),
        username: "bob".into(),
        password: "cisco123".into(),
    };

    println!();
    sally_email.print();
    println!();
    bob_email.print();

    println!();
    if let Err(err) = email.send_email("sally", "bob", "Hello from Sally!", "Hi Bob, the lab is working!") {
        println!("[EMAIL ERROR] {}", err);
    }
    email.check_inbox("bob");
    println!();

    println!(">>> PART 5: NTP Server\n");
    let mut ntp = NTPServer::new();
    ntp.enable();
    ntp.enable_authentication();
    ntp.add_key(1, "cisco123");
    ntp.sync_client("HQ_Router", 1, "cisco123");
    ntp.sync_client("RogueDevice", 1, "wrongpassword");
    println!();

    println!(">>> PART 6: AAA Server\n");
    let mut aaa = AAAServer::new();
    aaa.enable();
    aaa.add_network_client("HQ_Router", "10.44.1.1", "cisco123");
    aaa.add_user("admin", "cisco123");

    println!();
    aaa.authenticate("HQ_Router", "cisco123", "admin", "cisco123");
    aaa.authenticate("HQ_Router", "cisco123", "admin", "wrongpass");
    aaa.authenticate("UnknownRouter", "cisco123", "admin", "cisco123");
    aaa.show_accounting_log();

    println!();
    println!("{}", banner);
    println!("  Lab Complete — All 6 Services Configured");
    println!("  {:<20} {}", "FTP Server:", ftp.ip);
    println!("  {:<20} {}", "Web Server:", web.ip);
    println!("  {:<20} {}", "DNS Server:", dns.ip);
    println!("  {:<20} {}", "Email Server:", email.ip);
    println!("  {:<20} {}", "NTP Server:", ntp.ip);
    println!("  {:<20} {}", "AAA Server:", aaa.ip);
    println!("{}", banner);
}
