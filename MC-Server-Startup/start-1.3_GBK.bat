:: ����
 @echo off
 chcp 936 & :: ���ô���ҳ GBK
 set _restart=0 & :: ������������
 set _error=0 & ::����������ʾ����
 cls

::============================================================================================================================

:Welcome & ::
 title Hello! %username%, ��ӭʹ�ô˽ű�
 echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 echo ��ӭ%username%ʹ�ô˽ű�!
 echo �ű��汾: 1.3snapshot GBK
 echo �˽ű�Ϊ���հ�, ��BUG������ xieyuen163@163.com
 echo ʹ��ʱע��: �뽫�������������Ƹ�ΪStart.jar
 echo --------------------------------------
 echo ������־:
 echo 1.��ӷ�����������ʽѡ��
 echo --------------------------------------
 echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++

::============================================================================================================================

:Choose & ::������ʽѡ��
 set %ERRORLEVEL%=0
 echo ��ѡ�񿪷���ʽ:
 echo   [1]�Զ�����5��
 echo   [2]�Զ�����10��
 echo   [I]�����Զ�����
 echo   [0]ȡ��
 echo ����ѡ��Ĳ˵���:
 choice /C:12I0 /N
 set _erl=%errorlevel%
 goto Check

:Check & :: �����ѡ��ʽ
 if %_erl%==1 set _chk=5 & goto Start
 if %_erl%==2 set _chk=10 & goto Start 
 if %_erl%==3 set _chk=-1 & goto Confirm
 if %_erl%==4 exit /b

:Confirm & :: ȷ��ѡ��[infinity]
 set %ERRORLEVEL%=0
 echo ��ȷ��ѡ������ģʽ��?
 echo ����ģʽֻ���� Ctrl+C �� �رմ���(���Ƽ�)ֹͣ
 echo ����Yȷ��, ����N�ص�ѡ�����
 choice /C:YN /N
 set _erl=%errorlevel%
 if %_erl%==2 goto Choose
 if %_erl%==1 goto Start

::============================================================================================================================

:Start & :: ����
 title ������������ [��������:%_restart%��]
 echo =========================================
 echo               ���������ڿ���
 echo           The server is starting!
 echo =========================================
 java -jar -Dfile.encoding=GBK -Xms1G Start.jar nogui
 set /a _restart+=1
 set /a _error+=1
 if %_chk%==5 goto 5
 if %_chk%==10  goto 10
 if %_chk%==-1  goto Start

:5
 if %_restart%==6 (goto Crash) 
 goto Start
:10
 if %_restart%==11 (goto Crash) 
 goto Start

:Crash & :: ����
 set _restart=0
 title �������ѱ��� :(
 echo =========================================
 echo             �������ѱ���%_error%��
 echo          ���¿����ű�������������
 echo          ��������־�ļ���.\logs\��
 echo        ����������.\crash-report\��
 echo           ��C���رսű�, ��R������
 echo           ��B������ѡ�񿪷�ģʽ
 echo =========================================
 choice /C:CRB /N
 set _erl=%errorlevel%
 if %_erl%==1 exit /b
 if %_erl%==2 goto Check
 if %_erl%==3 goto Choose
