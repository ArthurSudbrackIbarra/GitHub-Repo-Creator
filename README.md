<h1 align="center">GitHub Repository Creator (GRC)</h1>

<br/>
GRC is a tool to automatically create and manage GitHub repositories using YAML templates. It comes with a CLI (Command Line Interface) that you can use to execute commands.
<br/>

<br/>
<p align="center">
  <img src="https://media.giphy.com/media/QsRN3q7lypKitwzV8R/giphy.gif">
</p>
<br/>

## Table of Contents

- [CLI Commands](#cli-commands)
- [Installation (Windows)](#installation-windows)
  - [Automatic Installation](#automatic-installation)
  - [Manual Installation](#manual-installation)
- [Installation (Linux and MacOS)](#installation-linux-and-macos)

## Visual Studio Code Extension

If you don't like using the command line, GRC also has a [Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=ArthurSudbrackIbarra.grc&ssr=false#user-content-requirements), which creates an abstraction on top of the GRC commands for you. Although more limited, it is a great option for people who don't want to memorize all the CLI commands.

| GRC Version | Compatible GRC Extension Version |
| :---------: | :------------------------------: |
|   v3.0.1    |              v0.0.1              |
|   v3.0.2    |              v0.0.2              |

<br/>
<p align="center">
  <img src="https://user-images.githubusercontent.com/69170322/177070202-29ee23fc-f66b-4798-b8ee-51cb859ce631.png">
</p>
<br/>

## CLI Commands

In the next sections, all the possible GRC commands will be listed and explained.

### General Commands

General commands have no prefix, they are used directly after 'grc'. Example: grc version.

- [help](#help)
- [version](#version)
- [update](#update)
- [authenticate](#authenticate)
- [user](#user)

### Template Commands

Template commands have the 'temp' prefix. Example: grc **temp** list.

- [apply](#temp-apply)
- [save](#temp-save)
- [list](#temp-list)
- [get](#temp-get)
- [choose](#temp-choose)
- [delete](#temp-delete)
- [generate](#temp-generate)
- [merge](#temp-merge)

### Repositories Commands

Repositories commands have the 'repo' prefix. Example: grc **repo** list. These commands apply to the **LOCAL repositories created with GRC**.

- [list](#repo-list)
- [open](#repo-open)
- [get](#repo-get)
- [remove](#repo-remove)

### Remote Repositories Commands

Remote repositories commands have the 'remote' prefix. Example: grc **remote** list. These commands apply to **your REMOTE repositories on GitHub**.

- [list](#remote-list)
- [add-collab](#remote-add-collab)
- [clone](#remote-clone)
- [url](#remote-url)

## Help

The 'help' command gives you orientation about what GRC is and how to use its commands.

```sh
# Usage:
grc help
```

## Version

The 'version' command shows you the GRC version that you are currently using.

```sh
# Usage:
grc version
```

## Update

The 'update' command automatically installs the latest GRC version in case you're still not using it.

```sh
# Usage:
grc update
```

## Authenticate

The 'authenticate' command is used so you can authenticate to GitHub and create repositories in your account. This is the **first command** you need to execute in order to start using GRC.

```sh
# Usage:
grc authenticate <ACCESS_TOKEN>

# Example:
grc authenticate ghp_3dh39j39874hs3d8PSBSHksbsbtx
```

## User

The 'user' command shows information about the current authenticated user.

```sh
# Usage:
grc user
```

Before running the command, you will need to generate a personal access token in GitHub if you don't have one yet. More on how to do that [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), make sure to check the 'repo' permission box when creating your token.

## (Temp) Apply

The 'apply' command creates a repository for you based on a YAML file that is passed as a parameter. The YAML file contains information about the repository you want to create and must follow the patterns defined in the [templates](https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/tree/main/templates).

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
grc temp apply <PATH_TO_YOUR_YAML_FILE>

# Example:
grc temp apply ./my-template.yaml
```

## (Temp) Save

The 'save' command is used to save a YAML file to your templates, so that you can later use it to create another repository with the same configurations but with a different repository name/description without having to specify the file path again.

```sh
# Usage:
grc temp save <PATH_TO_YOUR_YAML_FILE>

# Example:
grc temp save ./my-template.yaml
```

## (Temp) List

The 'list' command lists all the templates that are saved in your machine.

```sh
# Usage:
grc temp list
```

## (Temp) Get

The 'get' command shows the content of a template that is saved in your machine.

```sh
# Usage:
grc temp get <TEMPLATE_NAME>

# Example:
grc temp get my-template # Or...
grc temp get my-template.yaml
```

## (Temp) Choose

The 'choose' command lets you choose a file from your saved templates to create a repository based on it. When selecting a template, you have the option to use a different repository name/description than the one specified in the template file.

```sh
# Usage:
grc temp choose # Or...
grc temp choose <TEMPLATE_NAME>

# Example:
grc temp choose # Will show an enumerated list with the possible template options.

grc temp choose my-template # Will directly choose the template called "my-template".

# Options:

# -p, --private (true or false):
grc temp choose my-template --private true # Overrides the 'private' field.

# -i, --include_content (true or false):
grc temp choose my-template --include_content false # Overrides the 'includeContent' field.
```

## (Temp) Edit

The 'edit' command opens a text editor and lets you edit one of your saved templates. If you have [VSCode](https://code.visualstudio.com) installed in your computer, then it is used. If you don't, then a native text editor is used.

```sh
# Usage:
grc temp edit <TEMPLATE_NAME>

# Example:
grc temp edit my-template # Or...
grc temp edit my-template.yaml
```

## (Temp) Delete

The 'delete' command is used to delete a template from your saved templates.

```sh
# Usage:
grc temp delete <TEMPLATE_NAME>

# Examples:
grc temp delete my-template # Or...
grc temp delete my-template.yaml

grc temp delete all # Will delete all your templates.
```

## (Temp) Generate

The 'generate' command will ask you to input information, such as the repository name and collaborators, and then will generate and save an YAML template for you.

```sh
# Usage:
grc temp generate
```

## (Temp) Merge

The 'merge' command takes _N_ template names as a parameter and produces a new template joining the collaborators of all the templates inputed. In case some fields conflict, you will be asked to choose which values you want to keep.

```sh
# Usage:
grc temp merge <TEMPLATE_NAME> <TEMPLATE_NAME> ...
grc temp merge a b c d e f g ... # N number of templates.

# Example:
grc temp merge my-template-1 my-template-2
```

## (Repo) List

The 'list' command will list the name of all the repositories that you have created with GRC.

```sh
# Usage:
grc repo list
```

## (Repo) Open

The 'open' command takes the name of a repository that you have created with GRC and opens the repository folder in Visual Studio Code.

```sh
# Usage:
grc repo open <REPOSITORY_NAME>

# Example:
grc repo open my-repository
```

## (Repo) Get

The 'get' command shows you some information about a repository that was created with GRC.

```sh
# Usage:
grc repo get <REPOSITORY_NAME>

# Example:
grc repo get my-repository
```

## (Repo) Remove

The 'remove' commands removes a repository from your repositories list.

```sh
# Usage:
grc repo remove <REPOSITORY_NAME>

# Example:
grc repo remove my-repository

grc repo remove all # Removes all your repositories.
```

## (Remote) List

The 'list' command lists all the repositories in your GitHub account.

```sh
# Usage:
grc remote list
```

## (Remote) add-collab

The 'add-collab' command adds a collaborator to one of your remote repositories.

```sh
# Usage:
grc remote add-collab <REPO_NAME> <COLLABORATOR_NAME> <PERMISSION?>

# Examples:
grc remote add-collab My-Repository Arthur admin # Or...
grc remote add-collab My-Repository Arthur # Default permission is 'admin'.

# Permissions = [admin, pull, push].
```

## (Remote) Clone

The 'clone' command clones one of your remote repositories on GitHub to your machine.

```sh
# Usage:
grc remote clone <REPO_NAME>

# Example:
grc remote clone My-Repository
```

## (Remote) URL

The 'url' command shows you the web URL of a personal repository on GitHub.

```sh
# Usage:
grc remote url <REPO_NAME>

# Example:
grc remote url My-Repository
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
git clone https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator.git -b v3.0.3
```

2. Install the necessary dependencies using pip:

```sh
# In the root of the project:
pip install -r .\.program-files\requirements.txt
```

3. Add the project directory to your path:

![Path](https://user-images.githubusercontent.com/69170322/172077383-d22a075f-0cba-4886-88a1-63f326f136ce.png)

Copy the project directory path, as shown in the image above, and follow [this quick tutorial](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

## Installation (Linux and MacOS)

1. Open a terminal and run the command below, you will be asked to enter your sudo password:

```sh
sudo -- sh -c 'wget https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/raw/improve-unix-installation-process/grc-install.sh && bash ./grc-install.sh && rm ./grc-install.sh'
```
