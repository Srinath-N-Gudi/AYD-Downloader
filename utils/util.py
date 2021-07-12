import os
def get_ex_file(wrong_file_name, path):
        files = os.listdir(path)
        words = wrong_file_name.split()
        samples = []
        more = []
        cnt = 0
        file_split = [i.split() for i in files]
        values = [compare(words, i) for i in file_split]       
        return os.path.join(path, files[values.index(max(values))]).replace("\\\\", "/").replace("\\", "/")

def compare(list1, list2):
    cnt = 0
    for i, j in zip(list1, list2):
        if i.lower() == j.lower():
            cnt+=1
    return cnt
def get_sub_folder_path(path):
    return path[:path.rindex('/')]
def replace_string(list, word, w=""):
    for i in list:
        word = word.replace(i, "")
    return word

def rm(wrong_file_name, path):
    list = ['.', ","]
    files = os.listdir(path)
    file_split = [i.split() for i in files]
    file = replace_string(list, wrong_file_name, w="")
    for i in files:
        if file in i:
            return os.path.join(path, i).replace("\\", "/")
        else:
            pass
    return None
if __name__=="__main__":
    print(rm("Eredaze - Save Me (feat. Luke & Jolle) (Audio)", 'D:\Programs\Advanced Youtube Downloader\TestMp3'))
