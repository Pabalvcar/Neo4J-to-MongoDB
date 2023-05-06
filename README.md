<h2>Neo4J to MongoDB</h2>
A simple script that extracts certain metrics from a Neo4J graph. This was made specifically with the purpose of obtaining metrics from a <b>BPMN diagram</b> modelled as a Neo4J graph. You need to have a working MongoDB atlas database for the script to work.
<br><br>
The repository contains a python script (neo4j_to_mongodb.py) that includes a secton with the parameters that must be changed in order to connect to the Neo4J graph and the MongoDB Atlas database.
<br><br>
The metrics extracted are the following:
<br><br>
<ul>
<li>Count of begin events</li>
<li>Count of end events</li>
<li>Minimum number forks of exclusive gateways</li>
<li>Average number forks of exclusive gateways</li>
<li>Maximum number forks of exclusive gateways</li>
<li>Minimum number forks of inclusive gateways</li>
<li>Average number forks of inclusive gateways</li>
<li>Maximum number forks of inclusive gateways</li>
<li>Minimum number forks of parallel gateways</li>
<li>Average number forks of parallel gateways</li>
<li>Maximum number forks of parallel gateways</li>
<li>Number of nodes</li>
<li>Number of relations</li>
<li>Density</li>
<li>Lenght of the longest path</li>
<li>Lenght of the shortest path</li>
<li>Number of opening gateways</li>
<li>Number of closing gateways</li>
<li>Number of activities</li>
</ul>
Further information is included in the user manual also included in the repository, but it's only available in spanish (also excuse the weird numbering and lack of references, it's taken out of a bigger PDF file. Maybe will fix later.)