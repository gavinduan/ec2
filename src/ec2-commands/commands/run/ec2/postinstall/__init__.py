# $Id: __init__.py,v 1.5 2012/11/27 03:20:51 clem Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.5 (Mamba)
# 		         version 6.0 (Mamba)
# 
# Copyright (c) 2000 - 2012 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#


import sys
import os
import subprocess
import string
import rocks.commands

class Command(rocks.commands.HostArgumentProcessor, rocks.commands.run.command):
	"""
	This script can re-run a kickstart on an already installed host and 
	perform the remaining part of the script.

	<arg type='string' name='file'>
	The path to the file containing the kickstart file to be run on this 
	machine
	</arg>


	<example cmd='run ec2 postinstall /root/ks.cfg"'>
	Uses the /root/ks.cfg to finalize the installation on this machine.
	</example>
	"""


	def run(self, params, args):
		(args, file) = self.fillPositionalArgs(('file',))
	
		if not file:
			self.abort('missing kcikstartfile')
		try:
			kickstartFile = open(file)
		except IOError:
			self.abort("Unable to open kickstart file %s." % file)

		
		for line in kickstartFile:
			if line.startswith("%packages"):
				break
		#now we start with the packages
		packages = []
		for line in kickstartFile:
			if len(line.strip()) == 0:
				pass
			elif line.startswith("%"):
				break
			else:
				packages.append(line.strip())
	
		subprocess.Popen( ['yumdownloader', '--resolve', '--destdir', '/mnt/temp'] \
				+ packages, stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE).wait()

		subprocess.Popen('rpm --nodeps -Uh /mnt/temp/*.rpm', shell=True, \
				stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
				stderr=subprocess.PIPE).wait()


		#
		# get current installed rpms list
		#
                #stdout = subprocess.Popen( ['rpm','-qa'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                #        stderr=subprocess.PIPE).stdout
                #installedRpms = stdout.read().strip()
		#installedRpms = installedRpms.split('\n')



