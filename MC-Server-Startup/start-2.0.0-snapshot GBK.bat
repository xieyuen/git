:: ����
@echo off

:: �ű��༭ע������:
:: ��βע��Ҫ������ '&' ������Ϊע��
:: ��������ģ��ǵ�Ҫ�ո�

set _version=2.0.0 & :: �汾��
chcp 936 & :: ���� GBK ����ҳ
set _restart=0 & :: ������������
set _restart_dp=0 & :: ����������ʾ����
cls
if not exist config.bat (
   echo ��һ��ʹ�ã�
   echo ���������ļ���...
   start "https://github.com/xieyuen/Tool-Gallery/blob/main/MC-Server-Startup/README.MD"
   set _config=false
   goto Save_Config
 ::   set "_ACS=AutoCheckingServer"
 ::   :Initialize
 ::      set _RAMmax=4096
 ::      set _RAMmin=0
 ::      set "_Java=.\Java18\bin\java.exe" & :: ���� Java ·��
 ::      set "_Frpc=DISABLED"
 ::      set "_Frpc_Config=DISABLED"
 ::      set _config=false
 ::      :: �����޸�
 ::      if exist eula.txt (
 ::         set _eula=true 
 ::      ) else ( 
 ::         set _eula=false 
 ::      )
) else (
   call config.bat
   set _config=true
)
cls

::============================================================================================================================

:Welcome & ::��ӭ����

   title Hello! %USERNAME%, ��ӭʹ�ô˽ű�
   echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
   echo ��ӭ%USERNAME%ʹ�ô˽ű�!
   echo �ű��汾: %_version% snapshot GBK
   echo �˽ű�Ϊ���հ�, ��BUG������ xieyuen163@163.com
   echo.
   echo ��汾�������ʲôBUG�Ǿ���������ʽ���
   echo.
   echo --------------------------------------
   echo ������־:
   echo   ȥREADME.MD��(
   echo       README.MD: 
   echo   https://github.com/xieyuen/xieyuen/blob/main/�����ű�/README.MD
   echo --------------------------------------
   echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++

:Main_Action_Center & :: �������Ľ���

   echo.
   echo ��ѡ����Ŀ:
   echo   [1]��������������
   echo   [2]Frp��������[Under Development]
   echo   [9]�����ļ����[Under Development]
   echo   [0]�˳�
   echo.
   choice /C:0129C /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 exit /b
   if %_erl%==2 (
      cls
      goto Server_Action_Center
   )
   if %_erl%==3 (
      cls 
      echo.
      echo This feature is under development!
      echo This feature is under development! 
      echo This feature is under development! 
      echo.
      echo We didn't enable it
      echo.
      goto Main_Action_Center
   )
   if %_erl%==4 (
      cls
      goto Config
   )
   if %_erl%==5 (
      cls
      goto Welcome
   )  

:Frp_Action_Center

   cls

   echo  Frp��ǰ����:
   echo     frp·��:%_Frpc%
   echo     frp����·��:%_Frpc_Config%
   echo. 
   echo  ��ѡ�����:
   echo     [1]����frp
   echo     [2]����frp�����ű�
   echo     [0]��������������
   choice /C:012 /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 goto Main_Action_Center
   if %_erl%==2 goto Start_Frp
   if %_erl%==3 goto Save_Frp

:Server_Action_Center

   if %_config%==false (
      if %_ACS%==AutoCheckingServer (
         set "%_ACS%=unAutoCheckingServer"
         goto AutoCheckingServer
      )
   )

   echo ��������ǰ����:
   echo   ����:%_Server% 
   echo   ����ڴ�ռ��:%_RAMmax%MB 
   echo   ��С�ڴ�ռ��:%_RAMmin%MB
   echo   Java·��:%_Java%
   echo ��ѡ�����:
   echo   [1]����������
   echo   [2]��������������
   echo   [3]��������ڴ�ռ��
   echo   [4]������С�ڴ�ռ��
   echo   [5]����/���ģ��Ͳ��
   echo   [6]����Java·��
   echo   [C]����
   echo   [0]��������������
   echo ����ѡ��Ĳ˵���:
   choice /C:0123456C /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 goto Main_Action_Center
   if %_erl%==2 goto Choose
   if %_erl%==3 goto setServer
   if %_erl%==4 goto set_RAMmax
   if %_erl%==5 goto set_RAMmin
   if %_erl%==6 goto Modify_MODs_PLGs
   if %_erl%==7 goto Modify_Java
   if %_erl%==8 (
      cls
      set "_ACS=unAutoCheckingServer"
      goto Server_Action_Center
   )

::============================================================================================================================

:Modify_Java

   echo ������Java·��:
   set /p "_Java="
   ::���Java·��������
   if exist %_Java% (
      echo ���óɹ�!
      goto Server_Action_Center
   )
   if exist "%_Java%\java.exe" (
      echo ���ƺ��Ǵ���Դ�������ϸ��Ƶ�...?
      echo ��������java.exe�ⶫ��
      echo ��ΰ��㲹�Ϲ�~
      set "_Java='%_Java%\java.exe'"
      goto Server_Action_Center
   )
   set "_Java=java"
   echo ���ϴ�!��û��java.exe��
   echo �Ѿ��л�ΪĬ��java.
   goto Server_Action_Center

:RAM

   :set_RAMmin

      echo �������������С�ڴ�ռ��(��λ:MB,1GB=1024MB), Ĭ��ֵ:0
      set /p "_RAMmin="
      goto Check_RAM

   :set_RAMmax

      echo ���������������ڴ�ռ��(��λ:MB,1GB=1024MB), Ĭ��ֵ:4096
      set /p "_RAMmax="
      goto Check_RAM
   
   :Check_RAM

      if %_RAMmax%==0 (
         echo emmm...���Ϊ0M...
         echo ��������ô��?
         echo Ӧ������СΪ0M��...
         if %_RAMmin%==0 (
            echo ��СҲ��0M?
            echo �ȸ�����������
            if %_Server%==Bungeecord.jar (
               set _RAMmax=512
            ) else (
               set _RAMmax=4096
            )
            goto Server_Action_Center
         )
         echo �Ҹ��㻻�˹�
         set "_RAMmax=%_RAMmin%"
         set _RAMmin=0
         goto Server_Action_Center
      )
      set /a "_temp=%_RAMmax%-%_RAMmin%"
      if %_temp% GEQ 0 (
         echo ���óɹ�! 
         goto Server_Action_Center
      )
      echo [ERROR]:�������ڴ���Сֵ�������ֵ ( max:%_RAMmax% min:%_RAMmin% )
      echo ��ѡ�����:
      echo   [1]����ֵ
      echo   [2]�������ֵ
      echo   [3]������Сֵ
      choice /C:123 /N
      if %ERRORLEVEL%==1 (
         set _RAMmax=4096
         set _RAMmin=0
         goto Server_Action_Center
      )
      if %ERRORLEVEL%==2 goto set_RAMmax
      if %ERRORLEVEL%==3 goto set_RAMmin
      if %ERRORLEVEL%==0 goto Server_Action_Center

:Choose & :: ������ʽѡ��

   cls
   echo.
   echo ��ѡ�񿪷���ʽ:
   echo   [1]�Զ�����5��
   echo   [2]�Զ�����10��
   echo   [I]�����Զ�����
   echo   [3]���Է�����(����1��)
   echo   [4]���Է�����(������)
   echo   [5]�Զ������
   echo   [0]���ط�������������
   echo ����ѡ��Ĳ˵���:
   choice /C:12I0345 /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 (
      set _chk_mod=5
      goto Start_Server
   )
   if %_erl%==2 (
      set _chk_mod=10 
      goto Start_Server
   ) 
   if %_erl%==3 (
      set _chk_mod=infinity 
      goto Confirm
   )
   if %_erl%==4 goto Server_Action_Center
   if %_erl%==5 (
      set _chk_mod=1
      goto Start_Server
   )
   if %_erl%==6 (
     set _chk_mod=0
     goto Start_Server
   )
   if %_erl%==7 (
      set _chk_mod=Custom
   )

:Confirm & :: ȷ��ѡ��[infinity]

   cls
   set %ERRORLEVEL%=0
   echo ��ȷ��ѡ������ģʽ��?
   echo ����ģʽֻ���� Ctrl+C �� �رմ���(���Ƽ�) ���رշ�����
   echo ����Yȷ��, ����N�ص�ѡ�����
   choice /C:YN /N
   set _erl=%ERRORLEVEL%
   if %_erl%==2 goto Choose
   if %_erl%==1 goto Start_Server

:Modify_MODs_PLGs

 :: ����д��ϡ��...
 :: ���� DISABLED ��

   cls
   if %_mod%==false (
      echo �ƺ�...����Minecraftԭ�����!
      echo ԭ����Ĳ��ɼ��ز��/ģ��
      echo �����˻�...
      goto Server_Action_Center
   )
   echo ��ѡ����Ŀ:
   echo   [1]MOD
   echo   [2]PLUGIN
   echo   [3]���ط�������������
   echo ����ѡ��Ĳ˵���:
   choice /C:120 /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 goto Modify_MODs
   if %_erl%==2 goto Modify_PLUGINs
   if %_erl%==3 goto Server_Action_Center

   :Modify_MODs

      if not exist ".\mods" (
        echo [ERROR]:û��mods�ļ��� 
        echo [INFO]:������...
        md .\mods
        echo [INFO]:�������!
      ) 
      cd ".\mods"
      dir
      goto un_ban

   :Modify_PLUGINs

      if not exist ".\plugins" ( 
         echo [ERROR]:û��plugins�ļ��� 
         echo [INFO]:������:
         md .\plugins
         echo [INfO]:�������!
      )
      cd ".\plugins"
      dir

   :un_ban

      echo ������ģ��/�������:
      echo С��ʾ: ����������ѡ���������Ҽ����μ�����ɸ��ƺ�ճ��
      echo ע��: ��Ҫ���ƺ�׺!
      set /p "_mods_plgs="
      if not exist ".\%_mods_plgs%" ( 
         if exist ".\%_mods_plgs%.jar" ( 
            set mods_plgs=%_mods_plgs%.jar 
         ) else ( 
            if exist ".\%_mods_plgs%.ban" ( 
               ren ".\%_mods_plgs%.ban" %_mods_plgs% 
               echo ģ��/��� %_mods_plgs% ������
               cd .. 
               goto Server_Action_Center
            ) else ( 
               if exist ".\%_mods_plgs%.disabled" (
                  ren ".\%_mods_plgs%.disabled" %_mods_plgs%
                  echo ģ��/��� %_mods_plgs% ������
                  cd ..
                  goto Server_Action_Center
               )
               echo [ERROR]:������һ����������
               echo [ERROR]:�ڽ����ı�%_mods_plgs%����! 
               pause >nul 
               exit /b 
            ) 
         ) 
      )
   echo ��ѡ�����:
   echo [1]����ģ��
   echo [2]����ģ��
   echo ֱ���������
   choice /C:12 /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 ( 
     ren ".\%_mods_plgs%" %_mods_plgs%.ban 
     echo ģ��/��� %_mods_plgs% �ѽ��� 
   )
   if %_erl%==2 ( 
     if exist ".\%_mods_plgs%.ban" (
         ren ".\%_mods_plgs%.ban" %_mods_plgs% 
     )
     if exist ".\%_mods_plgs%.disabled" (
         ren ".\%_mods_plgs%.disabled" %_mods_plgs% 
     )
     echo ģ��/��� %_mods_plgs% ������ 
   )
   cd ..
   goto Server_Action_Center

:setServer & :: ���ú���(���δ��⵽)

   echo �������������:
   set /p "_Server="
   if not exist ".\*.jar" (
      echo û�к��ģ�
      echo �Ͻ�ȥ����һ��
      echo ��Ҫ��ʲô��������
      echo     [1] vanilla ԭ�������
      echo     [2] Fabric �Ƽ��߰汾
      echo     [3] Forge �Ƽ��Ͱ汾
      echo     [4] Carpet ���밲װFabric
      echo     [5] MCDR qb������(���� MCDR ֻ�Ƿ������Ŀ��ӣ����滹Ҫװ������...)
      echo     [6] Bukkit
      echo     [7] Paper
      echo     [8] Purpur
      echo     [9] Arclight
      echo     [0] �������
      choice /C:1234567890 /N
      pause >nul
      set _erl=%ERRORLEVEL%
      if %_erl%==1 (
         start https://www.fastmirror.net/#/download/Vanilla?coreVersion=release
      )
      if %_erl%==2 (
         start https://fabricmc.net
      )
      if %_erl%==3(
         start https://www.fastmirror.net/#/download/Forge?coreVersion=1.19.3
      )
      if %_erl%==4 (
         echo ��װ Fabric ��˵
         echo Fabric �� Fabric Api �� Carpet ��ǰ��Ҫ��
         echo ������ cmcl ��ģ������������
         echo ��װ���cmcl mod --install --source=cf --id=349239
      )
      if %_erl%==5 (
         start https://github.com/xieyuen/Tool-Gallery/blob/main/MCDR-Installer/README.md
      )
      if %_erl%==8 (
         start https://www.fastmirror.net/#/download/Purpur?coreVersion=1.19.3
      )
      if %_erl%==9 (
         start https://www.fastmirror.net/#/download/Arclight?coreVersion=GreatHorn
      )
      if %_erl%==10 (
         start https://www.fastmirror.net
      )
      echo ȥ���ذɣ�
      echo ����֮���ٿ��ű�
      pause >nul
      exit /b
   )
   if exist ".\%_Server%" (
      echo ��⵽����:%_Server% 
      set "_ACS=unAutoCheckingServer"
      goto Server_Action_Center
   ) 
   if exist ".\%_Server%.jar" (
      set _Server=%_Server%.jar 
      set "_ACS=unAutoCheckingServer"
      echo ��⵽����:%_Server% 
      goto Server_Action_Center
   )
   if exist ".\%_Server%.ban" (
      ren ".\%_Server%.ban" %_Server% 
      echo ���������� %_Server% �����ò�ѡ�� 
      set "_ACS=unAutoCheckingServer"
      goto Server_Action_Center
   )
   if exist ".\%_Server%.disabled" (
      ren ".\%_Server%.disabled" %_Server% 
      set "_ACS=unAutoCheckingServer"
      echo ���������� %_Server% �����ò�ѡ�� 
      goto Server_Action_Center
   )
   if exist ".\%_Server%.jar.ban" (
      ren ".\%_Server%.jar.ban" %_Server%.jar 
      set _Server=%_Server%.jar 
      set "_ACS=unAutoCheckingServer"
      echo ���������� %_Server% �����ò�ѡ�� 
      goto Server_Action_Center
   )
   if exist ".\%_Server%.jar.disabled" (
      ren ".\%_Server%.jar.disabled" %_Server%.jar 
      set "_ACS=unAutoCheckingServer"
      set _Server=%_Server%.jar 
      echo ���������� %_Server% �����ò�ѡ�� 
      goto Server_Action_Center
   )
   echo [ERROR]:����%_Server%������!
   if %_Chk_Server%==true (
      echo ��ѡ�����:
      echo  [1]�Զ����
      echo  [2]�ֶ�����
      echo  [3]����, ѡ��Ĭ�� Start.jar ����
      choice /C:123 /N
      set _erl=%ERRORLEVEL%
      if %_erl%==3 (
         echo ����ִ�в���...
         set "Server=Start.jar"
         goto Server_Action_Center
      )
      if %_erl%==2 goto AutoCheckingServer
      if %_erl%==1 goto setServer
   )
   set "_Server=Start.jar"
   echo ��ѡ��Ĭ�Ϻ���:Start.jar
   set "_ACS=unAutoCheckingServer"
   goto Server_Action_Center

:AutoCheckingServer & :: ������

   echo �Զ���������......
   :: Fabric ����
   if exist ".\fabric-server-launch.jar" (
      set _Chk_Server=true
      set "_Server=fabric-server-launch.jar"
      set "_mod=true"
      echo ��⵽����:fabric-server-launch.jar
      goto Server_Action_Center
   )
   :: Quilt ����
   if exist ".\quilt-server-launch.jar" (
      set _Chk_Server=true
      set "_Server=quilt-server-launch.jar" 
      set "_mod=true"
      echo ��⵽����:quilt-server-launch.jar 
      goto Server_Action_Center
   )
   :: Bungeecord ����
   if exist ".\BungeeCord.jar" (
      set _Chk_Server=true
     set "_Server=BungeeCord.jar"
     set _mod=true
     set _RAMmax=512
     echo ��,��Ȼ����������ű���BungeeCord
     echo �ȿ��ڴ�ռ�ã�
     goto Server_Action_Center
   )
   :: Vanilla ����
   if exist ".\Server.jar" (
      set _Chk_Server=true
      set "_Server=Server.jar" 
      set "_mod=false"
      echo ��⵽����:Server.jar 
      goto Server_Action_Center
   )
   if exist ".\minecraft_server.jar" (
      set _Chk_Server=true
      set "_Server=minecraft_server.jar"
      set "_mod=false" 
      echo ��⵽����:minecraft_server.jar 
      goto Server_Action_Center
   )
   if exist ".\minecraft-server.jar" (
      set _Chk_Server=true
      set "_Server=minecraft-server.jar"
      set "_mod=false"
      echo ��⵽����:minecraft-server.jar
      goto Server_Action_Center
   )
   echo δ��⵽����������! 
   goto setServer

::============================================================================================================================

:Config

   if %_config%==false (
      if not exist config.bat (
         echo û�������ļ�����������...
         goto Save_Config
      )
      echo �¸�������ļ�?
      echo ��˶� Github �ϵ������ļ�д��
      echo ���ȳ���������ң�
      echo ����...������һ��?
      echo ԭ�����ļ����ᱻ���Ϊ config-backup.txt
      echo.
      echo ������������������ļ�...
      echo.
      pause >nul
      rename config.bat config-backup.txt
      goto Save_Config
   )
   echo ��ѡ�����:
   echo [1]��������
   echo [2]��ȡ����
   echo [0]��������������
   choice /C:120 /N
   set _erl=%ERRORLEVEL%
   if %_erl%==1 goto Save_Config
   if %_erl%==2 goto Load_Config
   if %_erl%==3 cls & goto Main_Action_Center

   :Save_Config

      echo.
      echo ������...

      :: ��һ�δ����Ǳ��������ļ��Ĵ���
      :: >>config.bat �� >config.bat ����д�������ļ���
      :: ^^^^^^^^^^^^    ^^^^^^^^^^^
      ::   �����           �����
      ::  ���������        ����д��
      ::
      :: 'echo.' ��Ϊ����
      :: ����Ч���� README ��ʾ
      :: README����: https://github.com/xieyuen/Tool-Gallery/blob/main/%E5%BC%80%E6%9C%8D%E8%84%9A%E6%9C%AC/README.MD#%E9%BB%98%E8%AE%A4%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6
      echo @rem ���ǿ����ű��������ļ�>config.bat
      echo @rem ÿ�α��涼�Ḳ�ǵ��������ַ�>>config.bat
      echo @rem ��Ҫ�Ҹ�Ŷ���ر��� �� = �� ǰ��ģ�>>config.bat
      echo @rem Ҫ��Ҳֻ�ܸ�ÿ�� ��=�� �����>>config.bat
      echo. >>config.bat
      echo @rem ������������>>config.bat
      echo set _Server=%_Server%>>config.bat
      echo. >>config.bat
      echo @rem ����ڴ�ռ�ã���λMB>>config.bat
      echo set _RAMmax=%_RAMmax%>>config.bat
      echo. >>config.bat
      echo @rem ��С�ڴ�ռ�ã���λMB>>config.bat
      echo set _RAMmin=%_RAMmin%>>config.bat
      echo. >>config.bat
      echo @rem Java·��>>config.bat
      echo set "_Java=%_Java%">>config.bat
      echo. >>config.bat
      echo @rem EULA�Ƿ�ͬ��>>config.bat
      echo @rem ͬ�� true>>config.bat
      echo @rem ��ͬ�� false>>config.bat
      echo set "_eula=%_eula%">>config.bat

      if "%_temp%"="eula-false" (
         goto Start_Server
      )
      echo ����ɹ�
      if "%_config%==false" (
         echo �����ļ����������
         echo �밴�� README �е������ļ������д�����ļ���
         pause >nul
         exit /b
      )
      echo ���������������������...
      pause >nul
      goto Main_Action_Center

   :Load_Config

      if not exist config.bat (
         echo δʶ�������ļ���
         echo �밴���������...
         pause >nul
         goto Config
      )
      echo ���ڶ�ȡ...
      call config.bat
      echo ��ȡ���!
   
   goto Config

::============================================================================================================================

:Start_Server

   title ������������ [��������:%_restart_dp%��] ����رմ���!!!
   echo =========================================
   echo               ���������ڿ���
   echo           The server is starting!
   echo =========================================
   powershell /C %_Java% -jar -Dfile.encoding=GBK -Xms%_RAMmin%M -Xmx%_RAMmax%M %_Server% nogui
   if "%_eula%==false" goto First_Start
   set /a _restart+=1
   set /a _restart_dp+=1
   if %_chk_mod%==infinity goto Start_Server
   if %_chk_mod%==1 goto restart_1
   if %_chk_mod%==5 goto restart_5
   if %_chk_mod%==10 goto restart_10
   if %_chk_mod%==0 goto Server_Crash
   if "%_chk_mod%==Custom" goto restart_Custom

   :restart_1

      if %_restart%==1 goto Server_Crash
      goto Start_Server

   :restart_5

      if %_restart%==6 goto Server_Crash 
      goto Start_Server

   :restart_10

      if %_restart%==11 goto Server_Crash
      goto Start_Server

   :restart_Custom

      if %_restart%==%_restart_custom% goto Server_Crash
      goto Start_Server

   :First_Start & :: �����޸�

      echo Minecraft EULA Э��δͬ��!
      echo ��ͬ��Э��, Э���ļ��ڷ�������Ŀ¼�µ�EULA.txt
      echo ͬ��Э�鷽��: ��eula.txt, ���� eula=false Ϊ eula=true ������
      echo ͬ��Э����밴���������...
      pause >nul
      if exist ".\EULA.TXT" (
         set _eula=true
         set "_temp=eula-false"
         goto Save_Config
      )
      goto Start_Server

:Server_Crash & :: ����

   set _restart=0
   title ��������ֹͣ :(
   echo =========================================
   echo             �������ܼƱ���%_restart_dp%��
   echo          ��������־�ļ���.\logs\��
   echo        ����������.\crash-report\��
   echo =========================================
   echo ��C���رսű�
   echo ��R������������
   echo ��B������ѡ�񿪷�ģʽ
   echo ��P�����������ű�
   choice /C:CRBP /N
   set _erl=%ERRORLEVEL%
   if %_erl%==4 (
     cls 
     set "_ACS=unAutoCheckingServer" 
     goto Welcome
   )
   if %_erl%==3 goto Choose
   if %_erl%==2 goto Initialize
   if %_erl%==1 exit /b
