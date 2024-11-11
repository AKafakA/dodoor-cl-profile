"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()

num_nodes_1 = 2
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Add a raw PC to the request.
hardware_type = "c4130"
link = request.Link()
for i in range(num_nodes_1):
    node = request.RawPC("node" + str(i))
    node.hardware_type = hardware_type
    link.addNode(node)

num_nodes_2 = 8
hardware_type = "d7525"
for i in range(num_nodes_2):
    node = request.RawPC("node" + str(i + num_nodes_1))
    node.hardware_type = hardware_type
    link.addNode(node)

num_nodes_3 = 2
hardware_type = "d8545"
for i in range(num_nodes_3):
    node = request.RawPC("node" + str(i + num_nodes_1 + num_nodes_2))
    node.hardware_type = hardware_type
    link.addNode(node)


pc.printRequestRSpec(request)
