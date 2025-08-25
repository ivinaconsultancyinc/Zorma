import os
# Ensure the directory exists
os.makedirs("insurance_app/schemas", exist_ok=True)
# Overwrite __init__.py without any imports to avoid circular dependencies
with open("insurance_app/schemas/__init__.py", "w") as f:
    f.write("# Schema package initializer\n")
print("__init__.py file regenerated without imports to avoid circular import error.")


