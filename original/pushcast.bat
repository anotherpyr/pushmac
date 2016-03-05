@echo off
:: pushCash v0.5.2

::===User Config=================================================

set myFreq=4
set mediaPath=c:\users\mark\downloads\media
set pyTivoPath=c:\pyTivo\pyTivo.py
set pythonPath=c:\python27\python.exe
set gPodderPath="c:\program files (x86)\gpodder"

::===============================================================
:Start   
   set ver=0.5.2
   setlocal enabledelayedexpansion
   for %%I in (%*) do if /i "%%~I"=="-s" (
       powershell -window minimized -command ""
   )

::===========myMenu=============
:myMenu

   call :setScreen
   call :checkPyTivo
   call :checkGpodder
   call :checkAutoPush
   call :checkTaskScheduler

   ::====Command Line - Auto=======

   if "%1"=="-a" (
   	set pushCast=Auto
   	goto pushCast
   )

   set pushCast=Manual
   echo.
   echo ====================================
   echo  pushCast v%ver%            
   echo  OS: Windows                                        
   echo ====================================
   echo  App Toggles:                      
   echo.                   
   echo    1. pyTivo              [%pyTivo%]             
   echo    2. gPodder             [%gPodderGUI%]           
   echo    3. Auto_Push           [%AutoPush%] 
   echo    4. Scheduler [%myFreq%Hr]     [%TaskScheduler%]
   echo.
   echo ====================================
   echo  pushCast:                       
   echo.                                          
   echo    A. Run Auto ^& Exit    
   echo    M. Process Metadata
   echo.                                
   echo    G. gPodder GUI 
   echo    V. View AutoPush Log
   echo.
   echo    P. Pause All   
   echo    R. Resume All
   echo.                                          
   echo    X. Exit                           
   echo.                                          
   echo ====================================
   echo.
   choice /C:1234AMGVPRX /N /M "Select: "
   echo.
  
   if errorlevel 11 goto end
   if errorlevel 10 call :Resume
   if errorlevel 9 call :Pause
   if errorlevel 8 goto AutoPushView
   if errorlevel 7 goto gPodderGUI
   if errorlevel 6 goto MetaData
   if errorlevel 5 goto pushCast
   if errorlevel 4 call :taskScheduler
   if errorlevel 3 goto AutoPush
   if errorlevel 2 call :gPodder
   if errorlevel 1 call :pyTivo

goto myMenu

::====================================
:gPodderGUI

   if %gPodderGUI%==Stopped (
      cd %gPodderPath%
      start gpodder.exe 
   )
   goto myMenu

::====================================
:AutoPushView

   start notepad %mediaPath%\auto_push.txt
   goto myMenu

::====================================
:pushCast

   cls
   echo.
   echo Running pushCast - Auto v%ver%
   echo ============================
   echo.

::====================================
:pyTivo

   if %pyTivo%==Stopped (
      echo pushCast - Starting pyTivo
      Start "pushCast - pyTivo" /min %pythonPath% %pyTivoPath% /wait
   ) else (
      if %pushCast%==Manual (
      	echo pushCast - Stopping pyTivo
      	if %pyTivo%==Running taskkill /im python.exe >Nul
      )
   )
   if !pushCast!==Manual goto :eof
   
::====================================
:gPodder

   cls
   echo.
   echo pushCast - Running gPodder
   echo ==========================
   echo.
   cd %gPodderPath%
   call gpo update 2>nul 
   echo.
   call gpo download 2>nul
   echo.
   if !pushCast!==Manual goto myMenu

::====================================
:Metadata

   echo pushCast - Preparing Metadata

   set File1=filelist.txt
   set File2=filelist2.txt

   set cdPath=%mediaPath:~3%
   cd/%cdPath%

   ::Remove existing metadata files
   for /f "delims=" %%f in (%File2%) do del "%%f" 2>nul

   ::List current \Media files
   dir /s/b *.mp4 *.mkv *.m4v > %File1%

   ::Write metadata
   for /f "tokens=*" %%a in (%File1%) do ( 

      :: filename, w/extension
      set myFile=%%~nxa

      :: filename, no extension
      set myTitle=%%~na

      :: Full path, no filename
      set myPath=%%~dpa

      :: Parent folder
      for %%b in ("!myPath:~0,-1!") do set "myParent=%%~Nb" && set myFolder=~Misc Podcasts

rem ::===TiVo Folders=====================

      echo !myParent!|FINDSTR /i /c:"Google" >NUL
      if !errorlevel! == 0 set myFolder=~Google Podcasts

      echo !myParent!|FINDSTR /i /c:"B and H" >NUL
      if !errorlevel! == 0 set myFolder=~Photo Podcasts

      echo !myParent!|FINDSTR /i /c:"thrones" >NUL
      if !errorlevel! == 0 set myFolder=~Game of Thrones

      echo !myParent!|FINDSTR /i /c:"photo" /c:"jared polin" >NUL
      if !errorlevel! == 0 set myFolder=~Photo Podcasts

      echo !myParent!|FINDSTR /i /c:"photo" /c:"crunch" >NUL
      if !errorlevel! == 0 set myFolder=~TechCrunch Podcasts

      echo !myParent!|FINDSTR /i /c:"verge" >NUL
      if !errorlevel! == 0 set myFolder=~The Verge Podcasts

      echo !myParent!|FINDSTR /i /c:"cnet" /c:"how to" /c:"crave" /c:"googlicious" /c:"first look" /c:"next big thing" /c:"news" /c:"cracking open" /c:"apple byte" /c:"crave" /c:"car tech" >NUL
      if !errorlevel! == 0 set myFolder=~CNET Podcasts

      echo !myParent!|FINDSTR /i /c:"tedtalks" >NUL
      if !errorlevel! == 0 set myFolder=~TED Talks

      rem ::=============================
      :: Create Meta folder
      if not exist "!myPath!\.meta" mkdir "!myPath!.meta"

      set myMetaFile="!myPath!\.meta\!myFile!"
      echo title : !myFolder! > !myMetaFile!.txt
      echo seriesTitle :  !myFolder! >> !myMetaFile!.txt
      echo seriesId :  !myFolder! >> !myMetaFile!.txt
      echo episodeTitle :  !myTitle! >> !myMetaFile!.txt
      echo description :  !myTitle! >> !myMetaFile!.txt
      echo isEpisode : true >> !myMetaFile!.txt
      echo isEpisodic : true >> !myMetaFile!.txt
   )

   ::=============================
   
   dir /s/b *.*.txt > %File2%

   ::Count the Metadata files
   Set /a Qty=0
   For /f %%j in ('Type %File1%^|Find "" /v /c') Do Set /a Qty=%%j
   echo pushCast - %Qty% files processed
   if !pushCast!==Manual pause
   if !pushCast!==Manual goto myMenu

::=============subroutines============
:AutoPush

   if %AutoPush%==Stopped (
   	echo pushCast - Starting Auto_Push Service
   	echo. >> auto_push.txt
   	echo ***** pushCast - %date% %time% ***** >> auto_push.txt
   	cd\pytivo\service\win32
   	call start-service.bat >nul
	) else (
	   if %pushCast%==Manual (
		echo pushCast - Stopping Auto_Push Service
		cd\pytivo\service\win32
		call stop-service.bat >nul
	)
   )
	if !pushCast!==Manual goto myMenu
		
::====================================
:end

   echo.
   echo pushCast - Complete
   echo.
   echo.
   exit

::====================================
:checkPyTivo

   tasklist /FI "IMAGENAME eq python.exe" | find /I "python.exe">nul &&(
      set pyTivo=Running
   )||(
      set pyTivo=Stopped
   )
   goto :eof

::====================================
:checkGpodder

   tasklist /FI "IMAGENAME eq gPodder.exe" | find /I "gPodder.exe">nul &&(
      set gPodderGUI=Running
   )||(set gPodderGUI=Stopped)
   goto :eof

::====================================
:checkAutoPush

   sc query Auto_Push| find "RUNNING" >nul 2>&1 && set  AutoPush=Running
   sc query Auto_Push| find "RUNNING" >nul 2>&1 || set AutoPush=Stopped
   goto :eof

::====================================
:checkTaskScheduler

   set TaskScheduler=Stopped
   schtasks /query >doh
   findstr /B /I "pushCast" doh >nul
   if %errorlevel%==0  set TaskScheduler=Running
   goto :eof

::====================================
:TaskScheduler

   if %TaskScheduler%==Running (
      echo pushCast - Stopping Task Scheduler
      schtasks /delete /tn pushCast /F >Nul
   ) else (
      echo pushCast - Starting Task Scheduler
      schtasks /create /tn pushCast /tr "C:\pyTiVo\pushCast.bat -a -s" /sc hourly /mo %myFreq% > Nul
	)
   goto :eof

::====================================
:setScreen

   MODE CON: COLS=100 LINES=50
   COLOR 1B
   CLS
   goto :eof

::====================================
:Pause
   
   echo pushCast - Pausing...
   echo =====================
   echo.
   set pyTivo=Running
   set TaskScheduler=Running
   set autoPush=Running
   call :pyTivo
   call :TaskScheduler
   call :AutoPush
   echo.
   goto :eof
   
::====================================
:Resume

   echo pushCast - Resuming...
   echo ======================
   echo.
   set pyTivo=Stopped
   set TaskScheduler=Stopped
   set autoPush=Stopped
   call :pyTivo
   call :TaskScheduler
   call :AutoPush
   echo.
   goto :eof

::====================================
