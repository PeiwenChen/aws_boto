
"""
Author: Peiwen Chen
date: Sep 21, 2014
"""

import boto
import boto.ec2
import time
from config import *

def launch_instance():
	"""
	launch EC2 instance with given AMI
	read ec2_amis from config
	"""
	print "... creating EC2 instance ..."
	
	# setup connection
	conn = boto.connect_ec2(ec2_key,ec2_secret)
	
	# get security  groups, if the group does not exist, create it
	try:
		#group= conn.get_all_security_groups(groupnames=[ec2_group])[0]
		group= conn.get_all_security_groups()
		print " Security Groups: %s " % group 
	except conn.ResponseError, e:
		if e.code == 'InvalidGroup.Notfound':			
			print 'Creating Security Group: %s ' % ec2_group
			group = conn.create_security_group(ec2_group)
		else:
			raise
	
	# get key pair,  if it does not exist, create and save it
	try:
		key = conn.get_all_key_pairs(keynames=[ec2_key])[0]
		print " Key Pair is %s: " % key
	except conn.ResponseError, e:
		if e.code == 'InvalidKeyPair.NotFound':
			key_dir = '~/.ssh'
			print ' Creating a new key pair and save it to %s' % key_dir
			key = conn.create_key_pair(ec2_key)
			key.save(key_dir)
		else:
			raise
	
	reservation = conn.run_instances(ec2_amis,
					key_name=ec2_key,
					instance_type=ec2_instancetype, 
					security_groups=[ec2_group])
			
	instance = reservation.instances[0]
	conn.create_tags([instance.id], {"Name":ec2_tag})

	while instance.state  == u'pending':
		print "Instance state: %s" % instance.state
		time.sleep(10)
		instance.update()

	print "Instance.ID: %s: " % instance.id 
	print "Instance state: %s " % instance.state
	print "Public DNS: %s" % instance.public_dns_name

	return instance

def stop_instance(instance_id):
	"""
	stop EC2 instance with given ID 
	"""
	print "... stopping EC2 instance ..."
	conn = boto.connect_ec2(ec2_key,ec2_secret)	
	conn.stop_instances(instance_ids=[instance_id])

def terminate_instance(instance_id):
	"""
	terminate EC2 instance with given ID
	"""
	print "... terminating EC2 instance ..."
	conn = boto.connect_ec2(ec2_key,ec2_secret)
	conn = terminate_instances(instance_ids=[instance_id])


if __name__ == "__main__":
	instance = launch_instance()
	print " Sleep 200s before stopping the instance ... "
	time.sleep(200)
	stop_instance(instance.id)
