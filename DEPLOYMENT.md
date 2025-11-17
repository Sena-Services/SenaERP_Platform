# 🚀 Website CMS Deployment Guide

**IMPORTANT: This file contains sensitive credentials. DO NOT commit to Git.**

---

## 📋 Server Credentials

### Production Server Details
- **Server Name**: Platform (Sentra production server)
- **IP Address**: `159.89.174.135`
- **SSH User**: `sentra`
- **SSH Password**: `Sentra@magicserverportal`
- **Root User**: `root`
- **Root Password**: `Sena@wS$12345`

### Bench Location on Server
```
/home/sentra/Sentra
```

### Site Name
```
senamarketing.senaerp.com
```

### App Name
```
websitecms
```

---

## 🔑 Authentication Methods

### Method 1: SSH Key (Recommended - If Set Up)

**To verify it's working:**
```bash
ssh sentra@159.89.174.135 "echo 'Connection successful!'"
```

If this works without asking for a password, you're all set! ✅

---

### Method 2: Password Authentication (Fallback)

```bash
ssh sentra@159.89.174.135
```
**Password**: `Sentra@magicserverportal`

---

## 🎯 Quick Deployment Commands

### Emergency Quick Restart
```bash
cd ~/Sentra && bench use senamarketing.senaerp.com && sudo supervisorctl restart all && sudo nginx -t && sudo systemctl reload nginx
```

### Complete One-Liner (Full Safe Deploy)
```bash
cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/websitecms && git pull upstream main && cd ~/Sentra && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-website-cache && bench clear-cache && yes | bench setup nginx && sudo nginx -t && sudo systemctl reload nginx && sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart all
```

---

## 📖 Deployment Scenarios

Choose the appropriate deployment based on your changes:

---

## A) Python-only Code Change (No Schema, No Assets)

**When to use:** Only `.py` files changed, no DocType changes, no frontend changes

```bash
# Connect to server
ssh sentra@159.89.174.135

# Navigate to bench
cd ~/Sentra
bench use senamarketing.senaerp.com

# Pull websitecms app code
cd apps/websitecms && git pull upstream main && cd -

# If requirements.txt changed:
bench pip install -r apps/websitecms/requirements.txt

# Reload processes
sudo supervisorctl restart all
```

**Time:** ~30 seconds
**Downtime:** Minimal (during supervisor restart)

---

## B) DocType/Schema or Patch Changes (Requires Migrate)

**When to use:**
- New/modified DocTypes
- Database schema changes
- Patch files added
- Permission changes

```bash
# Connect to server
ssh sentra@159.89.174.135

# Navigate to bench
cd ~/Sentra
bench use senamarketing.senaerp.com

# (Optional: brief maintenance window)
bench --site senamarketing.senaerp.com set-maintenance-mode on

# Pull code
cd apps/websitecms && git pull upstream main && cd -

# If requirements changed:
bench pip install -r apps/websitecms/requirements.txt

# Migrate DB & clear cache
bench --site senamarketing.senaerp.com migrate
bench clear-cache

# Back online + restart processes
bench --site senamarketing.senaerp.com set-maintenance-mode off
sudo supervisorctl restart all
```

**Time:** 1-2 minutes
**Downtime:** Optional (use maintenance mode)

---

## C) Frontend/Asset Changes (JS/CSS/Web Templates)

**When to use:**
- JavaScript/CSS changes
- Web templates modified
- Vue/React components updated
- package.json updated

```bash
# Connect to server
ssh sentra@159.89.174.135

# Navigate to bench
cd ~/Sentra
bench use senamarketing.senaerp.com

# Pull code
cd apps/websitecms && git pull upstream main && cd -

# If package.json changed in websitecms:
cd apps/websitecms && yarn install --frozen-lockfile || npm ci && cd -

# Build assets for production
bench build

# Clear website cache
bench clear-website-cache

# Reload
sudo supervisorctl restart all
```

**Time:** 1-3 minutes (depending on build size)
**Downtime:** Minimal

---

## D) Full "Safe" Deploy (Covers Most Updates)

**When to use:**
- Unsure what changed
- Multiple types of changes
- Major version updates
- After merging multiple PRs

```bash
# Connect to server
ssh sentra@159.89.174.135

# Navigate to bench
cd ~/Sentra
bench use senamarketing.senaerp.com

# 1) Pull websitecms app
cd apps/websitecms && git pull upstream main && cd -

# 2) Dependencies (only if changed)
# Python deps:
bench pip install -r apps/websitecms/requirements.txt

# JS deps (if package.json changed):
cd apps/websitecms && (yarn install --frozen-lockfile || npm ci) && cd -

# 3) Database + assets + caches
bench --site senamarketing.senaerp.com migrate
bench build
bench clear-website-cache
bench clear-cache

# 4) Refresh nginx (safe even if unchanged)
yes | bench setup nginx
sudo nginx -t && sudo systemctl reload nginx

# 5) Restart app stack
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart all
```

**Time:** 2-5 minutes
**Downtime:** Minimal

---

## E) Post-Deployment Health Checks

### Backend Health Check
```bash
# Direct backend check
curl -i -H "Host: senamarketing.senaerp.com" http://127.0.0.1:8000/api/method/ping

# Through nginx
curl -I https://senamarketing.senaerp.com/login
curl -I https://senamarketing.senaerp.com/app
```

### Asset Check
```bash
# Check if assets are loading
curl -I https://senamarketing.senaerp.com/assets/websitecms/js/websitecms.bundle.js
curl -I https://senamarketing.senaerp.com/assets/frappe/dist/js/frappe-web.bundle.js
```

### Log Monitoring
```bash
# Web server logs
tail -n 120 -f ~/Sentra/logs/web.error.log

# Nginx error logs
sudo tail -n 120 -f /var/log/nginx/error.log

# Worker logs
tail -n 120 -f ~/Sentra/logs/worker.error.log

# Supervisor status
sudo supervisorctl status
```

### Check Running Processes
```bash
# All Frappe processes
sudo supervisorctl status | grep Sentra

# Just web workers
sudo supervisorctl status | grep Sentra-web

# Just background workers
sudo supervisorctl status | grep Sentra-workers
```

---

## F) Emergency Quick Restart

**When to use:** Site is down, unresponsive, or throwing 502 errors

```bash
# Quick restart everything
sudo supervisorctl restart all
sudo nginx -t && sudo systemctl reload nginx

# Or more granular:
sudo supervisorctl restart Sentra-web:Sentra-frappe-web
sudo supervisorctl restart Sentra-workers:*
```

**Time:** 10-20 seconds
**Downtime:** Brief (10-15 seconds)

---

## 🔧 Troubleshooting

### Problem: "upstream main" Not Found

**Solution:** Check git remotes
```bash
cd ~/Sentra/apps/websitecms
git remote -v

# If upstream doesn't exist, add it:
git remote add upstream https://github.com/Sena-Services/websitecms.git

# Or if origin exists:
git pull origin main
```

---

### Problem: Migration Fails

**Symptoms:** `bench migrate` throws errors

**Solutions:**

1. **Check migration logs:**
```bash
tail -n 200 ~/Sentra/logs/bench.log
```

2. **Try maintenance mode:**
```bash
bench --site senamarketing.senaerp.com set-maintenance-mode on
bench --site senamarketing.senaerp.com migrate --verbose
bench --site senamarketing.senaerp.com set-maintenance-mode off
```

3. **Check database connection:**
```bash
bench --site senamarketing.senaerp.com console
# In console:
frappe.db.get_value("DocType", "User", "name")
# Should return "User"
```

---

### Problem: Build Fails

**Symptoms:** `bench build` throws errors

**Solutions:**

1. **Check Node/Yarn version:**
```bash
node -v  # Should be 18.x or higher
yarn -v  # Should be 1.x or higher
```

2. **Clear node_modules and rebuild:**
```bash
cd ~/Sentra/apps/websitecms
rm -rf node_modules
yarn install
cd ~/Sentra
bench build --app websitecms
```

3. **Build with verbose output:**
```bash
bench build --app websitecms --verbose
```

---

### Problem: Assets Not Loading

**Symptoms:** 404 on CSS/JS files, blank pages

**Solutions:**

1. **Rebuild assets:**
```bash
bench build --app websitecms
bench clear-website-cache
bench clear-cache
```

2. **Check nginx configuration:**
```bash
sudo nginx -t
# If errors, regenerate:
yes | bench setup nginx
sudo systemctl reload nginx
```

3. **Check file permissions:**
```bash
ls -la ~/Sentra/sites/assets/websitecms/
# Should be readable by sentra user
```

---

### Problem: 502 Bad Gateway

**Symptoms:** Website shows nginx 502 error

**Solutions:**

1. **Check if Frappe is running:**
```bash
sudo supervisorctl status | grep Sentra
# All should be RUNNING
```

2. **Restart services:**
```bash
sudo supervisorctl restart all
```

3. **Check if port 8000 is listening:**
```bash
lsof -i :8000
# Should show gunicorn processes
```

4. **Check web logs:**
```bash
tail -n 100 ~/Sentra/logs/web.error.log
```

---

### Problem: Database Connection Error

**Symptoms:** "Could not connect to database" errors

**Solutions:**

1. **Check MariaDB is running:**
```bash
sudo systemctl status mariadb
# Should be active (running)
```

2. **Restart MariaDB:**
```bash
sudo systemctl restart mariadb
sudo supervisorctl restart all
```

3. **Check database credentials:**
```bash
cat ~/Sentra/sites/senamarketing.senaerp.com/site_config.json
# Should have db_name, db_password
```

---

## 📚 Useful Bench Commands

| Command | Description |
|---------|-------------|
| `bench version` | Show versions of all apps |
| `bench --site <site> list-apps` | List installed apps on site |
| `bench --site <site> migrate` | Run database migrations |
| `bench build` | Build all assets |
| `bench build --app websitecms` | Build only websitecms assets |
| `bench clear-cache` | Clear Redis cache |
| `bench clear-website-cache` | Clear website route cache |
| `bench --site <site> console` | Open Frappe console |
| `bench --site <site> mariadb` | Open MariaDB console |
| `bench --site <site> backup` | Create site backup |
| `bench restart` | Restart bench processes |
| `bench setup nginx` | Regenerate nginx config |

---

## 📚 Useful Supervisor Commands

| Command | Description |
|---------|-------------|
| `sudo supervisorctl status` | Show all processes |
| `sudo supervisorctl restart all` | Restart all processes |
| `sudo supervisorctl reread` | Reload config files |
| `sudo supervisorctl update` | Apply config changes |
| `sudo supervisorctl restart Sentra-web:*` | Restart web workers |
| `sudo supervisorctl restart Sentra-workers:*` | Restart background workers |
| `sudo supervisorctl tail -f Sentra-web:Sentra-frappe-web` | Follow web logs |

---

## 🎓 Understanding the CMS Deployment Flow

```
┌─────────────────┐
│  Your Mac       │
│  (Local Dev)    │
└────────┬────────┘
         │ git push
         ▼
┌─────────────────┐
│  GitHub         │
│  (Repository)   │
│  websitecms     │
└────────┬────────┘
         │ git pull
         ▼
┌─────────────────┐
│  Server         │
│  ~/Sentra/apps/ │
│  websitecms     │
└────────┬────────┘
         │ bench migrate
         │ bench build
         ▼
┌─────────────────┐
│  Frappe Site    │
│  senamarketing  │
│  .senaerp.com   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Supervisor     │
│  (gunicorn,     │
│   workers, etc) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Nginx          │
│  (Reverse       │
│   Proxy)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Website Live!  │
│  Port 443/80    │
└─────────────────┘
```

---

## 🔐 Security Notes

1. **Never commit this file to Git** - It contains passwords!
2. **SSH keys are more secure than passwords** - Prefer key authentication
3. **Change passwords regularly** - Contact server admin for updates
4. **Don't share credentials** - Keep them private
5. **Use VPN if required** - Check with your team
6. **Always test in maintenance mode first** - For critical changes

---

## 📝 Quick Reference Card

### Deploy Python Changes Only (30 seconds)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/websitecms && git pull upstream main && cd - && sudo supervisorctl restart all"
```

### Deploy with Migration (90 seconds)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/websitecms && git pull upstream main && cd - && bench --site senamarketing.senaerp.com migrate && bench clear-cache && sudo supervisorctl restart all"
```

### Deploy Frontend Changes (2 minutes)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/websitecms && git pull upstream main && cd - && bench build && bench clear-website-cache && sudo supervisorctl restart all"
```

### Full Safe Deploy (3 minutes)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/websitecms && git pull upstream main && cd - && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-website-cache && bench clear-cache && yes | bench setup nginx && sudo nginx -t && sudo systemctl reload nginx && sudo supervisorctl restart all"
```

### Check Site Status
```bash
ssh sentra@159.89.174.135 "sudo supervisorctl status && curl -I https://senamarketing.senaerp.com/login"
```

### Emergency Restart
```bash
ssh sentra@159.89.174.135 "sudo supervisorctl restart all && sudo nginx -t && sudo systemctl reload nginx"
```

---

## 🆘 Need Help?

1. **Check the logs first**:
   - Web: `tail -f ~/Sentra/logs/web.error.log`
   - Worker: `tail -f ~/Sentra/logs/worker.error.log`
   - Nginx: `sudo tail -f /var/log/nginx/error.log`

2. **Try emergency restart**: See section F above

3. **Contact team**: Share error messages and logs

4. **Server admin**: For infrastructure issues

---

## 📅 Pre-Deployment Checklist

Before each deployment:
- [ ] All code committed locally
- [ ] Code pushed to GitHub (branch: main)
- [ ] Tested locally if possible
- [ ] No Python/JS errors in code
- [ ] Database migrations tested locally
- [ ] Know which deployment scenario to use (A/B/C/D)

During deployment:
- [ ] SSH into server successfully
- [ ] Navigate to bench directory
- [ ] Set site context (`bench use ...`)
- [ ] Pull latest changes (no conflicts)
- [ ] Run appropriate commands for your scenario
- [ ] Monitor logs during deployment
- [ ] Check supervisor status (all RUNNING)
- [ ] Verify nginx config if changed
- [ ] Test website in browser

After deployment:
- [ ] Website loads correctly
- [ ] No 502/500 errors
- [ ] Assets loading (check browser console)
- [ ] All features working
- [ ] Check error logs (should be empty)
- [ ] Monitor for 5-10 minutes

---

## 📊 Deployment Decision Tree

```
What changed?
│
├─ Only .py files (no schema) ──────────> Use Scenario A
│
├─ DocTypes/DB schema/patches ─────────> Use Scenario B
│
├─ JS/CSS/templates/frontend ──────────> Use Scenario C
│
├─ Multiple types or unsure ───────────> Use Scenario D (Safe)
│
└─ Site is broken/emergency ───────────> Use Scenario F (Emergency)
```

---

**Last Updated**: 2025-11-17
**App Repository**: https://github.com/Sena-Services/websitecms.git
**Deployed Branch**: main
**Site**: senamarketing.senaerp.com
**Bench**: ~/Sentra

---

🎉 **Happy Deploying!**
