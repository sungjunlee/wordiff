[app]
title = WordDiff
package.name = wordiff
package.domain = com.sungjunlee
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js,ico
# 필요한 패키지 파일들 포함
source.include_patterns = wordiff/**/*
# Android 진입점 파일
source.main = main.py
version = 0.1.1.post1

# Android에서는 기본 webview 사용
requirements = python3,python-docx,colorama,android,plyer

orientation = portrait
fullscreen = 0
android.arch = arm64-v8a

# Android 권한
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Android API 레벨
android.api = 30
android.minapi = 21
android.build_tools = 29.0.3

# 빌드 설정
android.gradle_dependencies = androidx.webkit:webkit:1.4.0
android.add_aars =
android.add_jars =

# 빌드 도구 설정
android.accept_sdk_license = True
android.skip_update = False
# SDK는 buildozer가 자동으로 관리하도록 함

# Android 서명 설정
android.keystore = ~/.android/debug.keystore
android.keyalias = androiddebugkey
android.keystore.passwd = android
android.keyalias.passwd = android

# Python-for-android 설정
p4a.branch = release-2022.12.20
p4a.bootstrap = sdl2

# (str) Presplash of the application
android.presplash_color = #FFFFFF

# Android 인텐트 필터 추가
android.manifest.intent_filters = [{"action": ["android.intent.action.VIEW"], "category": ["android.intent.category.DEFAULT"], "data": [{"mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}]}]

[buildozer]
log_level = 2
warn_on_root = 1
