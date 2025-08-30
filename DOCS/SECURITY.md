# 🔒 Security Policy

## 📌 Project: Vultrix
**Stage**: Pre-development

---

## 🎯 Goals
- Protect user data confidentiality  
- Ensure system integrity  
- Prevent unauthorized access  
- Align with industry & ethical best practices  

---

## 🛡️ Planned Security Measures

### 1. Encryption
- Enforce **HTTPS (TLS 1.3)** for all connections.  
- Store sensitive data encrypted with **AES-256**.  
- Encryption keys managed via environment variables (`.env`) or a **Key Management System (KMS)**.  

### 2. Authentication
- Use **JWT** for user session management (short expiry + refresh tokens).  
- All API requests signed with **HMAC-SHA256**.  
- Require **password verification on every login attempt** (no auto-login).  

### 3. Storage & Servers
- Passwords hashed using **Argon2** (preferred) or **bcrypt** with random salt.  
- Secrets (API keys, credentials) stored in `.env` (never committed to Git).  
- Database connections restricted to app servers only.  
- Apply **regular security patches** to dependencies.  

---

## ⚠️ Plugins Security
- Plugin system is **closed-source** for now.  
- Only official `.zip` plugins should be used.  
- Copying unsupported/malicious files into `~/.vultrix/Plugins/` may crash the system.  
- Future versions will add **plugin validation**.  

---

## 📢 Reporting a Vulnerability
If you discover a security issue in Vultrix:  

1. **Do not** create a public GitHub issue.  
2. Contact the maintainers directly via email:  
   📧 **broodevx@gmail.com**  
3. Provide:  
   - Description of the issue  
   - Steps to reproduce  
   - Possible impact  

Responsible disclosure is appreciated.  

---

## 📌 Notes
This software is developed for **educational and experimental purposes only**.  
Users are responsible for ensuring compliance with:  
- Local and international laws  
- Exchange policies  
- Religious and ethical standards (see [LICENSE_ISLAMIC.md](./LICENCE_FORK.md))  
