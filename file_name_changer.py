import os
import datetime
import exifread

date_format = "%Y-%m-%d %H.%M.%S"


def reform_date_time_original(date_time_original):
    split_date = str(date_time_original).split(" ")

    if len(split_date) != 2:
        return None
    else:
        first_half = split_date[0].replace(":", "-")
        second_half = split_date[1].replace(":", ".")
        return first_half + " " + second_half


def get_date_time_original(file_path_absolute):
    with open(file_path_absolute, 'rb') as file_data:
        try:
            tags = exifread.process_file(file_data)
        except Exception:
            return None

        tag_date = 'EXIF DateTimeOriginal'

        if tag_date in tags:
            return reform_date_time_original(str(tags[tag_date]))
        else:
            return None


def get_time_of_modification(file_path_absolute):
    file_info = os.stat(file_path_absolute)
    return file_info.st_mtime


def get_time_of_last_change(file_path_absolute):
    file_info = os.stat(file_path_absolute)
    return file_info.st_ctime


def get_time_of_creation(file_path_absolute):
    if get_file_type(file_path_absolute).lower() in ["jpg", "jpeg", "tiff"]:
        date_time_original = get_date_time_original(file_path_absolute)
        if date_time_original is not None:
            return date_time_original

    time_of_last_change = get_time_of_last_change(file_path_absolute)
    time_of_last_modification = get_time_of_modification(file_path_absolute)

    file_time = min(time_of_last_change, time_of_last_modification)

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


def get_file_type(file_name):
    if "." in current_file_name:
        return str(file_name).split(".").pop()
    else:
        return ""


path = os.getcwd()

print("----------------------------------------------------------------------------------------")
print("Instructions:")
print("This program will ignores all the folders under the path., only change all the files.")
print("You will be asked if you want to change each file.")
print()
print("Hope you enjoy! -- William Tao")
print("----------------------------------------------------------------------------------------")
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

    current_file_type = get_file_type(current_file_name)

    target_file_name = get_time_of_creation(current_file_path)
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
