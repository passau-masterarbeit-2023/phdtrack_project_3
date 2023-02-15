import subprocess
import graphviz
from graph_data import GraphData
from params import ProgramParams
from graph_analyser import GraphAnalyser

import networkx as nx

def main():
    print("Running program...")

    params = ProgramParams(debug=True)

    graph_data = GraphData(
        params,
        params.TEST_HEAP_DUMP_RAW_FILE_PATH,
        params.BLOCK_BYTE_SIZE
    )
    graph_analyser = GraphAnalyser(graph_data)
    graph_analyser.annotate_graph()

    # generate graphviz file
    outfile_path = params.TEST_DATA_DIR + "/" + params.TEST_GRAPH_DATA_FILENAME
    nx.nx_agraph.write_dot(graph_data.graph, outfile_path)

    # filter out ValueNodes
    lines: list[str] = []
    with open(outfile_path, 'r') as f:
        lines = f.readlines()
        lines = [line for line in lines if "VN" not in line]

    # get only the first 100 lines, with first and last lines
    #lines = lines[:101] + lines[-1:]

    with open(outfile_path, 'w') as f:
        f.writelines(lines)

    # generate graph image
    # with open(outfile_path, 'r') as f:
    #     dot_graph_data = f.read()
    #     graph_png_file_path = outfile_path.replace('.gv', '.png')
    #     s = graphviz.Source(dot_graph_data)
    #     s.render(outfile=graph_png_file_path, format='png', view=True)

    # run sfdp command on graphviz file to generate graph image
    subprocess.Popen(
        ["sfdp", "-Gsize=67!", "-Goverlap=prism", "-Tpng", outfile_path, "-o", outfile_path.replace('.gv', '-sfdp.png')],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )



if __name__ == "__main__":
    main()
