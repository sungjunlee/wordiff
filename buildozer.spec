[app]
title = WordDiff
package.name = wordiff
package.domain = com.sungjunlee
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,css,js
version = 0.1.1.post1

requirements = python3,kivy,pywebview,python-docx,colorama
p4a.branch = master
p4a.hook = enable_hooks

orientation = portrait
fullscreen = 0
android.arch = arm64-v8a

# Android 권한
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Android API 레벨
android.api = 29
android.minapi = 21
android.build_tools = 29.0.0
android.ndk = 25b

# Java 설정
android.skip_update = True  # SDK 업데이트 건너뛰기
android.accept_sdk_license = True  # SDK 라이선스 자동 수락

# Android 서명 설정
android.keystore = ~/.android/debug.keystore
android.keyalias = androiddebugkey
android.keystore.passwd = android
android.keyalias.passwd = android

[buildozer]
log_level = 2
warn_on_root = 1
