import sys
import os
import shutil


video_folder = ["avi", "mp4", "mov", "mkv", "gif"]
audio_folder = ["mp3", "ogg", "wav", "amr", "m4a", "wma"]
images_folder = ["jpeg", "png", "jpg", "svg"]
doc_folder = ["doc", "docx", "txt", "pdf", "xlsx", "pptx", "html", "scss", "css", "map"]
arch_folder = ["zip", "gz", "tar", "rar"]


def get_main_path():
    main_path = ""
    args = sys.argv
    if len(args) == 1:
        main_path = input("Введіть шлях до папки: ")   
    else:
        main_path = args[1]
    while True:
        if not os.path.exists(main_path):
            if main_path:
                print(f"{main_path} не існує")
            main_path = input("Введіть шлях до папки: ")
        else:
            if os.path.isdir(main_path):
                break
            else:
                print(f"{main_path} це не папка")
                main_path = ""
    return around_dir(main_path)


def normalize(file):
    map = {"а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y", 
    "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", 
    "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "і": "i", "є": "e", "ї": "i", "А": "A", 
    "Б": "B", "В": "V", "Г": "G", "Д": "D", "Е": "E", "Ё": "E", "Ж": "h", "З": "Z", "И": "I", "Й": "Y", "К": "K", "Л": "L", 
    "М": "M", "Н": "N", "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T", "У": "U", "Ф": "F", "Х": "H", "Ц": "Ts", "Ч": "Ch", 
    "Ш": "Sh", "Щ": "Sch", "Ъ": "", "Ы": "Y", "Ь": "", "Э": "E", "Ю": "Yu", "Я": "Ya", "І": "I", "Є": "E",  "Ї": "I"}
    lists = file.split(".")
    name_file = ".".join(lists[0:-1])
    new_name = ""
    for el in name_file:
        if el in map:
            new_name += map[el]
        elif (ord("A") <= ord(el) <= ord("Z")) or (ord("a") <= ord(el) <= ord("z")) or el.isdigit():
            new_name += el
        else:
            new_name += "_"
    return new_name + "." + lists[-1]


def make_dirs(main_path):
    global video_path
    video_path = os.path.join(main_path, "video")
    if not os.path.exists(video_path):
        os.makedirs(video_path)

    global audio_path
    audio_path = os.path.join(main_path, "audio")
    if not os.path.exists(audio_path):
        os.makedirs(audio_path)

    global images_path
    images_path = os.path.join(main_path, "images")
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    global documents_path
    documents_path = os.path.join(main_path, "documents")
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    global archives_path
    archives_path = os.path.join(main_path, "archives")
    if not os.path.exists(archives_path):
        os.makedirs(archives_path)


def handling_file(main_path, file, file_path):
    file_name_divide = normalize(file).split(".")
    file_ending = ""
    if len(file_name_divide) > 1:
        file_ending = file_name_divide[-1]
    if not file_ending.lower():
        return None
    else:
        if file_ending in video_folder:
            new_path = os.path.join(video_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(video_path, normalize(file)))
    
        elif file_ending in audio_folder:
            new_path = os.path.join(audio_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(audio_path, normalize(file)))
        
        elif file_ending in images_folder:
            new_path = os.path.join(images_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(images_path, normalize(file)))
            
        elif file_ending in doc_folder:
            new_path = os.path.join(documents_path, file)
            os.replace(shutil.move(file_path, new_path), os.path.join(documents_path, normalize(file)))

        elif file_ending in arch_folder:
            new_path = os.path.join(archives_path, file)

            try:
                shutil.unpack_archive(shutil.move(file_path, new_path), os.path.join(archives_path, normalize(file).rstrip(file_ending)))
            except shutil.ReadError:
                print(f"Незнайомий формат, архів {normalize(file)}, не може розпакуватись. Імпортуйте додаткову бібліотеку.")
            finally:
                os.rename(os.path.join(archives_path, file), os.path.join(archives_path, normalize(file)), )

        else:
            os.replace(file_path, os.path.join(main_path, normalize(file)))
            return None


def around_dir(main_path):
    files = os.listdir(main_path)
    make_dirs(main_path)
    for file in files:
        file_path = os.path.join(main_path, file)
        if os.path.isfile(file_path):
            # make_dirs(main_path)
            handling_file(main_path, file, file_path)
        else:
            around_dir(file_path)
            if not os.listdir(file_path):
                os.rmdir(file_path)
                continue


if __name__ == "__main__":
    get_main_path()