#!/usr/bin/env python3
"""
Configure Pi - Restore tool
Usage: python3 restore.py [pi] -b <path>
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

def get_home():
    return Path.home()

def get_pi_dir():
    return get_home() / ".pi" / "agent"

def restore_pi(backup_dir: Path, dry_run: bool = False) -> bool:
    src = backup_dir
    dest = get_pi_dir()

    if not src.exists():
        print(f"[!] Backup dir not found: {src}")
        return False

    if not dest.exists():
        print(f"[!] Pi agent dir not found: {dest}")
        print("    Run 'pi' once first to create the directory structure.")
        return False

    # Safety backup before overwrite
    import os, time
    bak_path = dest.parent / f"pi-agent.bak-{os.getpid()}"
    if not dry_run and any(dest.iterdir()):
        if bak_path.exists():
            shutil.rmtree(bak_path)
        shutil.copytree(dest, bak_path)
        print(f"  ✓ Existing config backed up → {bak_path.name}")

    for item in src.iterdir():
        target = dest / item.name
        if item.is_file():
            if dry_run:
                print(f"  [dry-run] would copy {item.name}")
            else:
                shutil.copy2(item, target)
                print(f"  ✓ {item.name}")
        elif item.is_dir():
            if dry_run:
                print(f"  [dry-run] would copy {item.name}/")
            else:
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(item, target)
                print(f"  ✓ {item.name}/")

    if not dry_run:
        install_packages(backup_dir)
    else:
        settings_file = backup_dir / "settings.json"
        if settings_file.exists():
            s = json.loads(settings_file.read_text(encoding="utf-8"))
            pkgs = [p.removeprefix("npm:") for p in s.get("packages", []) if p.startswith("npm:")]
            if pkgs:
                print(f"  [dry-run] would npm install: {', '.join(pkgs)}")

    return True

def install_packages(backup_dir: Path):
    settings_file = backup_dir / "settings.json"
    if not settings_file.exists():
        return

    settings = json.loads(settings_file.read_text(encoding="utf-8"))
    packages = [
        p.removeprefix("npm:") for p in settings.get("packages", [])
        if p.startswith("npm:")
    ]
    if not packages:
        return

    pi_dir = get_pi_dir()
    print(f"\n[npm packages]")
    print(f"  Installing: {', '.join(packages)}")

    cmd = ["npm", "install"] + packages
    result = subprocess.run(cmd, cwd=str(pi_dir), capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  ✓ npm install complete")
    else:
        print(f"  ⚠️  npm install failed (packages may need manual install):")
        print(f"     {result.stderr.strip().splitlines()[-1] if result.stderr else 'unknown error'}")
        print(f"     Run manually: cd {pi_dir} && npm install {' '.join(packages)}")


def main():
    parser = argparse.ArgumentParser(description="Configure Pi - Restore")
    parser.add_argument("--backup-dir", "-b", type=str, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    backup_dir = Path(args.backup_dir)

    if not backup_dir.exists():
        print(f"❌ Backup dir not found: {backup_dir}")
        sys.exit(1)

    print(f"Restore Pi ← {backup_dir}")
    if args.dry_run:
        print("(dry-run mode)\n")
    else:
        print()

    if restore_pi(backup_dir, args.dry_run):
        print(f"\n✅ Restore complete!")
        if not args.dry_run:
            print("   ⚠️  Restart pi to apply changes.")
    else:
        print("\n⚠️  Restore finished with warnings.")

if __name__ == "__main__":
    main()