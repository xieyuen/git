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

::============================================================================================================================

::���ղ�����!
::������ܻ���BUG

::������ɫ: ��ʽ: call :dk_color(2) %��ɫ% "�ı�"

:_colorprep

if %_NCS% EQU 1 (
for /F %%a in ('echo prompt $E ^| cmd') do set "esc=%%a"

set     "Red="41;97m""
set    "Gray="100;97m""
set   "Black="30m""
set   "Green="42;97m""
set    "Blue="44;97m""
set  "Yellow="43;97m""
set "Magenta="45;97m""

set    "_Red="40;91m""
set  "_Green="40;92m""
set   "_Blue="40;94m""
set  "_White="40;37m""
set "_Yellow="40;93m""

exit /b
)

for /f %%A in ('"prompt $H&for %%B in (1) do rem"') do set "_BS=%%A %%A"
set "_coltemp=%SystemRoot%\Temp"

set     "Red="CF""
set    "Gray="8F""
set   "Black="00""
set   "Green="2F""
set    "Blue="1F""
set  "Yellow="6F""
set "Magenta="5F""

set    "_Red="0C""
set  "_Green="0A""
set   "_Blue="09""
set  "_White="07""
set "_Yellow="0E""

exit /b

:dk_color

if %_NCS% EQU 1 (
echo %esc%[%~1%~2%esc%[0m
) else (
%psc% write-host -back '%1' -fore '%2' '%3'
)
exit /b

:dk_color2

if %_NCS% EQU 1 (
echo %esc%[%~1%~2%esc%[%~3%~4%esc%[0m
) else (
%psc% write-host -back '%1' -fore '%2' '%3' -NoNewline; write-host -back '%4' -fore '%5' '%6'
)
exit /b

::============================================================================================================================