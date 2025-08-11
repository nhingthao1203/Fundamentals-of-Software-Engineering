# #!/bin/bash
# # Note: Use == for string comparison, not -eq which is for numbers
# echo -n "Do you want to install me? [y/n]: "
# read -r answer
# if [[ "${answer,,}" == "y" ]]; then
#     echo "Installed the package successfully!"
# else
#     echo "Cancelled installing the package!"
# fi


#!/bin/bash
# Note: Use tr for case conversion to support Bash 3.x (macOS default)
echo -n "Do you want to install me? [y/n]: "
read -r answer
# Convert answer to lowercase using tr instead of ${answer,,}
if [[ "$(echo "$answer" | tr '[:upper:]' '[:lower:]')" == "y" ]]; then
    echo "Installed the package successfully!"
else
    echo "Cancelled installing the package!"
fi