import json
import subprocess
import argparse


def parse_dependencies(json_file):
    try:
        dependencies = open(json_file)
        dependencies = dependencies.read()
        dependencies = json.loads(dependencies)
        dependency_list = dependencies["Dependencies"]
        return dependency_list
    except Exception as e:
        print("Exception: %s %s" %(type(e), e))
        print("Couldn't open file: %s" % json_file)

        
        
def install_dependency(dependency):
    try:
        subprocess.check_output(["pip", "install", dependency])
        print("Succcesfully installed %s" %dependency)
    except Exception as e:
        print("Exception: %s %s" %(type(e), e))
        print("Couldn't install dependency: %s %s" %( dependency.split("==")[0] ,dependency.split("==")[1]) )
        return 1
    return 0


def installer(json_file):
    print (json_file)
    dlist = parse_dependencies(json_file)
    icount = 0
    flist = list()
    for item in dlist:
        ret = install_dependency(item)
        if 0 == ret:
            icount=icount+1
        else:
            flist.append(item)
    if 0 < len(flist):
        print("Packages failed to install:")
        for item in flist:
            print (item.split("==")[0])
    elif 0 == len(flist):
        if len(dlist) == icount:
            print("Success")
            
parser = argparse.ArgumentParser(description="Dependency installer for python."
                                             "Expects input as a json file with"
                                             "dependencies in a list")
parser.add_argument("-f", "--json_file", type=str, help="path to json file")
args = parser.parse_args()
if args.json_file:
    installer(args.json_file)
else:
    parser.print_help()