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

num_nodes = 4
node_deployment_command = ("nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar edu.cam.dodoor.ServiceDaemon "
                           "-c ~/dodoor/config.conf -d false -s false -n true  1>service.out  2>/dev/null &")

scheduler_deployment_command = ("nohup java -cp dodoor/target/dodoor-1.0-SNAPSHOT.jar edu.cam.dodoor.ServiceDaemon "
                                "-c ~/dodoor/config.conf -d true -s true -n false  1>service.out 2>/dev/null &")
# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Add a raw PC to the request.
hardware_type = "m400"

nodes = []
for i in range(num_nodes):
    node = request.RawPC("node" + str(i))
    node.hardware_type = hardware_type
    nodes[i].addService(pg.Execute(shell="sh", command="/local/repository/setup.sh"))

    iface = node.addInterface("if" + str(i))
    iface.component_id = "eth" + str(i)
    iface.addAddress(pg.IPv4Address("192.168.1." + str(i), "255.255.255.0"))
    nodes.append(node)

node0 = nodes[0]
for i in range(1, num_nodes):
    link = request.Link(members=[node0, nodes[i]])
    nodes[i].addService(pg.Execute(shell="sh",
                                   command=node_deployment_command))
node0.addService(pg.Execute(shell="sh", command=scheduler_deployment_command))
# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
