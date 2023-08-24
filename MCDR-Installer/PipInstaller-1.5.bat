@echo off
chcp 936
title Self-service Pypi Installer
set "_pypi=https://pypi.org/simple"
cls

:main
    cls
    echo.
    echo pip����Դ: %_pypi%
    echo.
    echo ��ѡ�����:
    echo   [1]MCDR ѡ��
    echo   [2]ѡ�� pypi����Դ
    echo   [3]��װ Python ��
    echo   [4]���� pip --NEW!
    echo   [0]�˳��˰�װ��
    choice /C:12340 /N
    set _erl=%ERRORLEVEL%
    if %_erl%==1 goto :MCDR
    if %_erl%==2 goto :pypi_download_from
    if %_erl%==3 goto :python_package_install
    if %_erl%==4 goto :pip_upgrade
    if %_erl%==5 exit /b

:MCDR

    echo ��װ MCDR ǰ��Ҫ��װ Python 3.8 ����߰汾!!
    echo ��װ MCDR ǰ��Ҫ��װ Python 3.8 ����߰汾!!
    echo ��װ MCDR ǰ��Ҫ��װ Python 3.8 ����߰汾!!
    echo.
    echo �뽫�ű�������Ҫ��װMCDR���ļ�����
    echo.
    echo ��ѡ�����:
    echo   [1]��װ MCDR
    echo   [2]���� MCDR
    echo   [0]����������
    choice /C:120 /N
    set _erl=%ERRORLEVEL%
    if %_erl%==1 goto :MCDR_install
    if %_erl%==2 goto :MCDR_upgrade
    if %_erl%==3 goto :main


    :MCDR_install

        echo �밴�������װMCDR...
        pause >nul
        pip install mcdreforged -i %_pypi%
        echo ���ڳ�ʼ����...
        py -m mcdreforged init
        echo ��װ���!
        echo ʹ������ py -m mcdreforged ����MCDR (�ǵ��ù���ԱȨ��)
        echo ����������������ű�
        echo ��رմ������˳�...
        pause >nul
        goto :Print_startup_script

    :MCDR_upgrade

        if exist .\mcdreforged.py (
            echo ���Դ������������
            echo �����ֻ��һ����ͨ�� MCDR �û����밴�������������
            echo ������� MCDR �Ŀ����ߣ�����رմ˽ű�������Ϊ MCDR �û������İ�װ�ű�
            echo ����������ɾ�� MCDR �ڴ�Ŀ¼�µ�Դ����
            echo.
            pause
            echo.
            color 04
            echo ���㷴�ڵĻ���
            echo �⽫��ɾ��������ļ�
            echo ȷ����
            echo ���������������ȷ��ɾ����Ŀ¼�� MCDR ��Դ����
            echo ������رմ���
            pause >nul
            color 07

            @echo on 
            :: ɾ���ļ����µ� MCDR Դ����
            del /q .\.github
            del /q .\docs
            del /q .\mcdreforged
            del /q .\tests
            del .\.gitignore
            del .\.readthedocs.yml
            del .\LICENSE
            del /q .\logo_long
            del /q .\MANIFEST.in
            del .\MCDReforged.py
            del .\README.md
            del .\requirements.txt
            del .\setup.py
            @echo off
            
            echo ׼������...

        ) else (
            echo �밴���������MCDR...
            pause >nul
        )
        pip install mcdreforged -U -i %_pypi%
        echo �������!
        echo ʹ������ py -m mcdreforged ����MCDR (�ǵ��ù���ԱȨ��)
        echo �����������������...
        pause >nul
        goto :main

:pypi_download_from

    echo ��ѡ������Դ��(Ĭ��ʹ�ùٷ�Դ)
    echo.
    echo [0] �ٷ� pypi Դ
    echo [1] �廪 pypi ����վ
    echo [2] ������ pypi ����վ
    echo [3] USTC pypi ����վ
    echo [4] BFSU pypi ����վ
    echo [5] ���� pypi ����վ
    echo [6] ���пƼ���ѧ pypi ����վ
    echo [7] �Ϻ���ͨ��ѧ pypi ����վ
    echo [9] ������ pypi Դ URL
    echo.
    choice /N /C:012345679
    set _erl=%ERRORLEVEL%
    if %_erl%==1 set "_pypi=https://pypi.org/simple"
    if %_erl%==2 set "_pypi=https://pypi.tuna.tsinghua.edu.cn/simple"
    if %_erl%==3 set "_pypi=https://mirrors.aliyun.com/pypi/simple/"
    if %_erl%==4 set "_pypi=https://mirrors.ustc.edu.cn/pypi/"
    if %_erl%==5 set "_pypi=https://mirrors.bfsu.edu.cn/pypi/web/simple"
    if %_erl%==6 set "_pypi=http://pypi.douban.com/simple/"
    if %_erl%==7 set "_pypi=http://pypi.hustunique.com/simple/"
    if %_erl%==8 set "_pypi=https://mirror.sjtu.edu.cn/pypi/web/simple/"
    if %_erl%==9 set /p "_pypi=������ pypi Դ�� URL: "
    :: if %_erl%== set "_pypi="

    echo ������ɣ�
    goto :main

:python_package
    :python_package_install

        set /p "_ins=��������Ҫ���صİ�ID��"
        if %_ins% == "mcdreforged" (
            echo ������ת�� MCDR��װ
            goto :MCDR_install
        )
        pip install %_ins% -i %_pypi%
        echo OK!
        pause >nul
        goto :main
    
    :python_package_upgrade

        set /p "_upd = ��������Ҫ���µİ�ID:"
        if %_upd% == "mcdreforged" (
            echo ������ת�� MCDR����
            goto :MCDR_upgrade
        )

:Tools

    :Print_startup_script
    
        echo. >Startup_script.bat
        echo @echo off >>Startup_script.bat
        echo chcp 65001
        echo set _restart=0 >>Startup_script.bat
        echo title MCDReforged�����ű� >Startup_script.bat
        echo echo ������������������... >>Startup_script.bat
        echo pause >nul >>Startup_script.bat
        echo :start >>Startup_script.bat
        echo    title MCDReforged�����ű� [��������:%_restart%] >>Startup_script.bat
        echo    py -X utf8 mcdreforged >>Startup_script.bat
        echo    echo MCDR����5�������... >>Startup_script.bat
        echo    @ping 127.0.0.1 -n 6 >>Startup_script.bat
        echo    set /a _restart=+1 >>Startup_script.bat
        echo    goto :start >>Startup_script.bat
        echo �����ű������ɣ�
        echo ����������˳�...
        pause >nul
        exit /b

:pip_upgrade

    py -m pip install pip -U -i %_pypi%
    echo pip ������ɣ�
    goto :main
