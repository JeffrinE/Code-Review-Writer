import os
class codeToText:

    def __init__(self, folder_path, excluded_files):
        self.folder_path = folder_path
        self.excluded_files = excluded_files

    def parse_folder(self, folder_path):
        tree = ""
        for root, dirs, files in os.walk(folder_path):
            if root.startswith(tuple(self.excluded_files)):
                print(f"Excluded {root}")
                continue
            else:
                level = root.replace(folder_path, "").count(os.sep)
                indent = " " * 4 * level
                tree += f'{indent}{os.path.basename(root)}/\n'
                subindent = " " * 4 * (level+1)
                for f in files:
                    tree += f"{subindent}{f}\n"
        return tree


    def get_file_contents(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()


    def process_files(self, path):
        content = ""
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if root.startswith(tuple(self.excluded_files)) or file_path in self.excluded_files:
                    #print(f"Excluded {root}")
                    continue
                try :

                    file_content = self.get_file_contents(file_path)
                    content += f"File Path: {file_path}\n"
                    content += f"File type: {os.path.splitext(file_path)[1]}\n"
                    content += f"Code: \n{file_content}"

                    content += f"\n\n<---File End--->\n\n"
                except:
                    print(f"Couldn't process {file_path}")

        return content

    def get_text(self):
        file_contents = self.process_files(self.folder_path)
        final_file_contents = f"{file_contents}"
        return final_file_contents

    def get_tree(self):
        folder_structure = self.parse_folder(self.folder_path)
        final_file_structure = f"{folder_structure}"
        return final_file_structure

    def get_file(self):
        contents = self.get_text()
        structure = self.get_tree()

        try:
            if not os.path.exists(r"output"):
                os.mkdir("output")
        except:
            pass

        with open("output/file_content.txt", "w") as file_contents:
            file_contents.write(contents)

        with open("output/file_structure.txt", "w") as file_structure:
            file_structure.write(structure)

    def codeToTextRun(folder_path, excluded_folders_list):
        code_to_text = codeToText(folder_path,  excluded_folders_list)
        code_to_text.get_file()


