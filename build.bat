@echo off
chcp 65001 >nul
REM DeBugBuddy Build and Publish Script (Windows)
REM Makes packaging and publishing easier

echo.
echo 🐛 DeBugBuddy Build Script
echo ═══════════════════════════════════════════
echo.

REM
echo ▶ Cleaning old builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist debugbuddy-cli.egg-info rmdir /s /q debugbuddy-cli.egg-info
echo ✓ Cleaned old builds
echo.

REM
echo ▶ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python not found
    pause
    exit /b 1
)
echo ✓ Python found
echo.

REM
echo ▶ Checking dependencies...
pip install -q wheel twine setuptools build --upgrade
echo ✓ Dependencies installed
echo.

REM
echo ▶ Building package...
python -m build
if errorlevel 1 (
    echo ✗ Build failed
    pause
    exit /b 1
)
echo ✓ Package built
echo.

REM
echo ▶ Checking package...
twine check "dist\*"
if errorlevel 1 (
    echo ✗ Package check failed
    pause
    exit /b 1
)
echo ✓ Package check passed
echo.

REM
echo ═══════════════════════════════════════════
echo 📦 Package Information
echo ═══════════════════════════════════════════
dir dist
echo.

REM
echo What would you like to do?
echo   1) Test locally (pip install dist/*.whl)
echo   2) Upload to TestPyPI
echo   3) Upload to PyPI
echo   4) Exit
echo.
set /p choice="Enter choice [1-4]: "

if "%choice%"=="1" (
    echo ▶ Installing locally...
    pip uninstall debugbuddy-cli -y 2>nul
    for %%f in (dist\*.whl) do pip install %%f
    echo ✓ Installed locally
    echo.
    echo Test it:
    echo   db
    echo   db --version
    echo   db explain "test error"
    pause
    goto :end
) else if "%choice%"=="2" (
    echo ▶ Uploading to TestPyPI...
    twine upload --repository testpypi "dist\*"
    if errorlevel 1 (
        echo ✗ Upload failed
        pause
        exit /b 1
    )
    echo ✓ Uploaded to TestPyPI
    echo.
    echo Test it:
    echo   pip install --index-url https://test.pypi.org/simple/ debugbuddy-cli
    pause
    goto :end
) else if "%choice%"=="3" (
    echo ⚠ Are you sure you want to upload to PyPI?
    set "confirm="
    set /p confirm="This cannot be undone! [y/N]: "
    setlocal enabledelayedexpansion
    set "confirm=!confirm: =!"
    if defined confirm set "confirm=!confirm:~0,1!"
    if /i "!confirm!"=="y" (
        endlocal
        echo ▶ Uploading to PyPI...
        twine upload "dist\*"
        if errorlevel 1 (
            echo ✗ Upload failed
            pause
            exit /b 1
        )
        echo ✓ Uploaded to PyPI
        echo.
        echo 🎉 DeBugBuddy is now live on PyPI!
        echo.
        echo Install it:
        echo   pip install debugbuddy-cli
        echo.
        pause
        goto :end
    ) else (
        endlocal
        echo ⚠ Upload cancelled
        pause
        goto :end
    )
) else if "%choice%"=="4" (
    echo ✓ Build complete
    goto :end
) else (
    echo ✗ Invalid choice
    pause
    goto :end
)

:end
echo.
echo ✓ Done! 🎉
echo.