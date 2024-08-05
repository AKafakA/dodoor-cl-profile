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

num_scheduler_datastore = 1
num_nodes = 30
node_deployment_command = ("sudo nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar edu.cam.dodoor.ServiceDaemon "
                           "-c ~/dodoor/config.conf -d false -s false -n true  1>service.out  2>/dev/null &")

scheduler_deployment_command = ("sudo nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar edu.cam.dodoor.ServiceDaemon "
                                "-c ~/dodoor/config.conf -d true -s true -n false  1>service.out 2>/dev/null &")
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Add a raw PC to the request.
hardware_type = "m400"
link = request.Link()
nodes = []
for i in range(num_nodes + num_scheduler_datastore):
    node = request.RawPC("node" + str(i))
    node.hardware_type = hardware_type
    node.addService(pg.Execute(shell="sh", command="sudo ./local/repository/setup.sh"))
    link.addNode(node)
    nodes.append(node)

for i in range(0, num_nodes):
    nodes[i + num_scheduler_datastore].addService(pg.Execute(shell="sh",
                                                             command=node_deployment_command))
pc.printRequestRSpec(request)
