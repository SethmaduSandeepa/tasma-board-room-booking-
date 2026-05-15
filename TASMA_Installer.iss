; TASMA Board Room Booking System - Professional Standalone Installer
; Version 2.1 - Enterprise Ready
; Inno Setup 6.0+

[Setup]
AppName=TASMA Board Room Booking System
AppVersion=2.1.0
AppPublisher=TASMA Group
AppPublisherURL=https://www.tasmagroup.com
AppSupportURL=https://www.tasmagroup.com/support
AppUpdatesURL=https://www.tasmagroup.com/updates
AppCopyright=Copyright (C) 2025 TASMA Group. All Rights Reserved.
AppId=TASMA_Booking_System_Professional_2025
DefaultDirName={autopf}\TASMA Board Room Booking System
DefaultGroupName=TASMA Board Room Booking System
AllowNoIcons=no
OutputDir=.\setup_output
OutputBaseFilename=TASMA_Booking_System_Setup_v2.1_Professional
Compression=lzma2
SolidCompression=yes
ArchitecturesAllowed=x86 x64
ArchitecturesInstallIn64BitMode=x64
LicenseFile=LICENSE.txt
WizardStyle=modern
SetupIconFile=booking_icon.ico
UninstallDisplayIcon={app}\booking_icon.ico
UninstallDisplayName=TASMA Board Room Booking System v2.1
CloseApplications=yes
RestartApplications=yes
AllowUNCPath=no
PrivilegesRequired=admin
AllowRootDirectory=no
ShowLanguageDialog=no
VersionInfoVersion=2.1.0.0
VersionInfoProductName=TASMA Board Room Booking System
VersionInfoProductVersion=2.1
VersionInfoCompany=TASMA Group
VersionInfoCopyright=2025 TASMA Group
UninstallFilesDir={app}\Uninstall
CreateUninstallRegKey=yes
CreateAppDir=yes
UsePreviousAppDir=yes
UsePreviousTasks=yes

; User messages
[Messages]
WelcomeLabel1=Welcome to TASMA Board Room Booking System Installation
WelcomeLabel2=This wizard will install TASMA v2.1 on your computer.%n%nTASMA is a professional board room booking system designed for enterprise use.%n%nPlease close any running instances of TASMA before proceeding.
FinishedHeadingLabel=Installation Complete
FinishedLabelNoIcons=TASMA has been successfully installed on your computer.
FinishedLabel=TASMA has been successfully installed on your computer.%n%nClick Finish to launch the application.
ConfirmUninstall=Are you sure you want to completely remove TASMA Board Room Booking System and all its components?

[Files]
; Application executable - must be current version with bug fixes
Source: "deployment\TASMA Board Room Booking System.exe"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full
; Database - preserve on upgrades to protect user data and approvals
Source: "deployment\bookings.db"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-modify
; Support files
Source: "deployment\booking_icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full
Source: "deployment\tasma_logo.webp"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full
Source: "deployment\DEPLOYMENT_GUIDE.md"; DestDir: "{app}"; Flags: ignoreversion isreadme; Permissions: users-full
Source: "deployment\README.md"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full
Source: "deployment\FEATURES.md"; DestDir: "{app}"; Flags: ignoreversion; Permissions: users-full

[Icons]
; Start menu shortcuts
Name: "{group}\TASMA Board Room Booking System"; Filename: "{app}\TASMA Board Room Booking System.exe"; WorkingDir: "{app}"; IconFilename: "{app}\booking_icon.ico"; Comment: "Open TASMA Board Room Booking System"
Name: "{group}\Documentation\Features"; Filename: "{app}\FEATURES.md"; Comment: "View TASMA Features"
Name: "{group}\Documentation\Deployment Guide"; Filename: "{app}\DEPLOYMENT_GUIDE.md"; Comment: "Installation and Deployment Guide"
Name: "{group}\Documentation\README"; Filename: "{app}\README.md"; Comment: "Read Me First"
Name: "{group}\Uninstall TASMA"; Filename: "{uninstallexe}"; Comment: "Remove TASMA from your computer"
; Desktop shortcut (optional)
Name: "{commondesktop}\TASMA Board Room Booking System"; Filename: "{app}\TASMA Board Room Booking System.exe"; WorkingDir: "{app}"; IconFilename: "{app}\booking_icon.ico"; Tasks: desktopicon; Comment: "TASMA - Professional Board Room Booking"
; Startup shortcut (optional)
Name: "{commonstartup}\TASMA Board Room Booking System"; Filename: "{app}\TASMA Board Room Booking System.exe"; WorkingDir: "{app}"; Tasks: startupicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked
Name: "startupicon"; Description: "Launch &TASMA on startup"; GroupDescription: "Startup:"; Flags: unchecked

[Run]
Filename: "{app}\TASMA Board Room Booking System.exe"; Description: "Launch TASMA Board Room Booking System"; Flags: nowait postinstall skipifsilent

[Registry]
; Application info for Control Panel
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "DisplayName"; ValueData: "TASMA Board Room Booking System v2.1"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "2.1"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "Publisher"; ValueData: "TASMA Group"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "URLInfoAbout"; ValueData: "https://www.tasmagroup.com"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "URLUpdateInfo"; ValueData: "https://www.tasmagroup.com/updates"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\TASMA_Booking_System_Professional_2025"; ValueType: string; ValueName: "HelpLink"; ValueData: "https://www.tasmagroup.com/support"
Root: HKLM; Subkey: "Software\TASMA Group\TASMA Board Room Booking System"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\TASMA Group\TASMA Board Room Booking System"; ValueType: string; ValueName: "Version"; ValueData: "2.1"

[Code]
var
  IsUpgrade: Boolean;

function InitializeSetup(): Boolean;
begin
  Result := True;
  IsUpgrade := False;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ExistingDBPath: String;
  BackupPath: String;
begin
  if CurStep = ssInstall then
  begin
    ExistingDBPath := ExpandConstant('{app}\bookings.db');
    BackupPath := ExpandConstant('{app}\bookings.db.backup');
    
    { If database exists, this is an upgrade }
    if FileExists(ExistingDBPath) then
    begin
      IsUpgrade := True;
      { Back up the existing database }
      if FileExists(BackupPath) then
        DeleteFile(BackupPath);
      FileCopy(ExistingDBPath, BackupPath, False);
    end;
  end;
  
  { After files are copied, restore the backed up database if this was an upgrade }
  if CurStep = ssPostInstall then
  begin
    ExistingDBPath := ExpandConstant('{app}\bookings.db');
    BackupPath := ExpandConstant('{app}\bookings.db.backup');
    
    if IsUpgrade and FileExists(BackupPath) then
    begin
      { This is an upgrade - restore the backed up database }
      if FileExists(ExistingDBPath) then
        DeleteFile(ExistingDBPath);
      FileCopy(BackupPath, ExistingDBPath, False);
      DeleteFile(BackupPath);
    end;
  end;
end;
