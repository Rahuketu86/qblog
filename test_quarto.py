import os

# print(os.getenv("QUARTO_PROJECT_DIR"))

for key, value in os.environ.items():
    if key.startswith("QUARTO"):
        print('{}: {}'.format(key, value))