# audio_video_transfer

Create a virtual environment

In Windows (Use only command prompt not powershell to execute following commands)
	
	If python is installed in your system, then pip comes in handy.
	So simple steps are:
	1) Install virtualenv using

	 > pip install virtualenv 
	2)Now in which ever directory you are, this line below will create a virtualenv there

	 > virtualenv myenv

	And here also you can name it anything.

	3) Now if you are same directory then type,

	 > myenv\Scripts\activate

	You can explicitly specify your path too.

In Linux

	If pip is not in your system

	1)$ sudo apt-get install python-pip
	
	Then install virtualenv

	2)$ pip install virtualenv
	Now check your installation

	3)$ virtualenv --version
	Create a virtual environment now,

	4)$ virtualenv virtualenv_name
	After this command, a folder named virtualenv_name will be created. You can name anything to it. If you want to create a virtualenv for specific python version, type

	5)$ virtualenv -p /usr/bin/python3 virtualenv_name

	6)$ source virtualenv_name/bin/activate
	Now you are in a Python virtual environment
	

Install all required packges using command
	
	>pip install -r requirements.txt



run the the file using command

	>python audio_tansfer.py <ip_address_of_other_system>


if you want to know the Ip address of the system
use the following command
	
	>ipconfig
you will find your ip address here 
		IPv4 Address. . . . . . . . . . . : 192.168.0.98
