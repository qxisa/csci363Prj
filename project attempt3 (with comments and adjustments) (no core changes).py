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
        images, _ = subprocess.Popen(["docker", "images"], stdout=subprocess.PIPE).communicate()
        image_list = images.decode().strip().split("\n")
        output_text = "\n".join(image_list)
        if output_text:
            sg.popup(f"Available Docker Images:\n{output_text}")
        else:
            sg.popup("No Docker images found.")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# Function to list running Docker containers
def list_running_containers():
    try:
        containers, _ = subprocess.Popen(["docker", "ps"], stdout=subprocess.PIPE).communicate()
        container_list = containers.decode().strip().split("\n")
        output_text = "\n".join(container_list)
        if output_text:
            sg.popup(f"Running Containers:\n{output_text}")
        else:
            sg.popup("No running containers found.")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# Function to stop a Docker container
def stop_container(container_id):
    try:
        stop_command = f"docker stop {container_id}"
        process = subprocess.Popen(stop_command, shell=True)
        process.wait()
        if process.returncode == 0:
            sg.popup(f"Container '{container_id}' stopped successfully!")
        else:
            sg.popup_error(f"Error stopping container '{container_id}'.")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# Function to search Docker Hub for images
def search_docker_images(image_name):
    try:
        search_command = f"docker search {image_name}"
        results, _ = subprocess.Popen(search_command, stdout=subprocess.PIPE, shell=True).communicate()
        output_text = results.decode().strip()
        if output_text:
            sg.popup(f"Docker Hub Search Results for '{image_name}':\n{output_text}")
        else:
            sg.popup(f"No results found for '{image_name}' on Docker Hub.")
    except Exception as e:
        sg.popup_error(f"An error occurred: {e}")

# Function to pull a Docker image
def pull_docker_image(image_name):
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
    [sg.Text("CMS", font=("Helvetica", 20))],
    # VM Creation
    [sg.Text("Virtual Machine Creation", font=("Helvetica", 16))],
    [sg.Text("Predefined Options:", font=("Helvetica", 14))],
    [sg.Radio("Low-Power", "VmOptions", key='Low-Power', default=True, font=("Helvetica", 12))],
    [sg.Radio("Standard", "VmOptions", key='Standard', font=("Helvetica", 12))],
    [sg.Radio("High-Performance", "VmOptions", key='High-Performance', font=("Helvetica", 12))],
    [sg.Text("Custom Options:", font=("Helvetica", 14))],
    [sg.Text("CPU Cores:", font=("Helvetica", 12)), sg.InputText(key="cpu", font=("Helvetica", 12))],
    [sg.Text("Memory (MB):", font=("Helvetica", 12)), sg.InputText(key="memory", font=("Helvetica", 12))],
    [sg.Text("Disk Size (GB):", font=("Helvetica", 12)), sg.InputText(key="disk", font=("Helvetica", 12))],
    [sg.Button("Create VM", font=("Helvetica", 14))],
    # Docker Management
    [sg.Text("Docker Management", font=("Helvetica", 16))],
    [sg.Text("Dockerfile:", font=("Helvetica", 14))],
    [sg.InputText(key="dockerfile_path", font=("Helvetica", 12)), sg.FileBrowse(key="dockerfile_browse", font=("Helvetica", 12))],
    [sg.Multiline(key="dockerfile_content", autoscroll=True, font=("Helvetica", 12))],
    [sg.Button("Create Dockerfile", font=("Helvetica", 14))],
    [sg.Button("Build Image", font=("Helvetica", 14))],
    [sg.Text("Image Management:", font=("Helvetica", 14))],
    [sg.Button("List Images", font=("Helvetica", 14))],
    [sg.Button("List Running Containers", font=("Helvetica", 14))],
    [sg.Text("Stop Container:", font=("Helvetica", 14))],
    [sg.InputText(key="container_id", font=("Helvetica", 12))],
    [sg.Button("Stop", font=("Helvetica", 14))],
    [sg.Text("Search Docker Hub:", font=("Helvetica", 14))],
    [sg.InputText(key="search_term", font=("Helvetica", 12))],
    [sg.Button("Search", font=("Helvetica", 14))],
    [sg.Button("Pull Image", font=("Helvetica", 14))],
    [sg.Button("Exit", font=("Helvetica", 14))]
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
        list_running_containers()

    if event == "Stop":
        container_id = values["container_id"]
        if container_id:
            stop_container(container_id)
        else:
            sg.popup_error("Please enter a container ID to stop.")

    if event == "Search":
        search_term = values["search_term"]
        if search_term:
            search_docker_images(search_term)
        else:
            sg.popup("Please enter a search term for Docker images.")

    if event == "Pull Image":
        image_name = sg.popup_get_text("Enter image name to pull:")
        if image_name:
            pull_docker_image(image_name)
        else:
            sg.popup("Please enter an image name to pull.")

window.close()
