"""This is a trivial example of a gitrepo-based profile; The profile source code and other software, documentation, etc. are stored in in a publicly accessible GIT repository (say, github.com). When you instantiate this profile, the repository is cloned to all of the nodes in your experiment, to `/local/repository`. 

This particular profile is a simple example of using a single raw PC. It can be instantiated on any cluster; the node will boot the default operating system, which is typically a recent version of Ubuntu.

Instructions:
Wait for the profile instance to start, then click on the node in the topology and choose the `shell` menu item. 
"""

import geni.portal as portal
import geni.rspec.pg as pg

# Create a portal context.
pc = portal.Context()
num_scheduler_datastore = 1
num_nodes = 30
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Add a raw PC to the request.
executor_hardware_type = "m400"
scheduler_hardware_type = "m400"

link = request.Link()
executor_nodes = []

for i in range(num_scheduler_datastore, num_nodes + num_scheduler_datastore):
    node = request.RawPC("node" + str(i))
    node.hardware_type = executor_hardware_type
    node.addService(pg.Execute(shell="sh", command="sudo ./local/repository/setup.sh {}".format(num_nodes)))
    link.addNode(node)
    executor_nodes.append(node)


for i in range(0, num_scheduler_datastore):
    scheduler_node = request.RawPC("node" + str(i))
    scheduler_node.hardware_type = scheduler_hardware_type
    scheduler_node.addService(pg.Execute(shell="sh", command="sudo ./local/repository/setup.sh {}".format(num_nodes)))
    link.addNode(scheduler_node)

# for i in range(0, num_nodes):
#     executor_nodes[i].addService(pg.Execute(shell="sh", command=node_deployment_command))

pc.printRequestRSpec(request)
