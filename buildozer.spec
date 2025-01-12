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
android.api = 33
android.minapi = 21
# android.sdk = 33.0.0
android.ndk = 25b

# Android 서명 설정
android.keystore = ~/.android/debug.keystore
android.keyalias = androiddebugkey
android.keystore.passwd = android
android.keyalias.passwd = android

[buildozer]
log_level = 2
warn_on_root = 1
