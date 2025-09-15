# # schema_graph.py
# import networkx as nx
# from db_conn import get_sql_connection

# def extract_schema_to_graph():
#     conn = get_sql_connection()
#     cursor = conn.cursor()

#     G = nx.DiGraph()

#     cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
#     tables = [row[0] for row in cursor.fetchall()]
#     for table in tables:
#         G.add_node(table)

#     cursor.execute("""
#         SELECT 
#             tp.name AS ParentTable,
#             cp.name AS ParentColumn,
#             tr.name AS ReferencedTable,
#             cr.name AS ReferencedColumn
#         FROM 
#             sys.foreign_keys fk
#         JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
#         JOIN sys.tables tp ON tp.object_id = fk.parent_object_id
#         JOIN sys.columns cp ON cp.object_id = tp.object_id AND cp.column_id = fkc.parent_column_id
#         JOIN sys.tables tr ON tr.object_id = fk.referenced_object_id
#         JOIN sys.columns cr ON cr.object_id = tr.object_id AND cr.column_id = fkc.referenced_column_id
#     """)
#     for row in cursor.fetchall():
#         G.add_edge(row.ParentTable, row.ReferencedTable, from_col=row.ParentColumn, to_col=row.ReferencedColumn)

#     conn.close()
#     return G

# def get_table_relationships():
#     G = extract_schema_to_graph()
#     relationships = []
#     for u, v, d in G.edges(data=True):
#         relationships.append(f"{u}.{d['from_col']} → {v}.{d['to_col']}")
#     return "\n".join(relationships)

import networkx as nx
from db_conn import get_sql_connection
import matplotlib.pyplot as plt

# List of tables to include in the graph
TARGET_TABLES = {
    "PolicyType", 
    "Organizations", 
    "CompanyPolicy", 
    "Persons", 
    "PersonFamilyDetails", 
    "PersonExperiences", 
    "PersonEducations", 
    "PersonDocument"
}

# Step 1: Extract FK relationships into a directed graph (filtered)
def extract_filtered_schema_to_graph():
    conn = get_sql_connection()
    cursor = conn.cursor()

    G = nx.DiGraph()

    # Only add target tables
    for table in TARGET_TABLES:
        G.add_node(table)

    # Get all FK relationships
    cursor.execute("""
        SELECT 
            tp.name AS ParentTable,
            cp.name AS ParentColumn,
            tr.name AS ReferencedTable,
            cr.name AS ReferencedColumn
        FROM 
            sys.foreign_keys fk
        JOIN sys.foreign_key_columns fkc ON fkc.constraint_object_id = fk.object_id
        JOIN sys.tables tp ON tp.object_id = fk.parent_object_id
        JOIN sys.columns cp ON cp.object_id = tp.object_id AND cp.column_id = fkc.parent_column_id
        JOIN sys.tables tr ON tr.object_id = fk.referenced_object_id
        JOIN sys.columns cr ON cr.object_id = tr.object_id AND cr.column_id = fkc.referenced_column_id
    """)
    
    for row in cursor.fetchall():
        parent = row.ParentTable
        referenced = row.ReferencedTable

        # Add edge only if both tables are in TARGET_TABLES
        if parent in TARGET_TABLES and referenced in TARGET_TABLES:
            G.add_edge(
                parent,
                referenced,
                from_col=row.ParentColumn,
                to_col=row.ReferencedColumn,
                label=f"{row.ParentColumn} → {row.ReferencedColumn}"
            )


    conn.close()
    return G

# Step 2: Generate readable FK paths
def get_filtered_table_paths():
    G = extract_filtered_schema_to_graph()
    paths = []

    for source in G.nodes():
        for target in G.nodes():
            if source != target and nx.has_path(G, source, target):
                try:
                    path = nx.shortest_path(G, source=source, target=target)
                    for i in range(len(path) - 1):
                        from_table = path[i]
                        to_table = path[i + 1]
                        edge_data = G.get_edge_data(from_table, to_table)
                        paths.append(f"{from_table}.{edge_data['from_col']} → {to_table}.{edge_data['to_col']}")
                except nx.NetworkXNoPath:
                    continue

    return "\n".join(sorted(set(paths)))

def visualize_filtered_fk_graph():
    G = extract_filtered_schema_to_graph()

    pos = nx.spring_layout(G, seed=42)  # for consistent layout
    plt.figure(figsize=(12, 8))

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=2500, edgecolors='black')
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Draw edge labels (foreign key columns)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='green', font_size=8)

    plt.title("Filtered Foreign Key Relationships", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    
# if __name__ == "__main__":
#     visualize_filtered_fk_graph()
       