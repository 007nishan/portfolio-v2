"""
_weasy_env.py — LOCAL Windows dev shim for WeasyPrint's native (GTK/Pango/Cairo)
libraries and fontconfig. Import this module BEFORE importing weasyprint on a
Windows dev box that has no system-wide GTK3 runtime.

On the Linux deploy host this shim is a no-op (the apt-installed libs are on the
default loader path — see auto_deploy.sh step 3b in the standard), so importing
it is always safe and never required in production.

The GTK DLLs live in a user-local directory (no admin install needed); they were
extracted from the tschoonj GTK3 runtime installer.
"""
import os
import sys

_GTK_DIR = os.environ.get("PORTFOLIO_GTK_DIR", r"C:\Users\nishanrh\gtk-runtime")


def ensure_native_libs() -> bool:
    """Make WeasyPrint's native deps loadable on Windows. Returns True if the
    local GTK dir was wired in, False if not on Windows / dir absent (no-op)."""
    if sys.platform != "win32":
        return False
    bin_dir = os.path.join(_GTK_DIR, "bin")
    if not os.path.isdir(bin_dir):
        return False
    # 1) DLL search path for gobject/pango/cairo/etc.
    try:
        os.add_dll_directory(bin_dir)
    except (AttributeError, OSError):
        pass
    os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
    # 2) Fontconfig: point at the bundled fonts.conf so font matching/embedding works.
    fonts_conf = os.path.join(_GTK_DIR, "etc", "fonts", "fonts.conf")
    if os.path.isfile(fonts_conf):
        os.environ.setdefault("FONTCONFIG_FILE", fonts_conf)
        os.environ.setdefault("FONTCONFIG_PATH", os.path.dirname(fonts_conf))
    # 3) gdk-pixbuf loaders (harmless if absent).
    loaders = os.path.join(_GTK_DIR, "lib", "gdk-pixbuf-2.0", "2.10.0", "loaders.cache")
    if os.path.isfile(loaders):
        os.environ.setdefault("GDK_PIXBUF_MODULE_FILE", loaders)
    return True


ensure_native_libs()
