@rem ����Ŀ��
@rem 1.���ı���ɫ!
@rem 2.�Ż�EULAЭ��
@rem  2.1.��ȡEULA����
@rem  2.2.�Զ�ͬ��EULA
@rem 3.������������Config�ļ�
::===========================================================================================================================
:: ����
 @echo off
 chcp 936 & :: ���ô���ҳ GBK
 set RAMmax=4096
 set RAMmin=0
 set restart=0 & :: ������������
 set error=0 & :: ����������ʾ����
 set "Java=.\Java18\bin\java.exe" & ::���� Java ·��
 :: �����޸�
 if exist eula.txt (
   set eula=true 
 ) else ( 
   set eula=false 
 )
 cls

::============================================================================================================================

:Welcome & ::��ӭ����
 title Hello! %username%, ��ӭʹ�ô˽ű�
 echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 echo ��ӭ%username%ʹ�ô˽ű�!
 echo �ű��汾: 1.3.6 snapshot GBK
 echo �˽ű�Ϊ���հ�, ��BUG������ xieyuen163@163.com
 echo --------------------------------------
 echo ������־:
 echo 1.��BUG
 echo --------------------------------------
 echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 goto CheckServer

:Settings & :: ���ý���
 echo ��������ǰ����:
 echo   ����:%Server% 
 echo   ����ڴ�ռ��:%RAMmax%MB 
 echo   ��ʼ�ڴ�ռ��:%RAMmin%MB
 echo   Java·��:%Java%
 echo ��ѡ�����:
 echo   [1]����������
 echo   [2]��������������
 echo   [3]��������ڴ�ռ��
 echo   [4]������ʼ�ڴ�ռ��
 echo   [5]����/���ģ��Ͳ��
 echo   [6]����Java·��
 echo   [0]�˳��ű�
 echo ����ѡ��Ĳ˵���:
 choice /C:0123456 /N
 set erl=%errorlevel%
 if %erl%==1 (
    cls
    echo ���Ҫ�뿪����?
    echo ��������᳷�����ѡ��
    echo [y]ȷ������
    echo [n]�װ�
    choice /N
    if %ERRORLEVEL%==1 (
        echo Ү( ?? �� ?? )y
        goto Welcome
    )
    if %errorlevel%==2 (
        echo �װשd(?��?`)o
        echo ����Թر����������
        echo ������㰴Щʲô
        pause >nul
        exit /b
    )
 )
 if %erl%==2 goto Choose
 if %erl%==3 goto setServer
 if %erl%==4 goto setRAMmax
 if %erl%==5 goto setRAMmin
 if %erl%==6 goto Modify_MODs_PLGs
 if %erl%==7 goto Modify_Java
 if %ERRORLEVEL%==0 exit /b

:Modify_Java
 echo ������Java·��:
 set /p "Java="
 ::���Java·��������
 if exist %Java% (
    echo ���óɹ�!
    pause
    cls
    goto Settings
 )
 if exist "%Java%\java.exe" (
    echo ���ƺ��Ǵ���Դ�������ϸ��Ƶ�...?
    echo ��������java.exe�ⶫ��
    echo ��ΰ��㲹�Ϲ�~
    set "Java='%Java%\java.exe'"
    pause
    cls
    goto Settings
 )
 echo ���ϴ�!��û��java.exe��
 echo �Ѿ��л�ΪĬ��java.
 pause
 cls

:setRAMmin
 echo �������������ʼ�ڴ�ռ��(��λ:MB,1GB=1024MB), Ĭ��ֵ:0
 set /p "RAMmin="
 goto Check_RAM

:setRAMmax
 echo ���������������ڴ�ռ��(��λ:MB,1GB=1024MB), Ĭ��ֵ:4096
 set /p "RAMmax="
 goto Check_RAM

:Choose & :: ������ʽѡ��
 set %ERRORLEVEL%=0
 echo ��ѡ�񿪷���ʽ:
 echo   [1]�Զ�����5��
 echo   [2]�Զ�����10��
 echo   [I]�����Զ�����
 echo   [0]��������
 echo ����ѡ��Ĳ˵���:
 choice /C:12I0 /N
 set erl=%errorlevel%
:: �����ѡ��ʽ
 if %erl%==1 set chk_mod=5 & goto Start
 if %erl%==2 set chk_mod=10 & goto Start 
 if %erl%==3 set chk_mod=infinity & goto Confirm
 if %erl%==4 goto Settings

:Confirm & :: ȷ��ѡ��[infinity]
 cls
 set %ERRORLEVEL%=0
 echo ��ȷ��ѡ������ģʽ��?
 echo ����ģʽֻ���� Ctrl+C �� �رմ���(���Ƽ�) ���رշ�����
 echo ����Yȷ��, ����N�ص�ѡ�����
 choice /C:YN /N
 set erl=%errorlevel%
 if %erl%==2 goto Choose
 if %erl%==1 goto Start

:Modify_MODs_PLGs
if %mod%==nul (
  echo �ƺ�...����Minecraftԭ�����!
  echo ԭ����Ĳ��ɼ��ز��/ģ��
  echo �����˻�...
  goto Settings
)
 echo ��ѡ����Ŀ:
 echo   [1]MOD
 echo   [2]PLUGIN
 echo   [3]��������
 echo ����ѡ��Ĳ˵���:
 choice /C:120 /N
 set erl=%errorlevel%
 if %erl%==1 goto Modify_MODs
 if %erl%==2 goto Modify_PLUGINs
 if %erl%==3 goto Settings
 :Modify_MODs
  if not exist ".\mods" (
    echo [ERROR]:û��mods�ļ��� 
    echo �����˻�... 
    goto Settings 
  ) 
  cd ".\mods"
  dir
  goto un_ban
 :Modify_PLUGINs
  if not exist ".\plugins" ( 
    echo [ERROR]:û��plugins�ļ��� 
    echo �����˻�... 
    goto Settings 
  )
  cd ".\plugins"
  dir
 :un_ban
  echo ������ģ��/�������:
  echo С��ʾ:����������ѡ���������Ҽ����μ�����ɸ��ƺ�ճ��
  echo ע��:��Ҫ���ƺ�׺!
  set /p "%mods_plgs%="
  if not exist ".\%mods_plgs%" ( 
    if exist ".\%mods_plgs%.jar" ( 
      set mods_plgs=%mods_plgs%.jar 
    ) else ( 
      if exist ".\%mods_plgs%.ban" ( 
        ren ".\%mods_plgs%.ban" %mods_plgs% 
        echo ģ��/��� %mods_plgs% ������
        cd .. 
        goto Settings
      ) else ( 
        if exist ".\%mods_plgs%.disabled" (
            ren ".\%mods_plgs%.disabled" %mods_plgs%
            echo ģ��/��� %mods_plgs% ������
            cd ..
            goto Settings
        )
        echo [ERROR]:�޷�����Ĵ���[:(] 
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
  if %errorlevel%==1 ( 
    ren ".\%mods_plgs%" %mods_plgs%.ban 
    echo ģ��/��� %mods_plgs% �ѽ��� 
  )
  if %errorlevel%==2 ( 
    if exist ".\%mods_plgs%.ban" (
        ren ".\%mods_plgs%.ban" %mods_plgs% 
    )
    if exist ".\%mods_plgs%.disabled" (
        ren ".\%mods_plgs%.disabled" %mods_plgs% 
    )
    echo ģ��/��� %mods_plgs% ������ 
  )
  cd ..
  goto Settings

::============================================================================================================================

:CheckServer & :: ������
 echo �Զ���������......
 if exist ".\fabric-server-launch.jar" (
    set Check_Server=true
    set "Server=fabric-server-launch.jar"
    echo ��⵽����:fabric-server-launch.jar
    goto Settings
 )
 if exist ".\quilt-server-launch.jar" (
    set Check_Server=true
    set "Server=quilt-server-launch.jar" 
    echo ��⵽����:quilt-server-launch.jar 
    goto Settings
 )
 if exist ".\Server.jar" (
    set Check_Server=true
    set "Server=Server.jar" 
    set "mod=nul"
    echo ��⵽����:Server.jar 
    goto Settings
 )
 if exist ".\minecraft_server.jar" (
    set Check_Server=true
    set "Server=minecraft_server.jar"
    set "mod=nul" 
    echo ��⵽����:minecraft_server.jar 
    goto Settings
 )
 if exist ".\minecraft-server,jar" (
    set Check_Server=true
    set "Server=minecraft-server.jar"
    set "mod=nul"
    echo ��⵽����:minecraft-server.jar
    goto Settings
 )
 echo δ��⵽����������! & goto setServer

:setServer & :: ���ú���(���δ��⵽)
 echo �������������
 set /p "Server="
 if exist ".\%Server%" (
    echo ��⵽����:%Server% 
    goto Settings
 ) 
 if exist ".\%Server%.jar" (
   set Server=%Server%.jar 
   echo ��⵽����:%Server% 
   goto Settings
 )
 if exist ".\%Server%.ban" (
    ren ".\%Server%.ban" %Server% 
    echo ���������� %Server% �����ò�ѡ�� 
    goto Settings
 )
 if exist ".\%Server%.disabled" (
    ren ".\%Server%.disabled" %Server% 
    echo ���������� %Server% �����ò�ѡ�� 
    goto Settings
 )
 if exist ".\%Server%.jar.ban" (
    ren ".\%Server%.jar.ban" %Server%.jar 
    set Server=%Server%.jar 
    echo ���������� %Server% �����ò�ѡ�� 
    goto Settings
 )
 if exist ".\%Server%.jar.disabled" (
    ren ".\%Server%.jar.disabled" %Server%.jar 
    set Server=%Server%.jar 
    echo ���������� %Server% �����ò�ѡ�� 
    goto Settings
 )
 if %Check_Server%==true (
    echo [ERROR]����%Server%������!
    echo ��ѡ�����:
    echo  [1]�Զ����
    echo  [2]�ֶ�����
    choice /C:12 /N
    if %ERRORLEVEL%==2 goto CheckServer
    if %ERRORLEVEL%==1 goto setServer
 )
 echo [ERROR]:����%Server%������!
 if %CheckServer%==true ( goto CheckServer ) else ( set "Server=Start.jar" )
 ::if %Check_Server%==true (
 ::   echo ׼���Զ����...
 ::   goto CheckServer
 ::) 
 set "Server=Start.jar"
 echo ��ѡ��Ĭ�Ϻ���:Start.jar
 goto Settings
 

:Check_RAM
 if /I %RAMmax% GEQ %RAMmin% (
    echo ���óɹ�! 
    goto Settings
 )
 echo [ERROR]:�������ڴ��ʼֵ�������ֵ ( max:%RAMmax% min:%RAMmin% )
 echo ��ѡ�����:
 echo   [1]����ֵ
 echo   [2]�������ֵ
 echo   [3]���ĳ�ʼֵ
 choice /C:123 /N
 if %errorlevel%==1 set RAMmax=4096 & set RAMmin=0 & goto Settings
 if %errorlevel%==2 goto setRAMmax
 if %errorlevel%==3 goto setRAMmin
 if %ERRORLEVEL%==0 goto Settings
::============================================================================================================================

:Start & :: ����
 title ������������ [��������:%error%��] ����رմ���!!!
 echo =========================================
 echo               ���������ڿ���
 echo           The server is starting!
 echo =========================================
 powershell /C %Java% -jar -Dfile.encoding=GBK -Xms%RAMmin%M -Xmx%RAMmax%M %Server% nogui
 if %eula%==false goto First_Start
 set /a restart+=1
 set /a error+=1
 if %chk_mod%==5 goto restart_5
 if %chk_mod%==10 goto restart_10
 if %chk_mod%==infinity goto Start

:restart_5
 if %restart%==6 ( goto Crash ) 
 goto Start
:restart_10
 if %restart%==11 ( goto Crash ) 
 goto Start

:First_Start & :: �����޸�
 echo Minecraft EULA Э��δͬ��!
 echo ��ͬ��Э��, Э���ļ��ڷ�������Ŀ¼�µ�EULA.txt
 echo ͬ��Э�鷽��: ��eula.txt, ���� eula=false Ϊ eula=true ������
 echo ͬ��Э����밴���������...
 pause >nul
 if exist ".\EULA.TXT" set eula=true
 goto Start

:Crash & :: ����
 set restart=0
 title �������ѱ��� :(
 echo =========================================
 echo             �������ѱ���%error%��
 echo          ��������־�ļ���.\logs\��
 echo        ����������.\crash-report\��
 echo =========================================
 echo ��C���رսű�
 echo ��R������������
 echo ��B������ѡ�񿪷�ģʽ
 echo ��P�����������ű�
 choice /C:CRBP /N
 set erl=%errorlevel%
 if %erl%==4 cls & goto Welcome
 if %erl%==3 goto Choose
 if %erl%==2 goto Check
 if %erl%==1 exit /b
