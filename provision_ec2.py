import subprocess

#provisioning the created instances
print "Now provisioning the newly created instances"
subprocess.call('''ansible-playbook provision_ec2.yml --private-key=samplekey.pem -i hosts''', shell=True)

print "The instances have been successfuly provisioned"
