@echo off
title Minecraft BungeeCord Server {����������:BungeeCord}
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo ��ӭʹ�ô˽ű�! 
echo �˽ű���xieyuen��д
echo �ű��汾: 1.0-bungeecord
echo �˰汾ΪBungeeCord���ư�
echo �ű�ʹ��ѹ�������Java�ļ���[Minecraft1.12.2�����°汾�뻻ΪJava8������], �뽫�������������Ŀ¼
echo ��Ҫ���µĽű�˽��QQ: 2035381689
echo =========================================
echo            �������ڴ�ռ��: 512MB
echo             �������������Զ�����
echo             ��Enter������������
echo =========================================
echo ע: �˰汾Ҫ�رշ�����ֻ�ܹر�cmd����
echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
pause
set n=0
title Minecraft BungeeCord Server [��������:%n%��]
echo =========================================
echo               ���������ڿ���
echo           The server is starting!
echo =========================================
".\Java18\bin\java.exe" -jar-Dfile.encoding=GBK -Xmx512M -Xms512M _______.jar nogui
set /a n+=1 
:restart
echo =========================================
echo               ��������������
echo          The server is restarting!
echo =========================================
title Minecraft BungeeCord Server [��������:%n%��]
".\Java18\bin\java.exe" -jar -Dfile.encoding=GBK -Xmx512M -Xms4G _______.jar nogui
set /a n+=1
goto restart