@echo off
setlocal enabledelayedexpansion

echo Scanning for installed Java versions...
echo.

set FOUND_JAVA_LIST=

:: List all java locations
for /f "delims=" %%a in ('where java') do (
    echo   Found: %%a
    set FOUND_JAVA_LIST=!FOUND_JAVA_LIST!;%%a
)

echo.
echo Checking for Java 17 compatibility...
echo.

set JAVACMD=

:: Select first java path containing "17"
for /f "delims=" %%a in ('where java') do (
    echo %%a | findstr /c:"17" >nul
    if !errorlevel! == 0 (
        set JAVACMD="%%a"
        goto java_found
    )
)

echo ERROR: No Java 17 installation detected!
echo Please install Java 17, as LanguageTool requires it.
pause
exit /b

:java_found
echo Java 17 detected and selected: !JAVACMD!
echo.
echo Note: Only Java 17 is compatible with this LanguageTool server.
echo Starting LanguageTool server on port 8081...
echo.

!JAVACMD! -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081

pause
