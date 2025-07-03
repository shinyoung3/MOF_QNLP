import pormake as pm
from pormake import *

def build_mof_from_name(mof_name, cif_filename=None):
    """
    Build a MOF structure from a name string like 'kag N139 E161' using pormake,
    and write to a CIF file.
    
    Args:
        mof_name (str): String with format 'topology node edge', e.g. 'kag N139 E161'
        cif_filename (str or None): Output CIF filename. If None, use mof_name + '.cif'
    Returns:
        pm.MOF: Built MOF object
    """
    parts = mof_name.strip().split()
    if len(parts) != 3:
        raise ValueError(f"Invalid MOF name: {mof_name} (should have 3 parts: topology node edge)")

    topo_name, node_name, edge_name = parts
    print(f"Parsing MOF: Topology = {topo_name}, Node = {node_name}, Edge = {edge_name}")

    database = pm.Database()
    builder = pm.Builder()

    topo = database.get_topo(topo_name)
    node = database.get_bb(node_name)
    edge = database.get_bb(edge_name)

    mof_candidate = builder.build_by_type(topo, {(0): node}, {(0, 0): edge})

    if cif_filename is None:
        # Use an underscore-joined version for filename
        cif_filename = f"{mof_name.replace(' ', '_')}.cif"

    mof_candidate.write_cif(cif_filename)
    print(f"MOF CIF written to {cif_filename}")

    return mof_candidate