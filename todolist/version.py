from __future__ import annotations

from pbr import version as pbr_version

CMP_EXTRA_VENDOR = "TODOLIST"
CMP_EXTRA_PRODUCT = "TODOLIST API"
CMP_EXTRA_PACKAGE = None  # OS distro package version suffix

loaded = False
version_info = pbr_version.VersionInfo("todolist")
version_string = version_info.version_string
