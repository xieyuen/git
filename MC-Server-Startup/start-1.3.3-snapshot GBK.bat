:: ����
 @echo off
 chcp 936 & :: ���ô���ҳ GBK
 set RAMmax=4096
 set RAMmin=0
 set restart=0 & :: ������������
 set error=0 & :: ����������ʾ����
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
 echo �ű��汾: 1.3.2 snapshot GBK
 echo �˽ű�Ϊ���հ�, ��BUG������ xieyuen163@163.com
 echo --------------------------------------
 echo ������־:
 echo 1.��ӷ�����������ʽѡ��
 echo --------------------------------------
 echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 goto CheckServer

:Settings & :: ���ý���
 echo ��������ǰ����:
 echo   ����:%Server% ����ڴ�ռ��:%RAMmax%MB ��С�ڴ�ռ��:%RAMmin%MB
 echo ��ѡ�����:
 echo   [1]����������
 echo   [2]��������������
 echo   [3]��������ڴ�ռ��
 echo   [4]������С�ڴ�ռ��
 echo   [5]����/���ģ��Ͳ��
 echo ����ѡ��Ĳ˵���:
 choice /C:12345 /N
 set _erl=%errorlevel%
 if %_erl%==1 goto Choose
 if %_erl%==2 goto setServer
 if %_erl%==3 goto setRAMmax
 if %_erl%==4 goto setRAMmin
 if %_erl%==5 goto Modify_MODs_PLUGINs

:setRAMmin
 echo �������������С�ڴ�ռ��(��λ:MB,1GB=1024MB), Ĭ��ֵ:0
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
 set _erl=%errorlevel%
:: �����ѡ��ʽ
 if %_erl%==1 set chk_mod=5 & goto Start
 if %_erl%==2 set chk_mod=10 & goto Start 
 if %_erl%==3 set chk_mod=infinity & goto Confirm
 if %_erl%==4 goto Settings

:Confirm & :: ȷ��ѡ��[infinity]
 set %ERRORLEVEL%=0
 echo ��ȷ��ѡ������ģʽ��?
 echo ����ģʽֻ���� Ctrl+C �� �رմ���(���Ƽ�) ���رշ�����
 echo ����Yȷ��, ����N�ص�ѡ�����
 choice /C:YN /N
 set _erl=%errorlevel%
 if %_erl%==2 goto Choose
 if %_erl%==1 goto Start

:Modify_MODs_PLUGINs
if %Server%=minecraft_server (
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
 set _erl=%errorlevel%
 if %_erl%==1 goto Modify_MODs
 if %_erl%==2 goto Modify_PLUGINs
 if %_erl%==3 goto Settings
 :Modify_MODs
  if not exist ".\mods" (
    echo [ERROR]:û��mods�ļ��� & echo �����˻�... & goto Settings 
  ) 
  cd ".\mods"
  dir
  goto un_ban
 :Modify_PLUGINs
  if not exist ".\plugins" ( 
    echo [ERROR]:û��plugins�ļ��� & echo �����˻�... & goto Settings 
  )
  cd ".\plugins"
  dir
 :un_ban
  echo ������ģ��/�������:
  set /p "%mods_plugins%="
  if not exist ".\%mods_plugins%" ( 
    if exist ".\%mods_plugins%.jar" ( 
      set mods_plugins=%mods_plugins%.jar 
    ) else ( 
      if exist ".\%mods_plugins%.ban" ( 
        ren ".\%mods_plugins%.ban" %mods_plugins% & echo ģ��/��� %mods_plugins% ������ & cd .. & goto Settings
      ) else ( 
        echo [ERROR]:�޷�����Ĵ���[:(] & pause >nul & exit /b 
      ) 
    ) 
  )
  echo ��ѡ�����:{[1]����ģ��[2]����ģ��}(ֱ���������)
  choice /C:12 /N
  if %errorlevel%==1 ( 
    ren ".\%mods_plugins%" %mods_plugins%.ban & echo ģ��/��� %mods_plugins% �ѽ��� 
  )
  if %errorlevel%==2 ( 
    ren ".\%mods_plugins%.ban" %mods_plugins% & echo ģ��/��� %mods_plugins% ������ 
  )
  cd ..
  goto Settings

::============================================================================================================================

:CheckServer & :: ������
 echo �Զ���������......
 if exist ".\fabric-server-launch.jar" set "Server=fabric-server-launch.jar" & echo ��⵽����:fabric-server-launch.jar & goto Settings
 if exist ".\quilt-server-launch.jar" set "Server=quilt-server-launch.jar" & echo ��⵽����:quilt-server-launch.jar & goto Settings
 if exist ".\Server.jar" set "Server=Server.jar" & echo ��⵽����:Server.jar & goto Settings
 if exist ".\minecraft_server.jar" set "Server=minecraft_server.jar" & echo ��⵽����:minecraft_server.jar & goto Settings
 echo δ��⵽����������! & goto setServer

:setServer & :: ���ú���(���δ��⵽)
 echo �������������(��Ҫ����.jar��׺)
 set /p "Server="
 
 ::if exist ".\%Server%" ( echo ��⵽����:%Server% & goto Settings) else ( if exist ".\%Server%.jar" ( set Server=%Server%.jar & echo ��⵽����:%Server% & goto Settings ) else ( if exist ".\%Server%.ban" ( ren ".\%Server%.ban" %Server% & echo ���������� %Server% �����ò�ѡ�� ) else ( echo [ERROR]:�޷�����Ĵ���[:(] & pause >nul & exit /b ) ) )
 if exist ".\%Server%" (
  echo ��⵽����:%Server% & goto Settings
 ) else (
  if exist ".\%Server%.jar" (
    set Server=%Server%.jar & echo ��⵽����:%Server% & goto Settings
  ) else (
    if exist ".\%Server%.ban" (
      ren ".\%Server%.ban" %Server% & echo ���������� %Server% �����ò�ѡ�� & goto Settings
    ) else (
      if exist ".\%Server%.jar.ban" (
        ren ".\%Server%.jar.ban" %Server%.jar & set Server=%Server%.jar & echo ���������� %Server% �����ò�ѡ�� & goto Settings
      ) else (
        echo [ERROR]:���Ĳ�����!  & goto CheckServer
      )
    ) 
  )
 )
 ::echo [ERROR]:���������Ĳ�����!
 ::echo ����ƴд��ȷ�Ͻű��Ƿ��ڷ���������Ŀ¼��(�����, �밴Ctrl+C�رսű�)
 ::goto setServer

:Check_RAM
 if /I %RAMmax% GEQ %RAMmin% echo ���óɹ�! & goto Settings
 echo [ERROR]:�������ڴ���Сֵ�������ֵ (min:%RAMmin% max:%RAMmax%)
 echo ��ѡ�����:
 echo   [1]����ֵ
 echo   [2]�������ֵ
 echo   [3]������Сֵ
 choice /C:123 /N
 if %errorlevel%==1 set RAMmax=4096 & set RAMmin=0 & goto Settings
 if %errorlevel%==2 goto setRAMmax
 if %errorlevel%==3 goto setRAMmin

::============================================================================================================================

:Start & :: ����
 title ������������ [��������:%error%��] ����رմ���!!!
 echo =========================================
 echo               ���������ڿ���
 echo           The server is starting!
 echo =========================================
 ".\java18\bin\java.exe" -jar -Dfile.encoding=GBK -Xms%RAMmin%M -Xmx%RAMmax%M %Server% nogui
 if %eula%==false goto First_Start
 set /a restart+=1
 set /a error+=1
 if %chk_mod%==5 goto restart_5
 if %chk_mod%==10 goto restart_10
 if %chk_mod%==infinity goto Start

:restart_5
 if %restart%==6 (goto Crash) 
 goto Start
:restart_10
 if %restart%==11 (goto Crash) 
 goto Start

:First_Start
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
 echo        ��C���رսű�, ��R������������
 echo           ��B������ѡ�񿪷�ģʽ
 echo             ��P�����������ű�
 echo =========================================
 choice /C:CRBP /N
 set _erl=%errorlevel%
 if %_erl%==1 exit /b
 if %_erl%==2 goto Check
 if %_erl%==3 goto Choose
 if %_erl%==4 cls & goto Welcome
