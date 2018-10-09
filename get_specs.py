import subprocess
import os
import json
import shutil


if os.path.exists('ansible_facts_dir')==False:
	os.mkdir('ansible_facts_dir')
	print "Created a temporary directory ansible_facts_dir to store facts file"
	
#Executing the ansible playbook to get instances specifications
subprocess.call('''ansible-playbook get_specs.yml --private-key=samplekey.pem -i hosts''', shell=True)

#The following for loop exists only to get all the filenames in directory ansible_facts_dir
for root, dirs, files in os.walk('ansible_facts_dir'):
	print ""
	
#Now extracting the relevant information from all the facts files and printing it out on console	
for filename in files:
	with open('./ansible_facts_dir/'+filename, 'r') as fh:
		json_data = fh.read()
		data = json.loads(json_data)
		print "***********************************************************************************************"
		temp = filename.split('.json')
		node_name = temp[0]
		print "DETAILS FOR THE NODE "+node_name+":---->"
		print "Memory (in Megabytes):----"
		all_types = data['ansible_memory_mb']
		mem = all_types['real']
		print "Free:", mem['free']
		print "Total:", mem['total']
		print "Used:", mem['used']
		
		print "Linux distribution:", data['ansible_distribution']
		print "Linux distribution family type:", data['ansible_os_family']
		print "Linux distribution release:", data['ansible_distribution_release']
		print "Linux distribution version:", data['ansible_distribution_version']
		print "Linux kernel:", data['ansible_kernel']
		
		print "CPU information:-------"
		print "Number of processors:", data['ansible_processor_count']
		print "Number of processor cores:", data['ansible_processor_cores']
		print "Number of processor threads per core:", data['ansible_processor_threads_per_core']
		print "Number of virtual CPUs:", data['ansible_processor_vcpus']
		print "Details of virtual CPUs:"
		vcpus= data['ansible_processor']
		for i in vcpus:
			print i
	
	
#Now deleting the temporary directory that was being used to store facts file
if os.path.exists('ansible_facts_dir')==True:
	shutil.rmtree('ansible_facts_dir') #used shutil.rmtree() instead of os.rmdir() because latter can't delete non-empty directory
	print "Deleted the temporary directory that was being used to store facts file"
		
	
