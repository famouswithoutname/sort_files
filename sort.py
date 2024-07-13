import os
import subprocess
import shutil
import re

'''This programm created for Linux file system'''
folders_ignor = ['images','other','arch','doc','video','music']

# масиви з розширеннями файлів.


def rm_empty_folder(mas, way_to_folder) :
     '''Функція видаляє пусту теку'''
     if len(mas) == 0:
          os.rmdir(way_to_folder)


def normilize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for cs, tr in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(cs)] = tr
        TRANS[ord(cs.upper())] = tr.upper()

    trans_name = ""
    

    for i in name:
        letter = re.findall('[A-Za-z0-9_А-Яа-я.]',i)
        eng = re.findall('[A-Za-z.]',i)
        if i == " ":
            trans_name = trans_name + "_"
        elif len(letter) == 0:
             trans_name = trans_name + '_'
             
        elif i.isnumeric():
             trans_name = trans_name + i
        elif i in eng:
             trans_name = trans_name+i
        else:
            for key,val in TRANS.items():
                if ord(i) == key:
                    trans_name = trans_name + val
    return trans_name

def check_path(way_to_folder):
    '''Функція перевіряє чи існує ця папка або чи коректний шлях до неї'''    
    if os.path.exists(way_to_folder):
        return True
    else:
        print('Not exist')
        return False

def convert_to_format(word):
    '''Якщо файл має пробіли то функція приводить їх до формату, завдяки якому CLI може їх зчитати'''
    
    clear = ''
    letters = re.findall('[^\w.]',word)
    print(letters)
    for i in word:
        if i in letters:
            clear = clear + f'\{i}'
        else:
            clear = clear + i
    return clear         


def rename_files(mas, way_to_folder):
    '''функція за допомогою normilize перейменовує файли'''
   
    for i in mas:
        print(i)
        print(normilize(i))
        right_pass = convert_to_format(i)
        true_format = normilize(i)
                   
        subprocess.run(f'mv {way_to_folder}/{right_pass} {way_to_folder}/{true_format}', shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE )
    
         



def files_to_mas(way_to_folder):
    '''Функція перетворює файли у масив'''
    #запуск команди ls, щоб ми переглянули файли у папці, де будемо сортувати файли
    print(way_to_folder)
    clear_file = []
    
    command = subprocess.run(f'ls {way_to_folder}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # відкривається файл, куди запишемо список наших файлів і папок у папці
    with open('/home/famouswithoutname/Documents/programming/sort_project/files_list.txt','w') as file:
            file.write(command.stdout.decode('UTF-8')) # stdout зберігає результат виклику команди в бітовому значені, тому ми його розшифровуємо.
    # відкриваємо файл, для того, щоб прочитати вміст файлу
    with open('/home/famouswithoutname/Documents/programming/sort_project/files_list.txt','r') as file:
            files = file.readlines() # строки записуємо у масив
            #пребераємо масив та видаляємо зайві символи
    for i in files:
        clear_file.append(i.replace('\n',''))
    
    return clear_file


def sortfiles(way_to_folder):
    '''Функція сортування файлів'''
    images = ['JPEG', 'PNG', 'JPG', 'SVG','bat']
    video = ['AVI', 'MP4', 'MOV', 'MKV']
    doc = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    music = ['MP3', 'OGG', 'WAV', 'AMR']
    arch = ['ZIP', 'GZ', 'TAR']
    
    
    
    file_split = []
    remove_folder = None
    
    
    if check_path(way_to_folder) == True:
        
            files = files_to_mas(way_to_folder)
            print(files)
            rename_files(files,way_to_folder)
            files = files_to_mas(way_to_folder)
            for file in files:
            # відділяємо розширення файлу від назви
                file_split.append(file.split('.'))
            print(file_split)
            rm_empty_folder(file_split,way_to_folder)
            for elem in file_split: #перевірка файлу, до якої теки його сортувати
                print(elem)
                if len(elem) == 2: # якщо довжина масиву 2 то вона має розширення і це не тека        
                    
                    if elem[1].upper() in images: # Перевірка до якох теки відправити файл.
                        if not os.path.exists(f'{way_to_folder}/images'): # Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/images')
                        # переносимо файл у потрібну нам теку
                        command  = subprocess.run(f'mv {way_to_folder}/{'.'.join(elem)} {way_to_folder}/images/{'.'.join(elem)}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    elif elem[1].upper() in video: # Перевірка до якох теки відправити файл.
                        if not os.path.exists(f'{way_to_folder}/video'): # Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/video')
                        # переносимо файл у потрібну нам теку
                        command  = subprocess.run(f'mv {way_to_folder}/{'.'.join(elem)} {way_to_folder}/video/{'.'.join(elem)}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    elif elem[1].upper() in doc: # Перевірка до якох теки відправити файл.
                        if not os.path.exists(f'{way_to_folder}/doc'): # Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/doc')
                        # переносимо файл у потрібну нам теку
                        command  = subprocess.run(f'mv {way_to_folder}/{'.'.join(elem)} {way_to_folder}/doc/{'.'.join(elem)}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    elif elem[1].upper() in music: # Перевірка до якох теки відправити файл.
                        if not os.path.exists(f'{way_to_folder}/music'): # Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/music')
                        # переносимо файл у потрібну нам теку
                        command  = subprocess.run(f'mv {way_to_folder}/{'.'.join(elem)} {way_to_folder}/music/{'.'.join(elem)}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                    elif elem[1].upper() in arch: # Перевірка до якох теки відправити файл.
                        if not os.path.exists(f'{way_to_folder}/arch'):# Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/arch')
                        path = shutil.unpack_archive(f'{way_to_folder}/{'.'.join(elem)}', f'{way_to_folder}/arch/{'.'.join(elem)}' ) # розпакування архіву.
                    else: # якщо не знайдено потрібного розширення.
                        if not os.path.exists(f'{way_to_folder}/other'): # Перевірка, чи існує ця тека, якщо ні то створити
                            os.mkdir(f'{way_to_folder}/other')
                        # переносимо файл у потрібну нам теку
                        command  = subprocess.run(f'mv {way_to_folder}/{'.'.join(elem)} {way_to_folder}/other/{'.'.join(elem)}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                elif len(elem) == 1: # Якщо довжина елементу масиву 1 то це папка
                    if elem[0] in folders_ignor: # перевіряємо чи потрібно ігнорувати цю теку
                        continue
                    else:
                        folders_ignor.append(elem[0])
                        folder_path = way_to_folder + '/' + elem[0]   
                        remove_folder = '/' + elem[0]
                        sortfiles(folder_path)                # робимо рекурсію, щоб пройтись по усіх теках.
            if remove_folder == None:
                    return way_to_folder
            else:
                    return sortfiles(way_to_folder.replace(remove_folder,''))    
                              
            
    
    else:
        return None



#Користувач вводить шлях до папки
way = input('Please write the path to folder: ')


print(sortfiles(way))

