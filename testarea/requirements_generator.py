import os

# Define the path to your repo directory
repo_path = 'C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser'

# A set to store unique package names
packages = set()

# Walk through all the files in the specified directory
for root, dirs, files in os.walk(repo_path):
    for file in files:
        if file.endswith('.py'):
            # Construct the full file path
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    # Check if the line starts with an import statement
                    if line.startswith('import ') or line.startswith('from '):
                        # Extract the package name
                        parts = line.split()
                        if parts[0] == 'import':
                            package = parts[1].split('.')[0]
                        elif parts[0] == 'from':
                            package = parts[1].split('.')[0]

                        # Add the package name to the set
                        packages.add(package)

# Write the unique package names to requirements.txt
with open('requirements.txt', 'w') as f:
    for package in sorted(packages):
        f.write(package + '\n')

print('requirements.txt has been generated in the specified repo directory.')
