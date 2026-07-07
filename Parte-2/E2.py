import hashlib
from datetime import datetime

def _select_node_for_document(self, document_data):
    """
    Decide en qué nodo MongoDB guardar el documento.
    Usa sharding por hash para distribución uniforme.
    """

    # Obtener ID del documento (o generarlo si no existe)
    document_id = str(document_data.get("id", len(document_data)))

    # Crear hash del ID
    hash_value = hashlib.md5(document_id.encode()).hexdigest()

    # Elegir nodo
    node_index = int(hash_value, 16) % 2

    if node_index == 0:
        return self.db1, "node1"
    else:
        return self.db2, "node2"


def insert_document(self, data):
    # Seleccionar nodo
    target_db, node_name = self._select_node_for_document(data)

    # Documento a guardar
    document = {
        "_id": data.get("id"),
        "data": data,
        "node": node_name,
        "created_at": datetime.now()
    }

    # Insertar
    result = target_db.documents.insert_one(document)

    print(f"Guardado en {node_name}")

    return result.inserted_id


def find_document(self, document_id):
    """
    Busca un documento en ambos nodos.
    """

    results = []

    # Nodo 1
    if self.db1:
        doc1 = self.db1.documents.find_one({"_id": document_id})
        if doc1:
            doc1["source_node"] = "node1"
            results.append(doc1)

    # Nodo 2
    if self.db2:
        doc2 = self.db2.documents.find_one({"_id": document_id})
        if doc2:
            doc2["source_node"] = "node2"
            results.append(doc2)

    return results


def generate_sample_data(num_documents=100):
    sample_data = []

    for i in range(num_documents):
        sample_data.append({
            "id": i,
            "name": f"Documento_{i}",
            "value": i * 10,
            "category": f"categoria_{i % 5}",
            "timestamp": datetime.now()
        })

    return sample_data

from pymongo import MongoClient

class DistributedStorage:
    def __init__(self):
        self.client1 = MongoClient("mongodb://localhost:27017")
        self.db1 = self.client1["distributed_db"]

        self.client2 = MongoClient("mongodb://localhost:27018")
        self.db2 = self.client2["distributed_db"]

        
def _select_node_for_document(self, document_data):

    document_id = str(document_data.get("id"))

    hash_value = hashlib.md5(document_id.encode()).hexdigest()

    node_index = int(hash_value, 16) % 2

    if node_index == 0:
        return self.db1, "node1"
    else:
        return self.db2, "node2"


resultado = storage.find_document(5)

print(resultado)