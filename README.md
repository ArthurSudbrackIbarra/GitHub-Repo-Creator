<h1 align="center">GitHub Repository Creator (GRC)</h1>

<br/>
GRC is a tool to automatically create GitHub repositories using YAML templates. It comes with a CLI (Command Line Interface) that you can use to execute commands.
<br/>

## Commands

In the next sections, all the possible GRC commands will be listed and explained.

- [help](#help)
- [version](#version)
- [update](#update)
- [authenticate](#authenticate)
- [create](#create)
- [save](#save)
- [list](#list)
- [get](#get)
- [choose](#choose)
- [delete](#delete)
- [generate](#generate)
- [merge](#merge)
- [list-repos](#list-repos)
- [open-repo](#open-repo)
- [get-repo](#get-repo)
- [remove-repo](#remove-repo)

## Help

The 'help' command gives you orientation about what GRC is and how to use its commands.

```sh
# Usage:
grc help
```

## Version

The 'version' command shows you the GRC version that you are currently using.

![Version](https://user-images.githubusercontent.com/69170322/172204486-f139282f-6f32-4c3e-bf3d-c9188cf95691.png)

```sh
# Usage:
grc version
```

## Update

The 'update' command automatically installs the latest GRC version in case you're still not using it.

![Update](https://user-images.githubusercontent.com/69170322/172204826-73d4fa06-cd18-465e-b1f1-548246c1039c.png)

```sh
# Usage:
grc update
```

## Authenticate

The 'authenticate' command is used so you can authenticate to GitHub and create repositories in your account. This is the **first command** you need to execute in order to start using GRC.

![Authenticate](https://user-images.githubusercontent.com/69170322/172030151-00f09557-7129-4fc6-ab73-7b29078e8147.png)

```sh
# Usage:
grc authenticate <ACCESS_TOKEN>

# Example:
grc authenticate ghp_3dh39j39874hs3d8PSBSHksbsbtx
```

Before running the command, you will need to generate a personal access token in GitHub if you don't have one yet. More on how to do that [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), make sure to check the 'repo' permission box when creating your token.

## Create

The 'create' command creates a repository for you based on a YAML file that is passed as a parameter. The YAML file contains information about the repository you want to create and must follow the patterns defined in the [templates](https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/tree/main/templates).

![Create](https://user-images.githubusercontent.com/69170322/172030355-cf5c3e39-4753-4936-9f26-5c8b8a0799db.png)

**File:** my-template.yaml

```yaml
name: "My-Repository"
description: "This is my repository!"
private: true
includeContent: false

collaborators:
  - collaborator:
      name: "brun0-znx"
      permission: "admin"
  - collaborator:
      name: "Miguel-de-Castro"
      permission: "push"
```

```sh
# Usage:
grc create <PATH_TO_YOUR_YAML_FILE>

# Example:
grc create ./my-template.yaml
```

## Save

The 'save' command is used to save a YAML file to your templates, so that you can later use it to create another repository with the same configurations but with a different repository name/description without having to specify the file path again.

![Save](https://user-images.githubusercontent.com/69170322/172030218-a11db610-6de7-40b2-93e3-0466d31677b6.png)

```sh
# Usage:
grc save <PATH_TO_YOUR_YAML_FILE>

# Example:
grc save ./my-template.yaml
```

## List

The 'list' command lists all the templates that are saved in your machine.

![List](https://user-images.githubusercontent.com/69170322/172093152-a5f96ee0-4803-4b4f-9cb7-029338799e58.png)

```sh
# Usage:
grc list
```

## Get

The 'get' command shows the content of a template that is saved in your machine.

![Get](https://user-images.githubusercontent.com/69170322/172093282-b282c9c8-7ac0-4d00-a758-139880716cd1.png)

```sh
# Usage:
grc get <TEMPLATE_NAME>

# Example:
grc get my-template # Or...
grc get my-template.yaml
```

## Choose

The 'choose' command lets you choose a file from your saved templates to create a repository based on it. When selecting a template, you have the option to use a different repository name/description than the one specified in the template file.

![Choose](https://user-images.githubusercontent.com/69170322/172030272-9f62a9a9-a30e-48bc-8356-ec83b4743737.png)

```sh
# Usage:
grc choose
```

## Edit

The 'edit' command opens a text editor and lets you edit one of your saved templates. If you have [VSCode](https://code.visualstudio.com) installed in your computer, then it is used. If you don't, then a native text editor is used.

![Edit](https://user-images.githubusercontent.com/69170322/172093332-c08f74ba-5a3a-49f9-8811-eaeb01b3a2b9.png)

```sh
# Usage:
grc edit <TEMPLATE_NAME>

# Example:
grc edit my-template # Or...
grc edit my-template.yaml
```

## Delete

The 'delete' command is used to delete a template from your saved templates.

![Delete](https://user-images.githubusercontent.com/69170322/172030289-60f9be26-2575-4e13-a674-ba1519709beb.png)

```sh
# Usage:
grc delete <TEMPLATE_NAME>

# Examples:
grc delete my-template # Or...
grc delete my-template.yaml

grc delete all # Will delete all your templates.
```

## Generate

The 'generate' command will ask you to input information, such as the repository name and collaborators, and then will generate and save an YAML template for you.

![Generate](https://user-images.githubusercontent.com/69170322/173131022-e1e9f209-6812-4f12-995d-13ced317b496.png)

```sh
# Usage:
grc generate
```

## Merge

The 'merge' command takes *N* template names as a parameter and produces a new template joining the collaborators of all the templates inputed. In case some fields conflict, you will be asked to choose which values you want to keep.

![Merge](https://user-images.githubusercontent.com/69170322/174129645-48c988b2-ad4e-4a00-8335-c09e6c5abf83.png)

```sh
# Usage:
grc merge <TEMPLATE_NAME> <TEMPLATE_NAME> ...
grc merge a b c d e f g ... # N number of templates.

# Example:
grc merge my-template-1 my-template-2
```

## List-Repos

The 'list-repos' command will list the name of all the repositories that you have created with GRC.

![List-Repos](https://user-images.githubusercontent.com/69170322/173981692-5dd3c541-052f-4f11-af21-00b2fa6026dc.png)

```sh
# Usage:
grc list-repos
```

## Open-Repo

The 'open-repo' takes the name of a repository that you have created with GRC and opens the repository folder in Visual Studio Code.

```sh
# Usage:
grc open-repo <REPO_NAME>

# Example:
grc open-repo my-repository
```

## Get-Repo

The 'get-repo' command shows you some information about a repository that was created with GRC.

![Get-Repo](https://user-images.githubusercontent.com/69170322/173985059-0b12b4c9-804b-4983-a713-c82a2c69083c.png)

```sh
# Usage:
grc get-repo <REPO_NAME>

# Example:
grc get-repo my-repository
```

## Remove-Repo

The 'remove-repo' commands removes a repository from your repositories list.

```sh
# Usage:
grc remove-repo <REPO_NAME>

# Example:
grc remove-repo my-repository

grc remove-repo all # Removes all your repositories.
```

## Requirements

In order to use GRC, you must have the following tools installed in your machine:

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- (Optional, but recommended) [Visual Studio Code](https://code.visualstudio.com)

## Installation (Windows)

### Automatic installation

1. Open a **Powershell** terminal and run this command:

```ps1
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/main/grc-install.ps1'))
```

### Manual Installation

In case the automatic installation didn't work for you, it is possible to setup GRC manually:

1. Clone this repository:

```sh
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git
```

2. Install the necessary dependencies using pip:

```sh
# In the root of the project:
pip install -r .\.program-files\requirements.txt
```

3. Add the project directory to your path:

![Path](https://user-images.githubusercontent.com/69170322/172077383-d22a075f-0cba-4886-88a1-63f326f136ce.png)

Copy the project directory path, as shown in the image above, and follow [this quick tutorial](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

## Installation (Linux)

1. Open a terminal and run this commmand:

```sh
bash <(curl -s https://raw.githubusercontent.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/main/grc-install.sh)
```
