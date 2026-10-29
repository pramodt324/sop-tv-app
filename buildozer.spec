[app]
title = SOP Offline Player
package.name = sopofflineapp
package.domain = org.factory
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = landscape
osx.kivy_version = 2.1.0
fullscreen = 1
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, RECEIVE_BOOT_COMPLETED
android.api = 33
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.manifest.launch_mode = standard
[buildozer]
log_level = 2
warn_on_root = 1
