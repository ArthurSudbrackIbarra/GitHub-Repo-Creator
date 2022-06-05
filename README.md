# GitHub Repository Creator

GRC is a tool to automatically create GitHub repositories using YAML templates. It comes with a CLI (Command Line Interface) that you can use to execute commands.

## Installation

1. Install [Python 3](https://www.python.org/downloads/).

2. Install the necessary dependencies using pip:

```sh
# In the root of the project:
pip install -r .\.program-files\requirements.txt
```

### Windows-Specific Steps

3. Add the project directory to your path:

### Linux-Specific Steps

3. Run the linux-setup.sh script:

```sh
# In the root of the project:
chmod +x linux-setup.sh # First command.
bash linux-setup.sh # Second command.
```

## Commands

In this section, all the possible GRC commands will be listed and explained.

### Authenticate

![Authenticate](https://user-images.githubusercontent.com/69170322/172030151-00f09557-7129-4fc6-ab73-7b29078e8147.png)

The 'authenticate' command is used so you can authenticate to GitHub and create repositories in your account. This is the **first command** you need to execute in order to start using GRC.

```sh
# Usage:
grc authenticate <ACCESS_TOKEN>

# Example:
grc authenticate ghp_3dh39j39874hs3d8PSBSHksbsbtx
```

Before running the command, you will need to generate a personal access token in GitHub if you don't have one yet. More on how to do that [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), make sure to check the 'repo' permission box when creating your token.

### Create

The 'create' command creates a repository for you based on a YAML file that is passed as a parameter. The YAML file contains information about the repository you want to create and must follow the patterns defined in the [templates](https://github.com/ArthurSudbrackIbarra/GitHub-Repo-Creator/tree/main/templates).

![Create](https://user-images.githubusercontent.com/69170322/172030355-cf5c3e39-4753-4936-9f26-5c8b8a0799db.png)

**File:** my-template.yaml

```yaml
# The repository name. (Required).
name: "My-Repository"

# The repository description. (Optional).
description: "This is my repository!"

# Whether the repository is private or not. (Optional, default is true).
private: true

# Whether the repository should be cloned to your machine after created or not. (Optional, default is true).
autoClone: true

# Collaborators list (Optional).
collaborators:
  - collaborator:
      name: "brun0-znx" # Collaborator name. (Required).
      permission: "admin" # Collaborator permission -> push/pull/admin. (Optional, default is admin).
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

### Save

The 'save' command is used to save a YAML file to your templates, so that you can later use it to create another repository with the same configurations but with a different repository name/description without having to specify the file path again.

![Save](https://user-images.githubusercontent.com/69170322/172030218-a11db610-6de7-40b2-93e3-0466d31677b6.png)

```sh
# Usage:
grc save <PATH_TO_YOUR_YAML_FILE>

# Example:
grc save ./my-template.yaml
```

### Choose

The 'choose' command lets you choose a file from your saved templates to create a repository based on it. When selecting a template, you have the option to use a different repository name/description than the one specified in the template file.

![Choose](https://user-images.githubusercontent.com/69170322/172030272-9f62a9a9-a30e-48bc-8356-ec83b4743737.png)

```sh
# Usage:
grc choose
```

### Delete

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
