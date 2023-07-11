import os
import datetime


date_format = "%Y-%m-%d %H.%M.%S"


def get_modified_date(file_path):
    file_info = os.stat(file_path)

    file_stime = file_info.st_mtime
    file_ctime = file_info.st_ctime

    file_time = min(file_stime, file_ctime)

    file_datetime = datetime.datetime.fromtimestamp(file_time)
    return file_datetime.strftime(date_format)


def reset_file_name(old_path, new_path, file_type, index=1):
    new_path_with_file_type = append_file_type(new_path, file_type)

    if old_path == new_path_with_file_type:
        return

    try:
        os.rename(old_path, new_path_with_file_type)
    except FileExistsError:
        new_path = os.path.join(path, f"{target_file_name} {index}")
        reset_file_name(old_path, new_path, file_type, index + 1)


def append_file_type(file_path, file_type):
    return file_path + "." + file_type


path = os.getcwd()

print("Instructions:")
print("This program will ignores all the folders under the path., only change all the files.")
print("You will be asked if you want to change each file.")
print()
print("Hope you enjoy! -- William Tao")
print()
print(f"Current folder path: {path}   Press enter to continue.", end="")
input()
print()

file = os.listdir(path)

need_change_all_files = False

for i in file:
    current_file_name = str(i)
    current_file_path = os.path.join(path, current_file_name)
    if not os.path.isfile(current_file_path):
        continue

    if current_file_name.lower() == "file_name_changer.exe":
        continue

    current_file_type = ""
    if "." in current_file_name:
        current_file_type = str(current_file_name).split(".").pop()

    target_file_name = get_modified_date(current_file_path)
    target_file_path = os.path.join(path, target_file_name)

    print(f"{current_file_name} \t--> {append_file_type(target_file_name, current_file_type)}")

    if need_change_all_files:
        reset_file_name(current_file_path, target_file_path, current_file_type)
    else:
        user_input = input("Change file name? (ENTER key: change this file; s: skip; a: change all) ")
        print()

        if user_input == "":
            reset_file_name(current_file_path, target_file_path, current_file_type)
        elif user_input == "s":
            continue
        elif user_input == "a":
            need_change_all_files = True
            reset_file_name(current_file_path, target_file_path, current_file_type)
        else:
            break

print("This program is created by William Tao. Hope it was helpful for you!", end="")
input()
