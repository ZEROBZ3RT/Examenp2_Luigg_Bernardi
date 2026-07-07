import hashlib
from datetime import datetime

def _select_node_for_document(self, document_data):

#Decide en qué nodo MongoDB guardar el documento
#Usa 'sharding' por hash para distribución uniforme

# Obtener ID del documento (o generarlo si no existe)
document_id = str(document_data.get('id', len(document_data)))

# Crear hash del ID para distribución consistente
hash_value = hashlib.md5(document_id.encode()).hexdigest()

# Convertir hash a número y usar módulo para elegir nodo
node_index = int(hash_value, 16) % 2 # %2 porque tenemos 2 nodos

if node_index == 0:
    return self.db1, "node1"
else:
    return self.db2, "node2"


def insert_document(self, data):
    # 1. Seleccionar nodo automáticamente
    target_db, node_name = self._select_node_for_document(data)
    
    # 2. Preparar documento con metadatos
    document = {
        '_id': data.get('id'),
        'data': data,
        'node': node_name, # Guardamos en qué nodo quedó
        'created_at': datetime.now()
    }

# 3. Insertar en el nodo seleccionado

result = target_db.documents.insert_one(document)
print(f"Guardado en {node_name}")

#BÚSQUEDA DISTRIBUIDA
#Pista: Buscar en TODOS los nodos

def find_document(self, document_id):

#Busca un documento en todos los nodos MongoDB

results = []

# Buscar en el PRIMER nodo
if self.db1:
    doc1 = self.db1.documents.find_one({'_id': document_id})
    if doc1:
        doc1['source_node'] = 'node1' # Marcar de dónde vino
        results.append(doc1)

# Buscar en el SEGUNDO nodo
if self.db2:
    doc2 = self.db2.documents.find_one({'_id': document_id})
    if doc2:
        doc2['source_node'] = 'node2' # Marcar de dónde vino
        results.append(doc2)
return results

def init (self):
    # Conexión al PRIMER MongoDB (puerto 27017) self.client1
    = MongoClient('mongodb://localhost:27017') self.db1 =
    self.client1['distributed_db']
    # Conexión al SEGUNDO MongoDB (puerto 27018) self.client2
    = MongoClient('mongodb://localhost:27018') self.db2 =
    self.client2['distributed_db']

#Generar Datos

def generate_sample_data(num_documents=100):
    sample_data = []
    for i in range(num_documents):
        sample_data.append({
            'id': i, # ID único para cada documento
            'name': f'Documento_{i}',
            'value': i * 10,
            'category': f'categoria_{i % 5}', # 5 categorías diferentes
            'timestamp': datetime.now()
        })
    return sample_data
