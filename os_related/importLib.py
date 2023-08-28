import requests
from pathlib import Path
import importlib
from sys import path
from pkgutil import iter_modules
import subprocess

def import_from_github(https:str, file_name: str = "chosen from end of link", directory=path[0], load_lib = False):
    """This function is used to import a file to a chosen directory using a github raw link
    NOTE: The Repository used has to be public or the use of inconsistant tokens are required
    
    args:
        https: A  github raw website string.
        file_name: The name chosen for the file imported.
        directory: Chosen directory to place the file in
        load_lib: if the library should be returned

    Returns:
        bool: True or False, Success or Fail
        if load_lib: Library
        """
    
    file_name = "/".join(map(str,(https.split("/")[-1:]))) if file_name == "chosen from end of link" else file_name
    
    file_path = f"{directory}/{file_name}"
    file_path = file_path.replace("\\", "/").replace("//", "/")
    if Path(file_path).is_file():
        print(f"{file_path} already exists")
    else:
        print(f"{file_path} doesn't exist, download")
        try:
            request = requests.get(https)
        except requests.exceptions.MissingSchema:
            print("URL not found")
            return False
        if (str(request.content) == "b'404: Not Found'"):
            print(str(request.content)[2:-1])
            return False

        with open(file_path, "wb") as f:
            f.write(request.content)
    file_name = file_name.split(".")[0]
    if load_lib:
        module_spec = importlib.util.spec_from_file_location(file_name, file_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        return module
    return True

def import_from_github_using_path(from_path:str, file_name: str = "chosen from end of link", directory=path[0], load_lib = False):
    """This is an extension on import_from_github, which imports files using a github raw link
    
    args: 
        from_path: str = The path which the file is imported from, 
            examplewise: 
                1. repo/dir.../filename.type
                2. PyLibraries/os_related/importLib.py
        file_name: The name chosen for the file imported.
        directory: Chosen directory to place the file in
        load_lib: if the library should be returned

    Returns:
        bool: True or False, Success or Fail
        if load_lib: Library"""
    from_path = from_path.replace("\\", "/").replace("//","/")
    https = fr"https://raw.githubusercontent.com/GGisMee/{from_path}"
    return import_from_github(https=https,file_name=file_name, directory= directory, load_lib=load_lib)

def import_from_path(file_name, directory):
    """imports a file from path
    
    tip: use r'directory', to not have to worry about SyntaxError
    
    args:
        file_name: The name of the file to import.
        directory: the directory which the file comes from
    
    returns:
        bool: False if fail, library is true
    """
    file_path = f"{directory}/{file_name}"
    if not Path(file_path).is_file():
        print("file doesn't exist")
        return False
    module_spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    return module
        
def check_modules(modules:list[str], import_pip:bool=False, show:bool=False):
    """Checks if any of provided modules are not imported
    
    args:
        modules: list = modules to check
        import_pip: bool = if unimported modules should be downloaded using pip
        show: bool = shows unimported modules
    return:
        if len(list_of_unimported_modules) < 0:
            0
        else:
            list_of_unimported_modules"""
    list_of_unimported = []
    for module in modules:
        imported = False
        for module_info in iter_modules():
            if module == module_info.name:
                imported = True
                break
        if not imported:
            list_of_unimported.append(module)
    if list_of_unimported == []:
        return 0
    if show:
        print("Following modules were not found:")
        print(str(list_of_unimported)[1:-1].replace("'", ''))
    if not import_pip:
        return list_of_unimported
    for module in list_of_unimported:
        try:
            subprocess.check_call(['pip3', 'install', module])
        except subprocess.CalledProcessError:
            print(module+' not found in pip')
    return list_of_unimported