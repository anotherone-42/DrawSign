# 🎨 DrawSign v2.0

Automatic bot to draw on Edusign - Windows & Linux compatible

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)
## ✨ Features

- ✅ Automatically draws on Edusign canvas
- 🎨 "Contours only" mode for line drawings
- 📏 Proportional image resizing
- 🐧 Cross-platform: Windows & Linux
- 🖌️ Adjustable line thickness (1-4px)

## 📦 Installation

### Windows

```bash
python setup.py
```

### Linux

```bash
python3 setup.py
```

The installer will detect your OS automatically and install the correct dependencies.

## 🚀 Usage

### Windows
```bash
run.bat
```

### Linux
```bash
./run.sh
```

## 📋 Simple Workflow

1. **Paste your Edusign link** → Copy the link from your email and paste it in the text box
2. **Click "Open Edusign"** → Browser opens automatically
3. **Select your image** → Choose a PNG, JPG, or GIF file
4. **Adjust settings** → Mode, thickness, and size
5. **Click "Draw"** → Watch the bot draw automatically! 🎨

## 🎨 Drawing Modes

- **Contours only**: Extracts and draws only the outlines (perfect for line art)
- **Full image**: Draws the complete image with all details

## 🔧 Requirements

### Chrome/Chromium

**Windows:** Google Chrome  
**Linux:** Chromium browser

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# Arch
sudo pacman -S chromium

# Fedora
sudo dnf install chromium
```

## 📁 Project Structure

```
DrawSign/
├── drawbot_edusign.py       # Main script
├── setup.py                 # Cross-platform installer
├── requirements-windows.txt # Windows dependencies
├── requirements-linux.txt   # Linux dependencies
└── README.md
```

## 🐛 Troubleshooting

**Module not found?**
```bash
python setup.py  # Reinstall
```

**Chrome not found?**
- Install Google Chrome (Windows) or Chromium (Linux)

## 🤝 Contributing

Pull requests are welcome! Feel free to open issues for bugs or feature requests.

## 📝 License

AGPL-3.0
