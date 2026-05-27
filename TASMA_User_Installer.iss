; TASMA User Installer Setup Script
; Inno Setup v6.0+
; 
; This creates a professional installer EXE for end users
; Includes: TASMA app + centralized booking database + user authentication + setup wizard
;
; KEY FEATURES (v2.2+):
; ✓ Booking data synchronized with server database (shared across all users)
; ✓ User authentication via server
; ✓ Real-time synchronization between clients
; ✓ Automatic first-run setup wizard
; ✓ Network database connection validation
; ✓ Fixed: Database path method now correctly defined in all app classes
;
; LATEST FIXES (v2.2.1):
; - CRITICAL: Fixed missing threading import (was causing crash on startup)
; - Fixed slow startup (5-10 seconds) - now appears in <0.5 seconds with background setup
; - Fixed time input not captured correctly when typed into spinbox
; - Fixed calendar view not updating after new booking creation
; - Fixed AttributeError with get_db_path() in TasmaBookingApp
; - All booking operations now correctly use server database
; - Optimized network/database timeouts (2s network, 5s database)
;
; To build: Open this file in Inno Setup IDE and click Build > Compile

[Setup]
AppName=TASMA Board Room Booking System
AppVersion=2.2.1
AppPublisher=TASMA
AppPublisherURL=https://tasma.local
AppSupportURL=https://tasma.local
AppUpdatesURL=https://tasma.local
DefaultDirName={autopf}\TASMA
DefaultGroupName=TASMA Board Room Booking System
OutputDir=setup_output
OutputBaseFilename=TASMA_User_Setup_v2.2.1
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UsedUserAreasWarning=no
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable
Source: "installer_build\dist\TASMA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\SETUP_USER.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\SETUP_SERVER_CLIENT.py"; DestDir: "{app}"; Flags: ignoreversion

; User management (for server admin)
Source: "installer_build\dist\ADD_USER_TO_SERVER.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\SETUP_SERVER.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\MIGRATE_ADD_USER_REQUESTS.py"; DestDir: "{app}"; Flags: ignoreversion

; Logo and icons
Source: "installer_build\dist\tasma_logo.webp"; DestDir: "{app}"; Flags: ignoreversion

; Database modules
Source: "installer_build\dist\db_optimized.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\user_data_sync.py"; DestDir: "{app}"; Flags: ignoreversion

; Configuration template
Source: "installer_build\dist\config.ini.template"; DestDir: "{app}"; Flags: ignoreversion

; License
Source: "installer_build\dist\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

; Quick setup guide
Source: "installer_build\dist\CLIENT_QUICK_SETUP.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\QUICK_SETUP_CARD.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\FIX_REGISTRATION_ISSUE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\FIX_LOGIN_FREEZE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\BUILD_v2.2_FIXES_SUMMARY.md"; DestDir: "{app}"; Flags: ignoreversion

; Diagnostic tools
Source: "installer_build\dist\DATABASE_DIAGNOSTIC.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_build\dist\TROUBLESHOOT_USER_LOGIN.md"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "SETUP_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_DATA_SYNC_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "NETWORK_DATABASE_SETUP.md"; DestDir: "{app}"; Flags: ignoreversion

; v2.2.1 Fix Documentation
Source: "CALENDAR_REFRESH_FIX_v2.2.1.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "TIME_INPUT_FIX_v2.2.1.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "STARTUP_OPTIMIZATION_v2.2.1.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "DEPLOYMENT_PACKAGE_v2.2.1.md"; DestDir: "{app}"; Flags: ignoreversion

; Icon
Source: "booking_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\TASMA"; Filename: "{app}\TASMA.exe"; IconFilename: "{app}\booking_icon.ico"
Name: "{group}\Configuration"; Filename: "{app}\SETUP_USER.py"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,TASMA}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\TASMA"; Filename: "{app}\TASMA.exe"; IconFilename: "{app}\booking_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\TASMA.exe"; Description: "{cm:LaunchProgram,TASMA}"; Flags: nowait postinstall shellexec

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox('TASMA v2.2.1 installation complete!' + #13#13 +
           'The application is launching now...' + #13#13 +
           'NEW IN THIS VERSION:' + #13 +
           '✓ CRITICAL: Fixed startup crash (missing threading module)' + #13 +
           '✓ Optimized startup speed (now <0.5 seconds instead of 8-12 seconds)' + #13 +
           '✓ Fixed time input (typed hour values now captured correctly)' + #13 +
           '✓ Fixed calendar view updating after new bookings' + #13 +
           '✓ Reduced network/database timeout delays' + #13#13 +
           'QUICK START:' + #13 +
           '1. Run Configuration from Start menu' + #13 +
           '2. Enter server database path' + #13 +
           '3. Test connection and Save' + #13#13 +
           'For help, see documentation in the TASMA folder.',
           mbInformation, MB_OK);
  end;
end;

[Messages]
WelcomeLabel1=Welcome to TASMA Board Room Booking System Setup
WelcomeLabel2=This will install TASMA on your computer.%n%nKey Features:%n✓ Centralized booking database (all users share same bookings)%n✓ User authentication%n✓ Real-time synchronization%n%nServer Database Location:%n\\GVBSERVER\C$\Users\Administrator\AppData\Roaming\TASMA\bookings.db%n%nClick Next to continue.
FinishedHeadingLabel=Completing TASMA Board Room Booking System Setup
FinishedLabelNoIcons=Setup has finished installing TASMA on your computer.%n%nYou must now run the Configuration wizard to set up your database connection.%n%nAll bookings will be stored on the server and shared with other users.
FinishedLabel=Setup has finished installing TASMA on your computer.%n%nThe application is ready to use. You should now run the Configuration wizard from the Start menu.%n%nAll bookings will sync with the server database.
