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

def getAllSubjectCourses(directory, avaliableCourses):
    for file in sorted(os.listdir(directory)):                      # sort directory alphabetically like it shows in actual dir
        with open(f'{directory}{file}', 'r+') as openedFile:
            
            if openedFile == 'courseofferings_CS':
            
            lines = openedFile.readlines()

            lines[]
            for line in lines:
                parts = line.strip().split()
                if parts and parts[0] in avaliableCourses:
                    parts[1] = '1'
                openedFile.write('\t'.join(parts) + '\n')
                i+=1
                

if __name__ == '__main__':
    dir1 = './data/'
    dir2 = './dataCH/'
    # clearTxt(dir1)
    # clearTxt(dir2)
    
    # getAllSubjectCourses(dir2)