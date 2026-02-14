# 🚀 Senaerp Platform Deployment Guide

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
senaerp_platform
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

## 🎯 Quick Deployment (One Command)

### ✅ TESTED & WORKING - Use This Method

**This is the proven deployment process:**

```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && cd ~/Sentra && bench use senamarketing.senaerp.com && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

**What this does:**
1. Connects to server as sentra user (no root needed!)
2. Pulls latest code from GitHub (upstream/main)
3. Sets the active site context
4. Runs database migrations (for DocType schema changes)
5. Rebuilds frontend assets
6. Clears Redis cache
7. Gracefully reloads gunicorn workers (no downtime!)

**Time:** ~2-3 minutes
**Downtime:** Zero! (graceful reload)

---

## 🚨 If Git Pull Fails with Permission Errors

**Problem:** Sometimes git objects get owned by root from previous deployments.

**Symptoms:**
- `error: insufficient permission for adding an object`
- `Permission denied` when running `git pull`

**Solution: Fresh Clone (One-time fix)**

Run this ONCE to fix permissions permanently:

```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps && mv senaerp_platform senaerp_platform.bak && git clone https://github.com/Sena-Services/senaerp_platform.git && cd senaerp_platform && git remote add upstream https://github.com/Sena-Services/senaerp_platform.git"
```

**What this does:**
1. Backs up old senaerp_platform directory (in case you need it)
2. Clones fresh copy from GitHub (with correct permissions)
3. Adds upstream remote

Then run the normal deployment command above.

**Important:** After fresh clone, you'll need to run migration and build since it's a fresh copy:
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

---

## 🚨 DEPRECATED: Don't Use These Methods

**⚠️ This method has permission issues. Use the "One Command" method above instead.**

These steps were the old manual process but are no longer recommended:
- Requires root access
- Has permission conflicts
- More complex and error-prone
- Causes unnecessary downtime

**Use the tested one-command deployment instead!**

---

## 📝 Quick Reference - Copy & Paste These

### 🚀 Standard Deployment (Most Common)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && cd ~/Sentra && bench use senamarketing.senaerp.com && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

### ⚡ Python-Only Changes (Fastest)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

### 🔧 Fix Git Permissions (If git pull fails)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps && mv senaerp_platform senaerp_platform.bak && git clone https://github.com/Sena-Services/senaerp_platform.git && cd senaerp_platform && git remote add upstream https://github.com/Sena-Services/senaerp_platform.git"
```

### ✅ Check if Deployment Worked
```bash
curl -s "https://senamarketing.senaerp.com/api/method/ping" | python3 -m json.tool
```

### 📊 Check Website Environments
```bash
curl -s "https://senamarketing.senaerp.com/api/method/senaerp_platform.api.website_environment.get_environment_count" | python3 -m json.tool
```

---

## 📖 Step-by-Step Deployment Guide

### Prerequisites

Before deploying, make sure:
1. ✅ Your local changes are committed
2. ✅ Your changes are pushed to GitHub (branch: `main`)

**Check local status:**
```bash
cd /Users/aakashchid/workshop/sentraBench/apps/senaerp_platform
git status
git log upstream/main..HEAD  # Should be empty if everything is pushed
```

**Push if needed:**
```bash
git push upstream main
```

---

### Understanding What Changed

Choose the deployment type based on what you changed:

---

## A) Python-only Code Change (No Schema, No Assets)

**When to use:** Only `.py` files changed, no DocType changes, no frontend changes

**One command:**
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

**What this does:**
1. Pulls latest Python code
2. Gracefully reloads gunicorn workers (picks up new .py files)

**Time:** ~10 seconds
**Downtime:** Zero (graceful reload)

---

## B) DocType/Schema or Patch Changes (Requires Migrate)

**When to use:**
- New/modified DocTypes (like adding a field)
- Database schema changes
- Patch files added
- Permission changes

**One command (USE THIS!):**
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && cd ~/Sentra && bench use senamarketing.senaerp.com && bench --site senamarketing.senaerp.com migrate && bench clear-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

**What this does:**
1. Pulls latest code (including DocType JSON changes)
2. Sets active site
3. Runs database migrations (creates/modifies tables)
4. Clears cache
5. Gracefully reloads workers

**Time:** ~2-3 minutes
**Downtime:** Zero

**Example:** When we added the `category` field to Website Environment, this is what we used.

---

## C) Frontend/Asset Changes (JS/CSS/Web Templates)

**When to use:**
- JavaScript/CSS changes
- Web templates modified
- Vue/React components updated
- package.json updated

**One command:**
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && cd ~/Sentra && bench use senamarketing.senaerp.com && bench build && bench clear-website-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

**What this does:**
1. Pulls latest code
2. Sets active site
3. Builds frontend assets (compiles JS/CSS)
4. Clears website cache
5. Reloads workers

**Time:** ~1-2 minutes
**Downtime:** Zero

**Note:** senaerp_platform doesn't have complex frontend builds, so this is usually fast.

---

## D) Full "Safe" Deploy (Covers Everything)

**When to use:**
- Unsure what changed
- Multiple types of changes
- Major version updates
- After merging multiple PRs

**One command (Recommended!):**
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra/apps/senaerp_platform && git pull upstream main && cd ~/Sentra && bench use senamarketing.senaerp.com && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-cache && pkill -HUP -f 'gunicorn.*frappe.app:application'"
```

**What this does:**
1. Pulls latest code
2. Sets active site
3. Runs migrations (safe even if nothing to migrate)
4. Builds frontend (safe even if no changes)
5. Clears all caches
6. Reloads workers

**Time:** ~2-3 minutes
**Downtime:** Zero

**This is the safest option - when in doubt, use this!**

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
curl -I https://senamarketing.senaerp.com/assets/senaerp_platform/js/senaerp_platform.bundle.js
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
cd ~/Sentra/apps/senaerp_platform
git remote -v

# If upstream doesn't exist, add it:
git remote add upstream https://github.com/Sena-Services/senaerp_platform.git

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
cd ~/Sentra/apps/senaerp_platform
rm -rf node_modules
yarn install
cd ~/Sentra
bench build --app senaerp_platform
```

3. **Build with verbose output:**
```bash
bench build --app senaerp_platform --verbose
```

---

### Problem: Assets Not Loading

**Symptoms:** 404 on CSS/JS files, blank pages

**Solutions:**

1. **Rebuild assets:**
```bash
bench build --app senaerp_platform
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
ls -la ~/Sentra/sites/assets/senaerp_platform/
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
| `bench build --app senaerp_platform` | Build only senaerp_platform assets |
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
│  senaerp_platform     │
└────────┬────────┘
         │ git pull
         ▼
┌─────────────────┐
│  Server         │
│  ~/Sentra/apps/ │
│  senaerp_platform     │
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
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/senaerp_platform && git pull upstream main && cd - && sudo supervisorctl restart all"
```

### Deploy with Migration (90 seconds)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/senaerp_platform && git pull upstream main && cd - && bench --site senamarketing.senaerp.com migrate && bench clear-cache && sudo supervisorctl restart all"
```

### Deploy Frontend Changes (2 minutes)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/senaerp_platform && git pull upstream main && cd - && bench build && bench clear-website-cache && sudo supervisorctl restart all"
```

### Full Safe Deploy (3 minutes)
```bash
ssh sentra@159.89.174.135 "cd ~/Sentra && bench use senamarketing.senaerp.com && cd apps/senaerp_platform && git pull upstream main && cd - && bench --site senamarketing.senaerp.com migrate && bench build && bench clear-website-cache && bench clear-cache && yes | bench setup nginx && sudo nginx -t && sudo systemctl reload nginx && sudo supervisorctl restart all"
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
├─ Only .py files (no schema) ──────────> Scenario A: Python-only (~10 sec)
│
├─ DocTypes/DB schema/fields ──────────> Scenario B: With Migration (~2 min)
│
├─ JS/CSS/templates/frontend ──────────> Scenario C: With Build (~2 min)
│
├─ Multiple types or unsure ───────────> Scenario D: Full Safe Deploy (~3 min)
│
└─ Git permission errors ──────────────> Fix Git Permissions (one-time)
```

**When in doubt, use Scenario D (Full Safe Deploy) - it handles everything!**

---

---

## 🎓 Key Learnings

### Why This Works vs Old Methods

**Old Problem:**
- Used `sudo` and root access
- Git objects became owned by root
- Permission conflicts on every deployment
- Complex multi-step process

**New Solution:**
- Everything runs as `sentra` user (no sudo!)
- Uses `pkill -HUP` for graceful reload (no supervisor restart needed)
- One command does everything
- Zero downtime deployments

### Why Not Use `bench restart`?

`bench restart` requires `sudo supervisorctl` which needs password input in SSH. Instead we use:
```bash
pkill -HUP -f 'gunicorn.*frappe.app:application'
```

This sends a HUP signal to gunicorn master process, which gracefully reloads workers without downtime.

### Why Clone Fresh When Git Fails?

Git permission errors happen when root user has run git commands (from old deployment methods). The `.git/objects` directory gets root-owned files that sentra user can't modify.

**Quick fix:** Fresh clone with correct permissions from the start!

---

**Last Updated**: 2025-11-18
**Tested On**: Category field deployment
**App Repository**: https://github.com/Sena-Services/senaerp_platform.git
**Deployed Branch**: main
**Production Site**: senamarketing.senaerp.com
**Server**: 159.89.174.135
**Bench Path**: /home/sentra/Sentra

---

🎉 **Happy Deploying!**
