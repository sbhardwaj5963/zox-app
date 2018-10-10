<h1>zox-app</h1>
<h2>This project uses python scripts and ansible playbooks to achieve the desired functionality. Alongwith some of the
 companion files, the project consists of four main scripts:</h2>
 <h4>Important: Be patient while using these scripts,
 since the result of running a command (especially one that involves quering remote systems) may take a few moments to actually
 populate on the screen. Even if the script looks to be stuck at a place during runtime, don't assume that it will be stuck there forever.</h4>
<h3>1. The create_ec2.py script:</h3>
      This script is used to create the ec2 instances. When it is run, it asks the ami-id of the linux instance that we wanna
      create. (<b>NOTE:</b> For simplicity I have allowed to use only ubuntu and amazon-linux ami's. Also, avoid using extremely old 
      versions of ami, otherwise script may misbehave due to inappropriate dependencies.)
      Then, the script asks for type of the linux disribution of the ami (permissible values: ubuntu, amazon-linux). Then,
      script asks for instance type (e.g. t2.micro) and finally asks for the number of such instances to create. Then, the
      script proceeds to execute an ansible playbook called create_ec2.yml which contains the description of plays involved 
      to first create an approprite security group, then creating the instance and designating a key called samplekey that
      can be used in future to access those newly created instances.
      Finally, the script adds the ip and id of the newly created instances in the local hosts file called hosts which is 
      located in the root directory of this project.
<h3>2. The provision_ec2.py script:</h3>
      This script is used to first update the software cache on the instances and then installing iostat program and monit 
      program on those instances. The iostat program can be used to find out current cpu usage of the machine, and the monit
      program can be used to automatically monitor and create alerts when certains events occur (such as when % RAM usage
      is more than 80% for more than 5 minutes, % CPU usage is more than 90% for more than 2 minutes). The main heavylifting
      of the script is performed by the ansible playbook provision_ec2.yml that this script executes. The playbook 
      dynamically determines the type of package manager to use, installing programs and copying the configuration files
      from the root directory of the project to the appropriate location in the remote instances.
<h3>3. The get_specs.py script</h3>
      This script is used to get the desired specification information from the remote instances. The script utilizes the 
      facts gathering mechanism of ansible to collect all the informtion from the instances. (The playbook run by this script 
      is get_specs.yml.) Then the script saves all those collected facts in a file in the temporary directory called
      created_instance_details. Afterwards, the script selectively parses the facts files and gets only the relevant
      information like Memory (available, total etc in Megabytes), operating system information, cpu information etc.
      Then, the script print outs all that information on the console. Finally the temporary directory used to store all
      the facts file is deleted.
<h3>4. The delete_ec2.py script</h3>
      This script is used to terminate a running ec2 instance. When it is run, the script first shows the id and ip of all
      the instances that are currently running. Then the script proceeds to ask the user to enter the id of the instance
      which needs to be terminated. (<b>CAUTION:</b> you can't supply multiple instance ids at a time. Only a single id is desired
      at a time.)
      Then, the script proceeds to terminate that instance by running the ansible playbook delete_ec2.yml and finally
      removes the entry of that instance from the local inventory file.
<h2>Pre-requisites to run these scripts:</h2>
1. First of all clone the entire repo using the command:<br>
git clone <a href="https://github.com/sbhardwaj5963/zox-app.git">https://github.com/sbhardwaj5963/zox-app.git</a>  <br>
2. The script themselves are written in python, thus python needs to installed in your system. Since these script use
   ansible, you need to ensure that ansible is properly installed in your system.<br>
3. You should have an aws account. You also need to have the aws_access_key and aws_secret_key of an IAM user who has ec2
   administrative access. Then, you need to put those values in the apporpriate fields in the aws_creds.yml file in the 
   root directory of the project.<br>
4. You need to create a key called samplekey in the us-east-2 region of the aws. The scripts create the instances in the 
   us-east-2 region of the aws, and the created instances will be accessed using the key called samplekey. The key file 
   must be present in the root directory of the project. You can do that by simply downloading the samplekey from the aws
   web console and copy-paste that file in the root directory of the project. <br>(<b>CAUTION:</b>The name of the file that
   needs to be present in the root directory must be <b>samplekey.pem</b>, not samplekey <i>without the word .pem</i>)<br>

5. You need to ensure that boto3 is installed in your system. That can be installed using the following sequence of
commands in bash:
<p>
sudo pip install awscli boto <br>
sudo pip install boto3<br>
</p>

6. You need to edit the monit config file (called monitrc which is located in the root directory of the project)
so that when monit program is installed in the remote instances, it can work properly.
We need to make the following changes in the monitrc file:<br>
On line 80-82: change the gmail address in the double quotes to your own gmail address. Also change the password value
(enclosed in double quotes) to your own gmail password. This sets up the smtp server that will be used by the monit
program to send email alerts. However, for that to work properly, you will need to make a little change to your gmail
account settings: you need to enable "Less secure app access", which you can do by going here(https://myaccount.google.com/lesssecureapps)<br>
Then on line 140, you need to change the email address to the one where you'd like to email alerts fromt the monit
program.<br>

<h2>How to use these scripts:</h2>
(<b>IMPORTANT:</b> Before runnig any of the scripts, please ensure that you have met all the pre-requisites mentioned
 in the previous section.) <br>A basic workflow could look like this: First you run create_ec2.py script to create the ec2
  instances. install necessary Then you run provision_ec2.py script to programs on those instances. Then you run get_specs.py script 
  to get and print on the console, all the relevant information about those instances. Afterwards, when you wanna terminate any
   instance, you run delete_ec2.py script. <br>(<b>CAUTION:</b> Do not run delete_ec2.py before you have created any instances
    using create_ec2.py script because in that case, the inventory file would be empty, and there'd be nothing to delete.)<br>
