import re
import subprocess

print "The current running instances are:"

with open('hosts', 'r') as fh:
	for line in fh:
		if re.findall("[target]", line)=="[target]":
			continue
		elif re.findall(".+", line)==" ":
			continue
		else:
			temp = re.findall(r"i-[a-z0-9A-Z]+", line)
			node_id = temp[0]
						
			temp2 = re.findall(r"ansible_host=.+\.\d*", line)
			temp3 = temp2[0]
			temp4 = temp3.split('=')
			
			node_ip = temp4[1]
			print "Node with id "+node_id+" running at ip "+node_ip
			
			
print "Please enter the id of a running instance that you want to delete:"
n_del_val = str(raw_input())

#Now deleting the specified instance
subprocess.call('''ansible-playbook delete_ec2.yml --private-key=samplekey.pem --extra-vars "n_del_val='''+n_del_val+'''"''', shell=True)

with open('hosts', 'r') as gh:
	data = gh.read()
	
with open('hosts', 'w') as hh:
	new_data = re.sub(n_del_val+".*\n", '', data)
	hh.write(new_data)
	
	
print "The node was successfuly deleted."	
