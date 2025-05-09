[app]
title = PriceList
package.name = pricelist
package.domain = org.pricelist
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,txt,json
include_patterns = assets/**, views/**, controllers/**, modules/**, data/**
version = 1.0
requirements = python3,kivy==2.1.0,kivymd,pillow,pyjnius,pdfminer.six
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.minapi = 21
android.api = 33
android.ndk = 25b
android.archs = armeabi-v7a,arm64-v8a
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
android.allow_backup = True
android.hardwareAccelerated = True
android.meta_data = android.max_aspect=2.1

# Si necesitas una base de datos local o archivos temporales, esta línea ayuda
android.private_storage = True

[buildozer]
log_level = 2
warn_on_root = 1

[python]
# Incluir tus carpetas personalizadas
include_dirs = ./controllers,./modules,./views
