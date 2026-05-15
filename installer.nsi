; TASMA Board Room Booking System - Professional Installer
; This NSIS script creates a professional installer for deployment

!include "MUI2.nsh"
!include "x64.nsh"

; Name and file
Name "TASMA Board Room Booking System"
OutFile "TASMA_Booking_System_Installer.exe"

; Default installation folder
InstallDir "$PROGRAMFILES\TASMA Booking System"

; Variables
Var StartMenuFolder

; MUI Settings
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Install Application"
    SetOutPath "$INSTDIR"
    
    ; Copy executable
    File "dist\TASMA Board Room Booking System.exe"
    
    ; Copy database
    File "bookings.db"
    
    ; Copy logo
    File "tasma_logo.webp"
    
    ; Create shortcuts
    !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
        CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
        CreateShortcut "$SMPROGRAMS\$StartMenuFolder\TASMA Booking System.lnk" "$INSTDIR\TASMA Board Room Booking System.exe"
        CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    !insertmacro MUI_STARTMENU_WRITE_END
    
    ; Create desktop shortcut
    CreateShortcut "$DESKTOP\TASMA Booking System.lnk" "$INSTDIR\TASMA Board Room Booking System.exe"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Register uninstall in Control Panel
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA" \
                     "DisplayName" "TASMA Board Room Booking System"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA" \
                     "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA" \
                     "DisplayIcon" "$INSTDIR\TASMA Board Room Booking System.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA" \
                     "Publisher" "TASMA Group"
SectionEnd

; Uninstaller
Section "Uninstall"
    ; Delete shortcuts
    !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
    Delete "$SMPROGRAMS\$StartMenuFolder\TASMA Booking System.lnk"
    Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
    RMDir "$SMPROGRAMS\$StartMenuFolder"
    Delete "$DESKTOP\TASMA Booking System.lnk"
    
    ; Delete files
    Delete "$INSTDIR\TASMA Board Room Booking System.exe"
    Delete "$INSTDIR\bookings.db"
    Delete "$INSTDIR\tasma_logo.webp"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA"
SectionEnd
