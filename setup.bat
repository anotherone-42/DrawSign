@echo off
echo ========================================
echo    DrawBot Simple - Installation
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installe
    echo Telechargez: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Creation du venv...
python -m venv venv

echo [2/4] Activation du venv...
call venv\Scripts\activate.bat

echo [3/4] Mise a jour de pip...
python -m pip install --upgrade pip

echo [4/4] Installation des dependances...
pip install selenium pillow numpy webdriver-manager pyautogui opencv-python pynput

echo.
echo ========================================
echo    Installation terminee !
echo ========================================
echo.
echo Lancez: run.bat
pause