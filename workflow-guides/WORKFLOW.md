# Everyday Git + GitHub Workflow (for Bot Development)

This is your simple, repeatable process for working with Git and GitHub while developing your bot (or any project).

---

## Initial Setup (already done)

✅ `git init` → Started the Git project locally  
✅ `git remote add origin [GitHub URL]` → Linked local to GitHub  
✅ `git push -u origin master` → Pushed first version

---

## Daily Workflow

### 1️⃣ Make Changes

Edit your files as usual (add features, fix bugs, etc.).

### 2️⃣ Check what changed (optional but useful)

```bash
git status
```

This shows what files are new/modified.

### 3️⃣ Stage the changes

```bash
git add .
```

This adds **everything** that changed to be committed. You can also specify files individually if needed.

### 4️⃣ Commit the changes

```bash
git commit -m "Your commit message here"
```

Example:

```bash
git commit -m "Added new command to bot for rolling dice"
```

This saves the new version locally.

### 5️⃣ Push to GitHub

```bash
git push
```

This uploads the new version to GitHub → now your online repo is up to date!

### (Optional) Pull new changes if needed

If you switch to another machine or someone else makes changes:

```bash
git pull
```

This syncs your local version with the GitHub version.

---

## Summary of Commands

```bash
git status      # Check changes
git add .       # Stage all changes
git commit -m "Message"   # Save version locally
git push       # Upload to GitHub
git pull       # Download latest from GitHub
```

---

## Bonus (optional but good)

Add a README.md and .gitignore to make your repo clean and informative.

```bash
touch README.md
# edit it to explain your project

touch .gitignore
# add rules to ignore unnecessary files
