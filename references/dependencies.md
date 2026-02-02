# Xiaohongshu Automation Dependencies

To run browser automation locally and simulate real-user behavior effectively, you need the following:

## 1. System Requirements
- **Node.js**: Version 16.x or higher.
- **Chrome/Chromium Browser**: Installed on your machine.

## 2. NPM Packages
Run the following command in your project directory:

```bash
npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth
```

### Why these?
- **puppeteer**: The core engine to control Chrome.
- **puppeteer-extra**: Enables plugins for Puppeteer.
- **stealth-plugin**: **CRITICAL**. It patches common bot detection tests (navigator.webdriver, permissions, chrome.app, etc.). Without this, Xiaohongshu will likely trigger a CAPTCHA or block the request immediately.

## 3. Recommended IDE
- **VS Code**: With Prettier and ESLint for better JS editing.
