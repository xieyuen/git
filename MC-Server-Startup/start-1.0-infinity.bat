@echo off
title _______ Minecraft Server {����������:_______}
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ��ӭʹ�ô˽ű�! 
echo �˽ű���xieyuen��д
echo �ű��汾: 1.0-infinity
echo �ű�ʹ��ѹ�������Java�ļ���[Minecraft1.12.2�������뻻ΪJava11������], �뽫�������������Ŀ¼
echo �ű�����10,20,30,40,50,60,70,80,90,100������ʱ��ͣ
echo ��Ҫ���µĽű�˽��QQ: 2035381689
echo =========================================
echo             �������ڴ�ռ��: 4GB
echo       ʹ�ô˽ű��ķ������������Զ�����
echo             ��Enter������������
echo =========================================
echo ע: �˰汾Ҫ�رշ�����ֻ�ܹر�cmd����
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
pause
set n=0
title _______ Minecraft Server [��������:%n%��]
echo =========================================
echo               ���������ڿ���
echo           The server is starting!
echo =========================================
".\Java18\bin\java.exe" -jar-Dfile.encoding=GBK -Xmx4G -Xms4G _______.jar nogui
set /a n+=1 
:restart
echo =========================================
echo               ��������������
echo          The server is restarting!
echo =========================================
title _______ Minecraft Server [��������:%n%��]
".\Java18\bin\java.exe" -jar -Dfile.encoding=GBK -Xmx4G -Xms4G _______.jar nogui
set /a n+=1
if %n%==10 goto StopRestart
if %n%==20 goto StopRestart
if %n%==30 goto StopRestart
if %n%==40 goto StopRestart
if %n%==50 goto StopRestart
if %n%==60 goto StopRestart
if %n%==70 goto StopRestart
if %n%==80 goto StopRestart
if %n%==90 goto StopRestart
if %n%==100 goto StopRestart
goto restart
:StopRestart
title �������ѱ��� :(
echo =========================================
echo             �������ѱ���%n%��
echo       ���󱨸��뿴.\logs\latest.log
echo            ��Enter������������
echo =========================================
pause
goto restart