import subprocess
import os
import json

print "Please enter the ami id of the Linux instance (for example ami-0f65671a86f061fcd):"
ami_id = str(raw_input())
print "Please enter the distro type (permissible values: ubuntu, amazon-linux):"
distro_type = str(raw_input())
print "Please enter the instance type (for example t2.micro):"
ins_type = str(raw_input())
print "Please enter the number of such instances to create:"
num_ins = str(raw_input())
	
#Execute the ansible playbook to create the desired instances
subprocess.call('''ansible-playbook create_ec2.yml --extra-vars "ami_id='''+ami_id+''' ins_type='''+ins_type+''' num_ins='''+num_ins+'''"''', shell=True)


#Now saving the address of newly created instance to the inventory file
with open('created_instance_details/created_instance_details.json', 'r') as fh:
	json_data = fh.read()
	data = json.loads(json_data)
	instances = data['instances']
	for i in instances:
		with open('hosts', 'ar')as hfh:
			if distro_type=='ubuntu':
				hfh.write(i['id']+" ansible_user=ubuntu ansible_host="+i['public_ip']+" ansible_python_interpreter=/usr/bin/python3\n")
				
			else: 
				hfh.write(i['id']+" ansible_user=ec2-user ansible_host="+i['public_ip']+" ansible_python_interpreter=/usr/bin/python3\n")
	
	
	


print "Instances have been successfuly created. Please run the provision_ec2.py program to provision the created instances."

		
	
