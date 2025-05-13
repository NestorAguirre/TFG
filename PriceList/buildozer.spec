[app]
title = PriceList
package.name = pricelist
package.domain = org.pricelist

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json,db
include_patterns = modules/**, controllers/**, views/**, assets/**, data/**, data/*.db

version = 1.0
orientation = portrait
fullscreen = 1

# Requisitos
requirements = python3,kivy==2.1.0,kivymd==1.1.1,plyer,pymupdf,chardet,fitz==0.0.1.dev2

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
