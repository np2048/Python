# Simple configuration files management system

This scripts are used for copying Linux software configuration files from one machine to another and also store and synchronize them on Github.

## Example of a common use
Let's say you want to backup your *.vimrc* configuration file for *VIM*, save it on Github and then download and install it on other PC. Run **addfile.py** script:

    $ ./addfile.py vim ~/.vimrc

This will create *vim* sub directory at current path and copy your *.vimrc* file into it. It will also create *vim/path/.vimrc* file where the path for an actual *.vimrc* will be stored. Once it's done you can commit the changes to your Github repository:

    $ <Create new github repository for your config files if you don't have it yet>
    $ git add .
    $ git commit -m 'VIM config file'
    $ git push

On any other PC you'll be able to clone your config repository and install config files of any desired program by running the **install.py** script:

    $ git clone <your github config repository URL> Config
    $ Config/install.py vim

This will backup your current system *.vimrc* config file (actually rename it to *.vimrc.default* if it doesn't exist and to *.vimrc.old* if it does) and copy *.vimrc* from the repository to the system path stored it the *path/.vimrc* file

When a PC already has a local copy of your Config repository simply run

    $ git pull 
    $ ./install.py vim 

to update and synchronize your local Config with the repository.

## Template system support

The config files stored this way are processed with [*Jinja2*](https://jinja.palletsprojects.com/en/2.11.x/) by the **install.py** script. It allows you to have some configuration options specific to any particular machine. The **hostname** parameter of your operating system is used to set the value of the **device** variable that is passed to the templates:

    {% if device == 'HomePC' %}
    Include this string into the config file for my HomePC
    {% elif device == 'WorkPC' %}
    This string will be pasted only to the WorkPC config file
    {% else %}
    This string will be included on any other devices
    {% endif %}
