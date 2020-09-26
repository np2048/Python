# Simple configuration files management system

This scripts are used for copying Linux software configuration files from one machine to another and also store and synchronize them on Github.

## Common usage workflow example
Let's say you want to backup your .vimrc configuration file for VIM, save it on github and then download and install it on other PC. Run command:

    $ ./addfile.py vim ~/.vimrc

This will create Config/vim directory and copy your .vimrc file into it. Also it will create Config/vim/path/.vimrc file where the path for an actual .vimrc will be stored. Once it's done you can commit the changes to your github repository:

    $ <Create new github repository for your config files if you don't have it yet>
    $ git add .
    $ git commit -m 'VIM config file'
    $ git push

On any other PC you'll be able to clone your config repository and install config files of any desired program by running the install script:

    $ git clone <your github config repository URL> Config
    $ Config/install.py vim

This will backup your current system .vimrc config file (actually rename it to .vimrc.default) and copy .vimrc from the reposytory to the system path stored it the path/.vimrc file

When a PC already have local copy of your Config repository simply run

    $ git pull 
    $ ./install.py vim 

to update and synchronize your local Config with the repository.

## Template system support

The config files stored this way are processed with Jinja2 by the install.py script that allows to have some configuration options specific to any particular machine. The hostname parameter is used in the templates:

    {% if device == 'HomePC' %}
    Include this string into the config file for my HomePC
    {% elif device == 'WorkPC' %}
    This string will be pasted only to the WorkPC config file
    {% else %}
    This string will be included on any other devices
    {% endif %}
