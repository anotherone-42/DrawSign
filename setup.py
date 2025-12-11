#!/usr/bin/env python3
"""
DrawSign - Installation multiplateforme
Supporte Windows et Linux avec environnement virtuel
"""

import sys
import subprocess
import platform
import os
import venv
import urllib.request

def detect_os():
    """Détecte automatiquement le système d'exploitation"""
    system = platform.system()
    return system.lower()

def create_venv():
    """Crée un environnement virtuel"""
    venv_path = "venv"
    
    if os.path.exists(venv_path):
        print(f"\n📦 Virtual environment already exists: {venv_path}")
        return venv_path
    
    print(f"\n📦 Creating virtual environment: {venv_path}")
    try:
        venv.create(venv_path, with_pip=True)
        print("✅ Virtual environment created")
    except Exception as e:
        print(f"⚠️  Error creating venv with pip: {e}")
        print("🔧 Trying alternative method...")
        
        # Méthode alternative : créer sans pip puis installer manuellement
        venv.create(venv_path, with_pip=False)
        
        # Installer pip manuellement
        venv_python = get_venv_python(venv_path)
        
        print("📥 Downloading get-pip.py...")
        import urllib.request
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_path = "get-pip.py"
        
        try:
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            print("📦 Installing pip in venv...")
            subprocess.check_call([venv_python, get_pip_path])
            os.remove(get_pip_path)
            print("✅ Pip installed successfully")
        except Exception as pip_error:
            print(f"❌ Failed to install pip: {pip_error}")
            print("\n💡 Manual fix:")
            print(f"   1. Delete venv: rm -rf {venv_path}")
            print("   2. Install python3-venv: sudo apt install python3-venv")
            print("   3. Run setup.py again")
            raise
    
    return venv_path

def get_venv_python(venv_path):
    """Retourne le chemin vers le Python du venv"""
    os_type = detect_os()
    
    if os_type == "windows":
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        # Essayer python3 d'abord, puis python
        python3_path = os.path.join(venv_path, "bin", "python3")
        python_path = os.path.join(venv_path, "bin", "python")
        
        if os.path.exists(python3_path):
            return python3_path
        elif os.path.exists(python_path):
            return python_path
        else:
            # Fallback
            return python3_path
    
    return python_path

def install_packages(venv_python, packages):
    """Installe les packages Python dans le venv"""
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip
    subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install packages
    for package in packages:
        print(f"  └─ {package}")
    
    subprocess.check_call([venv_python, "-m", "pip", "install"] + packages)

def setup_windows(venv_path):
    """Configuration Windows"""
    print("\n🪟 Configuration for Windows")
    packages = [
        "selenium>=4.15.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "opencv-contrib-python>=4.8.0",
        "webdriver-manager>=4.0.0"
    ]
    
    venv_python = get_venv_python(venv_path)
    install_packages(venv_python, packages)
    
    # Créer run.bat
    with open("run.bat", "w", encoding="utf-8") as f:
        f.write("""@echo off
echo ========================================
echo    DrawSign v2.0 - Starting
echo ========================================

if not exist "venv\\Scripts\\python.exe" (
    echo [ERROR] Virtual environment not found
    echo Run setup.py first
    pause
    exit /b 1
)

venv\\Scripts\\python.exe drawbot_edusign.py
pause
""")
    print("\n✅ run.bat created")

def setup_linux(venv_path):
    """Configuration Linux"""
    print("\n🐧 Configuration for Linux")
    packages = [
        "selenium>=4.15.0",
        "pillow>=10.0.0",
        "numpy>=1.24.0",
        "opencv-contrib-python>=4.8.0",
        "webdriver-manager>=4.0.0"
    ]
    
    venv_python = get_venv_python(venv_path)
    install_packages(venv_python, packages)
    
    # Créer run.sh
    with open("run.sh", "w", encoding="utf-8") as f:
        f.write("""#!/bin/bash
echo "========================================"
echo "   DrawSign v2.0 - Starting"
echo "========================================"

if [ ! -f "venv/bin/python3" ]; then
    echo "[ERROR] Virtual environment not found"
    echo "Run setup.py first"
    exit 1
fi

venv/bin/python3 drawbot_edusign.py
""")
    
    # Rendre exécutable
    os.chmod("run.sh", 0o755)
    print("\n✅ run.sh created")

def interactive_setup():
    """Installation interactive"""
    print("""
╔════════════════════════════════════════╗
║                                        ║
║        🎨 DrawSign - Setup v2.0        ║
║     Cross-platform installation        ║
║                                        ║
╚════════════════════════════════════════╝
""")
    
    os_type = detect_os()
    print(f"🔍 System detected: {os_type.upper()}")
    
    # Créer le venv
    venv_path = create_venv()
    
    print("\nChoose your platform:")
    print("  1️⃣  Windows")
    print("  2️⃣  Linux")
    print("  3️⃣  Auto-detect (recommended)")
    print()
    
    choice = input("Your choice [3]: ").strip()
    
    # Si vide, utiliser 3 par défaut
    if not choice:
        choice = "3"
    
    print(f"\n🔧 Installing for: ", end="")
    
    if choice == "1":
        print("Windows (manual selection)")
        setup_windows(venv_path)
    elif choice == "2":
        print("Linux (manual selection)")
        setup_linux(venv_path)
    elif choice == "3":
        if os_type == "windows":
            print("Windows (auto-detected)")
            setup_windows(venv_path)
        elif os_type == "linux":
            print("Linux (auto-detected)")
            setup_linux(venv_path)
        else:
            print(f"\n❌ Unsupported system: {os_type}")
            print("Use option 1 or 2 to force installation.")
            sys.exit(1)
    else:
        print(f"\n❌ Invalid choice: '{choice}'")
        print("Please choose 1, 2, or 3")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("✅ Installation complete!")
    print("="*50)
    print(f"\n📁 Virtual environment: {venv_path}/")
    
    if os_type == "windows" or choice == "1":
        print("\n▶️  To start: run.bat")
        print("   (Double-click or type 'run.bat' in terminal)")
    else:
        print("\n▶️  To start: ./run.sh")
        print("   (Make executable: chmod +x run.sh)")
    
    print("\n📝 Files created:")
    if os.path.exists("run.bat"):
        print("  ✅ run.bat")
    if os.path.exists("run.sh"):
        print("  ✅ run.sh")
    if os.path.exists(venv_path):
        print(f"  ✅ {venv_path}/")
    
    input("\nPress Enter to exit...")

def main():
    try:
        interactive_setup()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()