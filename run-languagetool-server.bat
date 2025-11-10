@echo off
setlocal enabledelayedexpansion

:: Step 1 — Check if in the correct folder
if not exist "languagetool-server.jar" (
    echo ERROR: languagetool-server.jar not found!
    echo.
    echo Please make sure this batch file is in the LanguageTool folder.
    echo.
    pause
    exit /b
)

echo Correct folder detected.
echo.

:: Step 2 — Check for Java 17
echo Scanning for installed Java versions...
echo.

set JAVACMD=

for /f "delims=" %%a in ('where java') do (
    echo   Found: %%a
    echo %%a | findstr /c:"17" >nul
    if !errorlevel! == 0 (
        set JAVACMD="%%a"
        goto java_found
    )
)

echo.
echo ERROR: No Java 17 installation detected!
echo Please install Java 17, as LanguageTool requires it.
echo.
pause
exit /b

:java_found
echo.
echo Java 17 detected and selected:
echo   !JAVACMD!
echo.
echo Note: Only Java 17 works with this LanguageTool server.
echo.

:: Step 3 — Start server
echo Starting LanguageTool server on port 8081...
echo.

!JAVACMD! -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081

pause