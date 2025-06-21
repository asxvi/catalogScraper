import os

# helper function to quickly remove all garbage/ outdated txt files
def clearTxt(directory):
    if not os.path.isdir(directory):
        print("Directory doesn't exist.")
        return

    txtFiles = [file for file in os.listdir(directory) if file.endswith('.txt')]
    if not txtFiles:
        print("No txt files in directory")
        return
    
    for file in txtFiles:
        print(file) 
    
    confirm = input("Do you want to remove all of these files for good? (y/n): ").lower()
    if confirm:
        for file in txtFiles:
            os.remove(os.path.join(directory, file))


def getAllSubjectCourses(directory:str, avaliableCourses:list, semester:str):
    if semester.lower() == 'fall' or semester.lower() == 'spring':
        for file in sorted(os.listdir(directory)):                      # sort directory alphabetically like it shows in actual dir
                if file == '.DS_Store':
                    continue

                fullPath = f'{directory}{file}'
                # read file in, and compare if every course is in avaliableCourses for current semester
                with open(fullPath, 'r', encoding='utf-8') as openedFile:
                    lines = openedFile.readlines()
                
                updatedLines = []           # stores all non updated and updated strings in format: 'CS___101\t1\t0'
                for i, line in enumerate(lines):
                    parts = line.strip().split()
                    if parts and parts[0] in avaliableCourses and semester.lower() == 'fall':
                        parts[1] = '1'
                    elif parts and parts[0] in avaliableCourses and semester.lower() == 'spring':
                        parts[2] = '1' 
                    updatedLines.append('\t'.join(parts) + '\n')
        
                # cant easily update file in place, so have to write over existing information... ig thats the best way shrug
                with open(fullPath, 'w') as openedFile:
                    openedFile.writelines(updatedLines)
    else:
        print("semester parameter should be either 'fall' or 'spring'.")
                

if __name__ == '__main__':
    dir1 = './data/'
    dir2 = './dataCH/'
    clearTxt(dir1)
    clearTxt(dir2)