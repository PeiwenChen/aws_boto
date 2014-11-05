"""
create/store/delete/retrieve data from AWS S3 with Boto python API.
Author: Peiwen Chen
Date: Sep 23, 2014
"""

from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.key import key

conn = S3Connection(aws_access_key, aws_secret_key)

def create_reource():
	'create a bucket'
	bucket = conn.create_bucket('mybucket', location=Location.EU)
	# error handling

def update_resource():
	'store data in a bucket'
	b = conn.get_bucket('mybucket')
	k = Key(b)
	k.key = 'foobar'
	k.set_contents_from_filename('test.txt')

def delete_resource():
	'delete data in bucket'
	b = conn.get_bucket('bucket')
	for key in b.list():
		key.delete()
	# the bucket is empty now, delete it
	conn.delete_bucket('mybucket')

def download_resource():
	'retrieve data'
	b = conn.get_bucket('mybucket')
	k = Key(b)
	k.get_contents_to_filename('test.txt')



