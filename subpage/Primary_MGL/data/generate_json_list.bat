@echo off
setlocal enabledelayedexpansion

:: ����Ŀ���ļ���
set "targetFile=file_list.txt"

:: ʹ�� dir �����г����� .json �ļ����ļ�����������·����
dir /b "*.json" > "%targetFile%"

:: ����ļ��Ƿ����ɳɹ�
if exist "%targetFile%" (
    echo �ļ������ɣ� %targetFile%
    type "%targetFile%"  :: ��ӡ�ļ����ݵ�����̨
) else (
    echo �ļ�����ʧ�ܣ�
)


pause