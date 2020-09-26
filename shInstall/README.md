# Simple configuration files management system

This scripts are used for copying Linux software configuration files from one machine to another and also store and synchronize them on Github or any other file sharing service.


## Installation

In order to create a storage for your config files and start syncing it with your other machines using Github (or other VCS and file sharing services) you have to follow this steps:

1. Create a local directory where all the copies of your config files will be stored
1. Copy into the directory the following scripts from this repository:
    * addfile/addfile.py
    * install/install.py
1. Create a Github repository into the directory or setup synchronization with a file sharing service
1. You'll need Python and [*Jinja2*](https://jinja.palletsprojects.com/en/2.11.x/) module to use this scripts so install them to if you haven't done this already:
        
        $ <Install Python>
        $ pip install jinja2
        
That's pretty much it. You just need Python and a directory with a couple of script files into it to start.


## Example of a common use with Github
Let's say you want to backup your *.vimrc* configuration file for *VIM*, save it on Github and then download and install it on other PC. 

Setup the storage and copy the scripts as described in the **Installation** section above:

    $ mkdir ~/Config
    $ cp addfile/addfile.py ~/Config
    $ cp install/install.py ~/Config
    $ cd ~/Config

Run **addfile.py** script:

    $ ./addfile.py vim ~/.vimrc

This will create *vim* sub directory at current path and copy your *.vimrc* file into it. It will also create *vim/path/.vimrc* file where the path for an actual *.vimrc* will be stored. Once it's done you can commit the changes to your Github repository:

    $ <Create new github repository for your config files if you don't have it already>
    $ git add .
    $ git commit -m 'VIM config file'
    $ git push

>You can add some extra files to your *vim* storage sub directory: some scripts to install extensions and so on. Those files won't be copied to the new system automatically if you don't add a path file for them (by hand or by running **addfile.py** script). So you can store some additional helping scripts and data into your **Config** repository not only the config files itself.

On any other PC you'll be able to clone your **Config** repository and install config files of any desired program by running the **install.py** script:

    $ git clone <your github config repository URL> Config
    $ Config/install.py vim

This will backup your current system *.vimrc* config file (actually rename it to *.vimrc.default* if it doesn't exist and to *.vimrc.old* if it does) and copy *.vimrc* from the repository to the system path stored it the *path/.vimrc* file

When a PC already has a local copy of your **Config** repository simply run

    $ git pull 
    $ ./install.py vim 

to synchronize your local **Config** with the repository and update vim config file in your system.


## Template system support

The config files stored this way are processed with [*Jinja2*](https://jinja.palletsprojects.com/en/2.11.x/) by the **install.py** script. It allows you to have some configuration options specific to any particular machine. The **hostname** parameter of your operating system is used to set the value of the **device** variable that is passed to the templates:

    {% if device == 'HomePC' %}
    Include this string into the config file for my HomePC
    {% elif device == 'WorkPC' %}
    This string will be pasted only to the WorkPC config file
    {% else %}
    This string will be included on any other devices
    {% endif %}


## Tests

There are some test scripts in this repository that I have been using during the development process. You don't need to copy them to your **Config** storage directory. You only need the following ones:

*   **addfile.py** : To add a new config file into the storage
*   **install.py** : To copy all config files from a sub directory of the storage into the system
