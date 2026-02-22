import os
import shutil

root = os.path.dirname(os.path.abspath(__file__))

# Files to delete from root
files_to_delete = [
    'BUILD_COMPLETE.md',
    'Cold_Mail.ipynb',
    'GMAIL_OAUTH_FIX.md',
    'SMTP_TEST_CHECKLIST.md',
    'Untitled.ipynb',
    'gmail_credentials.json',
    'test_api.py',
    '.ipynb_checkpoints',
]

# Dirs to delete from root
dirs_to_delete = [
    'vectorstore',
]

# Files to delete from backend/
backend_files_to_delete = [
    os.path.join(root, 'backend', 'gmail_service.py'),
    os.path.join(root, 'backend', 'requirements-final.txt'),
    os.path.join(root, 'backend', 'requirements-simple.txt'),
]

# Files to delete from App/
app_files_to_delete = [
    os.path.join(root, 'App', 'CMGapp.py'),
    os.path.join(root, 'App', 'CMGmain.py'),
]

for f in files_to_delete:
    p = os.path.join(root, f)
    if os.path.isfile(p):
        os.remove(p)
        print(f"Deleted file: {f}")
    elif os.path.isdir(p):
        shutil.rmtree(p)
        print(f"Deleted dir: {f}")
    else:
        print(f"Not found (skip): {f}")

for d in dirs_to_delete:
    p = os.path.join(root, d)
    if os.path.isdir(p):
        shutil.rmtree(p)
        print(f"Deleted dir: {d}")
    else:
        print(f"Not found (skip): {d}")

for p in backend_files_to_delete + app_files_to_delete:
    if os.path.isfile(p):
        os.remove(p)
        print(f"Deleted: {p}")
    else:
        print(f"Not found (skip): {p}")

# Handle pydantic-core (may be file or dir)
pc = os.path.join(root, 'pydantic-core')
if os.path.isfile(pc):
    os.remove(pc)
    print("Deleted file: pydantic-core")
elif os.path.isdir(pc):
    shutil.rmtree(pc)
    print("Deleted dir: pydantic-core")
else:
    print("Not found (skip): pydantic-core")

print("\nDone!")
