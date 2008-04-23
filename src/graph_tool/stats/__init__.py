#! /usr/bin/env python
# graph_tool.py -- a general graph manipulation python module
#
# Copyright (C) 2007 Tiago de Paula Peixoto <tiago@forked.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
# RTLD_GLOBAL needs to be set in dlopen() if we want typeinfo and friends to
# work properly across DSO boundaries. See http://gcc.gnu.org/faq.html#dso

# The "except" is because the dl module raises a system error on ia64 and x86_64
# systems because "int" and addresses are different sizes.
try:
    from dl import RTLD_LAZY, RTLD_NOW, RTLD_GLOBAL
except ImportError:
    RTLD_LAZY = 1
    RTLD_NOW = 2
    RTLD_GLOBAL = 256
_orig_dlopen_flags = sys.getdlopenflags()

sys.setdlopenflags(RTLD_LAZY|RTLD_GLOBAL)
import libgraph_tool_stats
sys.setdlopenflags(_orig_dlopen_flags) # reset it to normal case to avoid
                                       # unnecessary symbol collision

from .. core import _degree
from numpy import *

__all__ = ["vertex_hist", "edge_hist", "label_components",
           "label_parallel_edges",  "label_self_loops"]

def vertex_hist(g, deg, bins=[1]):
    ret = libgraph_tool_stats.\
          get_vertex_histogram(g.underlying_graph(), _degree(deg), bins)
    return [ret[0], ret[1]]

def edge_hist(g, eprop, bins=[1]):
    ret = libgraph_tool_stats.\
          get_edge_histogram(g.underlying_graph(), eprop, bins)
    return [ret[0], ret[1]]

def label_components(g, vprop):
    if vprop not in g.vertex_properties:
        g.add_vertex_property(vprop, "int32_t")
    libgraph_tool_stats.\
          label_components(g.underlying_graph(), vprop)

def label_parallel_edges(g, eprop):
    if eprop not in g.edge_properties:
        g.add_edge_property(eprop, "int32_t")
    libgraph_tool_stats.\
          label_parallel_edges(g.underlying_graph(), eprop)

def label_self_loops(g, eprop):
    if eprop not in g.edge_properties:
        g.add_edge_property(eprop, "int32_t")
    libgraph_tool_stats.\
          label_self_loops(g.underlying_graph(), eprop)
