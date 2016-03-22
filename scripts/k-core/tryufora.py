import pyfora
print 'hello'
#import boto.ec2
#conn = boto.ec2.connect_to_region('us-west-1')
ufora = pyfora.connect("http://localhost:30000")
print 'hi'
print 'helloo'


def isPrime(p):
    x = 2
    while x*x <= p:
        if p%x == 0:
            return 0
        x = x + 1
    return 1

print 'hi'
with ufora.remotely.downloadAll():
	result = sum(isPrime(x) for x in xrange(10))

print result
