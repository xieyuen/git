@rem ǰ��
 @rem �˽ű��ɸ��ĵ����ݻ���"______"���(6��_)
 @rem ��ʹ��GB2312����༭�ű�[�Ƽ�ʹ��רҵ�༭���༭,����VSCode, Notepad++��]
 @rem Please edit the script using GB2312 encoding
 @rem ����Ϊ�ű�����

@echo off
 @rem ���ô���ҳ GB2312
  chcp 936
 cls

:Welcome
 @rem ���ñ���
  title ______
 @rem ���
  echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
  echo ��ӭ%username%ʹ�ô˽ű�!
  echo �ű��汾: 1.2snapshot GB2312
  echo �˽ű�Ϊ���հ�, ��BUG������ xieyuen163@163.com
  echo ---------------------------
  echo ���¼ƻ�:
  echo    �������:
  echo    �����ء���̨�����ĳ�������
  echo ---------------------------
  echo           �����������������
  echo ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 pause

@rem Ԥ����
:pretreatment
 @rem ����ĸ���
  @rem ����������ж������, ���ò�ͬ��API, �������������/����ģ��
   @rem ���� ren .\mods\______.jar ______.jar.ban
   @rem ��� ren .\mods\______.jar.ban ______.jar
  @rem ������������
   @rem ���� ren .\______.jar ______.jar.ban
   @rem ��� ren .\______.jar.ban ______.jar
 @rem ��������ڱ���ע������

@rem ������������
:Start 
 @rem ���ñ���n=0
 set n=0
 @rem ���ñ���
  title ______ [��������:%n%��]
 echo =========================================
 echo               ���������ڿ���
 echo           The server is starting!
 echo =========================================
 @rem ����[GB2312����]
 @rem "______.jar"�������������, "-Xmx______"�ڴ�ռ�����ֵ, "-Xms______"�ڴ�ռ����Сֵ, ��λM��G(1024M=1G)
  ".\Java18\bin\java.exe" -jar -Dfile.encoding=GB2312 -Xmx______ -Xms______ ______.jar nogui
 set /a n+=1
 @rem ��n=______[����n-1��]ʱת���������
  if %n%==______ goto Crash
  goto Start

@rem �������
:Crash
 title �������ѱ��� :(
 echo =========================================
 echo             �������ѱ���%n%��
 echo          ���¿����ű�������������
 echo            ��־�ļ���.\logs\��
 echo        ����������.\crash-report\��
 echo              ��������رսű�
 echo =========================================
 pause
 exit
