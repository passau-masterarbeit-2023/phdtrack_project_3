# -*- coding: utf-8 -*-
"""
SSH Key Discover
Library to discover SSH keys in memory dumps.
"""

__title__ = "ssh_key_discover"
__author__ = "Florian '0nyr' Rascoussier <florian.rascoussier@insa-lyon.fr), Clément Lahoche <clement.lahoche@insa-lyon.fr>"
__license__ = "GLP-3+"
__version__ = "0.0.1"

# modules
from . import mem_graph
from . import ml_discovery

# classes
from .mem_graph.graph_analyser import GraphAnalyser
from .mem_graph.graph_data import GraphData
