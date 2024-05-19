import PySimpleGUI as sg
import subprocess

   
                
                #creating a new vm with the given cpu, memory, and disk

def creatVM(cpu, memory, disk):
    qemu_command = f"qemu-system-x86_64 -smp cores={cpu} -m {memory}M -hda D:\\Nu\\csci363\\project\\vm_disk.img"
    process = subprocess.Popen(qemu_command, shell=True)
    _, stderr = process.communicate()


                #predefined values for the default VM settings
VmOptions = {
    "Low-Power": {"cpu": 1, "memory": 512, "disk": 10},
    "Standard": {"cpu": 2, "memory": 1024, "disk": 20},
    "High-Performance": {"cpu": 4, "memory": 2048, "disk": 40},
}

             



                #creating a docker file

def createDockerfile(filepath, content):
    try:
        with open(filepath, "w") as f:      #"w" is used to write to the file
            f.write(content)
    except Exception as e:
        sg.popup_error(f"error creating Dockerfile: {e}")


                #building a docker image

def buildDockerImg(dockerfile, image_name):
    build_command = f"docker build -t {image_name} -f {dockerfile}" #build command for the docker image
    process = subprocess.Popen(build_command, shell=True)
    process.wait()                          #wait for the process to finish
    sg.popup(f"Docker image '{image_name}' built successfully!")



                #listing docker images
def listDockerImgs():
    try:
        images, _ = subprocess.Popen(["docker", "images"], stdout=subprocess.PIPE).communicate() #list all the images in the docker container
        image_list = images.decode().strip().split("\n")
        output_text = "\n".join(image_list) #join the images in the list
        if output_text:
            sg.popup(f"available Docker images:\n{output_text}")
        else:
            sg.popup("no Docker images found.")
    except Exception as e:
        sg.popup_error(f"an error occurred: {e}")

                #listing running containers
def listRunningContainers():
    try:
        containers, _ = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE).communicate()
        container_list = containers.decode().strip().split("\n") #split the containers 
        output_text = "\n".join(container_list)
        if output_text:
            sg.popup(f"running Containers:\n{output_text}")
        else:
            sg.popup("no running containers found")
    except Exception as e:
        sg.popup_error(f"an error occurred: {e}")

                #stopping a running container
def stopContainer(container_id):
    try:
        stop_command = f"docker stop {container_id}"
        process = subprocess.Popen(stop_command, shell=True)
        process.wait()
        if process.returncode == 0:
            sg.popup(f"container '{container_id}' stopped!")
        else:
            sg.popup_error(f"error stopping container")
    except Exception as e:
        sg.popup_error(f"error returned {e}")

# Function to search Docker Hub for images
def searchDockerImgs(image_name):
    try:
        search_command = f"docker search {image_name}"
        results, _ = subprocess.Popen(search_command, stdout=subprocess.PIPE, shell=True).communicate()
        output_text = results.decode().strip()
        if output_text:
            sg.popup(f"search results: '{image_name}':\n{output_text}")
        else:
            sg.popup(f"no results found")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# Function to pull a Docker image
def pullDockerImg(image_name):
    try:
        pull_command = f"docker pull {image_name}"
        process = subprocess.Popen(pull_command, shell=True)
        process.wait()
        if process.returncode == 0:
            sg.popup(f"Docker image '{image_name}' pulled successfully!")
        else:
            sg.popup_error(f"Error pulling Docker image '{image_name}'. Check network connectivity or image name.")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# GUI layout definition
layout = [
    [sg.Text("CMS")],
    # VM Creation
    [sg.Text("create a virtual machine")],
    [sg.Radio("Low-Power", "VmOptions", key='Low-Power', default=True, )],
    [sg.Radio("standard", "VmOptions", key='Standard', )],
    [sg.Radio("High-Performance", "VmOptions", key='High-Performance', )],
    [sg.Text("custom virutal machine settings", )],
    [sg.Text("CPU Cores:", ), sg.InputText(key="cpu", )],
    [sg.Text("Memory (MB):", ), sg.InputText(key="memory", )],
    [sg.Text("Disk Size (GB):", ), sg.InputText(key="disk", )],
    [sg.Button("create", )],
    # Docker Management
    [sg.Text("Docker Management")],
    [sg.Text("Dockerfile:", )],
    [sg.InputText(key="dockerfile_path", ), sg.FileBrowse(key="dockerfile_browse", )],
    [sg.Multiline(key="dockerfile_content", autoscroll=True, )],
    [sg.Button("Create Dockerfile", )],
    [sg.Button("Build Image", )],
    [sg.Text("Image Management:", )],
    [sg.Button("List Images", )],
    [sg.Button("List Running Containers", )],
    [sg.Text("Stop Container:", )],
    [sg.InputText(key="container_id", )],
    [sg.Button("Stop", )],
    [sg.Text("Search Docker Hub:", )],
    [sg.InputText(key="search_term", )],
    [sg.Button("Search", )],
    [sg.Button("Pull Image", )],
    [sg.Button("Exit", )]
]

# Create the window
window = sg.Window("Cloud Management System", layout)

# Event loop to handle user interaction
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # VM Creation
    if event == "Create VM":
        selected_option = next((key for key, value in values.items() if value is True and key in VmOptions), None)
        if selected_option:  # Predefined option selected
            cpu = VmOptions[selected_option]["cpu"]
            memory = VmOptions[selected_option]["memory"]
            disk = VmOptions[selected_option]["disk"]
        else:  # Custom options
            try:
                cpu = int(values["cpu"])
                memory = int(values["memory"])
                disk = int(values["disk"])
            except ValueError:
                sg.popup_error("Invalid input for CPU, memory, or disk. Please enter integers.")
                continue
        creatVM(cpu, memory, disk)

    # Dockerfile Management
    if event == "Create Dockerfile":
        dockerfile_path = values["dockerfile_path"]
        dockerfile_content = values["dockerfile_content"]
        if dockerfile_path and dockerfile_content:
            createDockerfile(dockerfile_path, dockerfile_content)
        else:
            sg.popup_error("Please specify both Dockerfile path and content.")
            continue

    if event == "Build Image":
        dockerfile_path = values.get("dockerfile_path")
        image_name = sg.popup_get_text("Enter image name:")
        if dockerfile_path and image_name:
            buildDockerImg(dockerfile_path, image_name)
        else:
            sg.popup_error("Please specify both Dockerfile path and image name.")
            continue

    # Docker Image Management
    if event == "List Images":
        listDockerImgs()

    if event == "List Running Containers":
        listRunningContainers()

    if event == "Stop":
        container_id = values["container_id"]
        if container_id:
            stopContainer(container_id)
        else:
            sg.popup_error("Please enter a container ID to stop.")

    if event == "Search":
        search_term = values["search_term"]
        if search_term:
            searchDockerImgs(search_term)
        else:
            sg.popup("Please enter a search term for Docker images.")

    if event == "Pull Image":
        image_name = sg.popup_get_text("Enter image name to pull:")
        if image_name:
            pullDockerImg(image_name)
        else:
            sg.popup("Please enter an image name to pull.")

window.close()
