import os

# helper function to quickly remove all garbage/ outdated txt files
def clearTxt():
    directory = './data/'

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

def getAllSubjectCourses():
    folderPath = "./data/"

    # cool fact is there are about 7501 courses avaliable in catalog
    for file in os.listdir(folderPath):
        with open(f'{folderPath}{file}', 'r') as openedFile:
            for line in openedFile:
                print(line.split()[0])
            # mastercourselist_


if __name__ == '__main__':
    # clearTxt()
    getAllSubjectCourses()