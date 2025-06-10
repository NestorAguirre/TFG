[app]
title = PriceList
package.name = pricelist
package.domain = org.pricelist

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json
include_patterns = modules/**, controllers/**, views/**, assets/**

version = 1.2
orientation = portrait
fullscreen = 1

# Requisitos
requirements = python3,kivy==2.1.0,kivymd==1.1.1,plyer,pdfplumber==0.5.28,pdfminer.six==20201018,charset_normalizer==2.0.12,chardet,pillow,certifi,akivymd,cryptography,android,jnius

# Permisos
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.grant_permissions = True

# Android config
android.minapi = 21
android.api = 33
android.ndk = 25b
android.archs = armeabi-v7a,arm64-v8a
android.allow_backup = True
android.hardwareAccelerated = True
android.meta_data = android.max_aspect=2.1
android.private_storage = True
android.assets = assets/

# Iconos
icon.filename = assets/images/PriceListLogo.png
presplash.filename = assets/images/PriceListLogo.png

# Compat
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0

[buildozer]
log_level = 2
warn_on_root = 1

[python]
include_dirs = ./controllers,./modules,./views