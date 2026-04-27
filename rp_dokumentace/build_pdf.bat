@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo Building main.tex...
if exist main.pdf del main.pdf
pdflatex -interaction=nonstopmode -synctex=1 main.tex
pdflatex -interaction=nonstopmode -synctex=1 main.tex

if errorlevel 1 (
  echo.
  echo Build failed. Check output above for errors.
  exit /b 1
)

echo.
echo Build succeeded. Generated main.pdf
exit /b 0
