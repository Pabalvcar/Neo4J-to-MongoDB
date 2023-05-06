import pymongo
import neo4j

########################### Parámetros para manejar las conexiones a Neo4J y MongoDB ########################### 
NEO4J_CONNECTION_URL = "bolt://localhost:7687"
MONGODB_CONNECTION_URL = "mongodb+srv://admin:admin@bpmn-metrics.fu90ri1.mongodb.net/?retryWrites=true&w=majority"
MONGODB_DATABASE_NAME = "BPMN-Metrics"
MONGODB_COLLECTION_NAME = "metrics_test"
################################################################################################################

driver = neo4j.GraphDatabase.driver(NEO4J_CONNECTION_URL, auth=("neo4j", "password"))
session = driver.session()

# Ahora realizamos las consultas de cypher para insertar estadísticas en el documento:

# Número de eventos de inicio
query_1 = session.run("MATCH (n:Event) WHERE n.subtype IN ['Begin'] RETURN n.subtype, count(n) as Count")

# Número de eventos de fin
query_2 = session.run("MATCH (n:Event) WHERE n.subtype IN ['End'] RETURN n.subtype, count(n) as Count")

# Número medio, máximo y mínimo de forks en gateways del tipo exclusivas
query_3 = session.run("MATCH (n:Gateway)-[r]->() WHERE n.subtype = 'Exclusive' WITH n, count(*) as outDegree RETURN avg(outDegree) as Avg, max(outDegree) as Max, min(outDegree) as Min")

# Número medio, máximo y mínimo de forks en gateways del tipo inclusivas
query_4 = session.run("MATCH (n:Gateway)-[r]->() WHERE n.subtype = 'Inclusive' WITH n, count(*) as outDegree RETURN avg(outDegree) as Avg, max(outDegree) as Max, min(outDegree) as Min")

# Número medio, máximo y mínimo de forks en gateways del tipo paralelas
query_5 = session.run("MATCH (n:Gateway)-[r]->() WHERE n.subtype = 'Parallel' WITH n, count(*) as outDegree RETURN avg(outDegree) as Avg, max(outDegree) as Max, min(outDegree) as Min")

# Número de nodos, relaciones y densidad:
query_6 = session.run("MATCH (n) WITH count(*) as nodesCount MATCH (n)-[r]->() WITH nodesCount, count(r) as relationshipsCount RETURN toFloat(relationshipsCount)/ toFloat(nodesCount * (nodesCount - 1)) as Density, nodesCount as Nodes, relationshipsCount as Relations")

# Camino más largo entre evento de inicio y fin:
query_7 = session.run("MATCH (a:Event), (b:Event) WHERE a.subtype = 'Begin' AND b.subtype = 'End' WITH a,b MATCH p=(a)-[*]-(b) RETURN p, length(p) ORDER BY length(p) DESC LIMIT 1")

# Camino más corto entre evento de inicio y fin:
query_8 = session.run("MATCH (a:Event), (b:Event) WHERE a.subtype = 'Begin' AND b.subtype = 'End' WITH a,b MATCH p=(a)-[*]-(b) RETURN p, length(p) ORDER BY length(p) ASC LIMIT 1")

# Número de puertas de apertura
query_9 = session.run("MATCH (n:Gateway) WHERE n.type = 'Opening' RETURN n.type, count(n) as Count")

# Número de puertas de cierre
query_10 = session.run("MATCH (n:Gateway) WHERE n.type = 'Closing' RETURN n.type, count(n) as Count")

# Número de actividades
query_11 = session.run("MATCH (n:Activity) WITH count(*) as activityCount RETURN activityCount as Count")

# Instanciamos el cliente de MongoDB, obtenemos la BD y la colección de esta donde insertaremos el documento
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client[MONGODB_DATABASE_NAME]
collection = db[MONGODB_COLLECTION_NAME]

# Insertamos los resultados de las consultas en la colección en formato BSON

begin_count = query_1.single()["Count"]
end_count = query_2.single()["Count"]

min_forks_exclusive_gateways = query_3.peek()["Min"]
avg_forks_exclusive_gateways = query_3.peek()["Avg"]
max_forks_exclusive_gateways = query_3.single()["Max"]

min_forks_inclusive_gateways = query_4.peek()["Min"]
avg_forks_inclusive_gateways = query_4.peek()["Avg"]
max_forks_inclusive_gateways = query_4.single()["Max"]

min_forks_parallel_gateways = query_5.peek()["Min"]
avg_forks_parallel_gateways = query_5.peek()["Avg"]
max_forks_parallel_gateways = query_5.single()["Max"]

num_nodes = query_6.peek()["Nodes"]
num_relations = query_6.peek()["Relations"]
density = query_6.single()["Density"]

longest_path_lenght = query_7.single()["length(p)"]
shortest_path_lenght = query_8.single()["length(p)"]

opening_gates_count = query_9.single()["Count"]
closing_gates_count = query_10.single()["Count"]

num_activities = query_11.single()["Count"]

collection.insert_one({"Count of begin events":begin_count, "Count of end events":end_count,
                        "Minimum number forks of exclusive gateways":min_forks_exclusive_gateways, "Average number forks of exclusive gateways":avg_forks_exclusive_gateways,
                        "Maximum number forks of exclusive gateways":max_forks_exclusive_gateways, "Minimum number forks of inclusive gateways":min_forks_inclusive_gateways,
                        "Average number forks of inclusive gateways":avg_forks_inclusive_gateways, "Maximum number forks of inclusive gateways":max_forks_inclusive_gateways,
                        "Minimum number forks of parallel gateways":min_forks_parallel_gateways, "Average number forks of parallel gateways":avg_forks_parallel_gateways,
                        "Maximum number forks of parallel gateways":max_forks_parallel_gateways, "Number of nodes":num_nodes, "Number of relations":num_relations,
                        "Density":density, "Lenght of the longest path":longest_path_lenght, "Lenght of the shortest path":shortest_path_lenght,
                        "Number of opening gateways":opening_gates_count, "Number of closing gateways":closing_gates_count, "Number of activities":num_activities})
    
session.close()
print("Se ha realizado la extracción de datos con éxito")